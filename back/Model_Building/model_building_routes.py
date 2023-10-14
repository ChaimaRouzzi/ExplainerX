from fastapi import APIRouter, Depends, Request
from Data_Gathering.db_connection import connect_to_db, connect_to_db2
from Model_Building.model_building_svr_logic import build_svr_model, SVRParameters, save_model_details_svr, SavedModelSVR, get_all_model_details
from Data_Gathering.data_gathering_logic import fetch_data2
from Model_Building.model_building_rf_logic import build_rf_model, RandomForestParameters, save_model_details_rf, SavedModelRF
from Model_Building.external_model_building import upload_dataframe, get_dataframe, upload_model, save_external_model
from typing import List
from fastapi import UploadFile, File
from pydantic import BaseModel
from Authentication.authentication_logic import get_current_active_user
from Model_Building.model_building_mlr_logic import build_mlr_model, MLRParameters, SavedModelMLR, save_model_details_mlr


model_building_router = APIRouter()

@model_building_router.post("/build_svr_model/")
async def build_svr_model_endpoint(
    params: SVRParameters,
    connection=Depends(connect_to_db2),
    current_user: int = Depends(get_current_active_user),
):
    async with connection.acquire() as connection:
        print(current_user)
        data = await fetch_data2(connection)
        build_svr_response = build_svr_model(data, params)
        return build_svr_response
        

@model_building_router.post("/save_model_svr/")
async def save_model_endpoint_svr(saved_model: SavedModelSVR,  connection=Depends(connect_to_db), connection2=Depends(connect_to_db2)):
    save_model_response = await save_model_details_svr(connection, connection2, saved_model)
    return save_model_response

@model_building_router.post("/build_rf_model/")
async def build_rf_model_endpoint(params: RandomForestParameters, connection=Depends(connect_to_db2), current_user: int = Depends(get_current_active_user),
   ):
    async with connection.acquire() as connection:
        data = await fetch_data2(connection)
        build_rf_response = build_rf_model(data, params)
        return build_rf_response


@model_building_router.post("/build_mlr_model/")
async def build_mlr_model_endpoint(params: MLRParameters, connection=Depends(connect_to_db2), current_user: int = Depends(get_current_active_user),
   ):
    async with connection.acquire() as connection:
        data = await fetch_data2(connection)
        build_mlr_response = build_mlr_model(data, params)
        return build_mlr_response

@model_building_router.post("/save_model_mlr/")
async def save_model_endpoint_mlr(saved_model: SavedModelMLR,  connection=Depends(connect_to_db), connection2=Depends(connect_to_db2)):
    save_model_response = await save_model_details_mlr(connection, connection2, saved_model)
    return save_model_response        


@model_building_router.post("/save_model_rf/")
async def save_model_endpoint_rf(saved_model: SavedModelRF,  connection=Depends(connect_to_db), connection2=Depends(connect_to_db2)):
    save_model_response = await save_model_details_rf(connection, connection2, saved_model)
    return save_model_response

@model_building_router.get("/models_list/")
async def get_models(connection=Depends(connect_to_db)):
    model_details_list = await get_all_model_details(connection)
    return model_details_list

class UploadDataModel(BaseModel):
    features: List[str]
    horizon: str

    
@model_building_router.post("/upload_data/")
async def upload_data_endpoint(request_data: UploadDataModel, connection=Depends(connect_to_db2)):
    async with connection.acquire() as connection:
        feature_names = request_data.features
        horizon = request_data.horizon
        data = await fetch_data2(connection)
        response_upload_data = await upload_dataframe(data, feature_names, horizon)
        return response_upload_data

@model_building_router.post("/upload_model/")
async def upload_model_endpoint(file: UploadFile = File(...)):
    response_upload_model = await upload_model(file)
    return response_upload_model

class SaveModelRequest(BaseModel):
    user_id: int
    model_name: str
    features: List[str]
    target: str
    horizon: str

@model_building_router.post("/save_external_model/")
async def save_model_endpoint(request_data: SaveModelRequest, connection=Depends(connect_to_db), connection2=Depends(connect_to_db2)):
    user_id = request_data.user_id
    model_name = request_data.model_name
    features = request_data.features
    target = request_data.target
    horizon = request_data.horizon
    response_save_model = await save_external_model(connection, connection2, user_id, model_name, features, target, horizon)
    return response_save_model

    
@model_building_router.get("/get_data/")
async def get_data():
    dataframe = await get_dataframe()
    return dataframe