import pandas as pd
from datetime import datetime
from Data_Gathering.data_gathering_logic import fetch_data, fetch_data_version
import numpy as np 
import json
from Data_Understanding.Data_Analysis.data_analysis_logic import versions_number,updated_versions_number
def count_missing_values(data):
    total_values = len(data)
    print(total_values)
    missing_values = sum(1 for item in data if item is None)
    print(missing_values)
    if total_values != 0:
     missing_percentage = (missing_values / total_values) * 100
    else:
     missing_percentage = 0
    missing_percentage = round(missing_percentage, 2)  # Format the percentage to two decimal places
    missing_values_data = {
        'missing_values': missing_values,
        'missing_values_percentage': missing_percentage,
    }
    print (missing_values_data)
    return missing_values_data


def count_outliers(data): 
    data_series = pd.Series(data)
    data_series = data_series.dropna()
    q1 = data_series.quantile(0.25)
    q3 = data_series.quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    outliers = [item for item in data if item is not None and (item < lower_fence or item > upper_fence)]
    num_outliers = len(outliers)
    if len(data) != 0:
     percent_outliers = (num_outliers / len(data)) * 100
    else:
     percent_outliers = 0
    percent_outliers = round(percent_outliers, 2)  # Format the percentage to two decimal places
    outliers_data = {
        'num_outliers': num_outliers,
        'percent_outliers': percent_outliers,
        'outliers': outliers
    }
    return outliers_data

def count_negative_values(data):
    total_values = len(data)
    negative_values = sum(1 for item in data if item is not None and item < 0)
    if total_values != 0:
      negative_percentage = (negative_values / total_values) * 100
    else:
      negative_percentage = 0
    negative_percentage = round(negative_percentage, 2)  # Format the percentage to two decimal places
    negative_values_data = {
        'negative_values': negative_values,
        'negative_percentage': negative_percentage,
    }
    return negative_values_data


def count_zero_values(data):
    total_values = len(data)
    zero_values = sum(1 for item in data if item == 0)
    if total_values != 0:
      zero_percentage = round((zero_values / total_values) * 100, 2)
    else:
      zero_percentage = 0
    zero_values_data = {
        'zero_values': zero_values,
        'zero_percentage': zero_percentage,
    }
    return zero_values_data


def describe_data(data):
    data_series = pd.Series(data)
    data_series = data_series.dropna()
    data_series_desc = data_series.describe().to_dict()
    return data_series_desc


def detect_data_types(data):
    data_types = set()

    for item in data:
        if isinstance(item, datetime):
            data_types.add('datetime')
        elif isinstance(item, str):
            try:
                datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                data_types.add('datetime')
            except ValueError:
                data_types.add('str')
        elif item is not None:
            data_type = type(item).__name__
            data_types.add(data_type)

    return list(data_types)

def count_unique_values(data):
    total_values = len(data)
    unique_values = len(set(data)) 
    if total_values != 0:
     unique_percentage = (unique_values / total_values) * 100
    else:
      unique_percentage = 0
    unique_percentage = round(unique_percentage, 2)  # Format the percentage to two decimal places
    unique_values_data = {
        'unique_values': unique_values,
        'unique_percentage': unique_percentage,
    }
    return unique_values_data

