import pandas as pd
import files as uFiles

from typing import Optional, Any, Dict

def load_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """
    Loads a CSV file into a Pandas DataFrame.

    Args:
        filepath (str): The path of the CSV file to load.
        **kwargs: Additional keyword arguments to pass to pd.read_csv.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the CSV file.

    Raises:
        Exception: If an error occurred while loading the CSV file.
    """
    try:
        df = pd.read_csv(filepath, **kwargs)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")


def load_multiple_csvs(folder_path: str, **kwargs) -> pd.DataFrame:
    """
    Loads multiple CSV files into a Pandas DataFrame and keeps only the common data columns.

    Args:
        folder_path (str): The path of the folder containing the CSV files.
        **kwargs: Additional keyword arguments to pass to pd.read_csv.

    Returns:
        pd.DataFrame: A DataFrame containing the common data columns from all CSV files.
    """
    files = uFiles.search_files(type='csv', location=folder_path)
    
    # Load the first CSV file into a DataFrame and capitalise column names
    df = load_csv(files[0], **kwargs)
    df.columns = df.columns.str.upper()
    
    # Loop through the remaining CSV files and keep only the common columns
    for f in files[1:]:
        df_next = load_csv(f, **kwargs)
        columns_next = df_next.columns.upper().to_list()
        
        # Get the common columns between the two DataFrames
        common_columns = df.columns.intersection(columns_next)
        
        # Concatenate the two DataFrames using only the common columns
        df = pd.concat([df[common_columns], df_next[common_columns]], ignore_index=True)
    
    return df


def save_as_csv(df: pd.DataFrame, filename: str, location: Optional[str] = None, **kwargs) -> None:
    """
    Saves a Pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        filename (str): The name of the CSV file.
        location (str, optional): The directory where the CSV file will be saved. Defaults to the current directory.
        **kwargs: Additional keyword arguments to pass to pd.to_csv

    Raises:
        Exception: If an error occurred while saving the DataFrame.
    """
    try:
        # If a location is provided, join it with the filename
        if location:
            filepath = f'{location}/{filename}'
            # Create folder if not exists
            uFiles.mkdir(location)
        else:
            filepath = filename

        # Save the DataFrame to a CSV file
        df.to_csv(filepath, **kwargs)
    except Exception as e:
        print(f"An error occurred: {e}")


def replace_value(df: pd.DataFrame, column_name: str, another_column: str, old_value: Any, new_value: Any) -> pd.DataFrame:
    """
    Replaces a value in one column based on the value in another column.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        column_name (str): The name of the column to replace values in.
        another_column (str): The name of the column to check values in.
        old_value (Any): The value to replace.
        new_value (Any): The value to replace with.

    Returns:
        pd.DataFrame: The modified DataFrame.
    """
    # Check if the value in 'another_column' is 123
    mask = df[another_column] == 123
    
    # Access the cells in 'column_name' where the mask is True
    # Replace 'old_value' with 'new_value' in these cells
    df.loc[mask, column_name] = df.loc[mask, column_name].replace(old_value, new_value)

    return df


def replace_values(df: pd.DataFrame, replace_column: str, old_value: Any, new_value: Any, column_value_dict: Optional[Dict[str, Any]] = None, **kwargs) -> pd.DataFrame:
    """
    Replaces values in a specified column based on a mask created from a dictionary of column-value pairs.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        replace_column (str): The name of the column to replace values in.
        old_value (Any): The value to replace.
        new_value (Any): The value to replace with.
        column_value_dict (Optional[Dict[str, Any]]): A dictionary where the keys are column names and the values are the values to check. Defaults to None.
        **kwargs: Additional keyword arguments to pass to pd.DataFrame.replace

    Returns:
        pd.DataFrame: The modified DataFrame.

    >>> data = {'column1': [123, 234], 'column2': [456, 567], 'replace_column': ['old_value', 'other_value']}
    >>> df = pd.DataFrame(data)
    >>> replace_values(df, 'replace_column', 'old_value', 'new_value', {'column1': 123})
       column1  column2 replace_column
    0      123      456      new_value
    1      234      567    other_value
    """
    # If column_value_dict is not None, create the mask and replace values
    if column_value_dict:
        # Initialize an empty mask with the same length as the DataFrame
        mask = pd.Series([False]*len(df))

        # Iterate over the dictionary
        for column, value in column_value_dict.items():
            # For each column-value pair, create a mask where each element is True if the corresponding cell in the column is equal to the value
            # Combine this mask with the existing mask using a logical OR
            mask = mask | (df[column] == value)

        # Use the mask to replace values in the specified column
        df.loc[mask, replace_column] = df.loc[mask, replace_column].replace(old_value, new_value, **kwargs)
    else:
        # If column_value_dict is None, replace values in the specified column without creating a mask
        df[replace_column] = df[replace_column].replace(old_value, new_value)
    
    return df


