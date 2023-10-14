from fastapi import APIRouter, Depends
from Data_Gathering.db_connection import connect_to_db,connect_to_db2
from Data_Gathering.data_gathering_logic import fetch_data,fetch_data_version,fetch_data_updated_version

data_gathering_router = APIRouter()


@data_gathering_router.get("/get_data_from_dw")
async def get_data_from_db(connection=Depends(connect_to_db)):
    async with connection.acquire() as connection:
        response_data = await fetch_data(connection)
        return response_data
    

@data_gathering_router.get('/get_data_by_version/{version}')

async def get_data_from_db(version: str,connection=Depends(connect_to_db)):
    async with connection.acquire() as con:
        response_data = await fetch_data_version(con,version)
        return response_data
    



@data_gathering_router.get('/get_updated_data_by_version/{version}')

async def get_data_from_db(version: str,connection=Depends(connect_to_db2)):
    async with connection.acquire() as con:
        response_data = await fetch_data_updated_version(con,version)
        return response_data
    




