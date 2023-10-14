import os
from fastapi import HTTPException
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
import joblib
import shap
from sqlalchemy import create_engine
import seaborn as sns
from datetime import timedelta, date, datetime
from sklearn import linear_model
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
import datetime
import json
from typing import List
from fastapi import HTTPException
import shap
from fastapi.responses import JSONResponse
import dill
import os
from Model_Prediction.model_prediction_logic import models2
warnings.filterwarnings('ignore')
from frouros.metrics import PrequentialError
import xgboost
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from frouros.detectors.concept_drift import DDM, DDMConfig , EDDM, EDDMConfig ,ADWIN
from frouros.detectors.data_drift import KSTest,KL,EMD
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression, LinearRegression
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
from sklearn.linear_model import Ridge, Lasso
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
import subprocess

MODELS_DIR2 = "models/Custom_Models"  



async def upload_file(connection, connection2, file):
    time = await connection.fetch("SELECT * FROM time")
    electricity = await connection.fetch("SELECT * FROM electricity")
    gaz = await connection.fetch("SELECT * FROM gaz")
    temperature = await connection.fetch("SELECT * FROM temperature")
    humidity = await connection.fetch("SELECT * FROM humidity")
    solar_radiation = await connection.fetch("SELECT * FROM solar_radiation")
    response_data = []
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

    df_original = pd.DataFrame(response_data)

    filename = file.filename
    _, extension = os.path.splitext(filename)
    if extension.lower() != '.csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")

    df = pd.read_csv(file.file)

    order = ['date', 'Gas_01', 'Gas_02', 'Gas_03', 'Electricity', 'Maximum_Humidity', 'Solar_Radiation',
             'Day_Degree_Hot', 'Day_Degree_Cold', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp',
             'Min_OutdoorTemp', 'Year', 'Month', 'Week', 'Day', 'Hour']

    if (df.columns != order).any():
         raise HTTPException(status_code=400, detail="Uploaded file columns do not match the expected columns.")

    # Convert the 'date' column to a datetime format
    df_copy=df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'])

    # Calculate the time difference between consecutive timestamps
    time_diff = df_copy['date'].diff()

    # Define the expected time difference for hourly frequency
    expected_time_diff = timedelta(hours=1)

    # Check if the time differences are approximately equal to the expected time difference
    is_hourly = all(abs(td - expected_time_diff) < timedelta(minutes=1) for td in time_diff[1:])

    if not is_hourly:
        raise HTTPException(status_code=400, detail="Timestamps are not in hourly frequency.")
   
    
    
    json_data = df.to_json(orient="records")
    return json_data


    # Your logic for handling the CSV file goes here
    # For example, you can save the file, process its content, etc.

import numpy as np
import pandas as pd

def calculate_euclidean_distance(matrix1, matrix2):
    return np.sqrt(np.sum((matrix1 - matrix2) ** 2, axis=1))

def find_most_similar_month_df(df1, df2):
    monthly_dfs = [group for _, group in df1.resample("M")]
    best_similarity = float('inf')
    most_similar_month_df = None
    df2_matrix = df2.values
    for month_df1 in monthly_dfs:
        if len(month_df1) != len(df2):
            continue
       
        month_df1_matrix = month_df1.values
        distances = calculate_euclidean_distance(month_df1_matrix, df2_matrix)
        total_distance = np.sum(distances)
     
        if total_distance < best_similarity:
            best_similarity = total_distance
            most_similar_month_df = month_df1.copy()
    return most_similar_month_df


def find_most_similar_segment(df1, df2):
    segment_length = len(df2)
    num_segments = len(df1) - segment_length + 1

    best_similarity = float('inf')
    most_similar_segment_df = None
    df2_matrix = df2.values

    for i in range(num_segments):
        segment_df1 = df1.iloc[i : i + segment_length]
        segment_df1_matrix = segment_df1.values
        distances = calculate_euclidean_distance(segment_df1_matrix, df2_matrix)
        total_distance = np.sum(distances)

        if total_distance < best_similarity:
            best_similarity = total_distance
            most_similar_segment_df = segment_df1.copy()

    return most_similar_segment_df


