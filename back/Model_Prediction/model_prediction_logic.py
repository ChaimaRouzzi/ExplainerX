import joblib
import pandas as pd
from typing import List
from fastapi import HTTPException
import shap
from fastapi.responses import JSONResponse
import dill
import os
from Data_Gathering.data_gathering_logic import fetch_data

MODELS_DIR1 = "models/Pre_Trained_Models"  
MODELS_DIR2 = "models/Custom_Models"  

models1 = {}

def load_models():
    model_filenames = ["gas_hourly_xgboost.joblib", "gas_daily_xgboost.joblib", "gas_weekly_xgboost.joblib", "gas_monthly_xgboost.joblib", "electricity_hourly_xgboost.joblib", "electricity_daily_xgboost.joblib", "electricity_weekly_xgboost.joblib", "electricity_monthly_xgboost.joblib", "gas_daily_prophet.joblib"]
    for filename in model_filenames:
        model_name = filename.split(".")[0]
        model_path = f"{MODELS_DIR1}/{filename}"
        models1[model_name] = joblib.load(model_path)


models2 = {}

async def load_models2(connection, user_id):
    model_filenames_extension = []
    model_filenames = []
    model_info = []
    models = await connection.fetch("SELECT model_id, model_details FROM models WHERE user_id = $1", user_id)

    for model in models:
        model_details_json = model['model_details']
        model_details = json.loads(model_details_json)
        model_name = model_details["model_name"]
        predictors = model_details["params"]["predictors"]
        target = model_details["params"]["target"]
        horizon = model_details["params"]["horizon"]
        model_info.append({
            "model_name": model_name,
            "predictors": predictors, 
            "target": target, 
            "horizon": horizon
        })        
        
        model_name_with_extension = f"{model_name}.joblib"
        model_filenames_extension.append(model_name_with_extension)
        model_filenames.append(model_name)

    for filename in model_filenames_extension:
        model_name = filename.split(".")[0]
        model_path = f"{MODELS_DIR2}/{filename}"
        models2[model_name] = joblib.load(model_path)
    return model_info


def load_data_from_csv(file_path: str):
    return pd.read_csv(file_path, parse_dates=['date'],index_col='date')


async def predict_pretrained(model_name: str, input_data: List[float], connection):
    data = await fetch_data(connection, "False")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    if "hourly" in model_name:
        horizon = "H"
    elif "daily" in model_name:
        horizon = "D"
    elif "weekly" in model_name: 
        horizon = "W"
    elif "monthly" in model_name: 
        horizon = "M"

    if "gas" in model_name: 
        target = "Gas_01"
    elif "electricity" in model_name: 
        target = "Electricity"
    
    df_resampled = df.resample(horizon).mean()
    df_resampled.fillna(df_resampled.mean(), inplace=True)

    model = models1.get(model_name)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found.")

    prediction = model.predict([input_data])
    scaled_prediction = prediction 

    min_value = df_resampled[target].min()
    max_value = df_resampled[target].max()

    unscaled_prediction = scaled_prediction * (max_value - min_value) + min_value
    print(unscaled_prediction)
    rounded_number = '{:.4f}'.format(unscaled_prediction[0])
    print(rounded_number)


    return {"prediction": rounded_number}

async def predict_custom(model_name: str, input_data: List[float], target: str, horizon: str, connection):
    data = await fetch_data(connection, "False")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    if horizon == "Hourly":
        horizon = "H"
    if horizon == "Daily":
        horizon = "D"
    if horizon == "Weekly":
        horizon = "W"
    if horizon == "Monthly":
        horizon = "M"
    
    df_resampled = df.resample(horizon).mean()
    df_resampled.fillna(df_resampled.mean(), inplace=True)

    model = models2.get(model_name)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found.")

    prediction = model.predict([input_data])
    scaled_prediction = prediction 

    min_value = df_resampled[target].min()
    max_value = df_resampled[target].max()

    unscaled_prediction = scaled_prediction * (max_value - min_value) + min_value
    print(unscaled_prediction)
    rounded_number = '{:.4f}'.format(unscaled_prediction[0])
    print(rounded_number)


    return {"prediction": rounded_number}

async def calculate_shap(feature_names: List[str], model_name: str, data: List[float]):
    input_df = pd.DataFrame([data], columns=feature_names)
    
    model = models1.get(model_name)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found.")
    
    if not hasattr(model, 'predict') or not callable(model.predict):
        raise HTTPException(status_code=500, detail="Model's predict function is invalid.")
    
    explainer = shap.Explainer(model)
    
    shap_values = explainer(input_df)
    
    shap_df = pd.DataFrame({
        "feature": feature_names,
        "importance": shap_values.values.mean(0) 
    })
    
    shap_data = shap_df.to_dict(orient='records')
    print(shap_data)
    return JSONResponse(content=shap_data)



