from fastapi import APIRouter, Depends, HTTPException
from Data_Gathering.db_connection import connect_to_db
from typing import List
import openai
from pydantic import BaseModel
from fastapi.responses import JSONResponse  
from Model_Prediction.model_prediction_logic import predict_pretrained, predict_custom, calculate_shap, calculate_lime, calculate_anchors, load_models2, calculate_shap_custom, calculate_lime_custom, calculate_anchors_custom
model_prediction_router = APIRouter()
import pandas as pd
@model_prediction_router.post("/predict/regression/{model_name}/")
async def predict_pretrained_endpoint(model_name: str, data: List[float], connection=Depends(connect_to_db)):
    predict_response = await predict_pretrained(model_name, data, connection)
    return predict_response


class PredictionRequest(BaseModel):
    data: List[float]
    target: str
    horizon: str

@model_prediction_router.post("/predict/custom/{model_name}/")
async def predict_custom_endpoint(
    model_name: str,
    request_data: PredictionRequest,  
    connection=Depends(connect_to_db)
):
    data = request_data.data
    target = request_data.target
    horizon = request_data.horizon

    predict_response = await predict_custom(model_name, data, target, horizon, connection)

    return predict_response

@model_prediction_router.get("/list_custom_models/")
async def list_models_user(connection=Depends(connect_to_db)):
    models_response = await load_models2(connection=connection, user_id=1)
    return models_response

@model_prediction_router.post("/xai/shap/{model_name}/")
async def shap_endpoint(model_name: str, data: List[float], feature_names: List[str]):
    shap_response = await calculate_shap(feature_names, model_name, data) 
    return shap_response


@model_prediction_router.post("/xai/lime/{model_name}/")
async def lime_endpoint(model_name: str, data: List[float], feature_names: List[str]):
  
    path = f"min_max/{model_name}.csv"

    data_df = pd.read_csv(path)
    
    lime_response = await calculate_lime(feature_names, model_name, data, data_df) 
    return lime_response

@model_prediction_router.post("/xai/anchors/{model_name}/")
async def anchors_endpoint(model_name: str, data: List[float], feature_names: List[str]):
    anchors_response = await calculate_anchors(feature_names, model_name, data) 
    return anchors_response

@model_prediction_router.post("/xai_custom/shap/{model_name}/")
async def shap_endpoint(model_name: str, data: List[float], feature_names: List[str]):
    shap_response = await calculate_shap_custom(feature_names, model_name, data) 
    return shap_response

   
@model_prediction_router.post("/xai_custom/lime/{model_name}/")
async def lime_endpoint(model_name: str, data: List[float], feature_names: List[str]):
    lime_response = await calculate_lime_custom(feature_names, model_name, data) 
    return lime_response

@model_prediction_router.post("/xai_custom/anchors/{model_name}/")
async def anchors_endpoint(model_name: str, data: List[float], feature_names: List[str]):
    anchors_response = await calculate_anchors_custom(feature_names, model_name, data) 
    return anchors_response


openai.api_key = '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'

@model_prediction_router.post("/chat/")
async def explain_with_chatgpt(xai_data: dict):
    method = xai_data.get("method")
    horizon = xai_data.get("horizon")
    target = xai_data.get("target")
    prediction = xai_data.get("prediction")
    xai_result = xai_data.get("xaiResult")

    if not all([method, horizon, target, prediction, xai_result]):
        return JSONResponse(content={"error": "Missing required fields"}, status_code=422)

    prompt = f"{method} Result: {xai_result}\nAI: Explain the {method} result for the prediction {prediction} of {horizon} {target} consumption in smart buildings."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "system", "content": "You are a helpful assistant that explains XAI results and give insights and interpretations."}, {"role": "user", "content": prompt}],
    )
    reply = response["choices"][0]["message"]["content"]

    return {"response": reply}




