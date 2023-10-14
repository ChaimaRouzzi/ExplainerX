import json
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler,StandardScaler,RobustScaler
from Data_Understanding.Data_Analysis.data_analysis_logic import (fetch_data_updated_version)

import subprocess
async def missing_values_imputation(connection,connexion2,version,updated,method,column,const,knn):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)
    print(df)
    if(method=='imputation_mean'):
            mean_value = df[column].mean()
            df[column].fillna(mean_value, inplace=True)
          

    if(method=='imputation_median'):
        mode_value = stats.mode(df[column]).mode[0]
        df[column] = df[column].fillna(mode_value)     
    
    if(method=='imputation_back'):
        
        df[column] = df[column].fillna(method='bfill')
    if(method=='imputation_median'):
        mode_value = df[column].median()
        df[column] = df[column].fillna(mode_value)     
    if(method=='imputation_const'): 
        df[column] = df[column].fillna(const)     
    if(method=='imputation_for'):
        mode_value =df[column].fillna(method='ffill')
        df[column] = df[column].fillna(mode_value)     
    if(method=='imputation_lin'):

        df[column] = df[column].interpolate(method='linear')  
    if(method=='imputation_pol'):
        df[column] = df[[column]].interpolate(method='polynomial', order=2)[column]
    if(method=='imputation_knn'):
       knn_imputer = KNNImputer(n_neighbors= int(knn))  # Replace 2 with the desired number of neighbors
       df[column] = knn_imputer.fit_transform(df[[column]])

    insert_query = f'''INSERT INTO "operation_tracabilite" ("version", "Operation", "Column", "Method") 
                VALUES ('{version}', 'imputation', '{column}', '{method}')'''
    delete_query = f'''DELETE FROM "operation_tracabilite" WHERE "version"={version}'''
    if (updated=='False' and await check_updated_version(connexion2,version)==1):
         await connexion2.execute(delete_query)
    if(int(version)!=-1):
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version}  order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version} order by "date" desc  limit 1'''  
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
    else:
        version1=await get_first_version(connection)
        version2=await get_last_version(connection)
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version1} order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version2} order by "date" desc  limit 1''' 
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
   
    new_order = ['date', 'Gas_01', 'Gas_02', 'Gas_03', 'Electricity', 'Maximum_Humidity', 'Solar_Radiation',
             'Day_Degree_Hot', 'Day_Degree_Cold', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp',
             'Min_OutdoorTemp', 'Year', 'Month', 'Week', 'Day', 'Hour']

    df = df.reindex(columns=new_order)
    df = transform_float_precision(df)
    print(first_id,last_id)
    ids = list(range(first_id, last_id+1 ))
    df['id'] = ids
    
    await connexion2.execute(insert_query)
    df.to_csv('updated_data.csv', index=False)
    integrate_dimensions_update_data()
    integrate_facts_update_data()
    await update_version(version,connexion2)


async def outlires_handeling(connection,connexion2,version,updated,method,column):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)
    count_outliers(df,column)
    if(method=='IQR_capping'):
        df[column] = iqr_capping(df[column])

    if(method=='IQR_Trimming'):
           df[column] = iqr_trimming(df[column])
    if(method=='Mean_Imputation'):   
       df[column] = replace_outliers_with_mean(df[column])
    if(method=='Median_Imputation'):
         df[column] = replace_outliers_with_median(df[column])  

    insert_query = f'''INSERT INTO "operation_tracabilite" ("version", "Operation", "Column", "Method") 
                VALUES ('{version}', 'outlires handeling', '{column}', '{method}')'''
    delete_query = f'''DELETE FROM "operation_tracabilite" WHERE "version"={version}'''
    if (updated=='False' and await check_updated_version(connexion2,version)==1):
         await connexion2.execute(delete_query)
    if(int(version)!=-1):
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version}  order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version} order by "date" desc  limit 1'''  
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
    else:
        version1=await get_first_version(connection)
        version2=await get_last_version(connection)
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version1} order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version2} order by "date" desc  limit 1''' 
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
   
    new_order = ['date', 'Gas_01', 'Gas_02', 'Gas_03', 'Electricity', 'Maximum_Humidity', 'Solar_Radiation',
             'Day_Degree_Hot', 'Day_Degree_Cold', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp',
             'Min_OutdoorTemp', 'Year', 'Month', 'Week', 'Day', 'Hour']

    df = df.reindex(columns=new_order)
    df = transform_float_precision(df)
    print(first_id,last_id)
    ids = list(range(first_id, last_id+1 ))
    df['id'] = ids
    count_outliers(df,column)
    await connexion2.execute(insert_query)
    df.to_csv('updated_data.csv', index=False)
    integrate_dimensions_update_data()
    integrate_facts_update_data()
    await update_version(version,connexion2)


