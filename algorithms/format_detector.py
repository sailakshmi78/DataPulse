import re
import pandas as pd


def find_format_issues(dataframe, column, pattern):
    """
    Find values that do not match the configured format pattern.

    Missing values are ignored here because they are handled
    separately by the missing-value detector.
    """

    issues = []

    regex = re.compile(pattern)

    for index, value in dataframe[column].items():

        # Missing values belong to the missing-value detector
        if pd.isna(value):
            continue

        value = str(value).strip()

        # Empty strings are treated as invalid format
        if not value or not regex.fullmatch(value):
            issues.append({
                "row_number": index + 2,
                "column_name": column,
                "value": value,
                "message": "Invalid format detected."
            })

    return issues