import pdfplumber
import re
import pandas as pd
from typing import List, Dict

"""
The regular expression re.compile(r'([A-Z][0-9]{2}\.[0-9A-Za-z]+)([^\n\r]*)') is designed to match and extract ICD-10-CM codes and their descriptions from a string. The pattern is broken down as follows:
    ([A-Z][0-9]{2}\.[0-9A-Za-z]+):
        `([A-Z]`: This part matches exactly one uppercase letter from A to Z at the beginning of the ICD-10-CM code.
        `[0-9]{2}`: This matches exactly two digits, representing the category of the disease or condition in the ICD-10-CM code.
        `.`: This matches the literal dot (.) character that separates the category of the disease from its etiology, anatomical site, or severity.
        `[0-9A-Za-z]+)`: This part matches one or more alphanumeric characters (digits or letters), which further specify the disease or condition.
        `[^\n\r]*`: This matches any sequence of characters except for newline (\n) and carriage return (\r) characters. It's designed to capture the rest of the line after the ICD-10-CM code, which typically includes the description of the code.
"""
def preprocess_text(text: str) -> List[str]:
    """
    Preprocesses the given text to consolidate lines related to the same ICD-10-CM code.

    The function identifies lines that start with a new ICD-10-CM code and consolidates any
    subsequent lines that belong to the same code until a new code starts.

    Parameters:
    - text (str): The raw text containing ICD-10-CM codes and their descriptions, separated by new lines.

    Returns:
    - List[str]: A list of processed lines, where each line contains an ICD-10-CM code followed by its description.
    """
    # Split the text into individual lines
    lines = text.split('\n')

    # Initialize a list to hold the processed lines
    processed_lines = []
    # Initialize a string to accumulate the current line's content
    current_line = ''

    # Define a regular expression to identify lines that start with an ICD-10-CM code
    code_start_pattern = re.compile(r'^[A-Z][0-9]{2}\.[0-9A-Za-z]')

    for line in lines:
        if code_start_pattern.match(line):
            # If the line starts with a code, it's a new entry. Save the current entry and start a new one.
            if current_line:
                processed_lines.append(current_line)
            current_line = line
        else:
            # If the line doesn't start with a code, it's a continuation of the current entry.
            current_line += ' ' + line.strip()  # Append the line, removing leading/trailing whitespace

    # Add the last processed entry to the list
    processed_lines.append(current_line)

    return processed_lines

def extract_icd_codes(processed_lines: List[str]) -> List[Dict[str, str]]:
    """
    Extracts ICD-10-CM codes and their descriptions from a list of processed lines.

    Each line in the input list is expected to start with an ICD-10-CM code, followed by its description.
    The function uses regular expressions to identify and extract these components.

    Parameters:
    - processed_lines (List[str]): A list of processed lines, where each line contains an ICD-10-CM code followed by its description.

    Returns:
    - List[Dict[str, str]]: A list of dictionaries, each containing 'code' and 'description' keys for an ICD-10-CM entry.
    """
    # Define a regular expression pattern to match ICD-10-CM codes and their descriptions
    pattern = re.compile(r'([A-Z][0-9]{2}\.[0-9A-Za-z]+)([^\n\r]*)')

    # Initialize a list to store the extracted codes and descriptions
    icd_codes = []

    for line in processed_lines:
        match = pattern.match(line)
        if match:
            # For each match, add a dictionary with the code and its description to the list
            icd_codes.append({'code': match.group(1), 'description': match.group(2).strip()})

    return icd_codes






if __name__ == "__main__":
    # Specify the path to the ICD-10-CM PDF file
    pdf_path = r'C:\Users\Kosaraju\Documents\GitHub\ICD-10-CM\data\ICD-10-CMS.pdf'

    # Initialize an empty list to hold all the extracted ICD codes
    all_codes = []

    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through each page in the PDF
        for page in pdf.pages:
            # Extract text from the current page
            text = page.extract_text()
            # Preprocess the extracted text to consolidate related lines
            processed_lines = preprocess_text(text)
            # Extract ICD codes and their descriptions from the processed lines
            all_codes.extend(extract_icd_codes(processed_lines))

    # Convert the list of code dictionaries to a pandas DataFrame
    icd_codes_df = pd.DataFrame(all_codes)

    # Save the DataFrame to a CSV file
    csv_path = r'C:\Users\Kosaraju\Documents\GitHub\ICD-10-CM\data\ICD-10-CM_codes.csv'
    icd_codes_df.to_csv(csv_path, index=False)

    # Optionally, print a confirmation message
    print(f"ICD-10-CM codes and descriptions saved to CSV at: {csv_path}")