async def  detect_drift(connection,connection2,file,model_name,model_horizon,model_target,predictors,method,driftType):

    parts = predictors[0].split(',') 
    min_max_df= await get_min_max(connection,'hourly')
    time = await connection2.fetch('''SELECT * FROM time order by "Time_Id" asc''')
    electricity = await connection2.fetch('''SELECT * FROM electricity order by "Time_Id" asc''')
    gaz = await connection2.fetch('''SELECT * FROM gaz order by "Time_Id" asc''')
    temperature = await connection2.fetch('''SELECT * FROM temperature order by "Temperature_Id" asc''')
    humidity = await connection2.fetch('''SELECT * FROM humidity order by "Humidity_Id"  asc''')
    solar_radiation = await connection2.fetch('''SELECT * FROM solar_radiation order by "Solar_Radiation_Id"  asc''')
    response_data = [] 
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
  
    df_original= pd.DataFrame(response_data)  
   
    df_copy=df_original.copy()
   
    def is_between_0_and_1(x):
        return 0 < x <= 1

    # Iterate through the columns you want to apply scaling to
    columns_to_scale = ['Electricity', 'Gas_01', 'Gas_02', 'Gas_03', 'Day_Degree_Cold', 'Solar_Radiation', 'Day_Degree_Hot', 'Average_Humidity', 'Max_OutdoorTemp', 'Average_OutdoorTemp', 'Min_OutdoorTemp', 'Maximum_Humidity']

    for col_name in columns_to_scale:
        df_copy[col_name] = df_copy[col_name].apply(lambda x: rev_min_max_func(x, col_name, min_max_df.loc[col_name, 'max'], min_max_df.loc[col_name, 'min']) if is_between_0_and_1(x) else x)

    df_file=pd.read_csv(file.file)

    write=True

    df_copy['date'] = pd.to_datetime(df_copy['date'])
    df_copy.set_index('date', inplace=True)
   
   
    first_data_entry = df_file.loc[0, 'date']

    if first_data_entry in  df_original['date'].values :
        write=False
    print(model_horizon)
    features = parts + [model_target]
    print(features)
    desired_order = ['date','Electricity','Gas_01','Gas_02','Gas_03','Day_Degree_Cold','Day_Degree_Hot','Min_OutdoorTemp','Average_OutdoorTemp','Max_OutdoorTemp','Maximum_Humidity','Average_Humidity','Solar_Radiation','Hour','Day','Week','Month','Year']
    df_file = df_file[desired_order]
    df_file['date'] = pd.to_datetime(df_file['date'])
    df_file.set_index('date', inplace=True)
    df_result=find_most_similar_month_df(df_copy[features],df_file[features])
   
    df_result.to_csv('all.csv', index=True)
    model_pred=await load_joblib(connection,1,model_name)
    if model_pred is None:
        raise HTTPException(status_code=404, detail="Model not found.")
    data_drift_result=pd.DataFrame()
    concept_drift_result=False
    drift_index=0
  

    if(method=='KS'):
       data_drift_result,is_data_drift=detect_data_drift_Ks(df_result[features],df_file[features], 0.001)
    if(method=='KL'):
        data_drift_result,is_data_drift=detect_data_drift_KL(df_result[features],df_file[features], 0.001)
    if(method=='EMD'):
        data_drift_result,is_data_drift=detect_data_drift_EMD(df_file[features],df_file[features], 0.001)

    df_file_scaled=df_file.copy()
    if model_horizon=='Daily':
            order = ['Electricity','Gas_01','Gas_02','Gas_03','Day_Degree_Cold','Day_Degree_Hot','Min_OutdoorTemp','Average_OutdoorTemp','Max_OutdoorTemp','Maximum_Humidity','Average_Humidity','Solar_Radiation','Hour','Day','Week','Month','Year']
            df_file_scaled = pd.DataFrame(columns=order)
            min_max_df= await get_min_max(connection,'Daily')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('D').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('D').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('D').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('D').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('D').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('D').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('D').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('D').mean()
         
            
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('D').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('D').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('D').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('D').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Hour'] = df_file['Hour']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Hour',axis=1)
            df_file_scaled = df_file_scaled.ffill()
            df_file_scaled= df_file_scaled.reset_index(drop=False)
            pd.to_datetime(df_file_scaled['date'])
            df_file_scaled.set_index('date', inplace=True)
    if model_horizon=='Weekly':
            order = ['Electricity','Gas_01','Gas_02','Gas_03','Day_Degree_Cold','Day_Degree_Hot','Min_OutdoorTemp','Average_OutdoorTemp','Max_OutdoorTemp','Maximum_Humidity','Average_Humidity','Solar_Radiation','Day','Week','Month','Year']
            df_file_scaled = pd.DataFrame(columns=order)
            min_max_df= await get_min_max(connection,'Weekly')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('w').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('W').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('W').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('W').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('W').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('W').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('W').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('W').mean()
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('W').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('W').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('W').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('W').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Day',axis=1)
            df_file_scaled= df_file_scaled.reset_index(drop=False)
            pd.to_datetime(df_file_scaled['date'])
            df_file_scaled.set_index('date', inplace=True)
            df_file_scaled = df_file_scaled.ffill()
            df_file_scaled = df_file_scaled.bfill()
        
    if model_horizon=='Monthly':
            order = ['Electricity','Gas_01','Gas_02','Gas_03','Day_Degree_Cold','Day_Degree_Hot','Min_OutdoorTemp','Average_OutdoorTemp','Max_OutdoorTemp','Maximum_Humidity','Average_Humidity','Solar_Radiation','Day','Week','Month','Year']
            df_file_scaled = pd.DataFrame(columns=order)
           
            min_max_df= await get_min_max(connection,'Monthly')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('M').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('M').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('M').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('M').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('M').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('M').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('M').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('M').mean()
            
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('M').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('M').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('M').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('M').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Day',axis=1)
            df_file_scaled.drop('Week',axis=1)
            df_file_scaled= df_file_scaled.reset_index(drop=False)
            pd.to_datetime(df_file_scaled['date'])
            df_file_scaled.set_index('date', inplace=True)
            df_file_scaled = df_file_scaled.ffill()
            df_file_scaled = df_file_scaled.bfill()
            df_file_scaled = df_file_scaled.fillna(0)

    df_file_scaled['Electricity'] = df_file_scaled['Electricity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Electricity','max'],min_max_df.loc['Electricity','min']))
    df_file_scaled['Gas_01'] = df_file_scaled['Gas_01'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_01','max'],min_max_df.loc['Gas_01','min']))
    df_file_scaled['Gas_02'] = df_file_scaled['Gas_02'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_02','max'],min_max_df.loc['Gas_02','min']))
    df_file_scaled['Gas_03'] = df_file_scaled['Gas_03'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_03','max'],min_max_df.loc['Gas_03','min']))
    df_file_scaled['Day_Degree_Cold'] = df_file_scaled['Day_Degree_Cold'].apply(lambda x: min_max_scale(x,min_max_df.loc['Day_Degree_Cold','max'],min_max_df.loc['Day_Degree_Cold','min']))
    df_file_scaled['Solar_Radiation'] = df_file_scaled['Solar_Radiation'].apply(lambda x: min_max_scale(x,min_max_df.loc['Solar_Radiation','max'],min_max_df.loc['Solar_Radiation','min']))
    df_file_scaled['Day_Degree_Hot'] = df_file_scaled['Day_Degree_Hot'].apply(lambda x: min_max_scale(x,min_max_df.loc['Day_Degree_Hot','max'],min_max_df.loc['Day_Degree_Hot','min']))
    df_file_scaled['Average_Humidity'] = df_file_scaled['Average_Humidity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Average_Humidity','max'],min_max_df.loc['Average_Humidity','min']))
    df_file_scaled['Max_OutdoorTemp'] = df_file_scaled['Max_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Max_OutdoorTemp','max'],min_max_df.loc['Max_OutdoorTemp','min']))
    df_file_scaled['Average_OutdoorTemp'] = df_file_scaled['Average_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Average_OutdoorTemp','max'],min_max_df.loc['Average_OutdoorTemp','min']))
    df_file_scaled['Min_OutdoorTemp'] = df_file_scaled['Min_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Min_OutdoorTemp','max'],min_max_df.loc['Min_OutdoorTemp','min']))
    df_file_scaled['Maximum_Humidity'] = df_file_scaled['Maximum_Humidity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Maximum_Humidity','max'],min_max_df.loc['Maximum_Humidity','min']))


    metric = PrequentialError(alpha=1.0)
    X_test = df_file_scaled[parts].values   
    y_test = df_file_scaled[model_target].values
    X_original=df_original[parts].values
    y_original=df_original[model_target].values
    X_combined = np.concatenate((X_original, X_test), axis=0)
    y_combined = np.concatenate((y_original, y_test), axis=0)
   

    y_pred=model_pred.predict(X_original)
    print(X_combined,y_pred,y_combined) 
    # y_pred = np.vectorize(lambda x: min_max_scale(x, min_max_df.loc[model_target, 'max'], min_max_df.loc[model_target, 'min']))(y_pred)

   
    mean= mean_absolute_error(y_original,y_pred)
    rmse = mean_squared_error(y_original,y_pred, squared=False)
    mse=mean_squared_error(y_original,y_pred)
  
    if(method=='DDM'):
       
        data_drift_result,is_data_drift =detect_data_drift_Ks(df_result,df_file, 0.2)
        drifted_target=data_drift_result['DriftDetected'][data_drift_result['Column']==model_target]
       
        if(drifted_target.iloc[0]):
        
         config = DDMConfig(warning_level=1.0,drift_level=1.00000001,min_num_instances=10,)
        else:
            config = DDMConfig(warning_level=10.0,drift_level=10.00000001,min_num_instances=100,)
        detector = DDM(config=config)
        concept_drift_result,drift_index= concept_drift(y_pred=y_pred,y_test= y_test,metric=metric,detector=detector,)
    if(method=='EDDM'):
    
        data_drift_result,is_data_drift =detect_data_drift_Ks(df_result,df_file, 0.001)
        print(is_data_drift)
        drifted_target=data_drift_result['DriftDetected'][data_drift_result['Column'] == model_target]
        if(drifted_target.iloc[0]):
         config=EDDMConfig(alpha =2, beta= 1, level= 1.01, min_num_misclassified_instances = 5)
        else:
            config=EDDMConfig(alpha =0.5, beta= 0.4, level= 1.01, min_num_misclassified_instances = 100) 
        detector = EDDM(config)
        concept_drift_result,drift_index= concept_drift(y_pred=y_pred,y_test= y_test,metric=metric,detector=detector,)
       
    
    if(method=='ADWIN'):
        data_drift_result,is_data_drift =detect_data_drift_Ks(df_result,df_file, 0.001)
        drifted_target=data_drift_result['DriftDetected'][data_drift_result['Column'] == model_target]
        # if(drifted_target[0]):
        #  config=EDDMConfig(alpha =2, beta= 1, level= 3.01, min_num_misclassified_instances = 40)
        # else:
        #     config=EDDMConfig(alpha =0.5, beta= 0.4, level= 1.01, min_num_misclassified_instances = 100) 
        detector = ADWIN()
        concept_drift_result,drift_index= concept_drift(y_pred=y_pred,y_test= y_test,metric=metric,detector=detector,)
      
    if  drift_index!=0 and pd.notnull(drift_index):
         df_file=df_file.reset_index(drop=False)
         index =df_file['date'].iloc[drift_index]
         dt_object = index.to_pydatetime()
         index = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    else:
        index=0
    X =df_file_scaled.loc[:, parts]
    X_np = X.values
    shap_data=[]
    if (driftType=='Data Drift'):
    
        try:
            with open('xai/Custom/%s_shap.pkl' % model_name, 'rb') as file:
              
                if model_pred is None:
                    raise HTTPException(status_code=404, detail="Model not found.")                    
                loaded_object = dill.load(file)
             
                shap_values = loaded_object.shap_values(X_np)
                mean_abs_shap_values = np.abs(shap_values).mean(axis=0)
                feature_importance_df = pd.DataFrame({'Feature': X.columns, 'MeanAbsSHAP': mean_abs_shap_values})
                feature_importance_df = feature_importance_df.sort_values(by='MeanAbsSHAP', ascending=False)
                shap_data= feature_importance_df.to_dict(orient='records')

        except Exception as e:
            # Handle any exceptions that might occur during the code execution
            print("An error occurred:", e)
            # You can add more specific error handling or logging here

    df_file.reset_index(inplace=True)  
    df_file['date'] = pd.to_datetime(df_file['date'])
    df_file['date'] = df_file['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data=df_file.to_dict(orient='records')     
   
    data_drift_result= data_drift_result.astype(str)
   
    
    data_drift_result=data_drift_result.to_dict(orient='records')
    result={
             'data':data,
             "mea":mean,"msae":mse,"rmse":rmse,
            'data_drift_detected':is_data_drift,
            'data_drift_result':data_drift_result,
            'concept_drift_detected':concept_drift_result,
            'index':index,
            'shap':shap_data,
            'target':model_target,
            'write':write
           
            
            }
  
    return  json.dumps(result)
    



async def save_data(connection,connection2,file):
    df_file=pd.read_csv(file.file)
    transform_float_precision(df_file)
    df_file.to_csv("C:/Users/Admin/Desktop/PFE/original_dataset/new_dataset_stramlit.csv",index=False)
    
    integrate_dimensions_new_data()
    integrate_facts_new_data()   
    integrate_dimensions2_new_data()
    integrate_facts2_new_data() 

    last_id= await get_last_id(connection)+1
    version=await get_last_version(connection)+1
    first_id=(last_id-len(df_file))   
    
    await incremate_version(connection,version,first_id,last_id)
    await incremate_version(connection2,version,first_id,last_id)
    date=get_current_datetime()

    await update_date(connection,date, first_id, last_id)
    await set_updated(connection2,0,first_id,last_id)
    
     
  

async  def get_last_id(connection):
    query = '''SELECT "Time_Id" FROM electricity  ORDER BY "Time_Id" DESC LIMIT 1''' 
    time = await connection.fetchrow(query)
    id=time['Time_Id'] if time else None
    return id

async  def get_last_version(connection):
    query = '''SELECT "version" FROM electricity  ORDER BY "version" DESC LIMIT 1''' 
    time = await connection.fetchrow(query)
    id=time['version'] if time else None
    return id
async  def incremate_version(connection,version,first_id,last_id):
     query1 = f'''UPDATE electricity 
                SET "version" = '{version}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''
     
     query2= f'''UPDATE gaz 
                SET "version" = '{version}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''
     
     query3=f'''UPDATE time 
                SET "version" = '{version}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''
     
     query4=f'''UPDATE temperature 
                SET "version" = '{version}'
                WHERE "Temperature_Id" BETWEEN {first_id} AND {last_id}'''
     
     query5=  f'''UPDATE solar_radiation 
                SET "version" = '{version}'
                WHERE "Solar_Radiation_Id" BETWEEN {first_id} AND {last_id}'''
     
     query6=f'''UPDATE humidity 
                SET "version" = '{version}'
                WHERE "Humidity_Id" BETWEEN {first_id} AND {last_id}'''
     await connection.execute(query1)
     await connection.execute(query2)
     await connection.execute(query3)
     await connection.execute(query4)
     await connection.execute(query5)
     await connection.execute(query6)

async  def set_updated(connection,updated,first_id,last_id):
     query1 = f'''UPDATE electricity 
                SET "updated" = '{updated}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''
     
     query2= f'''UPDATE gaz 
                SET "updated" = '{updated}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''
     
     query3=f'''UPDATE time 
                SET "updated" = '{updated}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''
     
     query4=f'''UPDATE temperature 
                SET "updated" = '{updated}'
                WHERE "Temperature_Id" BETWEEN {first_id} AND {last_id}'''
     
     query5=  f'''UPDATE solar_radiation 
                SET "updated" = '{updated}'
                WHERE "Solar_Radiation_Id" BETWEEN {first_id} AND {last_id}'''
     
     query6=f'''UPDATE humidity 
                SET "updated" = '{updated}'
                WHERE "Humidity_Id" BETWEEN {first_id} AND {last_id}'''
     await connection.execute(query1)
     await connection.execute(query2)
     await connection.execute(query3)
     await connection.execute(query4)
     await connection.execute(query5)
     await connection.execute(query6)
async def update_date(connection,date,first_id,last_id):
    query1 = f'''UPDATE electricity 
                SET "version_date" = '{date}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''
    query2= f'''UPDATE gaz 
                SET "version_date" = '{date}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''

    query3=f'''UPDATE time 
                SET "version_date" = '{date}'
                WHERE "Time_Id" BETWEEN {first_id} AND {last_id}'''

    query4=f'''UPDATE temperature 
                SET "version_date" = '{date}'
                WHERE "Temperature_Id" BETWEEN {first_id} AND {last_id}'''

    query5= f'''UPDATE solar_radiation 
                SET "version_date" = '{date}'
                WHERE "Solar_Radiation_Id" BETWEEN {first_id} AND {last_id}'''

    query6= f'''UPDATE humidity 
                SET "version_date" = '{date}'
                WHERE "Humidity_Id" BETWEEN {first_id} AND {last_id}''' 
    await connection.execute(query1)
    await connection.execute(query2)
    await connection.execute(query3)
    await connection.execute(query4)
    await connection.execute(query5)
    await connection.execute(query6)


    

def integrate_dimensions_new_data(): 

    
    # Set the CSV file path to be passed as a context parameter
    csv_file_path = "C:/Users/Admin/Desktop/PFE/original_dataset/new_dataset_stramlit.csv"
    # Define the path to the Talend job executable
    talend_job_path_dimensions ="C:/Program Files (x86)/TOS_DI-8.0.1/studio/create_dimentions_table/create_dimentions_table_run.bat"
    # Construct the command to run the Talend job with the context parameter
    command_dimensions = [
        talend_job_path_dimensions,
        "--context=context",  # Replace 'your_context_name' with the actual context name in your Talend job
        "-job", "create_dimentions_table 0.1",  # Replace 'your_talend_job_name' with the actual Talend job name
        "--context_param",
        f"csvpath={csv_file_path}"
    ]

    # Execute the command using subprocess
    subprocess.run(command_dimensions, shell=True)


def integrate_facts_new_data(): 

    
    # Set the CSV file path to be passed as a context parameter
    csv_file_path = "C:/Users/Admin/Desktop/PFE/original_dataset/new_dataset_stramlit.csv"
    talend_job_path_facts= "C:/Program Files (x86)/TOS_DI-8.0.1/studio/create_facts_table/create_facts_table_run.bat"
    # Construct the command to run the Talend job with the context parameter
    command_facts = [
        talend_job_path_facts,
        "--context=context",  # Replace 'your_context_name' with the actual context name in your Talend job
        "-job", "create_facts_table 0.1",  # Replace 'your_talend_job_name' with the actual Talend job name
        "--context_param",
        f"csvpath={csv_file_path}"
    ]

    subprocess.run(command_facts, shell=True)
    

def integrate_dimensions2_new_data(): 

    
    # Set the CSV file path to be passed as a context parameter
    csv_file_path = "C:/Users/Admin/Desktop/PFE/original_dataset/new_dataset_stramlit.csv"
    # Define the path to the Talend job executable
    talend_job_path_dimensions ="C:/Program Files (x86)/TOS_DI-8.0.1/studio/insert_dilentions_2/insert_dilentions_2_run.bat"
    # Construct the command to run the Talend job with the context parameter
    command_dimensions = [
        talend_job_path_dimensions,
        "--context=context",  # Replace 'your_context_name' with the actual context name in your Talend job
        "-job", "create_dimentions_table 0.1",  # Replace 'your_talend_job_name' with the actual Talend job name
        "--context_param",
        f"csvpath={csv_file_path}"
    ]

    # Execute the command using subprocess
    subprocess.run(command_dimensions, shell=True)


def integrate_facts2_new_data(): 

    
    # Set the CSV file path to be passed as a context parameter
    csv_file_path = "C:/Users/Admin/Desktop/PFE/original_dataset/new_dataset_stramlit.csv"
    talend_job_path_facts= "C:/Program Files (x86)/TOS_DI-8.0.1/studio/insert_facts_2/insert_facts_2_run.bat"
    # Construct the command to run the Talend job with the context parameter
    command_facts = [
        talend_job_path_facts,
        "--context=context",  # Replace 'your_context_name' with the actual context name in your Talend job
        "-job", "create_facts_table 0.1",  # Replace 'your_talend_job_name' with the actual Talend job name
        "--context_param",
        f"csvpath={csv_file_path}"
    ]

    subprocess.run(command_facts, shell=True)
    


def get_current_datetime():
    current_datetime = datetime.datetime.now()
    return current_datetime

def transform_float_precision(df):
    for column in df.columns:
        if df[column].dtype == float:
            df[column] = df[column].round(6)
    return df

async def retrainIncremantale(connection,connection2,file,model_name,model_horizon,model_target,predictors):
    parts = predictors[0].split(',') 
    min_max_df= await get_min_max(connection,'hourly')
    time = await connection2.fetch('''SELECT * FROM time order by "Time_Id" asc''')
    electricity = await connection2.fetch('''SELECT * FROM electricity order by "Time_Id" asc''')
    gaz = await connection2.fetch('''SELECT * FROM gaz order by "Time_Id" asc''')
    temperature = await connection2.fetch('''SELECT * FROM temperature order by "Temperature_Id" asc''')
    humidity = await connection2.fetch('''SELECT * FROM humidity order by "Humidity_Id"  asc''')
    solar_radiation = await connection2.fetch('''SELECT * FROM solar_radiation order by "Solar_Radiation_Id"  asc''')
   
    response_data = [] 
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
  
    df_original= pd.DataFrame(response_data)  
    df_copy=df_original

    df_file=pd.read_csv(file.file)

   

    df_copy['date'] = pd.to_datetime(df_copy['date'])
    df_copy.set_index('date', inplace=True)
   
    df_file['date'] = pd.to_datetime(df_file['date'])
   
    desired_order = ['date','Electricity','Gas_01','Gas_02','Gas_03','Day_Degree_Cold','Day_Degree_Hot','Min_OutdoorTemp','Average_OutdoorTemp','Max_OutdoorTemp','Maximum_Humidity','Average_Humidity','Solar_Radiation','Hour','Day','Week','Month','Year']
    df_file = df_file[desired_order]
   
    df_file.set_index('date', inplace=True)
    model_pred=await load_joblib(connection,1,model_name)
    if model_pred is None:
        raise HTTPException(status_code=404, detail="Model not found.")
    df_file_scaled=df_file.copy()
    if model_horizon=='Daily':
            min_max_df= await get_min_max(connection,'Daily')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('D').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('D').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('D').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('D').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('D').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('D').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('D').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('D').mean()
            
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('D').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('D').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('D').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('D').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Hour',axis=1)
            df_file_scaled = df_file_scaled.ffill()
    if model_horizon=='Weekly':
            min_max_df= await get_min_max(connection,'Weekly')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('w').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('W').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('W').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('W').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('W').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('W').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('W').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('W').mean()
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('W').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('W').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('W').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('W').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Hour',axis=1)
            df_file_scaled.drop('Day',axis=1)
            df_file_scaled = df_file_scaled.ffill()
            df_file_scaled = df_file_scaled.bfill()
           
    if model_horizon=='Monthly':
            
           
            min_max_df= await get_min_max(connection,'Monthly')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('M').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('M').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('M').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('M').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('M').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('M').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('M').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('M').mean()
            
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('M').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('M').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('M').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('M').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Hour',axis=1)
            df_file_scaled.drop('Day',axis=1)
            df_file_scaled.drop('Week',axis=1)
            df_file_scaled = df_file_scaled.fillna(0)
       
    df_file_scaled['Electricity'] = df_file_scaled['Electricity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Electricity','max'],min_max_df.loc['Electricity','min']))
    df_file_scaled['Gas_01'] = df_file_scaled['Gas_01'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_01','max'],min_max_df.loc['Gas_01','min']))
    df_file_scaled['Gas_02'] = df_file_scaled['Gas_02'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_02','max'],min_max_df.loc['Gas_02','min']))
    df_file_scaled['Gas_03'] = df_file_scaled['Gas_03'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_03','max'],min_max_df.loc['Gas_03','min']))
    df_file_scaled['Day_Degree_Cold'] = df_file_scaled['Day_Degree_Cold'].apply(lambda x: min_max_scale(x,min_max_df.loc['Day_Degree_Cold','max'],min_max_df.loc['Day_Degree_Cold','min']))
    df_file_scaled['Solar_Radiation'] = df_file_scaled['Solar_Radiation'].apply(lambda x: min_max_scale(x,min_max_df.loc['Solar_Radiation','max'],min_max_df.loc['Solar_Radiation','min']))
    df_file_scaled['Day_Degree_Hot'] = df_file_scaled['Day_Degree_Hot'].apply(lambda x: min_max_scale(x,min_max_df.loc['Day_Degree_Hot','max'],min_max_df.loc['Day_Degree_Hot','min']))
    df_file_scaled['Average_Humidity'] = df_file_scaled['Average_Humidity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Average_Humidity','max'],min_max_df.loc['Average_Humidity','min']))
    df_file_scaled['Max_OutdoorTemp'] = df_file_scaled['Max_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Max_OutdoorTemp','max'],min_max_df.loc['Max_OutdoorTemp','min']))
    df_file_scaled['Average_OutdoorTemp'] = df_file_scaled['Average_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Average_OutdoorTemp','max'],min_max_df.loc['Average_OutdoorTemp','min']))
    df_file_scaled['Min_OutdoorTemp'] = df_file_scaled['Min_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Min_OutdoorTemp','max'],min_max_df.loc['Min_OutdoorTemp','min']))
    df_file_scaled['Maximum_Humidity'] = df_file_scaled['Maximum_Humidity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Maximum_Humidity','max'],min_max_df.loc['Maximum_Humidity','min']))
    X_new = df_file_scaled[parts].values
    y_new = df_file_scaled [model_target].values
    X_original=df_original[parts].values
    y_original=df_original[model_target].values
    X_combined = np.concatenate((X_original, X_new), axis=0)
    y_combined = np.concatenate((y_original, y_new), axis=0)
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.4, random_state=42)
    model_str = repr(model_pred)
    model_type = model_str.split('(')[0]
    param_string = model_str.split('(')[1].split(')')[0]

    # Remove single quotes from parameter values
    param_string_cleaned = param_string.replace("'", "")

    # Split the parameter string into individual parameter assignments
    param_assignments = param_string_cleaned.split(',')

    # Create a dictionary to store the parameters
    params = {}
    for assignment in param_assignments:
        # Split based on the first equal sign
        param_parts = assignment.split('=', 1)
        param_name = param_parts[0].strip()
        param_value = param_parts[1].strip()

        # Convert parameter value to appropriate data type
        try:
            param_value = eval(param_value)  # Safely evaluate parameter value
        except:
            pass  # Use the value as is if conversion fails
        
        params[param_name] = param_value

    # Print the extracted parameters
    if model_type == 'RandomForestClassifier':
     retrained_model = RandomForestClassifier(**params)
    elif model_type == 'RandomForestRegressor':
        retrained_model = RandomForestRegressor(**params)
    elif model_type == 'SVC':
        retrained_model = SVC(**params)
    elif model_type == 'SVR':
        retrained_model = SVR(**params)
    elif model_type == 'LogisticRegression':
        retrained_model = LogisticRegression(**params)
    elif model_type == 'LinearRegression':
        retrained_model = LinearRegression(**params)
    elif model_type == 'Ridge':
        retrained_model = Ridge(**params)
    elif model_type == 'Lasso':
        retrained_model = Lasso(**params)
    elif model_type == 'XGBClassifier':
        retrained_model = xgb.XGBClassifier(**params)
    elif model_type == 'XGBRegressor':
        retrained_model = xgb.XGBRegressor(**params)
    elif model_type == 'LGBMClassifier':
        retrained_model = lgb.LGBMClassifier(**params)
    elif model_type == 'LGBMRegressor':
        retrained_model = lgb.LGBMRegressor(**params)
    elif model_type == 'CatBoostClassifier':
        retrained_model = cb.CatBoostClassifier(**params)
    elif model_type == 'CatBoostRegressor':
        retrained_model = cb.CatBoostRegressor(**params)
    elif model_type == 'KNeighborsClassifier':
        retrained_model = KNeighborsClassifier(**params)
    elif model_type == 'KNeighborsRegressor':
        retrained_model = KNeighborsRegressor(**params)
    elif model_type == 'GaussianNB':
        retrained_model = GaussianNB(**params)
    # Add more cases for other model types

    # Retrain the model on your training data
    

    retrained_model.fit(X_train, y_train)


    X_test = df_file_scaled[parts].values   
    y_test = df_file_scaled[model_target].values

    y_pred=retrained_model.predict(X_test)
    
    # y_pred = np.vectorize(lambda x: min_max_scale(x, min_max_df.loc[model_target, 'max'], min_max_df.loc[model_target, 'min']))(y_pred)

    mean= mean_absolute_error(y_test,y_pred)
    rmse = mean_squared_error(y_test,y_pred, squared=False)
    mse=mean_squared_error(y_test,y_pred)
    result ={}
    result={
        'mean':mean,
        'mse':mse,
        'rmse':rmse
    }

    models_dir = "models/Custom_Models/"  
    os.makedirs(models_dir, exist_ok=True)  
    model_filename = os.path.join(models_dir, f"{model_name}.joblib")
    joblib.dump(retrained_model, model_filename)

    return json.dumps(result)
   
