import json
from datetime import datetime
import pandas as pd

async def fetch_data_version(connection,version,updated):
    if (version=="-1"):
     time = await connection.fetch("SELECT * FROM time")
     electricity = await connection.fetch("SELECT * FROM electricity")
     gaz = await connection.fetch("SELECT * FROM gaz")
     temperature = await connection.fetch("SELECT * FROM temperature")
     humidity = await connection.fetch("SELECT * FROM humidity")
     solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
     time = await connection.fetch(f'''SELECT * FROM time where "version"={version} order by "Time_Id"   ASC''')
     electricity = await connection.fetch(f'''SELECT * FROM electricity where "version"={version} order by "Time_Id"   ASC''')
     gaz = await connection.fetch(f'''SELECT * FROM gaz where "version"={version} order by "Time_Id"   ASC''')
     temperature = await connection.fetch(f'''SELECT * FROM temperature  where "version"={version} order by "Temperature_Id"   ASC''')
     humidity = await connection.fetch(f'''SELECT * FROM humidity  where "version"={version} order by "Humidity_Id" ASC  ''')
     solar_radiation = await connection.fetch(f'''SELECT * FROM solar_radiation where "version"={version} order by "Solar_Radiation_Id" ASC''')
    # Convert data to JSON response
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

    response_json = json.dumps(response_data)
    return response_json


async def fetch_data_updated_version(connection,version,updated):
   
    if (version=="-1"):
     time = await connection.fetch("SELECT * FROM time")
     electricity = await connection.fetch("SELECT * FROM electricity")
     gaz = await connection.fetch("SELECT * FROM gaz")
     temperature = await connection.fetch("SELECT * FROM temperature")
     humidity = await connection.fetch("SELECT * FROM humidity")
     solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
     time = await connection.fetch(f'''SELECT * FROM time where "version"={version} order by "Time_Id"   ASC''')
     electricity = await connection.fetch(f'''SELECT * FROM electricity where "version"={version} order by "Time_Id"   ASC''')
     gaz = await connection.fetch(f'''SELECT * FROM gaz where "version"={version} order by "Time_Id"   ASC''')
     temperature = await connection.fetch(f'''SELECT * FROM temperature  where "version"={version} order by "Temperature_Id"   ASC''')
     humidity = await connection.fetch(f'''SELECT * FROM humidity  where "version"={version} order by "Humidity_Id" ASC  ''')
     solar_radiation = await connection.fetch(f'''SELECT * FROM solar_radiation where "version"={version} order by "Solar_Radiation_Id" ASC''')
    # Convert data to JSON response
   
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

    response_json = json.dumps(response_data)
    return response_json


async def fetch_rows(connection, version):
    if version == "-1":
        time = await connection.fetch("SELECT * FROM time")
    else:
        time = await connection.fetch(f'SELECT * FROM time WHERE "version"={version} ORDER BY "Time_Id" ASC')

    # Get the number of rows
    num_rows = len(time)

    # Return the number of rows as a JSON response
    
    response_json = json.dumps(num_rows)
    return num_rows


async def fetch_columns(connection,version,updated):
   
    if (version=="-1"):
     time = await connection.fetch("SELECT * FROM time")
     electricity = await connection.fetch("SELECT * FROM electricity")
     gaz = await connection.fetch("SELECT * FROM gaz")
     temperature = await connection.fetch("SELECT * FROM temperature")
     humidity = await connection.fetch("SELECT * FROM humidity")
     solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
     time = await connection.fetch(f'''SELECT * FROM time where "version"={version} order by "Time_Id"   ASC''')
     electricity = await connection.fetch(f'''SELECT * FROM electricity where "version"={version} order by "Time_Id"   ASC''')
     gaz = await connection.fetch(f'''SELECT * FROM gaz where "version"={version} order by "Time_Id"   ASC''')
     temperature = await connection.fetch(f'''SELECT * FROM temperature  where "version"={version} order by "Temperature_Id"   ASC''')
     humidity = await connection.fetch(f'''SELECT * FROM humidity  where "version"={version} order by "Humidity_Id" ASC  ''')
     solar_radiation = await connection.fetch(f'''SELECT * FROM solar_radiation where "version"={version} order by "Solar_Radiation_Id" ASC''')
    # Convert data to JSON response

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

    num_columns = len(response_data[0])
    response_json = json.dumps(num_columns)
    return response_json


async def get_first_index(connection, version):
    if version=="-1" :
     time = await connection.fetchrow(f'''SELECT "version" FROM time   ORDER BY "Time_Id" ASC Limit 1''')
     version=time['version'] if time else None
    time = await connection.fetchrow(f'SELECT date FROM time where version={version} order by "date" asc  limit 1')
    first_index = time['date'].strftime("%Y-%m-%d %H:%M:%S") if time else None
    # Convert datetime object to string
    if isinstance(first_index, datetime):
        first_index = first_index.isoformat()

   

    response_json = json.dumps(first_index)
    return response_json



