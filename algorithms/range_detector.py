import pandas as pd


def find_out_of_range(dataframe, column, minimum, maximum):
    """
    Find values outside the allowed range for a numeric column.

    Returns:
        list of dictionaries containing out-of-range values.
    """

    issues = []

    if dataframe.empty:
        return issues

    if column not in dataframe.columns:
        return issues

    series = pd.to_numeric(
        dataframe[column],
        errors="coerce"
    )

    invalid_mask = (
        series.notna()
        & (
            (series < minimum)
            | (series > maximum)
        )
    )

    indices = dataframe.index[invalid_mask]

    for index in indices:

        value = dataframe.loc[index, column]

        issues.append({
            "row_number": int(index) + 2,
            "column_name": column,
            "value": value,
            "minimum": minimum,
            "maximum": maximum
        })

    return issues