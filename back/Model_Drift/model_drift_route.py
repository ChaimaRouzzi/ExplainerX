from fastapi import APIRouter, Depends,File,UploadFile,Form
from Data_Gathering.db_connection import connect_to_db, connect_to_db2
from Model_Drift.model_drift_logic import upload_file,detect_drift,retrainTotale,retrainIncremantale,save_data
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
model_drift_route = APIRouter()
async def get_connection():
    connection = await connect_to_db()
    return connection


async def get_connection2():
    connection = await connect_to_db2()
    return connection


@model_drift_route.post('/uploud_file')
async def variabels(
    file: UploadFile = File(...),
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   
        response_data = await upload_file(connection,connection2,file)
        return response_data 

class DriftDetectionData(BaseModel):
    model_name: str
    model_horizon:str
    model_target:str
    predictors: List[str]
    method: str
    driftType: str 
  

@model_drift_route.post('/drift_detection/')
async def detect_drift_endpoint(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    model_horizon: str = Form(...),
    model_target: str = Form(...),
    predictors:List[str]=Form(...),
    method: str = Form(...),
    driftType: str = Form(...),
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   
        response_data = await detect_drift(connection,connection2,file,model_name,model_horizon,model_target,predictors,method,driftType)
        return response_data 


@model_drift_route.post('/retrain_totale/')
async def retrain_totale_endpoint(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    model_horizon: str = Form(...),
    model_target: str = Form(...),
    predictors:List[str]=Form(...),
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   
        response_data = await retrainTotale(connection,connection2,file,model_name,model_horizon,model_target,predictors)
        return response_data 

@model_drift_route.post('/retrain_incremantale/')
async def retrain_incremantal_endpoint(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    model_horizon: str = Form(...),
    model_target: str = Form(...),
    predictors:List[str]=Form(...),
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   
        response_data = await retrainIncremantale(connection,connection2,file,model_name,model_horizon,model_target,predictors)
        return response_data 


@model_drift_route.post('/save_data/')
async def retrain_incremantal_endpoint(
    file: UploadFile = File(...),
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   
        response_data = await save_data(connection,connection2,file)
        return response_data 