async def scaling(connection,connexion2,version,updated,method,column):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)
    print(df)
    if(method=='Standard_Scaler'):
       
        standard_scaler = StandardScaler()
        print(df[column])
        df[column] = standard_scaler.fit_transform(df[column].values.reshape(-1, 1))  
        print(df[column])

    if(method=='Min-Max_Scaler'):
        min_max_scaler = MinMaxScaler()
        df[column] = min_max_scaler.fit_transform(df[column].values.reshape(-1, 1))   
    if(method=='Robust_Scaler'):
        
      robust_scaler = RobustScaler()
      df[column] = robust_scaler.fit_transform(df[column].values.reshape(-1, 1))  
   
    
    print(df[column])
    insert_query = f'''INSERT INTO "operation_tracabilite" ("version", "Operation", "Column", "Method") 
                VALUES ('{version}', 'scaling', '{column}', '{method}')'''
    delete_query = f'''DELETE FROM "operation_tracabilite" WHERE "version"={version}'''
    if (updated=='False' and await check_updated_version(connexion2,version)==1):
         await connexion2.execute(delete_query)
    if(int(version)!=-1):
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version}  order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version} order by "date" desc  limit 1'''  
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
    else:
        version1=await get_first_version(connection)
        version2=await get_last_version(connection)
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version1} order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version2} order by "date" desc  limit 1''' 
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
   
    new_order = ['date', 'Gas_01', 'Gas_02', 'Gas_03', 'Electricity', 'Maximum_Humidity', 'Solar_Radiation',
             'Day_Degree_Hot', 'Day_Degree_Cold', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp',
             'Min_OutdoorTemp', 'Year', 'Month', 'Week', 'Day', 'Hour']

    df = df.reindex(columns=new_order)
    df = transform_float_precision(df)
    print(first_id,last_id)
    ids = list(range(first_id, last_id+1 ))
    df['id'] = ids
    
    await connexion2.execute(insert_query)
    df.to_csv('updated_data.csv', index=False)
    integrate_dimensions_update_data()
    integrate_facts_update_data()
    await update_version(version,connexion2)





async def encoding(connection,connexion2,version,updated,method,column):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)
    print(df)
    data_type = df[column].dtype
    is_categorical = data_type == 'object' or pd.api.types.is_categorical_dtype(df[column])
    if is_categorical:
        df[column]=pd.get_dummies(df, columns=[column])
    
    print(df[column])
    insert_query = f'''INSERT INTO "operation_tracabilite" ("version", "Operation", "Column", "Method") 
                VALUES ('{version}', 'scaling', '{column}', '{method}')'''
    delete_query = f'''DELETE FROM "operation_tracabilite" WHERE "version"={version}'''
    if (updated=='False' and await check_updated_version(connexion2,version)==1):
         await connexion2.execute(delete_query)
    if(int(version)!=-1):
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version}  order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version} order by "date" desc  limit 1'''  
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
    else:
        version1=await get_first_version(connection)
        version2=await get_last_version(connection)
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version1} order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version2} order by "date" desc  limit 1''' 
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
   
    new_order = ['date', 'Gas_01', 'Gas_02', 'Gas_03', 'Electricity', 'Maximum_Humidity', 'Solar_Radiation',
             'Day_Degree_Hot', 'Day_Degree_Cold', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp',
             'Min_OutdoorTemp', 'Year', 'Month', 'Week', 'Day', 'Hour']

    df = df.reindex(columns=new_order)
    df = transform_float_precision(df)
    print(first_id,last_id)
    ids = list(range(first_id, last_id+1 ))
    df['id'] = ids
    
    await connexion2.execute(insert_query)
    df.to_csv('updated_data.csv', index=False)
    integrate_dimensions_update_data()
    integrate_facts_update_data()
    await update_version(version,connexion2)


