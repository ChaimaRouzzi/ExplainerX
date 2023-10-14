from fastapi import APIRouter, Depends
from Data_Gathering.db_connection import connect_to_db, connect_to_db2
from Data_Preparation.data_preparation_logic import missing_values_imputation,verify_missing_values,outlires_handeling,scaling,verify_outlires,categorical_variabels,check_duplicates,delete_duplicate,encoding,verify_scaling,get_trace,get_status,get_column_status,preprocessing_tracabilité, time_series_transformation
router_data_preparation = APIRouter()


async def get_connection():
    connection = await connect_to_db()
    return connection


async def get_connection2():
    connection = await connect_to_db2()
    return connection


@router_data_preparation.get('/imputation/{version}/{updated}/{method}/{column}/{const}/{knn}')
async def imputation(
    version: str,
    updated:str,
    method:str,
    column:str,
    const:str,
    knn:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await missing_values_imputation(connection,connection2, version, updated, method,column,const,knn)
    else:
        response_data = await missing_values_imputation(connection2,connection2, version, updated, method,column,const,knn)
    return response_data


@router_data_preparation.get('/categorical/{version}/{updated}')
async def variabels(
    version: str,
    updated:str,
  
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await categorical_variabels(connection,connection2, version, updated)
    else:
        response_data = await categorical_variabels(connection2,connection2, version, updated)
    return response_data


@router_data_preparation.get('/check_duplecate/{version}/{updated}')
async def dup(
    version: str,
    updated:str,
  
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await check_duplicates(connection,connection2, version, updated)
    else:
        response_data = await check_duplicates(connection2,connection2, version, updated)
    return response_data

@router_data_preparation.get('/outlires/{version}/{updated}/{method}/{column}')
async def imputation(
    version: str,
    updated:str,
    method:str,
    column:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await outlires_handeling(connection,connection2, version, updated, method,column)
    else:
        response_data = await outlires_handeling(connection2,connection2, version, updated, method,column)
    return response_data


@router_data_preparation.get('/scaling/{version}/{updated}/{method}/{column}')
async def imputation(
    version: str,
    updated:str,
    method:str,
    column:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await scaling(connection,connection2, version, updated, method,column)
    else:
        response_data = await scaling(connection2,connection2, version, updated, method,column)
    return response_data


@router_data_preparation.get('/delete_duplecate/{version}/{updated}')
async def delete(
    version: str,
    updated:str,
   
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await  delete_duplicate(connection,connection2, version, updated)
    else:
        response_data = await  delete_duplicate(connection2,connection2, version, updated)
    return response_data

@router_data_preparation.get('/encoding/{version}/{updated}/{method}/{column}')
async def en(
    version: str,
    updated:str,
    method:str,
    column:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await encoding(connection,connection2, version, updated, method,column)
    else:
        response_data = await encoding(connection2,connection2, version, updated, method,column)
    return response_data

@router_data_preparation.get('/check_missing_values/{version}/{updated}/{threshold_percentage}')
async def check_missing_values(
    version: str,
    updated:str,
    connection=Depends(get_connection), 
    threshold_percentage=str, 
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await verify_missing_values(connection, version, updated,int(threshold_percentage))
    else:
        response_data = await verify_missing_values(connection2, version, updated,int(threshold_percentage))
    return response_data






@router_data_preparation.get('/check_outlires/{version}/{updated}/{threshold_percentage}')
async def check_outlires(
    version: str,
    updated:str,
    connection=Depends(get_connection), 
    threshold_percentage=str, 
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await verify_outlires(connection, version, updated,int(threshold_percentage))
    else:
        response_data = await verify_outlires(connection2, version, updated,int(threshold_percentage))
    return response_data


@router_data_preparation.get('/check_scaling/{version}/{updated}')
async def check_outlires(
    version: str,
    updated:str,
    connection=Depends(get_connection), 
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await verify_scaling(connection, version, updated)
    else:
        response_data = await verify_scaling(connection2, version, updated)
    return response_data

@router_data_preparation.get('/get_trace/{version}')
async def trace(
    version: str,
    connection2=Depends(get_connection2)):
   
    response_data = await get_trace(connection2, version)
    
    return response_data

@router_data_preparation.get('/get_status/{version}/{updated}')
async def stat(
    version: str,
    updated:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   
    if updated.lower() == 'false':
        response_data = await get_status(connection, version, updated)
    else:
        response_data = await get_status(connection2, version, updated)
    return response_data
    
   
@router_data_preparation.get('/get_column_status/{version}/{updated}')
async def col_stat(
    version: str,
    updated:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   
    if updated.lower() == 'false':
        response_data = await get_column_status(connection, version, updated)
    else:
        response_data = await get_column_status(connection2, version, updated)
    return response_data
    
   
@router_data_preparation.get('/preprocessing_trace/{version}/{updated}')
async def pr_trac(
    version: str,
    updated:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
   

    response_data = await preprocessing_tracabilité(connection,connection2, version, updated)
    return response_data
    
   

@router_data_preparation.get('/time_series/{version}/{updated}/{method}/{column}')
async def imputation(
    version: str,
    updated:str,
    method:str,
    column:str,
    connection=Depends(get_connection),
    connection2=Depends(get_connection2)):
    if updated.lower() == 'false':
        response_data = await time_series_transformation(connection,connection2, version, updated, method,column)
    else:
        response_data = await time_series_transformation(connection2,connection2, version, updated, method,column)
    return response_data