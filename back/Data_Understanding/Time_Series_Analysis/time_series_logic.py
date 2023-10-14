import pandas as pd
import json
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.seasonal import STL
import statsmodels.api as sm
from typing import List
import numpy as np
from scipy.stats import norm
from scipy.special import logsumexp
from statsmodels.tsa.stattools import acf, pacf

def handle_nan_values(data, column_name):
    # Convert list to DataFrame
    df = pd.DataFrame(data, columns=[column_name])
    # Fill NaN values with the mean of non-missing values
    mean_value = df[column_name].mean()
    df[column_name].fillna(mean_value, inplace=True)
    # Display the DataFrame
    print(df)
    return df[column_name]


def perform_stationarity_adf_test(data, column_name):
    cleaned_values = handle_nan_values(data, column_name)
    data_list = cleaned_values.tolist()
    result = ts.adfuller(data_list)
    adf_statistic = round(result[0], 4)
    p_value = round(result[1], 4)
    critical_values = {key: round(value, 4) for key, value in result[4].items()}

    adf_results = {
        'ADF Statistic': adf_statistic,
        'p-value': p_value,
        'Critical Values': critical_values
    }

    if p_value < 0.05:
        print("The time series is stationary (reject null hypothesis).")
        adf_results['Stationarity'] = 'Stationary'
    else:
        print("The time series is non-stationary (fail to reject null hypothesis).")
        adf_results['Stationarity'] = 'Non-Stationary'

    return adf_results

def perform_stationarity_kpss_test(data, column_name):
    cleaned_values = handle_nan_values(data, column_name)
    data_list = cleaned_values.tolist()
    result = ts.kpss(data_list)
    kpss_statistic = round(result[0], 4)
    p_value = round(result[1], 4)
    critical_values = {key: round(value, 4) for key, value in result[3].items()}

    kpss_results = {
        'KPSS Statistic': kpss_statistic,
        'p-value': p_value,
        'Critical Values': critical_values
    }

    if p_value < 0.05:
        print("The time series is non-stationary (reject null hypothesis).")
        kpss_results['Stationarity'] = 'Non-Stationary'
    else:
        print("The time series is stationary (fail to reject null hypothesis).")
        kpss_results['Stationarity'] = 'Stationary'

    return kpss_results


def perform_stationarity_pp_test(data, column_name):
    cleaned_values = handle_nan_values(data, column_name)
    data_list = cleaned_values.tolist()
    result = ts.adfuller(data_list, regression='ct', autolag='AIC')
    pp_statistic = round(result[0], 4)
    p_value = round(result[1], 4)
    critical_values = result[4]

    pp_results = {
        'PP Statistic': pp_statistic,
        'p-value': p_value,
        'Critical Values': critical_values
    }

    if p_value < 0.05:
        print("The time series is stationary (reject null hypothesis).")
        pp_results['Stationarity'] = 'Stationary'
    else:
        print("The time series is non-stationary (fail to reject null hypothesis).")
        pp_results['Stationarity'] = 'Non-Stationary'

    print(pp_results)

    return pp_results


def perform_time_series_decomposition(data, column_name, model):
    cleaned_values = handle_nan_values(data, column_name)
    print(cleaned_values)
    data_list = cleaned_values.tolist()

    index = pd.date_range(start='2018-09-01 05:00:00', periods=len(data_list), freq="H")
    series = pd.Series(data_list, index=index)
    print(series)

    if model == 'additive':
        decomposition = sm.tsa.seasonal_decompose(series, model='additive', period=12)
    elif model == 'multiplicative':
        if any(value <= 0 for value in series):
            error_message = {
            'Error': "Multiplicative seasonality is not appropriate for zero and negative values.",
            }
            return error_message
        else: 
            decomposition = sm.tsa.seasonal_decompose(series, model='multiplicative', period=12)
    else:
        print("Invalid model specified. Defaulting to 'additive' model.")
        decomposition = sm.tsa.seasonal_decompose(series, model='additive', period=12)

    observed = decomposition.observed
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    trend = trend.ffill().bfill()
    observed = observed.ffill().bfill()
    seasonal = seasonal.ffill().bfill()
    residual = residual.ffill().bfill()
    decomposition_results = {
        'Date': series.index.strftime("%Y-%m-%d %H:%M:%S").tolist(),
        'Observed': observed.tolist(),
        'Trend': trend.tolist(),
        'Seasonal': seasonal.tolist(),
        'Residual': residual.tolist()
    }

    return decomposition_results

def calculate_acf(data, column_name, num_lags):
    cleaned_values = handle_nan_values(data, column_name)
    print(cleaned_values)
    data_list = cleaned_values.tolist()

    acf_values = acf(data_list, nlags=num_lags, fft=True)
    acf_list = [
        str(value) if not np.isnan(value) and not np.isinf(value) and np.abs(value) < 1e100 else "null"
        for value in acf_values
    ]
    return acf_list


def calculate_pacf(data, column_name, num_lags):
    cleaned_values = handle_nan_values(data, column_name)
    print(cleaned_values)
    data_list = cleaned_values.tolist()

    max_lags = min(len(data_list) - 1, num_lags)  # Set the maximum number of lags
    pacf_values = pacf(data_list, nlags=max_lags, method='ywm')
    pacf_list = [
        str(value) if not np.isnan(value) and not np.isinf(value) and np.abs(value) < 1e100 else "null"
        for value in pacf_values
    ]
    return pacf_list