async def single_column(connection,connection2,updated,column_name,version):
    if(updated=='False'):
        print(updated)
        if version == "-1": 
            data = await fetch_data(connection,updated)
            column_values = [entry[column_name] for entry in data]
            missing_values = count_missing_values(column_values)
            outliers = count_outliers(column_values)
            negative_values = count_negative_values(column_values)
            zero_values = count_zero_values(column_values)
            desc = describe_data(column_values)
            types = detect_data_types(column_values)
            unique_values = count_unique_values(column_values)
            column_values = [0 if value is None else value for value in column_values]
            hist_counts, hist_bins = np.histogram(column_values, bins='auto')
            date_values = [entry["date"] for entry in data if entry["date"] is not None]
            date_values = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() for date_str in date_values]
        
            daily_date_values = list(set(date_values))  
            daily_date_values.sort()  

            daily_date_values_str = [str(daily_date) for daily_date in daily_date_values]
            aggregated_values = []
            for daily_date in daily_date_values:
                daily_value_sum = sum([value if date == daily_date and value is not None else 0 for value, date in zip(column_values, date_values)])
                aggregated_values.append(daily_value_sum)


            column_data = {
                "column_values": aggregated_values,
                "hist_counts": hist_counts.tolist(),
                "hist_bins": hist_bins.tolist(),
                "date_values": daily_date_values_str  
            }
        else:   
                data = await fetch_data_version(connection, version,updated)
                column_values = [entry[column_name] for entry in data]
                missing_values = count_missing_values(column_values)
                outliers = count_outliers(column_values)
                negative_values = count_negative_values(column_values)
                zero_values = count_zero_values(column_values)
                desc = describe_data(column_values)
                types = detect_data_types(column_values) 
                column_values = [entry[column_name] for entry in data if entry[column_name] is not None]
                unique_values = count_unique_values(column_values)
                hist_counts, hist_bins = np.histogram(column_values, bins='auto')
                date_values = [entry["date"] for entry in data if entry["date"] is not None]
                date_values = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() for date_str in date_values]
            
                daily_date_values = list(set(date_values))  
                daily_date_values.sort()  

                daily_date_values_str = [str(daily_date) for daily_date in daily_date_values]
                aggregated_values = []
                for daily_date in daily_date_values:
                    daily_value_sum = sum([value for value, date in zip(column_values, date_values) if date == daily_date])
                    aggregated_values.append(daily_value_sum)


                column_data = {
                    "column_values": aggregated_values,
                    "hist_counts": hist_counts.tolist(),
                    "hist_bins": hist_bins.tolist(),
                    "date_values": daily_date_values_str  
                }
    else:
            if version == "-1": 
                data = await fetch_data(connection2,updated)
                print(data)   
                column_values = [entry[column_name] for entry in data]
                missing_values = count_missing_values(column_values)
                outliers = count_outliers(column_values)
                negative_values = count_negative_values(column_values)
                zero_values = count_zero_values(column_values)
                desc = describe_data(column_values)
                types = detect_data_types(column_values)
                unique_values = count_unique_values(column_values)
                column_values = [entry[column_name] for entry in data if entry[column_name] is not None]
                hist_counts, hist_bins = np.histogram(column_values, bins='auto')
                date_values = [entry["date"] for entry in data if entry["date"] is not None]
                date_values = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() for date_str in date_values]
            
                daily_date_values = list(set(date_values))  
                daily_date_values.sort()  

                daily_date_values_str = [str(daily_date) for daily_date in daily_date_values]
                aggregated_values = []
                for daily_date in daily_date_values:
                    daily_value_sum = sum([value for value, date in zip(column_values, date_values) if date == daily_date])
                    aggregated_values.append(daily_value_sum)


                column_data = {
                    "column_values": aggregated_values,
                    "hist_counts": hist_counts.tolist(),
                    "hist_bins": hist_bins.tolist(),
                    "date_values": daily_date_values_str  
                }
            else: 
                data = await fetch_data_version(connection2, version,updated)
                column_values = [entry[column_name] for entry in data]

                missing_values = count_missing_values(column_values)
                outliers = count_outliers(column_values)
                negative_values = count_negative_values(column_values)
                zero_values = count_zero_values(column_values)
                desc = describe_data(column_values)
                types = detect_data_types(column_values)
                column_values = [entry[column_name] for entry in data if entry[column_name] is not None]
                unique_values = count_unique_values(column_values)
                hist_counts, hist_bins = np.histogram(column_values, bins='auto')
                date_values = [entry["date"] for entry in data if entry["date"] is not None]
              
                date_values = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() for date_str in date_values]
            
                daily_date_values = list(set(date_values))  
                daily_date_values.sort()  

                daily_date_values_str = [str(daily_date) for daily_date in daily_date_values]
                aggregated_values = []
                for daily_date in daily_date_values:
                    daily_value_sum = sum([value for value, date in zip(column_values, date_values) if date == daily_date])
                    aggregated_values.append(daily_value_sum)


                column_data = {
                    "column_values": aggregated_values,
                    "hist_counts": hist_counts.tolist(),
                    "hist_bins": hist_bins.tolist(),
                    "date_values": daily_date_values_str  
                }
    updated_ver= await updated_versions_number(connection2)
    nb_versions=await versions_number(connection)
    result={ "updated_version":updated_ver,
             "versions_number":nb_versions,
             "missing_values":missing_values,
             "outlires":outliers,
             "negative_values":negative_values,
             'unique':unique_values,
             'type':types,
             'zero_values':zero_values,
             "column_data":column_data }
    print(result)
    return  json.dumps(result)

        
        