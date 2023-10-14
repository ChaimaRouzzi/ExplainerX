from fastapi import APIRouter, Depends
from Data_Gathering.db_connection import connect_to_db, connect_to_db2
from Data_Understanding.Data_Analysis.data_analysis_logic import (
    get_missing_values,
    get_outlier_values,
    get_duplicate_rows,
    get_negative_values,
    get_missing_values_columns,
    get_outliers_columns,
    timeline,
    versions_rows,
    data_analysis,
    fetch_rows, 
    fetch_columns, 
    get_first_index, 
    get_last_index

)
from Data_Understanding.Multi_Column_Profiling.multi_column_logic import (multi_column)
from Data_Understanding.Initial_Profiling.initial_profiling_logic import initilal_profiling
router_understanding = APIRouter()


async def get_connection():
    connection = await connect_to_db()
    return connection


async def get_connection2():
    connection = await connect_to_db2()
    return connection


@router_understanding.get('/get_rows_number_by_version/{version}')
async def get_rows_number_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await fetch_rows(connection, version)
    return response_data


@router_understanding.get('/get_columns_number_by_version/{version}')
async def get_columns_number_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await fetch_columns(connection, version)
    return response_data


@router_understanding.get('/get_first_index_by_version/{version}')
async def get_first_index_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_first_index(connection, version)
    return response_data


@router_understanding.get('/get_last_index_by_version/{version}')
async def get_last_index_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_last_index(connection, version)
    return response_data


@router_understanding.get('/get_missing_values_by_version/{version}')
async def get_missing_values_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_missing_values(connection, version)
    return response_data


@router_understanding.get('/get_outliers_by_version/{version}')
async def get_outliers_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_outlier_values(connection, version)
    return response_data


@router_understanding.get('/get_duplicates_by_version/{version}')
async def get_duplicates_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_duplicate_rows(connection, version)
    return response_data


@router_understanding.get('/get_negative_values_by_version/{version}')
async def get_negative_values_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_negative_values(connection, version)
    return response_data


@router_understanding.get('/get_columns_missing_values_by_version/{version}')
async def get_columns_missing_values_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_missing_values_columns(connection, version)
    return response_data


@router_understanding.get('/get_columns_outliers_by_version/{version}')
async def get_columns_outliers_by_version(
    version: str,
    connection=Depends(get_connection)
):
    response_data = await get_outliers_columns(connection, version)
    return response_data


@router_understanding.get('/timeline')
async def get_timeline(connection=Depends(get_connection)):
    response_data = await timeline(connection)
    return response_data


@router_understanding.get('/versions_rows')
async def get_versions_rows(connection=Depends(get_connection)):
    response_data = await versions_rows(connection)
    return response_data

@router_understanding.get('/data_analysis/{version}/{updated}')
async def analyze_data(version: str, updated: str, connection=Depends(get_connection),connection2=Depends(get_connection2)):
    if (updated=='False'):
     response_data = await data_analysis(connection,connection2, version, updated)
    else:
      response_data = await data_analysis(connection2,connection, version, updated)    
    return response_data

@router_understanding.get('/multi_column_profiling/{version}/{updated}/{method}')
async def multi_column_profiling(version: str, updated: str,method:str, connection=Depends(get_connection),connection2=Depends(get_connection2)):
    if (updated=='False'):
     response_data = await multi_column(connection,connection2, version, updated,method)
    else:
       response_data = await multi_column(connection2,connection, version, updated,method)  
    return response_data

@router_understanding.get('/initial_profiling')
async def in_profiling( connection=Depends(get_connection),connection2=Depends(get_connection2)):
    response_data = await initilal_profiling(connection,connection2)
    return response_data


