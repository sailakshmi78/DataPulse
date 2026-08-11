import pandas as pd


def find_missing_values(dataframe):
    """
    Find missing values in every column.

    Returns:
        list of dictionaries containing missing-value information.
    """

    missing_values = []

    if dataframe.empty:
        return missing_values

    for column in dataframe.columns:

        mask = dataframe[column].isna()

        missing_count = int(mask.sum())

        if missing_count == 0:
            continue

        indices = dataframe.index[mask]

        missing_rows = [
            int(index) + 2
            for index in indices
        ]

        missing_values.append({
            "column_name": column,
            "missing_count": missing_count,
            "rows": missing_rows
        })

    return missing_values