async def categorical_variabels(connection,connexion2,version,updated):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)
    print(df)
    response_data=[]
    for column in df.columns:
        data_type = df[column].dtype
        is_categorical = data_type == 'object' or pd.api.types.is_categorical_dtype(df[column])
        if is_categorical and column !='date':
            response_data.append(column)
    return json.dumps(response_data)



async def check_duplicates(connection,connexion2,version,updated):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    result=[]
    df = pd.DataFrame(response_data)
    print(df)
    duplicate_rows = df.duplicated()
    response_data=''
    if duplicate_rows.any():
      return  True
    else:
       return json.dumps(result) 



async def delete_duplicate(connection,connexion2,version,updated,Hour,Day,Month,year):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)
    df = df.drop((df['Day'] ==  Day) & (df['Month'] == Month) & (df['Hour'] == Hour) & (df['Year'] == year))
    insert_query = f'''INSERT INTO "operation_tracabilite" ("version", "Operation", "Column", "Method") 
                VALUES ('{version}', 'delete_duplicates', 'all', '')'''
    delete_query = f'''DELETE FROM "operation_tracabilite" WHERE "version"={version}'''
    if (updated=='False' and await check_updated_version(connexion2,version)==1):
         await connexion2.execute(delete_query)
    if(int(version)!=-1):
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version}  order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version} order by "date" desc  limit 1'''  
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
    else:
        version1=await get_first_version(connection)
        version2=await get_last_version(connection)
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version1} order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version2} order by "date" desc  limit 1''' 
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
   
    new_order = ['date', 'Gas_01', 'Gas_02', 'Gas_03', 'Electricity', 'Maximum_Humidity', 'Solar_Radiation',
             'Day_Degree_Hot', 'Day_Degree_Cold', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp',
             'Min_OutdoorTemp', 'Year', 'Month', 'Week', 'Day', 'Hour']

    df = df.reindex(columns=new_order)
    df = transform_float_precision(df)
    print(first_id,last_id)
    ids = list(range(first_id, last_id+1 ))
    df['id'] = ids
    
    await connexion2.execute(insert_query)
    df.to_csv('updated_data.csv', index=False)
    integrate_dimensions_update_data()
    integrate_facts_update_data()
    await update_version(version,connexion2)




def integrate_dimensions_update_data(): 
   
   
    # Set the CSV file path to be passed as a context parameter
    csv_file_path = "C:/Users/Admin/Desktop/ExplainerX_Backend/updated_data.csv"
    # Define the path to the Talend job executable
    talend_job_path_dimensions = 'C:/Program Files (x86)/TOS_DI-8.0.1/studio/create_dimentions_table_version_2/create_dimentions_table_version_2_run.bat'
    # Construct the command to run the Talend job with the context parameter
    command_dimensions = [
        talend_job_path_dimensions,
        "--context=context",  # Replace 'your_context_name' with the actual context name in your Talend job
        "-job", "create_dimentions_table_version_2 0.1",  # Replace 'your_talend_job_name' with the actual Talend job name
        "--context_param",
        f"csvpath={csv_file_path}"
    ]

    # Execute the command using subprocess
    subprocess.run(command_dimensions, shell=True)

   
def integrate_facts_update_data(): 

   
    # Set the CSV file path to be passed as a context parameter
    csv_file_path ="C:/Users/Admin/Desktop/ExplainerX_Backend/updated_data.csv"
    talend_job_path_facts= "C:/Program Files (x86)/TOS_DI-8.0.1/studio/create_facts_2/create_facts_2_run.bat"
    # Construct the command to run the Talend job with the context parameter
    command_facts = [
        talend_job_path_facts,
        "--context=context",  # Replace 'your_context_name' with the actual context name in your Talend job
        "-job", "create_facts_2 0.1",  # Replace 'your_talend_job_name' with the actual Talend job name
        "--context_param",
        f"csvpath={csv_file_path}"
    ]
    subprocess.run(command_facts, shell=True)

