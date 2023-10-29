from typing import Any, Dict, Callable, List, Optional, Union
import pandas as pd
import re


def get_column_index(df, primary_column, secondary_column):
    if primary_column in df.columns:
        return df.columns.get_loc(primary_column)
    elif secondary_column in df.columns:
        return df.columns.get_loc(secondary_column)
    else:
        return -1  # Return -1 if neither column exists


def parse_date_columns(df: pd.DataFrame, convert_dates: bool = False) -> Union[list, pd.DataFrame]:
    """
    Identify date columns in a DataFrame and optionally convert them to datetime objects.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        convert_dates (bool, optional): If True, returns a new DataFrame with date columns converted to datetime objects.
                                         If False, returns a list of date column names. Defaults to False.

    Returns:
        Union[list, pd.DataFrame]: A list of date column names or a DataFrame with date columns converted to datetime objects.

    Raises:
        ValueError: If the input is not a pandas DataFrame.
        TypeError: If the convert_dates parameter is not a boolean.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The first argument must be a pandas DataFrame.")

    if not isinstance(convert_dates, bool):
        raise TypeError("The second argument must be a boolean.")

    date_columns = []
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
        r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
        r'\d{2}/\d{2}/\d{2}',  # DD/MM/YY
        r'\d{2}-\d{2}-\d{2}',  # DD-MM-YY
        r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY
        r'\d{2}\.\d{2}\.\d{2}',  # DD.MM.YY
    ]

    for col in df.columns:
        unique_values = df[col].dropna().unique()

        if len(unique_values) == 0:
            continue

        sample_value = unique_values[0]

        for pattern in date_patterns:
            if re.match(pattern, str(sample_value)):
                date_columns.append(col)
                break  # no need to check other patterns if a match is found

    if convert_dates:
        df_copy = df.copy()
        df_copy[date_columns] = df_copy[date_columns].apply(pd.to_datetime, errors='coerce')
        return df_copy

    return date_columns


def indexing_groups(df: pd.DataFrame, date_columns: List[str]) -> pd.Series:
    """
    Generate a group index for a DataFrame based on multiple date columns using NaT.

    Usage:
    This function is manly used in Group Counseling Data.
    The function creates a mapping based on the first date column and then refines
    this mapping using subsequent date columns. NaN values in the final mapping are
    set to 0, which typically correspond to rows where all date columns have NaT.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the date columns.
    - date_columns (List[str]): List of date column names in df to be processed in the specified order.

    Returns:
    - pd.Series: A Series representing the group index for each row in df.

    Raises:
    - TypeError: If any of the inputs have an incorrect type.
    """

    # Type checking for input parameters
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected df to be of type pd.DataFrame, but got {type(df)}")
    if not isinstance(date_columns, list) or not all(isinstance(col, str) for col in date_columns):
        raise TypeError(f"Expected date_columns to be a list of strings, but got {type(date_columns)}")

    # Generate initial mapping based on unique dates from the first date column, excluding NaT
    primary_date_col = date_columns[0]
    unique_dates = df[~df[primary_date_col].isna()][primary_date_col].unique()
    sorted_dates = sorted(unique_dates)
    primary_mapping = {date: index + 1 for index, date in enumerate(sorted_dates)}

    # Map the initial date column to a group index series
    group_index_series = df[primary_date_col].map(primary_mapping).astype('Int64')

    # Refine the group index using the subsequent date columns
    for date_col in date_columns[1:]:
        valid_rows = (group_index_series.notna()) & (~df[date_col].isna())
        refinement_mapping = dict(zip(df[date_col][valid_rows], group_index_series[valid_rows]))

        missing_values = group_index_series.isna()
        group_index_series[missing_values] = df[date_col][missing_values].map(refinement_mapping)

    # Handle remaining NaN values, which correspond to NaT in all columns
    group_index_series[group_index_series.isna()] = 0

    return group_index_series


def melt_and_categorize_dates(input_df, date_columns, sort_by_date=False, var_name='', value_name=''):
    """
    This function processes the given dataframe by performing the following steps:
    1. Validate input and convert date columns to a datetime type.
    2. Melt the dataframe to transform date columns into a single column 'scdate'.
    3. Drop rows with NaT values in the 'scdate' column.
    4. Ensure 'sctype' is the 5th column and 'scdate' is the 6th column in the resulting dataframe.
    5. Optionally sort the resulting dataframe by the 'scdate' column.
    6. Verify that the number of non-null values in date columns before melting equals the number of rows
    in the resulting dataframe.

    Parameters:
    input_df (pd.DataFrame): The input dataframe.
    Date_columns (list): A list of date column names to process.
    Sort_by_date (bool, optional): Whether to sort the resulting dataframe by the 'scdate' column. Defaults to False.
    Var_name (str, optional): The name of the variable column. Defaults to 'sctype'.
    Value_name (str, optional): The name of the value column. Defaults to 'scdate'.
    Var_position (int, optional): The position of the variable column. Defaults to 5.
    Value_position (int, optional): The position of the value column. Defaults to 6.

    Returns:
    pd.DataFrame: The processed dataframe.
    """
    if not isinstance(input_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if not all(col in input_df.columns for col in date_columns):
        missing_cols = [col for col in date_columns if col not in input_df.columns]
        raise ValueError(f"Columns {missing_cols} not found in dataframe.")

    # Convert date columns to datetime type
    for date_column in date_columns:
        if not pd.api.types.is_datetime64_any_dtype(input_df[date_column]):
            input_df[date_column] = pd.to_datetime(input_df[date_column], errors='coerce')

    # Melt the dataframe to transform date columns into a single column 'scdate'.
    melted_df = pd.melt(input_df, id_vars=[col for col in input_df.columns if col not in date_columns],
                        value_vars=date_columns, var_name=var_name, value_name=value_name)

    # Drop rows with NaT values in the 'scdate' column
    melted_df.dropna(subset=[value_name], inplace=True)

    # Ensure 'sctype' is the var_position column and 'scdate' is the value_position column in the resulting dataframe
    columns = list(melted_df.columns)
    var_index = columns.index(var_name)
    value_index = columns.index(value_name)
    position1 = get_column_index(melted_df, 'fcid', 'rid') + 1
    position2 = position1 + 1
    columns.insert(position1, columns.pop(var_index))  # var_position column
    columns.insert(position2, columns.pop(value_index))  # value_position column
    melted_df = melted_df[columns]

    # Optionally sort the resulting dataframe by the 'scdate' column.
    if sort_by_date:
        melted_df.sort_values(by=value_name, inplace=True)
        melted_df.reset_index(drop=True, inplace=True)

    return melted_df


if __name__ == '__main__':
    pass