async def retrainTotale(connection,connection2,file,model_name,model_horizon,model_target,predictors):
    parts = predictors[0].split(',') 
    min_max_df= await get_min_max(connection,'hourly')
    time = await connection2.fetch('''SELECT * FROM time order by "Time_Id" asc''')
    electricity = await connection2.fetch('''SELECT * FROM electricity order by "Time_Id" asc''')
    gaz = await connection2.fetch('''SELECT * FROM gaz order by "Time_Id" asc''')
    temperature = await connection2.fetch('''SELECT * FROM temperature order by "Temperature_Id" asc''')
    humidity = await connection2.fetch('''SELECT * FROM humidity order by "Humidity_Id"  asc''')
    solar_radiation = await connection2.fetch('''SELECT * FROM solar_radiation order by "Solar_Radiation_Id"  asc''')
   
    response_data = [] 
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
  
    df_original= pd.DataFrame(response_data)  
    df_copy=df_original

    df_file=pd.read_csv(file.file)

   

    df_copy['date'] = pd.to_datetime(df_copy['date'])
    df_copy.set_index('date', inplace=True)
   
    df_file['date'] = pd.to_datetime(df_file['date'])
   
    desired_order = ['date','Electricity','Gas_01','Gas_02','Gas_03','Day_Degree_Cold','Day_Degree_Hot','Min_OutdoorTemp','Average_OutdoorTemp','Max_OutdoorTemp','Maximum_Humidity','Average_Humidity','Solar_Radiation','Hour','Day','Week','Month','Year']
    df_file = df_file[desired_order]
   
    df_file.set_index('date', inplace=True)
    model_pred=await load_joblib(connection,1,model_name)
    if model_pred is None:
        raise HTTPException(status_code=404, detail="Model not found.")
    df_file_scaled=df_file.copy()
    if model_horizon=='Daily':
            min_max_df= await get_min_max(connection,'Daily')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('D').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('D').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('D').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('D').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('D').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('D').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('D').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('D').mean()
            
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('D').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('D').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('D').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('D').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Hour',axis=1)
            df_file_scaled = df_file_scaled.ffill()
    if model_horizon=='Weekly':
            min_max_df= await get_min_max(connection,'Weekly')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('w').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('W').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('W').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('W').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('W').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('W').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('W').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('W').mean()
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('W').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('W').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('W').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('W').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Hour',axis=1)
            df_file_scaled.drop('Day',axis=1)
            df_file_scaled = df_file_scaled.ffill()
            df_file_scaled = df_file_scaled.bfill()
           
    if model_horizon=='Monthly':
            
           
            min_max_df= await get_min_max(connection,'Monthly')
            df_file_scaled['Day_Degree_Cold'] = df_file['Day_Degree_Cold'].resample('M').mean()
            df_file_scaled['Day_Degree_Hot'] = df_file['Day_Degree_Hot'].resample('M').mean()
            df_file_scaled['Min_OutdoorTemp'] = df_file['Min_OutdoorTemp'].resample('M').mean()
            df_file_scaled['Average_OutdoorTemp'] = df_file['Average_OutdoorTemp'].resample('M').mean()
            df_file_scaled['Max_OutdoorTemp'] = df_file['Max_OutdoorTemp'].resample('M').max()
            df_file_scaled['Maximum_Humidity'] = df_file['Maximum_Humidity'].resample('M').max()
            df_file_scaled['Average_Humidity'] = df_file['Average_Humidity'].resample('M').mean()
            df_file_scaled['Solar_Radiation'] = df_file['Solar_Radiation'].resample('M').mean()
            
            df_file_scaled['Electricity'] = df_file['Electricity'].resample('M').sum()
            df_file_scaled['Gas_01'] = df_file['Gas_01'].resample('M').sum()
            df_file_scaled['Gas_02'] = df_file['Gas_02'].resample('M').sum()
            df_file_scaled['Gas_03'] = df_file['Gas_03'].resample('M').sum()
            df_file_scaled['Day'] = df_file['Day']
            df_file_scaled['Week'] = df_file['Week']
            df_file_scaled['Month'] = df_file['Month']
            df_file_scaled['Year'] = df_file['Year']
            df_file_scaled.drop('Hour',axis=1)
            df_file_scaled.drop('Day',axis=1)
            df_file_scaled.drop('Week',axis=1)
            df_file_scaled = df_file_scaled.fillna(0)
       
    df_file_scaled['Electricity'] = df_file_scaled['Electricity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Electricity','max'],min_max_df.loc['Electricity','min']))
    df_file_scaled['Gas_01'] = df_file_scaled['Gas_01'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_01','max'],min_max_df.loc['Gas_01','min']))
    df_file_scaled['Gas_02'] = df_file_scaled['Gas_02'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_02','max'],min_max_df.loc['Gas_02','min']))
    df_file_scaled['Gas_03'] = df_file_scaled['Gas_03'].apply(lambda x: min_max_scale(x,min_max_df.loc['Gas_03','max'],min_max_df.loc['Gas_03','min']))
    df_file_scaled['Day_Degree_Cold'] = df_file_scaled['Day_Degree_Cold'].apply(lambda x: min_max_scale(x,min_max_df.loc['Day_Degree_Cold','max'],min_max_df.loc['Day_Degree_Cold','min']))
    df_file_scaled['Solar_Radiation'] = df_file_scaled['Solar_Radiation'].apply(lambda x: min_max_scale(x,min_max_df.loc['Solar_Radiation','max'],min_max_df.loc['Solar_Radiation','min']))
    df_file_scaled['Day_Degree_Hot'] = df_file_scaled['Day_Degree_Hot'].apply(lambda x: min_max_scale(x,min_max_df.loc['Day_Degree_Hot','max'],min_max_df.loc['Day_Degree_Hot','min']))
    df_file_scaled['Average_Humidity'] = df_file_scaled['Average_Humidity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Average_Humidity','max'],min_max_df.loc['Average_Humidity','min']))
    df_file_scaled['Max_OutdoorTemp'] = df_file_scaled['Max_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Max_OutdoorTemp','max'],min_max_df.loc['Max_OutdoorTemp','min']))
    df_file_scaled['Average_OutdoorTemp'] = df_file_scaled['Average_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Average_OutdoorTemp','max'],min_max_df.loc['Average_OutdoorTemp','min']))
    df_file_scaled['Min_OutdoorTemp'] = df_file_scaled['Min_OutdoorTemp'].apply(lambda x: min_max_scale(x,min_max_df.loc['Min_OutdoorTemp','max'],min_max_df.loc['Min_OutdoorTemp','min']))
    df_file_scaled['Maximum_Humidity'] = df_file_scaled['Maximum_Humidity'].apply(lambda x: min_max_scale(x,min_max_df.loc['Maximum_Humidity','max'],min_max_df.loc['Maximum_Humidity','min']))
    X_new = df_file_scaled[parts].values
    y_new = df_file_scaled [model_target].values
    X_original=df_original[parts].values
    y_original=df_original[model_target].values
    X_combined = np.concatenate((X_original, X_new), axis=0)
    y_combined = np.concatenate((y_original, y_new), axis=0)
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.4, random_state=42)
    model_str = repr(model_pred)
    model_type = model_str.split('(')[0]
    param_string = model_str.split('(')[1].split(')')[0]

    # Remove single quotes from parameter values
    param_string_cleaned = param_string.replace("'", "")

    # Split the parameter string into individual parameter assignments
    param_assignments = param_string_cleaned.split(',')

    # Create a dictionary to store the parameters
    params = {}
    for assignment in param_assignments:
        # Split based on the first equal sign
        param_parts = assignment.split('=', 1)
        param_name = param_parts[0].strip()
        param_value = param_parts[1].strip()

        # Convert parameter value to appropriate data type
        try:
            param_value = eval(param_value)  # Safely evaluate parameter value
        except:
            pass  # Use the value as is if conversion fails
        
        params[param_name] = param_value

    # Print the extracted parameters
    if model_type == 'RandomForestClassifier':
     retrained_model = RandomForestClassifier(**params)
    elif model_type == 'RandomForestRegressor':
        retrained_model = RandomForestRegressor(**params)
    elif model_type == 'SVC':
        retrained_model = SVC(**params)
    elif model_type == 'SVR':
        retrained_model = SVR(**params)
    elif model_type == 'LogisticRegression':
        retrained_model = LogisticRegression(**params)
    elif model_type == 'LinearRegression':
        retrained_model = LinearRegression(**params)
    elif model_type == 'Ridge':
        retrained_model = Ridge(**params)
    elif model_type == 'Lasso':
        retrained_model = Lasso(**params)
    elif model_type == 'XGBClassifier':
        retrained_model = xgb.XGBClassifier(**params)
    elif model_type == 'XGBRegressor':
        retrained_model = xgb.XGBRegressor(**params)
    elif model_type == 'LGBMClassifier':
        retrained_model = lgb.LGBMClassifier(**params)
    elif model_type == 'LGBMRegressor':
        retrained_model = lgb.LGBMRegressor(**params)
    elif model_type == 'CatBoostClassifier':
        retrained_model = cb.CatBoostClassifier(**params)
    elif model_type == 'CatBoostRegressor':
        retrained_model = cb.CatBoostRegressor(**params)
    elif model_type == 'KNeighborsClassifier':
        retrained_model = KNeighborsClassifier(**params)
    elif model_type == 'KNeighborsRegressor':
        retrained_model = KNeighborsRegressor(**params)
    elif model_type == 'GaussianNB':
        retrained_model = GaussianNB(**params)
    # Add more cases for other model types

    # Retrain the model on your training data
    

    retrained_model.fit(X_train, y_train)


    X_test = df_file_scaled[parts].values   
    y_test = df_file_scaled[model_target].values

    y_pred=retrained_model.predict(X_test)
    mean= mean_absolute_error(y_test,y_pred)
    rmse = mean_squared_error(y_test,y_pred, squared=False)
    mse=mean_squared_error(y_test,y_pred)
    result ={}
    result={
        'mean':mean,
        'mse':mse,
        'rmse':rmse
    }

    models_dir = "models/Custom_Models/"  
    os.makedirs(models_dir, exist_ok=True)  
    model_filename = os.path.join(models_dir, f"{model_name}.joblib")
    joblib.dump(retrained_model, model_filename)

    return json.dumps(result)
  
    
    




