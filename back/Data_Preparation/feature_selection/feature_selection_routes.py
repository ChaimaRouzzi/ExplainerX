from fastapi import HTTPException
from fastapi import APIRouter, Depends
from Data_Gathering.db_connection import connect_to_db
import pandas as pd
feature_selection_router = APIRouter()
from typing import List, Dict
from Data_Gathering.data_gathering_logic import fetch_data

from Data_Preparation.feature_selection.feature_selection_logic import correlation_feature_selection, mutual_info_feature_selection


@feature_selection_router.post("/{method}")
async def feature_selection_correlation(method: str, target: str, horizon: str, k: int = 2, connection=Depends(connect_to_db)):
    data = await fetch_data(connection, "False")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    if horizon == "Hourly": 
        horizon = "H"
    elif horizon == "Daily": 
        horizon = "D"
    elif horizon == "Weekly": 
        horizon = "W"
    elif horizon == "Monthly": 
        horizon = "M"
    df_resampled = df.resample(horizon).mean()
    df_resampled.fillna(df_resampled.mean(), inplace=True)
    if target == 'Electricity': 
        columns_to_delete = ['Gas_02', 'Gas_03', 'Gas_01']
    elif target == 'Gas_01': 
        columns_to_delete = ['Gas_02', 'Gas_03', 'Electricity']
    elif target == 'Gas_02': 
        columns_to_delete = ['Gas_01', 'Gas_03', 'Electricity']
    elif target == 'Gas_03': 
        columns_to_delete = ['Gas_01', 'Gas_02', 'Electricity']

    df_resampled = df_resampled.drop(columns=columns_to_delete)

    if method == 'pearson' or method == "kendall" or method == "spearman":
        list = correlation_feature_selection(method, df_resampled, k, target)
    elif method == "mutual_info": 
        list = mutual_info_feature_selection(df_resampled, k, target, is_classification=False)
    else: 
        return {"error": "Invalid method"}

    return {"selected_features": list}