async def update_version(version,connexion2):
    if(int(version)!=-1):
        update_electricity = f'''UPDATE electricity 
                    SET "updated" = '{1}'
                    WHERE "version"={version}'''
        update_gaz = f'''UPDATE gaz 
                    SET "updated" = '{1}'
                    WHERE "version"={version}'''
        update_time = f'''UPDATE time 
                    SET "updated" = '{1}'
                    WHERE "version"={version}'''
        update_temperature = f'''UPDATE temperature 
                    SET "updated" = '{1}'
                    WHERE "version"={version}'''
        
    

        update_solar_radiation = f'''UPDATE solar_radiation 
                    SET "updated" = '{1}'
                    WHERE "version"={version}'''
        update_humidity = f'''UPDATE humidity 
                SET "updated" = '{1}'
                    WHERE "version"={version}'''
    else:
        update_electricity = f'''UPDATE electricity 
                    SET "updated" = '{1}' '''
        update_gaz = f'''UPDATE gaz 
                    SET "updated" = '{1}' '''
        update_time = f'''UPDATE time 
                    SET "updated" = '{1}' '''
        update_temperature = f'''UPDATE temperature 
                    SET "updated" = '{1}' '''
        
    

        update_solar_radiation = f'''UPDATE solar_radiation 
                    SET "updated" = '{1}' '''
        update_humidity = f'''UPDATE humidity 
                SET "updated" = '{1}' '''
    await connexion2.execute(update_electricity)
    await connexion2.execute(update_gaz)
    await connexion2.execute(update_humidity)
    await connexion2.execute(update_solar_radiation)
    await connexion2.execute(update_temperature)
    await connexion2.execute(update_time)
def transform_float_precision(df):
    for column in df.columns:
        if df[column].dtype == float:
            df[column] = df[column].round(6)
    return df

async def get_first_version(connection):
    first_version_q=f'''SELECT "version" FROM time   order by "Time_Id" asc  limit 1''' 
    first_version_query=await connection.fetchrow(first_version_q)
    first_version=first_version_query["version"] if first_version_query else None
    return first_version
async def get_last_version(connection):
    first_version_q=f'''SELECT "version" FROM time   order by "Time_Id" desc  limit 1''' 
    first_version_query=await connection.fetchrow(first_version_q)
    first_version=first_version_query["version"] if first_version_query else None
    return first_version
async def check_updated_version(connection2,version):
    first_version_q=f'''SELECT "updated" FROM time where "version"={version}  order by "Time_Id" desc  limit 1''' 
    first_version_query=await connection2.fetchrow(first_version_q)
    first_version=first_version_query["updated"] if first_version_query else None
   
    return first_version

async def verify_missing_values(connection,version,updated,threshold_percentage):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []

    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)

    print(df)
    response = []
    total_rows = len(df)
    threshold_count = int(total_rows * threshold_percentage / 100)
    print(threshold_count)

    for column in df.columns:
        missing_values = sum(1 for item in df[column] if item is None)
        print(column,threshold_count,missing_values)
        if df[column].isnull().sum() > threshold_count:
            response.append(column)
     
    
    return  json.dumps(response)


async def verify_outlires(connection,version,updated,outlier_percentage):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []

    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)

    response = []
    total_rows = len(df)
    outlier_threshold_count = int(total_rows * outlier_percentage / 100)

    for column in df.columns:
        col_values = df[column]
        is_numeric = pd.api.types.is_numeric_dtype(col_values)
        if is_numeric:
        # Check if the column contains any outliers
            has_outliers = False
            q1 = col_values.quantile(0.25)
            q3 = col_values.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            num_outliers = ((col_values < lower_bound) | (col_values > upper_bound)).sum()
            
            # Check if the percentage of outliers exceeds the specified threshold
            if num_outliers > outlier_threshold_count:
             response.append(column)
    return json.dumps(response)





async def verify_scaling(connection,version,updated):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []

    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)

    response = []
    for column in df.columns:
        
             response.append(column)
    return json.dumps(response)




def iqr_capping(series, lower_percentile=0.25, upper_percentile=0.75):
    q1 = series.quantile(lower_percentile)
    q3 = series.quantile(upper_percentile)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return series.apply(lambda x: min(upper_bound, max(lower_bound, x)))

