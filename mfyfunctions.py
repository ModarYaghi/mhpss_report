from io import BytesIO
import msoffcrypto
import numpy as np
from numpy import ndarray, dtype
import os
import pandas as pd
from pandas import DataFrame, Series
from typing import Any, Dict, Callable, List, Optional, Union



def read_encrypted_excels(
        directory: str,
        password_dict: Dict[str, str]
) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Reads encrypted Excel files from a directory using a dictionary of filenames and passwords.

    Args:
    - directory (str): The directory containing the encrypted Excel files.
    - password_dict (dict): A dictionary where keys are filenames and values are passwords.

    Returns:
    - dict: A dictionary where the keys are filenames and the values are another dictionary where keys are
            sheet names and values are DataFrames of the sheet content.

    Errors:
    - Raises specific error messages for file not found, decryption failure, and reading sheet failure.
    """

    # Calculate total number of sheets for the progress bar
    total_sheets = 0
    for file, password in password_dict.items():
        file_path = os.path.join(directory, file)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                crypto = msoffcrypto.OfficeFile(f)
                crypto.load_key(password=password)

                decrypted_file = BytesIO()
                crypto.decrypt(decrypted_file)
                decrypted_file.seek(0)

                xls = pd.ExcelFile(decrypted_file)
                total_sheets += len(xls.sheet_names)

    print(f"Processing {total_sheets} sheets across all files:")

    result = {}
    for file, password in password_dict.items():
        file_path = os.path.join(directory, file)

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist. Skipping...")
            continue

        try:
            with open(file_path, "rb") as f:
                crypto = msoffcrypto.OfficeFile(f)
                crypto.load_key(password=password)

                decrypted_file = BytesIO()
                crypto.decrypt(decrypted_file)
                decrypted_file.seek(0)  # Reset file pointer to the beginning

                xls = pd.ExcelFile(decrypted_file)
                sheets = {}
                for sheet_name in xls.sheet_names:
                    try:
                        sheets[sheet_name] = pd.read_excel(xls, sheet_name, engine='openpyxl')
                        print('#', end='', flush=True)  # Progress bar update
                    except Exception as e:
                        print(f"\nError reading sheet {sheet_name} from file {file_path}. Error message: {e}")

                result[file] = sheets
        except msoffcrypto.exceptions.DecryptionError:
            print(f"\nDecryption error for file {file_path}. Possibly incorrect password.")
        except Exception as e:
            print(f"\nError processing file {file_path}. Error message: {e}")

    # Erase the progress bar
    print("\r" + " " * total_sheets, end='', flush=True)
    print("\r", end='', flush=True)

    # Print the structure of the result
    print("Processed files and sheets:")
    for file, sheets in result.items():
        print(f"- {file}: {', '.join(sheets.keys())}")

    return result


def intake_validate(nt1, nt2, nt3, ntre):
    """
    Purpose:
        The service_code function categorizes service instances into distinct codes based on
        the logical and temporal relationship among four potential date entries.
        These date entries indicate different sessions or stages in service provision.
    Parameters:
        nt1: First date (string or datetime-like object). The start date of the service.
        nt2: Second date (string or datetime-like objects). The completion date of the initial service.
        nt3: Third date (string or datetime-like objects). The date of a follow-up or additional session if applicable.
        ntre: Fourth date (string or datetime-like objects).
            The date of a repeated or additional service session if applicable.

    Returns:
        An integer code indicating the status or category of the service based on the input dates.

    Encoding Scheme:
        -1: Service Started but Not Completed. Only D1 is provided.
        1: Valid Service. D1 and D2 are provided with D2 > D1.
        2: Three Session Service. D1, D2, and D3 are provided with D3 > D2 > D1.
        3: Repeated Service. D1, D2, and D4 are provided with D4 > D2 > D1, and if D3 is provided, D4 > D3.
        0: Data Entry Error. Any other combinations or date arrangements that do not adhere to the above criteria,
        indicating possible data entry issues.
    """

    try:
        # Convert dates, handle NaN/NaT properly
        d1 = pd.Timestamp(nt1) if pd.notna(nt1) else None
        d2 = pd.Timestamp(nt2) if pd.notna(nt2) else None
        d3 = pd.Timestamp(nt3) if pd.notna(nt3) else None
        d4 = pd.Timestamp(ntre) if pd.notna(ntre) else None

        # Service Started but Not Completed
        if d1 and not d2 and not d3 and not d4:
            return -1
        # Valid Service
        elif d1 and d2 and not d3 and not d4 and d2 > d1:
            return 1
        # Three Session Service
        elif d1 and d2 and d3 and not d4 and d3 > d2 > d1:
            return 2
        # Repeated Service
        elif d1 and d2 and d4 and d4 > d2 > d1 and (not d3 or (d3 and d4 > d3)):
            return 3
        # Data Entry Error
        else:
            return 0
    except ValueError as ve:
        print(f"Value Error: {ve}. Check your date formats.")
        return None
    except TypeError as te:
        print(f"Type Error: {te}. Ensure inputs are date-like or strings that can be converted to dates.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}.")
        return None


def create_binary_pattern(
        input_dataframe: pd.DataFrame,
        first_column: str,
        last_column: str,
        binary_codes: Optional[Dict[str, str]] = None,
        agg_func: Optional[Callable] = ''.join
) -> pd.Series:
    """
    ...

    Create a binary sequence based on the comparison of dates within a subset of DataFrame columns.

    The function generates a binary sequence for each row in the DataFrame based on the following rules:
    - '1' if the date in the current column is greater than the date in the previous column and not NaN.
    - '0' otherwise.
    Special cases:
    - If the first date is NaN and any of the subsequent dates is not NaN, return '-1'.
    - If the third date is present and the second date is NaN, return '-1'.

    Parameters:
    - input_dataframe (pd.DataFrame): The input DataFrame containing the date columns to compare.
    - first_column (str): The name of the first column in the subset of columns to compare.
    - last_column (str): The name of the last column in the subset of columns to compare.
    - binary_codes (dict, optional): A dictionary containing custom binary codes for different conditions.
                                     Default: {
                                        'greater_than_previous_and_notna': '1',
                                        'else': '0',
                                        'first_col_notna': '1',
                                        'first_col_na': '0'
                                     }
    - agg_func (callable, optional): A function that aggregates the binary values.
                                     Default is ''.join, which concatenates the binary strings.

    Returns:
    - pd.Series: A Pandas' Series containing the binary sequence for each row in the input DataFrame.

    Example:
    # >>> df = pd.DataFrame({
    # ...     'date1': ['2021-01-01', np. nan, '2021-01-03'],
    # ...     'date2': ['2021-01-02', '2021-01-02', np. nan],
    # ...     'date3': ['2021-01-03', '2021-01-03', '2021-01-01']
    # ... })
    # >>> df['binary_seq'] = create_binary_pattern(df, 'date1', 'date3')
    #        date1      date2      date3 binary_seq
    # 0 2021-01-01 2021-01-02 2021-01-03        111
    # 1        NaT 2021-01-02 2021-01-03         -1
    # 2 2021-01-03        NaT 2021-01-01         -1

    ...
    """
    if binary_codes is None:
        binary_codes = {
            'greater_than_previous_and_notna': '1',
            'else': '0',
            'first_col_notna': '1',
            'first_col_na': '0'
        }

    start_idx = input_dataframe.columns.get_loc(first_column)
    end_idx = input_dataframe.columns.get_loc(last_column) + 1

    column_subset = input_dataframe.iloc[:, start_idx:end_idx]

    # Handle special conditions: return -1 if the first date is NaN, and any subsequent dates are not NaN
    # or if the third date is present while the second one is not
    mask_invalid = (
                           column_subset.iloc[:, 0].isna() & column_subset.iloc[:, 1:].notna().any(axis=1)
                   ) | (
                           column_subset.iloc[:, 2].notna() & column_subset.iloc[:, 1].isna()
                   )

    binary_values = (
            (column_subset > column_subset.shift(axis=1)) & ~column_subset.isna()
    ).astype(int).astype(str).replace({'1': binary_codes['greater_than_previous_and_notna'],
                                       '0': binary_codes['else']})

    binary_values.iloc[:, 0] = (~column_subset.iloc[:, 0].isna()
                                ).astype(int).astype(str).replace({'1': binary_codes['first_col_notna'],
                                                                   '0': binary_codes['first_col_na']})

    binary_sequence = binary_values.agg(agg_func, axis=1)
    binary_sequence[mask_invalid] = '-1'

    return binary_sequence


# The compare_date_columns() funtion used to deal with TD consultation and consent sessions dates
def compare_date_columns(
        dataframe: DataFrame,
        first_column: str,
        second_column: str
) -> ndarray:
    """
    Compare two date columns in a DataFrame and return a binary representation for their relationship.

    Parameters:
        :param dataframe: The DataFrame containing the columns to compare.
        :param first_column: The name of the first column to compare.
        :param second_column: The name of the second column to compare.

    Returns:
        ndarray: A NumPy ndarray of shape (n), where n is the number of rows in the dataframe.
                 Each element of the array is a string representing the binary relationship
                 between the corresponding dates in the input columns, according to the following code:

                     - '000': Both dates are NaN.
                     - '011': Both dates are the same and not NaN.
                     - '010': First date is NaN, second date is not.
                     - '001': Second date is NaN, first date is not.
                     - '101': Dates are different and neither is NaN.

                 The dtype of the returned ndarray is a string.
                 Note that operations on this
                 ndarray will use NumPy functionality, and if Pandas functionality is desired,
                 you may convert it to a Pandas' Series object.

    Raises:
        ValueError: If the provided columns are not found in the DataFrame or are not datetime dtype.
    """
    # Error handling for non-existent columns
    for col in [first_column, second_column]:
        if col not in dataframe.columns:
            raise ValueError(f"Column {col} not found in DataFrame.")

    # Type checking and handling for non-datetime columns
    if not pd.api.types.is_datetime64_any_dtype(dataframe[first_column]) or \
            not pd.api.types.is_datetime64_any_dtype(dataframe[second_column]):
        raise ValueError("Both columns should be of datetime dtype.")

    conditions = [
        pd.isna(dataframe[first_column]) & pd.isna(dataframe[second_column]),
        (dataframe[first_column] == dataframe[second_column]) & \
        ~pd.isna(dataframe[first_column]) & ~pd.isna(dataframe[second_column]),
        pd.isna(dataframe[first_column]) & ~pd.isna(dataframe[second_column]),
        ~pd.isna(dataframe[first_column]) & pd.isna(dataframe[second_column])
    ]

    binary_choices = ['000', '011', '010', '001']

    return np.select(conditions, binary_choices, default='101')


def validate_records(df: pd.DataFrame,
                     key: Union[str, int],
                     date_columns: List[str]) -> pd.DataFrame:
    """
    Validate records in a dataframe based on specified date columns and a unique key.

    Usage:
    Used mainly with Screening.

    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - key (str): The column name that acts as the unique identifier.
    - Date_columns (List[str]): A list of column names that represent session dates.

    Returns:
    - pd.DataFrame: A dataframe with warnings or an empty dataframe if no issues are found.
    """

    # Ensure the provided columns exist in the dataframe
    if key not in df.columns:
        raise ValueError(f"The key '{key}' is not found in the dataframe columns.")
    for col in date_columns:
        if col not in df.columns:
            raise ValueError(f"The date column '{col}' is not found in the dataframe columns.")

    # Create a mask for valid dates
    valid_dates_masks = df[date_columns].notna()

    # Group by the key and count valid dates for each date column
    valid_counts = valid_dates_masks.groupby(df[key]).sum()

    # Identify keys that have more than one valid date for any date column
    duplicate_sessions = valid_counts[valid_counts > 1].dropna(how='all').index

    # Check for Excess Records
    record_counts = df[key].value_counts()
    excess_records = record_counts[record_counts > len(date_columns)].index

    # Combine all keys that triggered warnings
    all_warning_keys = duplicate_sessions.union(excess_records)

    # Filter the original dataframe for these keys
    warnings_df = df[df[key].isin(all_warning_keys)].copy()

    # Annotate with a warning message
    warnings_df['warning'] = np.where(warnings_df[key].isin(duplicate_sessions),
                                      'Multiple records for the same session type',
                                      f'More than {len(date_columns)} records')

    return warnings_df


def repeated_client_indicator(df: pd.DataFrame, client_id: str, service_index: str) -> pd.Series:
    """
    Generate an indicator for repeated client IDs and their associated service indices.

   Usage:
    This function is mainly used in Group Counseling Data.
    Indicating clients that participated in more than one group.
    Indicator is the number of occurrences with the groups' indices where the occurrences happened.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - client_col (str): Name of the column containing client IDs.
    - Service_col (str): Name of the column containing service indices.

    Returns:
    pd.Series: A Series containing the generated indicator.
    """
    # Validate input column names
    if client_id not in df.columns or service_index not in df.columns:
        raise ValueError("Specified column names must exist in the DataFrame.")

    # Validate data types of specified columns
    if not pd.api.types.is_integer_dtype(df[client_id]) and not pd.api.types.is_integer_na_dtype(df[client_id]):
        raise TypeError(f"{client_id} must have integer (or Int64) data type.")
    if not pd.api.types.is_integer_dtype(df[service_index]) and not pd.api.types.is_integer_na_dtype(df[service_index]):
        raise TypeError(f"{service_index} must have integer (or Int64) data type.")

    # Ensure no NaN values in the specified columns for reliable calculations
    if df[client_id].isna().any() or df[service_index].isna().any():
        raise ValueError("Columns used for indicator calculation should not contain NaN values.")

    # Count the number of occurrences regarding each client_id
    df['id_count'] = df.groupby(client_id)[client_id].transform('count')

    # Generate a string with the other service indices
    def other_indices(row: pd.Series) -> str:
        other_rows = df[(df[client_id] == row[client_id]) & (df[service_index] != row[service_index])]
        return ''.join([f"{idx:02d}" for idx in other_rows[service_index]])

    df['other_indices'] = df.apply(other_indices, axis=1)

    # Combine the count and the other_indices string, and convert to integer
    df['indicator'] = (df['id_count'].astype(str) + df['other_indices']).astype(int)

    # Drop temporary columns used for calculations
    df = df.drop(columns=['id_count', 'other_indices'])

    return df['indicator']


if __name__ == "__main__":
    # Code to run when this module is executed directly goes here
    # For now, it's just a placeholder
    pass
