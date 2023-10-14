import json

async def fetch_data2(connection):
    time = await connection.fetch("SELECT * FROM time ")
    electricity = await connection.fetch("SELECT * FROM electricity")
    gaz = await connection.fetch("SELECT * FROM gaz")
    temperature = await connection.fetch("SELECT * FROM temperature")
    humidity = await connection.fetch("SELECT * FROM humidity")
    solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    
    # Convert data to JSON response
    response_data = []
    for Time, Electricity, Gas, Temp, Humidity, Solar in zip(
        time, electricity, gaz, temperature, humidity, solar_radiation
    ):  
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
    return response_data

async def fetch_data(connection,updated):
    time = await connection.fetch("SELECT * FROM time ")
    electricity = await connection.fetch("SELECT * FROM electricity")
    gaz = await connection.fetch("SELECT * FROM gaz")
    temperature = await connection.fetch("SELECT * FROM temperature")
    humidity = await connection.fetch("SELECT * FROM humidity")
    solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    
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
    return response_data

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

    return response_data


async def fetch_data_updated_version(connection,version):
    print(version)
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
    print(time[0])
    response_data = []
    for Time, Electricity, Gas, Temp, Humidity, Solar in zip(
        time, electricity, gaz, temperature, humidity, solar_radiation
    ):  
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
                "Date": formatted_date,
                "Electricity": electricity,
                "Gas_Boiler1": gas_02,
                "Gas_Boiler2":  gas_01,
                "Gas_Boiler3":  gas_03,
                "Day_Degree_Cold":day_degree_cold,
                "Day_Degree_Hot": day_degree_hot,
                "Min_OutdoorTemp": min_outdoor_temp,
                "Average_OutdoorTemp":average_outdoor_temp,
                "Max_OutdoorTemp": max_outdoor_temp,
                "Maximum_Humidity": max_humidity,
                "Average_Humidity": average_humidity,
                "Solar_Radiation": solar_radiation,
                "Hour": Time[1],
                "Day": Time[2],
                "Week": Time[3],
                "Month": Time[4],
                "Year": Time[5],
            }
        )
    response_json = json.dumps(response_data)
    return response_json


