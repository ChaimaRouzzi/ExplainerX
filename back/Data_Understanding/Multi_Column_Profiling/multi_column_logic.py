import asyncpg
import json
from datetime import datetime
import pandas as pd
import numpy as np
import subprocess
import ast
from Data_Understanding.Multi_Column_Profiling.df import fd
from Data_Understanding.Data_Analysis.data_analysis_logic import (fetch_rows,fetch_columns,versions_number,fetch_data_updated_version,fetch_data_version)


async def get_correlation(connection,version,method,updated):
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
    correlation_data=df.corr(method)
   
    core_list = correlation_data.to_dict(orient='records')
    # Create a dictionary to store the results
 

    # Include the dictionary in the return statement as a JSON object
    return json.dumps(core_list)



async def get_Top_corelation_Electricity(connection,version,updated):
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

    excluded_columns = ['Electricity', 'Gas_01', 'Gas_02', 'Gas_03']

    correlation_data = (df.drop(excluded_columns, axis=1).corrwith(df['Electricity'])).round(6)


    # Sort the correlation values in descending order
    correlation_data_sorted = correlation_data.sort_values(ascending=False,key=lambda x: abs(x))

    # Create a dictionary to store the results
    correlation_dict = []
    for col in correlation_data_sorted.index:
        correlation_dict.append({'column':col,'correlation': correlation_data_sorted[col]})
    # Include the dictionary in the return statement as a JSON object
    return json.dumps(correlation_dict)


async def get_Top_corelation_Gaz(connection,version,updated):
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

    excluded_columns = ['Electricity', 'Gas_01', 'Gas_02', 'Gas_03']

    correlation_data = (df.drop(excluded_columns, axis=1).corrwith(df['Gas_01'])).round(6)


    # Sort the correlation values in descending order
    correlation_data_sorted = correlation_data.sort_values(ascending=False,key=lambda x: abs(x))

    # Create a dictionary to store the results
    correlation_dict = []
    for col in correlation_data_sorted.index:
        correlation_dict.append({'column':col,'correlation': correlation_data_sorted[col]})
       

    # Include the dictionary in the return statement as a JSON object
    return json.dumps(correlation_dict)

async def get_Functional_depandancies(connection,version,updated):
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
    final_resul=[]
    for col in fd:
         val =str(col[0])
         item1=set(val)
         if 'G' in val or 'H'  in val or 'I'in val  or 'J'in val :
           1+1
         else:
          mapping = {
                    'A': 'date',
                    'B': 'Hour',
                    'C': 'Day',
                    'D': 'Week',
                    'E': 'Month',
                    'F': 'Year',
                    'G': 'Gas_02',
                    'H': 'Gas_01',
                    'I': 'Gas_03',
                    'J': 'Electricity',
                    'K': 'Average_Humidity',
                    'L': 'Maximum_Humidity',
                    'M': 'Solar_Radiation',
                    'N': 'Day_Degree_Cold',
                    'O': 'Day_Degree_Hot',
                    'P': 'Min_OutdoorTemp',
                    'Q': 'Average_OutdoorTemp',
                    'R': 'Max_OutdoorTemp'
                }
          new_item = ''
          for char in str(item1):
            if char in mapping:
                new_item += mapping[char]
            else:
                new_item += char
          co=mapping[col[1]]
          final_resul.append([(new_item),co])
    return json.dumps(final_resul)  


def execute_terminal_code(code,column):
  
    # Run the code in the terminal
    process = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and error messages
    output, error = process.communicate()

    # Decode the byte strings into regular strings
    output = output.decode('utf-8')
    error = error.decode('utf-8')
    
    # Print the output and error messages
    start_index = output.find("[[")
    end_index = output.find("]]") + 2
    extracted_list = output[start_index:end_index]
    result = ast.literal_eval(extracted_list)
  
    filtered_list1 = [sublist for sublist in result if sublist[1] in ['B', 'C', 'D', 'E']]

    sublist_b = [sublist for sublist in result if sublist[1] ==column]
  
    final_list=[]
    for i in range(len(sublist_b)):
      final_list.append(sublist_b[i][0])
    # for i in range(len(final_list)):
    #  if final_list[i] == "A":
    #     final_list[i] = "date"
    #  if final_list[i] == "C":
    #     final_list[i] = "Maximum_Humidity"
    #  if final_list[i] == "D":
    #     final_list[i] = "Solar_Radiation"
    #  if final_list[i] == "E":
    #     final_list[i] = "Day_Degree_Hot"
    #  if final_list[i] == "F":
    #     final_list[i] = "Day_Degree_Cold"
    #  if final_list[i] == "F":
    #     final_list[i] = "Average_Humidity"
    #  if final_list[i] == "G":
    #     final_list[i] = "Max_OutdoorTemp"
    #  if final_list[i] == "H":
    #     final_list[i] = "Average_OutdoorTemp"
    #  if final_list[i] == "Min_OutdoorTemp":
    #     final_list[i] = "Average_OutdoorTemp"
    #  if final_list[i] == "I":
    #     final_list[i] = "Year"
    #  if final_list[i] == "J":
    #     final_list[i] = "Month"
    #  if final_list[i] == "K":
    #     final_list[i] = "Week"
    #  if final_list[i] == "L":
    #     final_list[i] = "Day"
    #  if final_list[i] == "M":
    #     final_list[i] = "Day"

    author_list = []
    for item in final_list:
     if isinstance(item, str) and item != "":
        for char in item:
            if char not in author_list:
                author_list.append(char)

    return(author_list) 

async def updated_versions_number(connection):
    versions= await connection.fetchrow(f'''SELECT COUNT (DISTINCT "version") as versions FROM electricity''')
    version_number=int(versions['versions']) if versions else None
    versions=[]
    for i in range(version_number):
      updated=await check_updated_version(connection,i)
      if(int(updated)==1):
          versions.append(i)

    return  json.dumps(versions)


async def check_updated_version(connection,version):
    first_version_q=f'''SELECT "updated" FROM time where "version"={version}  order by "Time_Id" desc  limit 1''' 
    first_version_query=await connection.fetchrow(first_version_q)
    first_version=first_version_query["updated"] if first_version_query else None
   
    return first_version


async def multi_column(connection,connection2,version,updated,method):

    if(updated=='True'):
        data= await fetch_data_updated_version(connection,version,updated)
        updated_ver= await updated_versions_number(connection)
        rows= await fetch_rows(connection,version)
        columns=await fetch_columns(connection,version,updated)
        top_gaz=await  get_Top_corelation_Gaz(connection,version,updated)
        top_electricity=await get_Top_corelation_Electricity(connection,version,updated)
        nb_versions=await versions_number(connection)
        core=await get_correlation(connection,version,method,updated)
        depandancies=await get_Functional_depandancies(connection,version,updated)
    else:
        data= await fetch_data_updated_version(connection,version,updated)
        updated_ver= await updated_versions_number(connection2)
        rows= await fetch_rows(connection,version)
        columns=await fetch_columns(connection,version,updated)
        top_gaz=await  get_Top_corelation_Gaz(connection,version,updated)
        top_electricity=await get_Top_corelation_Electricity(connection,version,updated)
        nb_versions=await versions_number(connection)
        core=await get_correlation(connection,version,method,updated)
        depandancies=await get_Functional_depandancies(connection,version,updated)

    result={ "updated_version":updated_ver ,  "data":data,
        "rows":rows,"columns":columns,

            "versions_number":nb_versions,
            "correlation":core,
            "top_elecricity":top_electricity,
            "top_gaz":top_gaz,
            'depandancies':depandancies
        
            }
         
    
    return  json.dumps(result)
        