async def calculate_shap_custom(connection, feature_names: List[str], model_name: str, data: List[float]):


    with open('xai/Custom/%s_shap.pkl' % model_name, 'rb') as file:
        model =load_joblib(connection,1,model_name)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found.")                    
        loaded_object = dill.load(file)
       

        shap_values = loaded_object.shap_values(data)

        shap_df = pd.DataFrame({
        "feature": feature_names,
        "importance": shap_values
        })
    
    shap_data = shap_df.to_dict(orient='records')
  
    return JSONResponse(content=shap_data)
    

def min_max_scale(value, max_val , min_val):
    if(value==0) :return value
    scaled_val = (value - min_val) / (max_val - min_val)
    return round(scaled_val,6)

def rev_min_max_func(scaled_val,target,max,min):
    max_val = max
    min_val = min
    og_val = (scaled_val*(max_val - min_val)) + min_val
    if(target=='Electricity' or target=='Solar_Radiation'):
      og_val= round(og_val,2) 
    return  og_val







def detect_data_drift_EMD(original_data, drift_data, alpha):
   
    detector = EMD()
    result_data = []
    any_drift_detected = False
    for col_name in original_data.columns:
        original_col = original_data[col_name].values
        drift_col = drift_data[col_name].values
        detector.fit(X=original_col)
        result = detector.compare(X=drift_col)
        distance = result[0].distance
        drift_detected = distance > alpha
        result_data.append((col_name, distance, alpha, drift_detected))
        if drift_detected:
            any_drift_detected = True
    result_df = pd.DataFrame(result_data, columns=['Column', 'Distance', 'Alpha', 'DriftDetected'])
    return result_df, any_drift_detected