async def get_last_index(connection, version):
    if version=="-1" :
         time = await connection.fetchrow(f'''SELECT "version" FROM time  ORDER BY "Time_Id" DESC Limit 1''')
         version=time['version'] if time else None
       
    time = await connection.fetchrow(f'SELECT date FROM time where version={version} order by "date" desc  limit 1')
    first_index = time['date'].strftime("%Y-%m-%d %H:%M:%S") if time else None

    # Convert datetime object to string
    if isinstance(first_index, datetime):
        first_index = first_index.isoformat()

    response_data = {"first_index": first_index}

    response_json = json.dumps(response_data)
    return response_json


async def get_last_index(connection, version):
    if version=="-1" :
         time = await connection.fetchrow(f'''SELECT "version" FROM time  ORDER BY "Time_Id" DESC Limit 1''')
         version=time['version'] if time else None
       
       
    time = await connection.fetchrow(f'SELECT date FROM time where version={version} order by "date" desc  limit 1')
    first_index = time['date'].strftime("%Y-%m-%d %H:%M:%S") if time else None

    # Convert datetime object to string
    if isinstance(first_index, datetime):
        first_index = first_index.isoformat()

   

    response_json = json.dumps(first_index)
    return response_json


 



async def get_missing_values(connection,version,updated):
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
   
    num_missing_values = int(df.isnull().sum().sum()) 
    total_cells = df.size  # Calculate the total number of cells in the DataFrame
    missing_percentage = round((num_missing_values / total_cells) * 100,2)  # Calculate the percentage of missing values

    # Create a dictionary to store the results
    result = {
        "num_missing_values": num_missing_values,
        "missing_percentage": missing_percentage
    }

    # Include the dictionary in the return statement as a JSON object
    return json.dumps(result)

    # Include the number of missing values

   


async def get_outlier_values(connection, version,updated):
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

    # Calculate outliers
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    is_outlier = (df < lower_bound) | (df > upper_bound)

    num_outliers = int(is_outlier.sum().sum())
    total_cells = df.size  # Calculate the total number of cells in the DataFrame
    outlier_percentage = round((num_outliers / total_cells) * 100, 2)  # Calculate the percentage of outliers

    # Create a dictionary to store the results
    result = {
        "num_outliers": num_outliers,
        "outlier_percentage": outlier_percentage
    }

    # Include the number of outliers
    return json.dumps(result)
async def get_duplicate_rows(connection, version,updated):
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

    num_duplicates = int(df.duplicated().sum())
    total_rows = df.shape[0]
    duplicate_percentage = round((num_duplicates / total_rows) * 100, 2)

    result = {
        "num_duplicates": num_duplicates,
        "duplicate_percentage": duplicate_percentage
    }

    return json.dumps(result)



async def get_negative_values(connection, version,updated):
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

    numeric_columns = df.select_dtypes(include=[float, int]).columns
    numeric_df = df[numeric_columns]

    num_negatives = int((numeric_df < 0).sum().sum())
    total_cells = numeric_df.size
    negative_percentage = round((num_negatives / total_cells) * 100 , 2)

    result = {
        "num_negatives": num_negatives,
        "negative_percentage": negative_percentage
    }
    return json.dumps(result)

async def get_missing_values_columns(connection, version,updated):
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

    result = {}
    response=[]
    for column in df.columns:
        num_missing_values = int(df[column].isnull().sum())
       
   
        result = {
            "column":column,
            "num_missing_values": num_missing_values,
           }
        response.append(result)

    labels = [item['column'] for item in response]
    values = [item['num_missing_values'] for item in response]
    result={"labels":labels,"values":values}
        
    return  json.dumps(result)



async def get_outliers_columns(connection, version,updated):
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

    result = {}
    response=[]
    for column in df.columns:
        col_values = df[column]
        is_numeric = pd.api.types.is_numeric_dtype(col_values)
        if is_numeric:
            q1 = col_values.quantile(0.25)
            q3 = col_values.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            num_outliers = ((col_values < lower_bound) | (col_values > upper_bound)).sum()
            outliers_percentage = round((num_outliers / len(col_values)) * 100,2)

            result= {
                "column":column,
                "num_outliers":int(num_outliers)
            }
        else:
            result ={
                "column":column,
                "num_outliers": 0,
            }
        response.append(result)
    labels = [item['column'] for item in response]
    values = [item['num_outliers'] for item in response]
    result={"labels":labels,"values":values}
        
    return  json.dumps(result)

  

async def memory_usage(connection, version,updated):
    if version == "-1":
        # Fetch data from the database
        time = await connection.fetch("SELECT * FROM time")
        electricity = await connection.fetch("SELECT * FROM electricity")
        gaz = await connection.fetch("SELECT * FROM gaz")
        temperature = await connection.fetch("SELECT * FROM temperature")
        humidity = await connection.fetch("SELECT * FROM humidity")
        solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    else:
        # Fetch data with version filter from the database
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

    result = {}
    response = []

    # Calculate memory usage of each column
    memory_usage = df.memory_usage(deep=True)
    memory_usage_megabytes = (memory_usage / (1024 * 1024)).round(2)
    for column, usage in memory_usage_megabytes.items():
        result = {
            "column": column,
            "memory_usage": usage,
        }
        response.append(result)
    labels = [item['column'] for item in response]
    values = [item['memory_usage'] for item in response]
    result={"labels":labels,"values":values}

    return json.dumps(result)


