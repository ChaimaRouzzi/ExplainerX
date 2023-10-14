from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import lightgbm as lgb
from pydantic import BaseModel
from sklearn.preprocessing import MinMaxScaler
import shap
from sklearn.inspection import permutation_importance
from typing import List
import numpy as np
import pandas as pd 
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import random
import os
import joblib
import json
import shap
import dill 
import time
from anchor import anchor_tabular
import lime
import lime.lime_tabular
from fastapi.responses import JSONResponse
from Data_Gathering.data_gathering_logic import fetch_data2

random_seed = 0
np.random.seed(random_seed)
random.seed(random_seed)
app = FastAPI()

class SVRParameters(BaseModel):
    model_name: str
    predictors: List[str]
    all_predictors: List[str]
    target: str
    horizon: str
    kernel: str
    degree: int
    gamma: str
    coef0: float
    tol: float
    C: float
    epsilon: float
    shrinking: bool
    cache_size: int
    verbose: bool
    max_iter: int
    random_state: int
    test_size: float

class SavedModelSVR(BaseModel):
    model_name: str
    user_id: int
    params: SVRParameters
    performance: dict
    shap_data: List[dict]
    pfi_data: List[dict]

    def to_dict(self):
        return {
            "model_name": self.model_name,
            "user_id": self.user_id,
            "params": jsonable_encoder(self.params),
            "performance": self.performance,
            "shap_data": self.shap_data,
            "pfi_data": self.pfi_data
        }


def build_svr_model(data, params):
    processed_data = handle_missing_values_with_mean(data)

    df = pd.DataFrame(processed_data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    
    if params.horizon == "Hourly": 
        horizon = "H"
    elif params.horizon == "Daily": 
        horizon = "D"
    elif params.horizon == "Weekly": 
        horizon = "W"
    elif params.horizon == "Monthly": 
        horizon = "M"

    df_resampled = df.resample(horizon).mean()
    df_resampled.fillna(df_resampled.mean(), inplace=True)
    
    target_variable = params.target
    predictor_columns = params.predictors
    
    X = df_resampled[predictor_columns].values
    X_all = df_resampled[params.all_predictors].values

    y = df_resampled[target_variable].values

    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    X_scaled_all = scaler_X.fit_transform(X_all)

    scaler_y = MinMaxScaler()
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=params.test_size / 100)
    X_train_all, X_test_all, y_train_all, y_test_all = train_test_split(X_scaled_all, y_scaled, test_size=params.test_size / 100)

    svr_model = SVR(
        kernel=params.kernel,
        degree=params.degree,
        gamma=params.gamma,
        coef0=params.coef0,
        tol=params.tol,
        C=params.C,
        epsilon=params.epsilon,
        shrinking=params.shrinking,
        cache_size=params.cache_size,
        verbose=params.verbose,
        max_iter=params.max_iter
    )

    svr_model_all = SVR(
        kernel=params.kernel,
        degree=params.degree,
        gamma=params.gamma,
        coef0=params.coef0,
        tol=params.tol,
        C=params.C,
        epsilon=params.epsilon,
        shrinking=params.shrinking,
        cache_size=params.cache_size,
        verbose=params.verbose,
        max_iter=params.max_iter
    )
    start_time = time.time()
    exec_time = time.time()-start_time
    print(exec_time)

    svr_model.fit(X_train, y_train.ravel())
    svr_model_all.fit(X_train_all, y_train_all.ravel())
    models_dir = "models/Custom_Models"  
    os.makedirs(models_dir, exist_ok=True)  
    model_filename = os.path.join(models_dir, f"{params.model_name}.joblib")
    joblib.dump(svr_model, model_filename)
    print(f"Fitted SVR model saved as {model_filename}")

    y_pred_test = svr_model.predict(X_test)
    y_pred_all_data = svr_model.predict(X_scaled)

    mae = mean_absolute_error(y_test, y_pred_test)
    mse = mean_squared_error(y_test, y_pred_test)
    rmse = np.sqrt(mse)

    explainer = shap.KernelExplainer(svr_model_all.predict, X_train_all)

    shap_values = explainer.shap_values(X_test_all)

    summary_df = pd.DataFrame(shap_values, columns=params.all_predictors)

    importance_df_shap = pd.DataFrame(summary_df.abs().mean(), columns=['Importance'])
    importance_df_shap = importance_df_shap.sort_values(by='Importance', ascending=False)

    perm_importance = permutation_importance(svr_model_all, X_test_all, y_test_all, n_repeats=30, random_state=0)

    importance_df_pfi = pd.DataFrame(perm_importance.importances_mean, index=params.all_predictors, columns=['Importance'])
    importance_df_pfi = importance_df_pfi.sort_values(by='Importance', ascending=False)

    shap_data = importance_df_shap.reset_index().rename(columns={'index': 'feature', 'Importance': 'importance'}).to_dict(orient='records')
    pfi_data = importance_df_pfi.reset_index().rename(columns={'index': 'feature', 'Importance': 'importance'}).to_dict(orient='records')

    # Inverse transform the reshaped y_pred_scaled
    date_column = df_resampled.index.strftime("%Y-%m-%d").tolist()

    return {
        "mse": mse,
        "rmse": rmse,
        "mae": mae,
        "shap": shap_data,
        "pfi": pfi_data,
        "actual_values": y_scaled.tolist(),
        "predicted_values": y_pred_all_data.tolist(),
        "dates": date_column
    }

