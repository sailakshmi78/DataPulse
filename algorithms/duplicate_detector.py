def find_duplicates(dataframe, columns=None):
    """
    Find duplicate rows/values in a pandas DataFrame.

    NULL, empty, or whitespace-only values are NOT considered
    duplicates.

    Returns:
        list of dictionaries containing duplicate row information.
    """

    if dataframe.empty:
        return []

    if columns is None:
        columns = list(dataframe.columns)

    columns = [
        column
        for column in columns
        if column in dataframe.columns
    ]

    if not columns:
        return []

    working_df = dataframe.copy()

    # Ignore NULL / empty / whitespace-only values when checking
    # uniqueness for the configured duplicate columns.
    for column in columns:

        working_df = working_df[
            working_df[column].notna()
            & (
                working_df[column]
                .astype(str)
                .str.strip()
                .ne("")
            )
        ]

    duplicate_mask = working_df.duplicated(
        subset=columns,
        keep="first"
    )

    duplicate_indices = working_df.index[duplicate_mask]

    duplicates = []

    for index in duplicate_indices:

        row = dataframe.loc[index, columns]

        duplicates.append({
            "row_number": int(index) + 2,
            "columns": columns,
            "values": row.to_dict()
        })

    return duplicates