async def calculate_lime(feature_names: List[str], model_name: str, data: List[float], min_max_df: pd.DataFrame):
    with open('xai/Lime/%s_lime.pkl' % model_name, 'rb') as file:
        input_df = pd.DataFrame([data], columns=feature_names)
        model = models1.get(model_name)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found.")   
                         
        loaded_object = dill.load(file)
        # Extract minimum and maximum values from the provided DataFrame
        min_values = min_max_df['Min'].values
        max_values = min_max_df['Max'].values
        
        # Separate the features that need scaling and those that don't
        scaled_features = ['Maximum_Humidity', 'Solar_Radiation', 'Day_Degree_Hot', 'Day_Degree_Cold',
                           'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp', 'Min_OutdoorTemp']
        non_scaled_features = ['Year', 'Quarter', 'Month', 'Week', 'Day', 'Is_Weekend', 'Is_Holiday']
        
        # Scale the features that need scaling
        scaled_data = (data[:len(scaled_features)] - min_values[:len(scaled_features)]) / (max_values[:len(scaled_features)] - min_values[:len(scaled_features)])
        
        # Combine scaled and non-scaled features
        scaled_data = list(scaled_data) + data[len(scaled_features):]
        
        # Create a DataFrame with the scaled data
        input_df = pd.DataFrame([scaled_data], columns=feature_names)
        
        instance = input_df.to_numpy()[0]
        explanation = loaded_object.explain_instance(instance, model.predict, num_features=len(feature_names))
    
    lime_importance = [{'feature': f.split()[0], 'importance': i} for f, i in explanation.as_list()]
    
    print(lime_importance)
    
    return JSONResponse(content=lime_importance)

import json 

async def calculate_anchors(feature_names: List[str], model_name: str, data: List[float]):    
    with open('xai/Anchors/%s_anchors.pkl' % model_name, 'rb') as file:
        input_df = pd.DataFrame([data], columns=feature_names)
        model = models1.get(model_name)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found.")                    
        loaded_object = dill.load(file)
        instance = input_df.to_numpy()[0]
        explanation = loaded_object.explain_instance(instance, model.predict, threshold=0.95)
    
        anchor_json = {
            "Explanation Features": explanation.precision(),
            "Explanation Coverage": explanation.coverage(),
            "Anchor": explanation.names()
        }
        print(anchor_json)
    
    return json.dumps(anchor_json)



async def calculate_shap_custom(feature_names: List[str], model_name: str, data: List[float]):

    with open('xai/Custom/%s_shap.pkl' % model_name, 'rb') as file:
        input_df = pd.DataFrame([data], columns=feature_names)
        model = models2.get(model_name)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found.")                    
        loaded_object = dill.load(file)
        instance = input_df.to_numpy()[0]

        shap_values = loaded_object.shap_values(instance)

        shap_df = pd.DataFrame({
        "feature": feature_names,
        "importance": shap_values
        })
    
    shap_data = shap_df.to_dict(orient='records')
    print(shap_data)
    return JSONResponse(content=shap_data)
    
async def calculate_lime_custom(feature_names: List[str], model_name: str, data: List[float]):
    with open('xai/Custom/%s_lime.pkl' % model_name, 'rb') as file:
        input_df = pd.DataFrame([data], columns=feature_names)
        model = models2.get(model_name)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found.")                    
        loaded_object = dill.load(file)
        instance = input_df.to_numpy()[0]
        explanation = loaded_object.explain_instance(instance, model.predict, num_features=len(feature_names))
    
    lime_importance = [{'feature': f.split()[0], 'importance': i} for f, i in explanation.as_list()]
    
    print(lime_importance)
    
    return JSONResponse(content=lime_importance)


import numpy as np


import json 

async def calculate_anchors_custom(feature_names: List[str], model_name: str, data: List[float]):    
    with open('xai/Custom/%s_anchors.pkl' % model_name, 'rb') as file:
        input_df = pd.DataFrame([data], columns=feature_names)
        model = models2.get(model_name)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found.")                    
        loaded_object = dill.load(file)
        instance = input_df.to_numpy()[0]
        explanation = loaded_object.explain_instance(instance, model.predict, threshold=0.95)
    
        anchor_json = {
            "Explanation Features": explanation.precision(),
            "Explanation Coverage": explanation.coverage(),
            "Anchor": explanation.names()
        }
        print(anchor_json)
    
    return json.dumps(anchor_json)