import asyncpg
from fastapi import APIRouter, Depends
from Data_Gathering.db_connection import connect_to_db,connect_to_db2
from Data_Gathering.data_gathering_logic import fetch_data, fetch_data_version

from Data_Understanding.Time_Series_Analysis.time_series_logic import perform_stationarity_kpss_test, perform_stationarity_adf_test, perform_stationarity_pp_test, perform_time_series_decomposition, calculate_acf, calculate_pacf


time_series_router = APIRouter()

@time_series_router.get("/{updated}/stationarity_kpsstest")
async def perform_stationarity_test_endpoint(column_name: str, version: str,updated=str, connection=Depends(connect_to_db), connection2=Depends(connect_to_db2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 

                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]

                stationarity_results = perform_stationarity_kpss_test(column_values, column_name)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                stationarity_results = perform_stationarity_kpss_test(column_values, column_name)
            return stationarity_results
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_kpss_test(column_values, column_name)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                stationarity_results = perform_stationarity_kpss_test(column_values, column_name)
            return stationarity_results

        
@time_series_router.get("/{updated}/stationarity_adftest")
async def perform_stationarity_test_endpoint(column_name: str, version: str,updated=str, connection=Depends(connect_to_db),connection2=Depends(connect_to_db2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 

                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_adf_test(column_values, column_name)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_adf_test(column_values, column_name)
            return stationarity_results
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_adf_test(column_values, column_name)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_adf_test(column_values, column_name)
            return stationarity_results
        

    

@time_series_router.get("/{updated}/stationarity_pptest")
async def perform_stationarity_test_endpoint(column_name: str, version: str,updated=str, connection=Depends(connect_to_db),connection2=Depends(connect_to_db2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 
                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_pp_test(column_values, column_name)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_pp_test(column_values, column_name)
            return stationarity_results
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_pp_test(column_values, column_name)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]
                stationarity_results = perform_stationarity_pp_test(column_values, column_name)
            return stationarity_results
    
    


@time_series_router.get("/{updated}/decomposition")
async def perform_stationarity_test_endpoint(column_name: str, model_type: str, version: str,updated=str, connection=Depends(connect_to_db),connection2=Depends(connect_to_db2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 
                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]
                decomposition_data = perform_time_series_decomposition(column_values, column_name, model_type)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]
                decomposition_data = perform_time_series_decomposition(column_values, column_name, model_type)
            return decomposition_data
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]
                decomposition_data = perform_time_series_decomposition(column_values, column_name, model_type)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]
                decomposition_data = perform_time_series_decomposition(column_values, column_name, model_type)
            return decomposition_data 
    

@time_series_router.get("/{updated}/acf")
async def calculate_acf_endpoint(column_name: str, num_lags: int, version: str,updated=str, connection=Depends(connect_to_db),connection2=Depends(connect_to_db2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 
                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]
                acf_values = calculate_acf(column_values, column_name, num_lags)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]
                acf_values = calculate_acf(column_values, column_name, num_lags)
            return acf_values
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]
                acf_values = calculate_acf(column_values, column_name, num_lags)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]
                acf_values = calculate_acf(column_values, column_name, num_lags)
            return acf_values
    


@time_series_router.get("/{updated}/pacf")
async def calculate_acf_endpoint(column_name: str, num_lags: int, version: str,updated=str, connection=Depends(connect_to_db),connection2=Depends(connect_to_db2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 
                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]
                pacf_values = calculate_pacf(column_values, column_name, num_lags)
            else: 
                data = await fetch_data_version(connection,version,updated)
                column_values = [entry[column_name] for entry in data]
                pacf_values = calculate_pacf(column_values, column_name, num_lags)
            return pacf_values
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]
                pacf_values = calculate_pacf(column_values, column_name, num_lags)
            else: 
                data = await fetch_data_version(connection2,version,updated)
                column_values = [entry[column_name] for entry in data]
                pacf_values = calculate_pacf(column_values, column_name, num_lags)
            return pacf_values
