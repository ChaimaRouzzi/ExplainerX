from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
import pandas as pd


def correlation_feature_selection(method, df, k, target):
    correlation_with_target = df.corrwith(df[target], method=method)
    sorted_correlations = correlation_with_target.sort_values(ascending=False)
    top_correlated_features = sorted_correlations.head(k + 1)
    top_correlated_features = top_correlated_features.drop(target)
    top_features_list = top_correlated_features.index.tolist()  # Convert the index to a list
    print(top_features_list)
    return top_features_list


def mutual_info_feature_selection(df, k, target, is_classification=True):
    if is_classification:
        mi_func = mutual_info_classif
    else:
        mi_func = mutual_info_regression

    mutual_info_with_target = mi_func(df.drop(target, axis=1), df[target])
    mutual_info_series = pd.Series(mutual_info_with_target, index=df.columns.drop(target))
    sorted_mutual_info = mutual_info_series.sort_values(ascending=False)
    top_mutual_info_features = sorted_mutual_info.head(k)
    top_features_list = top_mutual_info_features.index.tolist()
    print(top_features_list)
    return top_features_list