# IQR Trimming
def iqr_trimming(series, lower_percentile=0.25, upper_percentile=0.75):
    q1 = series.quantile(lower_percentile)
    q3 = series.quantile(upper_percentile)
    return series.apply(lambda x: x if q1 <= x <= q3 else np.nan)
def replace_outliers_with_mean(series, lower_percentile=0.25, upper_percentile=0.75):
    q1 = series.quantile(lower_percentile)
    q3 = series.quantile(upper_percentile)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Calculate the mean of the non-outlier values
    non_outliers = series[(series >= lower_bound) & (series <= upper_bound)]
    mean_non_outliers = non_outliers.mean()

    # Replace outliers with the mean of non-outliers
    return series.apply(lambda x: mean_non_outliers if (x < lower_bound or x > upper_bound) else x)
def replace_outliers_with_median(series, lower_percentile=0.25, upper_percentile=0.75):
    q1 = series.quantile(lower_percentile)
    q3 = series.quantile(upper_percentile)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Calculate the median of the non-outlier values
    non_outliers = series[(series >= lower_bound) & (series <= upper_bound)]
    median_non_outliers = non_outliers.median()

    # Replace outliers with the median of non-outliers
    return series.apply(lambda x: median_non_outliers if (x < lower_bound or x > upper_bound) else x)
def count_outliers(df, column_name):
    # Calculate Q1 and Q3
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    
    # Calculate IQR
    IQR = Q3 - Q1
    
    # Define the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter the outliers and count them
    outliers_count = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)][column_name].count()
    
    print(outliers_count)



async def get_trace(connection,version,updated):
    if(updated=='True'):
        if (version==-1):
            query = f'''SELECT "Operation", "Column", "Method" FROM operation_tracabilite'''
        else:
            query = f'''SELECT "Operation", "Column", "Method" FROM operation_tracabilite WHERE version IN ({version}, -1) ''' 
            operations = await connection.fetch(query)
            response_array = []
            for operation in operations:
                response_record = {
                    "operation": operation["Operation"],
                    "column": operation["Column"],
                    "method": operation["Method"]
                }
                response_array.append(response_record)
        
        return json.dumps(response_array)
    else:
          response_array = [] 
          return json.dumps(response_array)


async def get_status(connection,version,updated):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    response=[]

    df = pd.DataFrame(response_data)
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    # Find outliers using the IQR method
    outliers = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))

    # Count the number of outliers
    number_of_outliers = int(outliers.sum().sum())

    stats = {
    'number_of_rows': len(df),
    'number_of_columns': len(df.columns),
    'number_of_missing_values': int(df.isnull().sum().sum()),
    'number_of_zero_values': int((df == 0).sum().sum()),
    'number_of_duplicate_rows': int(df.duplicated().sum()),
    'number_of_outliers': number_of_outliers
     }
    response.append(stats)
    return response


async def get_column_status(connection,version,updated):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')
    data= await fetch_data_updated_version(connection,version,updated)
    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    response = []
    df = pd.DataFrame(response_data)

    for column in df.columns:
        column_data = df[column]
        if pd.api.types.is_numeric_dtype(column_data):  # Check if the column is numeric
            Q1 = column_data.quantile(0.25)
            Q3 = column_data.quantile(0.75)
            IQR = Q3 - Q1

    
            outliers = ((column_data < (Q1 - 1.5 * IQR)) | (column_data > (Q3 + 1.5 * IQR)))

    
            number_of_outliers = int(outliers.sum().sum())
            stats = {
                'column': column,
                'Min': round(float(column_data.min()),2),
                'Max': round(float(column_data.max()),2),
                'Mean':round(float(column_data.mean()),2),
                'Unique': int(column_data.nunique()),
                'Missing_Values': int(column_data.isnull().sum()),
                'Outliers': number_of_outliers,  # Implement your outlier detection logic here
                'Negative': int((column_data < 0).sum()),
                'Zeros': int((column_data == 0).sum())
            }
            response.append(stats)
    response_json = json.dumps(response)
   
    return response_json




