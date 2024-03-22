import pandas as pd


def filter_data(df, include=None, exclude=None):
    if include:
        for key, value in include.items():
            df = df[df[key].isin(value)]
    if exclude:
        for key, value in exclude.items():
            df = df[~df[key].isin(value)]
    return df

def aggregate_data(df, columns_to_groupby, columns_to_sum):
    df = df.groupby(columns_to_groupby)[columns_to_sum].sum()
    return df

def rename_columns(df, column_mapping):
    df = df.rename(columns=column_mapping)
    return df

def rename_values(df, rename_dict):
    """
    Renames values in a DataFrame based on a provided dictionary, with added checks
    for column existence.
    
    Parameters:
    - df: pandas.DataFrame to be modified.
    - rename_dict: Dictionary specifying rename operations in the form 
                   {column_name: {old_value: new_value}}, with a check for column existence.
                   
    Returns:
    - Modified DataFrame with values renamed according to rename_dict, if columns exist.
    """
    # Ensure the DataFrame is not modified in place
    df_modified = df.copy()
    
    # Iterate over the dictionary to replace values in the specified columns, with a check for column existence
    for column, replacements in rename_dict.items():
        if column in df_modified.columns:
            df_modified[column] = df_modified[column].replace(replacements)
        else:
            print(f"Column '{column}' does not exist in the DataFrame.")
        
    return df_modified


def diff_from(df, base_field: str, base_item: str):
    """
    Calculate the difference of each row in the dataframe (df) from a base row
    identified by a base item (base_item) within a base field (base_field).

    Args:
    df (pd.DataFrame): The dataframe to process.
    base_field (str): The name of the column (for MultiIndex) or the index name (for SingleIndex) 
                      used to identify the base row.
    base_item (str): The value within the base field or index to identify the base row.

    Returns:
    pd.DataFrame: A dataframe with the differences calculated.
    """
    # MultiIndex case: Original logic for MultiIndex structure
    if isinstance(df.index, pd.MultiIndex):
        idx_reference = [base_item in index for index in df.index]
        df_reference = df[idx_reference].droplevel(base_field)
        idx = [not i for i in idx_reference]
        df = df[idx].subtract(df_reference, axis = 1, fill_value=0)
    
    # SingleIndex case: Adapted logic for a single-level index
    else:
        # Check if the dataframe's index matches the base field for consistency
        if df.index.name == base_field:
            # Ensure the base item exists in the index
            if base_item in df.index:
                # Select the base row and perform subtraction for the other rows
                df_reference = df.loc[[base_item]]
                # Exclude the base row from the main dataframe
                df_filtered = df.drop(base_item)
                # Subtract the base row from the rest of the dataframe
                df = df_filtered.subtract(df_reference.squeeze(), axis=1)
            else:
                raise ValueError(f"Base item '{base_item}' not found in the index.")
        else:
            raise ValueError(f"Dataframe index ('{df.index.name}') does not match the base field ('{base_field}').")

    return df