async def timeline(connection):
    versions= await connection.fetchrow(f'''SELECT COUNT (DISTINCT "version") as versions FROM electricity''')
    version_number=versions['versions'] if versions else None
    timeline_data=[]
    for i in range(version_number):
        rows_qyery=await connection.fetchrow(f'''SELECT Count ("Time_Id") as rows FROM electricity where version={i}''')
        rows=rows_qyery['rows'] if rows_qyery else None
        if i==0: columns=18 
        else: columns=0
        date_query=await connection.fetchrow(f'''SELECT version_date FROM electricity where version={i} limit 1''')
        date=date_query['version_date'].strftime('%Y-%m-%d %H:%M:%S') if date_query else None
 
        first_index_query=await connection.fetchrow(f'''SELECT date FROM time where version={i} limit 1''')
        last_index_query=await connection.fetchrow(f'''SELECT date FROM time where version={i}  order by "date" desc limit 1''')
        first_index=first_index_query['date'].strftime('%Y-%m-%d %H:%M:%S') if first_index_query else  None
        last_index=last_index_query['date'].strftime('%Y-%m-%d %H:%M:%S') if last_index_query else  None
        
        timeline_data.append({"version":i, "date": date, "rows": rows, "columns": columns,"first_index":first_index,"last_index":last_index})
        
    return  json.dumps(timeline_data)


async def versions_rows(connection):
    versions= await connection.fetchrow(f'''SELECT COUNT (DISTINCT "version") as versions FROM electricity''')
    version_number=versions['versions'] if versions else None
    timeline_data=[]
    for i in range(version_number):
        rows_qyery=await connection.fetchrow(f'''SELECT Count ("Time_Id") as rows FROM electricity where version={i}''')
        rows=rows_qyery['rows'] if rows_qyery else None
       
        timeline_data.append({"version":i, "rows": rows})
    labels = []
    values = []

    for data in timeline_data:
     labels.append(f"version{int(data['version'])+1}")
     values.append(data['rows'])
    result={"labels":labels,"values":values}
        
    return  json.dumps(result)

async def versions_number(connection):
    versions= await connection.fetchrow(f'''SELECT COUNT (DISTINCT "version") as versions FROM electricity''')
    version_number=int(versions['versions']) if versions else None
   
        
    return  json.dumps(version_number)




async def versions_number(connection):
    versions= await connection.fetchrow(f'''SELECT COUNT (DISTINCT "version") as versions FROM electricity''')
    version_number=int(versions['versions']) if versions else None
   
        
    return  json.dumps(version_number)




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

async def data_analysis(connection,connection2, version,updated):
    print(updated)
    if(updated=='True'):
        data= await fetch_data_updated_version(connection,version,updated)
        updated_ver= await updated_versions_number(connection)
        rows= await fetch_rows(connection2,version)
        columns=await fetch_columns(connection,version,updated)
        missing_values=await get_missing_values(connection,version,updated)
        outlires=await get_outlier_values(connection,version,updated)
        negative=await get_negative_values(connection,version,updated)
        duplicate=await get_duplicate_rows(connection,version,updated)
    
        timeline_data=await timeline(connection2)
        version_data=await versions_rows(connection2)
        missing_values_columns=await get_missing_values_columns(connection,version,updated)
        outlires_columns=await get_outliers_columns(connection,version,updated)
        nb_versions=await versions_number(connection2)
        column_memory=await memory_usage(connection,version,updated)
    else:
        
        data= await fetch_data_updated_version(connection,version,updated)
        updated_ver= await updated_versions_number(connection2)
        rows= await fetch_rows(connection,version)
        columns=await fetch_columns(connection,version,updated)
        missing_values=await get_missing_values(connection,version,updated)
        outlires=await get_outlier_values(connection,version,updated)
        negative=await get_negative_values(connection,version,updated)
        duplicate=await get_duplicate_rows(connection,version,updated)
    
        timeline_data=await timeline(connection)
        version_data=await versions_rows(connection)
        missing_values_columns=await get_missing_values_columns(connection,version,updated)
        outlires_columns=await get_outliers_columns(connection,version,updated)
        nb_versions=await versions_number(connection)
        column_memory=await memory_usage(connection,version,updated)

    result={"updated_version":updated_ver,
        "data":data,"rows":rows,"columns":columns,
             "missing_values": missing_values,
            "outlires": outlires,
           "negative": negative,
               "duplicate":duplicate,
              "timeline_data": timeline_data,
              "version_data":version_data,
              "missing_values_columns":missing_values_columns,
            "outlires_columns" : outlires_columns,
            "versions_number":nb_versions,
            "column_memory":column_memory}
         
    
    return  json.dumps(result)
        
