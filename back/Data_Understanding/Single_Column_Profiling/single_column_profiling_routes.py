import asyncpg
from fastapi import APIRouter, Depends
from Data_Gathering.db_connection import connect_to_db,connect_to_db2
from Data_Gathering.data_gathering_logic import fetch_data, fetch_data_version
import numpy as np 
from Data_Understanding.Single_Column_Profiling.single_column_profiling_logic import count_missing_values, count_negative_values, count_outliers, count_unique_values, count_zero_values, describe_data, updated_versions_number, detect_data_types, single_column
from Data_Understanding.Data_Analysis.data_analysis_logic import versions_number
from datetime import datetime
single_column_profiling_router = APIRouter()
 
async def get_connection():
    connection = await connect_to_db()
    return connection


async def get_connection2():
    connection = await connect_to_db2()
    return connection

@single_column_profiling_router.get("/{updated}/missing_values")
async def missing_values_endpoint(column_name: str, version: str,updated=str, connection=Depends(get_connection) ,connection2=Depends(get_connection2)):
    
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 
                data = await fetch_data(connection,updated)
                print(data)
                column_values = [entry[column_name] for entry in data]

                missing_values = count_missing_values(column_values)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                missing_values = count_missing_values(column_values)
            return missing_values
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]

                missing_values = count_missing_values(column_values)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                missing_values = count_missing_values(column_values)
            return missing_values


@single_column_profiling_router.get("/{updated}/outliers")
async def outliers_endpoint(column_name: str,updated:str, version: str, connection=Depends(get_connection), connection2=Depends(get_connection2)):
    async with connection.acquire() as connection:
        if (updated=='False'):
            if version == "-1": 
                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]

                outliers = count_outliers(column_values)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                outliers = count_outliers(column_values)
            return outliers
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]

                outliers = count_outliers(column_values)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                outliers = count_outliers(column_values)
            return outliers  

@single_column_profiling_router.get("/{updated}/negative_values")
async def negative_values_endpoint(column_name: str, version: str,updated=str, connection=Depends(get_connection),connection2=Depends(get_connection2)):
    async with connection.acquire() as connection:
        if (updated=='False'):
            if version == "-1": 

                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]

                negative_values = count_negative_values(column_values)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                negative_values = count_negative_values(column_values)
            return negative_values
        else:
            if version == "-1": 

                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]

                negative_values = count_negative_values(column_values)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                negative_values = count_negative_values(column_values)
            return negative_values 

@single_column_profiling_router.get("/{updated}/zero_values")
async def zero_values_endpoint(column_name: str, version: str,updated=str, connection=Depends(get_connection),connection2=Depends(get_connection2)):
    async with connection.acquire() as connection:
        if (updated=='False'):
            if version == "-1": 

                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]

                zero_values = count_zero_values(column_values)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                zero_values = count_zero_values(column_values)
            return zero_values
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]

                zero_values = count_zero_values(column_values)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                zero_values = count_zero_values(column_values)
            return zero_values

@single_column_profiling_router.get("/{updated}/describe")
async def describe_data_endpoint(column_name: str, version: str,updated=str, connection=Depends(get_connection),connection2=Depends(get_connection2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1": 
                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]

                desc = describe_data(column_values)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                desc = describe_data(column_values)
            return desc
        else: 
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]

                desc = describe_data(column_values)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                desc = describe_data(column_values)
            return desc 
        
        

@single_column_profiling_router.get("/{updated}/data_types")
async def data_types_endpoint(column_name: str, version: str,updated=str, connection=Depends(get_connection), connection2=Depends(get_connection2)):
    if(updated=='False'):
        async with connection.acquire() as connection:
            if version == "-1": 

                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]

                types = detect_data_types(column_values)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                types = detect_data_types(column_values)
            return types
    else:
            if version == "-1": 

                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]

                types = detect_data_types(column_values)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                types = detect_data_types(column_values)
            return types  
    
@single_column_profiling_router.get("/{updated}/unique_values")
async def unique_values_endpoint(column_name: str, version: str,updated=str, connection=Depends(get_connection), connection2=Depends(get_connection2)):
    async with connection.acquire() as connection:
        if (updated=='False'):
            if version == "-1": 

                data = await fetch_data(connection,updated)
                column_values = [entry[column_name] for entry in data]

                unique_values = count_unique_values(column_values)
            else: 
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]

                unique_values = count_unique_values(column_values)
            return unique_values
        else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                column_values = [entry[column_name] for entry in data]

                unique_values = count_unique_values(column_values)
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                unique_values = count_unique_values(column_values)
            return unique_values 


@single_column_profiling_router.get("/{updated}/get_column_data_by_version")
async def gt_column(column_name: str, version: str,updated=str, connection=Depends(get_connection),connection2=Depends(get_connection2)):
    async with connection.acquire() as connection:
        if(updated=='False'):
            if version == "-1":
                data = await fetch_data(connection,updated)
            else:
                data = await fetch_data_version(connection, version,updated)


            column_values = [entry[column_name] for entry in data if entry[column_name] is not None]


            hist_counts, hist_bins = np.histogram(column_values, bins='auto')


            date_values = [entry["date"] for entry in data if entry["date"] is not None]
            date_values = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() for date_str in date_values]
        
            daily_date_values = list(set(date_values))  
            daily_date_values.sort()  


            aggregated_values = []
            for daily_date in daily_date_values:
                daily_value_sum = sum([value for value, date in zip(column_values, date_values) if date == daily_date])
                aggregated_values.append(daily_value_sum)


            result = {
                "column_values": aggregated_values,
                "hist_counts": hist_counts.tolist(),
                "hist_bins": hist_bins.tolist(),
                "date_values": daily_date_values  
            }


            return result
        else:
            if version == "-1":
                data = await fetch_data(connection2,updated)
            else:
                data = await fetch_data_version(connection2, version,updated)


            column_values = [entry[column_name] for entry in data if entry[column_name] is not None]


            hist_counts, hist_bins = np.histogram(column_values, bins='auto')


            date_values = [entry["date"] for entry in data if entry["date"] is not None]
            date_values = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() for date_str in date_values]
        
            daily_date_values = list(set(date_values))  
            daily_date_values.sort()  


            aggregated_values = []
            for daily_date in daily_date_values:
                daily_value_sum = sum([value for value, date in zip(column_values, date_values) if date == daily_date])
                aggregated_values.append(daily_value_sum)


            result = {
                "column_values": aggregated_values,
                "hist_counts": hist_counts.tolist(),
                "hist_bins": hist_bins.tolist(),
                "date_values": daily_date_values  
            }


            return result


@single_column_profiling_router.get('/{updated}/version_number')
async def ver_num(
    connection=(Depends(get_connection))
):
    response_data = await versions_number(connection)
    return response_data

@single_column_profiling_router.get('/{updated}/updated_versions')
async def ver_num(
    connection2=(Depends(get_connection2))
):
    response_data = await updated_versions_number(connection2)
    return response_data


@single_column_profiling_router.get('/{version}/{updated}/{column_name}')
async def single_column_profiling(version: str, updated: str,column_name:str, connection=Depends(get_connection),connection2=Depends(get_connection2)):
    
     response_data = await single_column(connection,connection2,updated,column_name,version) 
     return response_data
