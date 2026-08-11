import pandas as pd


def profile_dataset(dataframe):
    """
    Analyze a pandas DataFrame and return basic data-quality statistics.
    """

    profile = {
        "row_count": len(dataframe),
        "column_count": len(dataframe.columns),
        "columns": {}
    }

    for column in dataframe.columns:
        series = dataframe[column]

        profile["columns"][column] = {
            "data_type": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "unique_count": int(series.nunique(dropna=True)),
            "duplicate_count": int(series.duplicated().sum()),
        }

    return profile