import pandas as pd
import numpy as np
from typing import Tuple

# This function is used to process the ICD-10-CM codes to split them into their components.
# It handles cases where the code has a special character or additional digits beyond the standard format.
def split_condition(code: str) -> Tuple[str, str]:
    """
    Splits the ICD-10-CM code into its components based on its length and character composition.
    
    Parameters:
    - code (str): The ICD-10-CM code as a string.
    
    Returns:
    - Tuple[str, str]: A tuple containing the special character (if any) and the numeric component after the first three characters.
    """
    if len(code) > 3:
        if code[-1].isalpha():
            return code[3:-1], code[-1]
        else:
            return code[3:], np.nan
    else:
        return np.nan, np.nan

if __name__ == "__main__":
    # Path to the ICD-10-CM codes file
    file_path = r'data\icd10cm_order_2024.txt'
    
    # Define the widths of the columns in the fixed-width file
    col_widths = [6, 8, 2, 61, 1000]  # Column widths as specified in the file format
    col_names = ['Index', 'Code', 'Unused', 'Description_short', 'Description_full']  # Column names for the DataFrame

    # Reading the fixed-width formatted file
    df = pd.read_fwf(file_path, widths=col_widths, header=None, names=col_names)
    
    # Setting the 'Index' column as the DataFrame index
    df = df.set_index("Index")
    
    # Adding a column for the ICD-10-CM code with a dot inserted for readability
    df['icd_Code_with_dot'] = df['Code'].apply(lambda x: x[:3] + '.' + x[3:])
    
    # Splitting the 'Code' column into its constituent parts for further analysis
    df['icd_1'] = df['Code'].str[0]  # The first character
    df['icd_2'] = df['Code'].str[1:3]  # The next two characters
    
    # Applying the split_condition function to each code to separate out any special characters and additional components
    df[['icd_3', 'icd_4']] = df.apply(lambda row: pd.Series(split_condition(row['Code'])), axis=1)

    # Save the DataFrame to a CSV file
    csv_file_path = r'data\filtered\icd10cm_order_csv_2024.csv'
    df.to_csv(csv_file_path, index=False)
    a, b, c, d = df.icd_1.unique().shape[0], df.icd_2.unique().shape[0], df.icd_3.unique().shape[0], df.icd_4.unique().shape[0]
    print(f"Unique values summary:\n"
      f"- first character: {a} unique values\n"
      f"- next two numbers: {b} unique values\n"
      f"- middle component: {c} unique values\n"
      f"- last characters: {d} unique values\n"
      f" - Total unique values: {a + b + c + d}")
    # Optionally, print a message to confirm the file has been saved
    print(f"ICD-10-CM codes and descriptions saved to CSV at: {csv_file_path}")


    """"
    Unique values summary:
    - first character: 26 unique values
    - next two numbers: 107 unique values
    - middle component: 2814 unique values
    - last characters: 18 unique values
    - Total unique values: 2965
    """