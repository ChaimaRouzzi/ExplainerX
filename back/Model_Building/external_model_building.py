from fastapi import UploadFile, File
from pydantic import BaseModel
import joblib
import os
import json
import pandas as pd
from fastapi.responses import JSONResponse
from typing import List
from Data_Gathering.data_gathering_logic import fetch_data2
import shap
import dill 
from anchor import anchor_tabular
import lime
import lime.lime_tabular
models = {}

MODELS_DIR2 = "models/Custom_Models"  

async def upload_model(file: UploadFile = File(...)):
    global uploaded_model_name
    with open(os.path.join(MODELS_DIR2, file.filename), "wb") as model_file:
        contents = await file.read()
        model_file.write(contents)

    # Load the newly uploaded model
    model_name = file.filename[:-7]
    uploaded_model_name = model_name
    model_path = os.path.join(MODELS_DIR2, file.filename)
    model = joblib.load(model_path)

    # Store the model object in the dictionary
    models[model_name] = model

    return {"message": "Model uploaded successfully"}

dataframe = None

async def upload_dataframe(data, feature_names: List[str], horizon: str):
    global dataframe
    try:
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        if horizon == "Hourly": 
            horizon = "H"
        elif horizon == "Daily": 
            horizon = "D"
        elif horizon == "Weekly": 
            horizon = "W"
        elif horizon == "Monthly": 
            horizon = "M"
        df_resampled = df.resample(horizon).mean()
        df_resampled.fillna(df_resampled.mean(), inplace=True)
        df_resampled = df_resampled[feature_names]
        dataframe = df_resampled
        return {"message": "DataFrame uploaded successfully"}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

async def get_dataframe():
    global dataframe
    
    if dataframe is not None:
        # Filter or adjust data here if necessary
        # Convert DataFrame to JSON
        json_data = dataframe.to_json(orient='records')
        return json_data
    else:
        return {"message": "DataFrame not available"}



from datetime import datetime

async def save_external_model(connection, connection2,  user_id: int, model_name: str, features: List[str], target: str, horizon: str):
    data = await fetch_data2(connection2)
    model_path = os.path.join(MODELS_DIR2, f"{model_name}.joblib")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    if horizon == "Hourly": 
        horizon2 = "H"
    elif horizon == "Daily": 
        horizon2 = "D"
    elif horizon == "Weekly": 
        horizon2 = "W"
    elif horizon == "Monthly": 
        horizon2 = "M"
    df_resampled = df.resample(horizon2).mean()
    df_resampled.fillna(df_resampled.mean(), inplace=True)
    df_resampled = df_resampled[features]
    print(df_resampled)
    X = df_resampled.values    

    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "Model not found"})
    
    def convert_to_serializable(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        
        return str(obj)
    
    model_params = {}
    for attr in dir(model):
        if not attr.startswith("__") and not callable(getattr(model, attr)):
            model_params[attr] = convert_to_serializable(getattr(model, attr))
    
    model_details = {
        "model_name": model_name,
        "user_id": user_id,
        "params": {
            "model_name": model_name,
            "predictors": features,
            "all_predictors": [
                "Day_Degree_Cold", "Day_Degree_Hot", "Min_OutdoorTemp",
                "Average_OutdoorTemp", "Max_OutdoorTemp", "Maximum_Humidity",
                "Average_Humidity", "Solar_Radiation", "Hour", "Day", "Week", "Month", "Year"
            ],
            "target": target,
            "horizon": horizon,
            **model_params, 
        },
        "performance" : "", 
        "user_name": None,
    }
    
    user_name_query = "SELECT name FROM users WHERE user_id = $1;"
    user_name = await connection.fetchval(user_name_query, user_id)
    model_details['user_name'] = user_name
    
    model_details_json = json.dumps(model_details, default=convert_to_serializable, indent=4)

    insert_query = "INSERT INTO models (model_details, user_id) VALUES ($1, $2) RETURNING model_id;"
    model_id = await connection.fetchval(insert_query, model_details_json, user_id)
    shap_explainer = shap.KernelExplainer(model.predict, X)
    anchors_explainer = anchor_tabular.AnchorTabularExplainer(
    class_names=None,
    feature_names=features,
    train_data=X)
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(X, feature_names=features, class_names=[target], mode='regression')


    with open('xai/Custom/%s_anchors.pkl' % model_name, 'wb') as file:
        dill.dump(anchors_explainer, file)
    with open('xai/Custom/%s_shap.pkl' % model_name, 'wb') as file:
        dill.dump(shap_explainer, file)
    with open('xai/Custom/%s_lime.pkl' % model_name, 'wb') as file:
        dill.dump(lime_explainer, file)

    return model_id