async def preprocessing_tracabilité(connection,connection2, version,updated):
   
    data1=await fetch_data_updated_version(connection,version,'False')
    data2= await fetch_data_updated_version(connection2,version,'True')
    status1= await get_status(connection,version,'False')
    columns_status1=await get_column_status(connection,version,'False')
    trace=await get_trace(connection2,version,updated)
    status2=await get_status(connection2,version,'True')
    columns_status2= await get_column_status(connection2,version,'True')
        

    result={"trace":trace,"status1":status1,"columns_status1":columns_status1,"status2":status2,"columns_status2":columns_status2,'data1':data1,'data2':data2}
         
    
    return  json.dumps(result)
        


async def time_series_transformation(connection,connexion2,version,updated,method,column):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')
        electricity = await connection.fetch(f'SELECT * FROM electricity WHERE "version"={version} ORDER BY "Time_Id" ASC')
        gaz = await connection.fetch(f'SELECT * FROM gaz WHERE "version"={version} ORDER BY "Time_Id" ASC')
        temperature = await connection.fetch(f'SELECT * FROM temperature WHERE "version"={version} ORDER BY "Temperature_Id" ASC')
        humidity = await connection.fetch(f'SELECT * FROM humidity WHERE "version"={version} ORDER BY "Humidity_Id" ASC')
        solar_radiation = await connection.fetch(f'SELECT * FROM solar_radiation WHERE "version"={version} ORDER BY "Solar_Radiation_Id" ASC')

    response_data = []
    if(updated=='False'):
        for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):
            formatted_date = Time[0].strftime("%Y-%m-%d %H:%M:%S")
            day_degree_cold = round(float(Temp[3]), 6) if isinstance(Temp[3], float) else Temp[3]
            day_degree_hot = round(float(Temp[4]), 6) if isinstance(Temp[4], float) else Temp[4]
            min_outdoor_temp = round(float(Temp[0]), 6) if isinstance(Temp[0], float) else Temp[0]
            average_outdoor_temp = round(float(Temp[1]), 6) if isinstance(Temp[1], float) else Temp[1]
            max_outdoor_temp = round(float(Temp[2]), 6) if isinstance(Temp[2], float) else Temp[2]
            max_humidity = round(float(Humidity[1]), 6) if isinstance(Humidity[1], float) else Humidity[1]
            average_humidity = round(float(Humidity[0]), 6) if isinstance(Humidity[0], float) else Humidity[0]
            solar_radiation_val = round(float(Solar[0]), 6) if isinstance(Solar[0], float) else Solar[0]
            electricity_val = round(float(Electricity[4]), 6) if isinstance(Electricity[4], float) else Electricity[4]
            gas_01 = round(float(Gas[5]), 6) if isinstance(Gas[5], float) else Gas[5]
            gas_02 = round(float(Gas[4]), 6) if isinstance(Gas[4], float) else Gas[4]
            gas_03 = round(float(Gas[6]), 6) if isinstance(Gas[6], float) else Gas[6]

            response_data.append(
                {
                    "date": formatted_date,
                    "Electricity": Electricity[0],
                    "Gas_01": Gas[1],
                    "Gas_02": Gas[2],
                    "Gas_03": Gas[0],
                    "Day_Degree_Cold": Temp[0],
                    "Day_Degree_Hot":Temp[1],
                    "Min_OutdoorTemp": Temp[2],
                    "Average_OutdoorTemp": Temp[3],
                    "Max_OutdoorTemp": Temp[4],
                    "Maximum_Humidity": Humidity[1],
                    "Average_Humidity": Humidity[0],
                    "Solar_Radiation": Solar[0],
                    "Hour": Time[1],
                    "Day": Time[2],
                    "Week": Time[3],
                    "Month": Time[4],
                    "Year": Time[5],
                }
            )
    else:
            for Time, Electricity, Gas, Temp, Humidity, Solar in zip(time, electricity, gaz, temperature, humidity, solar_radiation):  
                formatted_date = Time[5].strftime("%Y-%m-%d %H:%M:%S")
                day_degree_cold = round(Temp[3], 6) if isinstance(Temp[3], float) else Temp[3]
                day_degree_hot = round(Temp[4], 6) if isinstance(Temp[4], float) else Temp[4]
                min_outdoor_temp = round(Temp[0], 6) if isinstance(Temp[0], float) else Temp[0]
                average_outdoor_temp = round(Temp[1], 6) if isinstance(Temp[1], float) else Temp[1]
                max_outdoor_temp = round(Temp[2], 6) if isinstance( Temp[2], float) else Temp[2]
                max_humidity = round(Humidity[1], 6) if isinstance(Humidity[1], float) else Humidity[1]
                average_humidity = round(Humidity[0], 6) if isinstance( Humidity[0], float) else Humidity[0]
                solar_radiation = round(Solar[0], 6) if isinstance(Solar[0], float) else Solar[0]
                electricity=round(Electricity[4], 6) if isinstance(Electricity[4], float) else Electricity[4]
                gas_01=round(Gas[5], 6) if isinstance(Gas[5], float) else Gas[5]
                gas_02=round(Gas[4], 6) if isinstance(Gas[4], float) else Gas[4]
                gas_03=round(Gas[6], 6) if isinstance(Gas[6], float) else Gas[6]
                response_data.append(
                    {
                        "date": formatted_date,
                        "Electricity": electricity,
                        "Gas_01": gas_01,
                        "Gas_02":  gas_02,
                        "Gas_03":  gas_03,
                        "Day_Degree_Cold":day_degree_cold,
                        "Day_Degree_Hot": day_degree_hot,
                        "Min_OutdoorTemp": min_outdoor_temp,
                        "Average_OutdoorTemp":average_outdoor_temp,
                        "Max_OutdoorTemp": max_outdoor_temp,
                        "Maximum_Humidity": max_humidity,
                        "Average_Humidity": average_humidity,
                        "Solar_Radiation": solar_radiation,
                        "Hour": Time[0],
                        "Day": Time[1],
                        "Week": Time[2],
                        "Month": Time[3],
                        "Year": Time[4],
                    }
                )
    df = pd.DataFrame(response_data)
    if(method=='first_difference'):
        df[column] = df[column].diff().dropna()

    if(method=='log_difference'):
        mode_value = stats.mode(df[column]).mode[0]
        df[column] = df[column].apply(lambda x: np.log(x)).diff().dropna()    
    
    if(method=='seasonal_difference'):
        df[column] = df[column].diff(12).dropna()

    insert_query = f'''INSERT INTO "operation_tracabilite" ("version", "Operation", "Column", "Method") 
                VALUES ('{version}', 'time_series_transformation', '{column}', '{method}')'''
    delete_query = f'''DELETE FROM "operation_tracabilite" WHERE "version"={version}'''
    if (updated=='False' and await check_updated_version(connexion2,version)==1):
         await connexion2.execute(delete_query)
    if(int(version)!=-1):
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version}  order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version} order by "date" desc  limit 1'''  
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
    else:
        version1=await get_first_version(connection)
        version2=await get_last_version(connection)
        first_id_q = f'''SELECT "Time_Id" FROM time where version={version1} order by "Time_Id" asc limit 1''' 
        last_id_q=f'''SELECT "Time_Id" FROM time where version={version2} order by "date" desc  limit 1''' 
        first_id_query=await connection.fetchrow(first_id_q)
        first_id= int(first_id_query['Time_Id']) if first_id_query else None
        last_id_query=await connection.fetchrow(last_id_q)
        last_id=int(last_id_query['Time_Id']) if first_id_query else None
   
    new_order = ['date', 'Gas_01', 'Gas_02', 'Gas_03', 'Electricity', 'Maximum_Humidity', 'Solar_Radiation',
             'Day_Degree_Hot', 'Day_Degree_Cold', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp',
             'Min_OutdoorTemp', 'Year', 'Month', 'Week', 'Day', 'Hour']

    df = df.reindex(columns=new_order)
    df = transform_float_precision(df)
    print(first_id,last_id)
    ids = list(range(first_id, last_id+1 ))
    df['id'] = ids
    
    await connexion2.execute(insert_query)
    df.to_csv('updated_data.csv', index=False)
    integrate_dimensions_update_data()
    integrate_facts_update_data()
    await update_version(version,connexion2)