def detect_data_drift_Ks(original_data, drift_data, alpha):
    detector = KSTest()
    detected_drift_columns = []
    any_drift_detected = False
    for col_name in original_data.columns:
        original_col = original_data[col_name].values
        drift_col = drift_data[col_name].values
        detector.fit(X=original_col)
        result = detector.compare(X=drift_col)
        p_value = result[0].p_value
        
        drift_detected = p_value < alpha
        detected_drift_columns.append((col_name, p_value, alpha, drift_detected))
        
        if drift_detected:
            any_drift_detected = True
    
    result_df = pd.DataFrame(detected_drift_columns, columns=['Column', 'PValue', 'Alpha', 'DriftDetected'])
    
    return result_df, any_drift_detected



def detect_data_drift_KL(original_data, drift_data, alpha):
    detector = KL()
    detected_drift_columns = []
    all_p_values = []
    any_drift_detected = False
    for col_name in original_data.columns:
        original_col = original_data[col_name].values
        drift_col = drift_data[col_name].values
        detector.fit(X=original_col)
        result = detector.compare(X=drift_col)
        distance = result[0].distance
        all_p_values.append((col_name, distance))
        
        drift_detected = distance > alpha
        detected_drift_columns.append((col_name, distance, alpha, drift_detected))
        
        if drift_detected:
            any_drift_detected = True
    
    result_df = pd.DataFrame(detected_drift_columns, columns=['Column', 'Distance', 'Alpha', 'DriftDetected'])
    
    return result_df, any_drift_detected