def handle_missing_values_with_mean(data):
    df = pd.DataFrame(data)
    column_means = df.drop(columns=["date"]).mean()
    df = df.fillna(column_means)
    processed_data = df.to_dict(orient="records")

    return processed_data

MODELS_DIR2 = "models/Custom_Models"  

async def save_model_details_svr(connection, connection2,  model_details: SavedModelSVR):
    data = await fetch_data2(connection2)
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    horizon = model_details.params.horizon
    if model_details.params.horizon == "Hourly": 
        horizon = "H"
    elif horizon == "Daily": 
        horizon = "D"
    elif horizon == "Weekly": 
        horizon = "W"
    elif horizon == "Monthly": 
        horizon = "M"
    df_resampled = df.resample(horizon).mean()
    df_resampled.fillna(df_resampled.mean(), inplace=True)
    df_resampled = df_resampled[model_details.params.predictors]
    print(df_resampled)
    X = df_resampled.values    
    user_id = model_details.user_id 
    insert_query = "INSERT INTO models (model_details, user_id) VALUES ($1, $2) RETURNING model_id;"

    user_name_query = "SELECT name FROM users WHERE user_id = $1;"
    user_name = await connection.fetchval(user_name_query, user_id)
    print(user_name)
    print("hiiii")

    model_details_dict = model_details.dict()
    model_details_dict['user_name'] = user_name

    model_details_json = json.dumps(model_details_dict)

    model_id = await connection.fetchval(insert_query, model_details_json, user_id)
    model_path = os.path.join(MODELS_DIR2, f"{model_details.model_name}.joblib")
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "Model not found"})
    shap_explainer = shap.KernelExplainer(model.predict, X)
    anchors_explainer = anchor_tabular.AnchorTabularExplainer(
    class_names=None,
    feature_names=model_details.params.predictors,
    train_data=X)
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(X, feature_names=model_details.params.predictors, class_names=[model_details.params.target], mode='regression')


    with open('xai/Custom/%s_anchors.pkl' % model_details.model_name, 'wb') as file:
        dill.dump(anchors_explainer, file)
    with open('xai/Custom/%s_shap.pkl' % model_details.model_name, 'wb') as file:
        dill.dump(shap_explainer, file)
    with open('xai/Custom/%s_lime.pkl' % model_details.model_name, 'wb') as file:
        dill.dump(lime_explainer, file)
    return model_id

async def get_all_model_details(connection):
    select_query = "SELECT model_id, model_details FROM models;"
    model_records = await connection.fetch(select_query)

    model_details_list = []
    for record in model_records:
        model_id, model_details_json = record
        model_details_list.append({"model_id": model_id, "model_details": model_details_json})

    return model_details_list