def concept_drift(y_pred, y_test, metric, detector):
    print(y_pred)
    concept_drift_detected = False
    drift_index = None
    drift_y_pred = None

    for i, (yd, y) in enumerate(zip(y_pred, y_test)):
        yd = round(yd, 1)
        y = round(y, 1)
        print(yd, y)
        error = 1 - int((yd == y))
        
        prequential_error = metric(error_value=error)
      
        _ = detector.update(value=error)
        status = detector.status
       
        if status['drift']:
            concept_drift_detected = True
            drift_index = i
            drift_y_pred = yd
            break
           
    

    
    return concept_drift_detected, drift_index


async def load_joblib(connection, user_id,model_name):
    models = await connection.fetch("SELECT model_id, model_details FROM models WHERE user_id = $1", user_id)
   
    
    model_name_with_extension = f"{model_name}.joblib"
    
    model_path = f"{MODELS_DIR2}/{model_name_with_extension}"

    return joblib.load(model_path)

async def get_min_max(connection,model_horizon):
    time = await connection.fetch('''SELECT * FROM time order by "Time_Id" asc''')
    electricity = await connection.fetch('''SELECT * FROM electricity order by "Time_Id" asc''')
    gaz = await connection.fetch('''SELECT * FROM gaz order by "Time_Id" asc''')
    temperature = await connection.fetch('''SELECT * FROM temperature order by "Temperature_Id" asc''')
    humidity = await connection.fetch('''SELECT * FROM humidity order by "Humidity_Id"  asc''')
    solar_radiation = await connection.fetch('''SELECT * FROM solar_radiation order by "Solar_Radiation_Id"  asc''')
   
    response_data = []
  
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
   
    df = pd.DataFrame(response_data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date',inplace=True)
    df_copy=df.copy()
    if model_horizon == 'Daily':
        df_copy['Day_Degree_Cold'] = df['Day_Degree_Cold'].resample('D').mean()
        df_copy['Day_Degree_Hot'] = df['Day_Degree_Hot'].resample('D').mean()
        df_copy['Min_OutdoorTemp'] = df['Min_OutdoorTemp'].resample('D').mean()
        df_copy['Average_OutdoorTemp'] = df['Average_OutdoorTemp'].resample('D').mean()
        df_copy['Max_OutdoorTemp'] = df['Max_OutdoorTemp'].resample('D').max()
        df_copy['Maximum_Humidity'] = df['Maximum_Humidity'].resample('D').max()
        df_copy['Average_Humidity'] = df['Average_Humidity'].resample('D').mean()
        df_copy['Solar_Radiation'] = df['Solar_Radiation'].resample('D').mean()
        
        df_copy['Electricity'] = df['Electricity'].resample('D').sum()
        df_copy['Gas_01'] = df['Gas_01'].resample('D').sum()
        df_copy['Gas_02'] = df['Gas_02'].resample('D').sum()
        df_copy['Gas_03'] = df['Gas_03'].resample('D').sum()
        df_copy['Day'] = df['Day']
        df_copy['Week'] = df['Week']
        df_copy['Month'] = df['Month']
        df_copy['Year'] = df['Year']
    if model_horizon == 'Weekly':
        df_copy['Day_Degree_Cold'] = df['Day_Degree_Cold'].resample('W').mean()
        df_copy['Day_Degree_Hot'] = df['Day_Degree_Hot'].resample('W').mean()
        df_copy['Min_OutdoorTemp'] = df['Min_OutdoorTemp'].resample('W').mean()
        df_copy['Average_OutdoorTemp'] = df['Average_OutdoorTemp'].resample('W').mean()
        df_copy['Max_OutdoorTemp'] = df['Max_OutdoorTemp'].resample('W').max()
        df_copy['Maximum_Humidity'] = df['Maximum_Humidity'].resample('W').max()
        df_copy['Average_Humidity'] = df['Average_Humidity'].resample('W').mean()
        df_copy['Solar_Radiation'] = df['Solar_Radiation'].resample('W').mean()
        
        df_copy['Electricity'] = (df['Electricity'].resample('W').sum())
        df_copy['Gas_01'] = df['Gas_01'].resample('W').sum()
        df_copy['Gas_02'] = df['Gas_02'].resample('W').sum()
        df_copy['Gas_03'] = df['Gas_03'].resample('W').sum()
        df_copy['Day'] = df['Day']
        df_copy['Week'] = df['Week']
        df_copy['Month'] = df['Month']
        df_copy['Year'] = df['Year']
    if model_horizon == 'Monthly':
        df_copy['Day_Degree_Cold'] = df['Day_Degree_Cold'].resample('M').mean()
        df_copy['Day_Degree_Hot'] = df['Day_Degree_Hot'].resample('M').mean()
        df_copy['Min_OutdoorTemp'] = df['Min_OutdoorTemp'].resample('M').mean()
        df_copy['Average_OutdoorTemp'] = df['Average_OutdoorTemp'].resample('M').mean()
        df_copy['Max_OutdoorTemp'] = df['Max_OutdoorTemp'].resample('M').max()
        df_copy['Maximum_Humidity'] = df['Maximum_Humidity'].resample('M').max()
        df_copy['Average_Humidity'] = df['Average_Humidity'].resample('M').mean()
        df_copy['Solar_Radiation'] = df['Solar_Radiation'].resample('M').mean()
        
        df_copy['Electricity'] = (df['Electricity'].resample('M').sum())
        df_copy['Gas_01'] = df['Gas_01'].resample('M').sum()
        df_copy['Gas_02'] = df['Gas_02'].resample('M').sum()
        df_copy['Gas_03'] = df['Gas_03'].resample('M').sum()
        df_copy['Day'] = df['Day']
        df_copy['Week'] = df['Week']
        df_copy['Month'] = df['Month']
        df_copy['Year'] = df['Year']


    
       




           
    min_max_dict = {}
    for column in df.columns:
        min_max_dict[column] = {
            'min': df_copy[column].min(),
            'max': df_copy[column].max()
        }
    min_max_df = pd.DataFrame.from_dict(min_max_dict, orient='index')
    return min_max_df
