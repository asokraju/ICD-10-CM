import pandas as pd
import requests
import zipfile
import os

os.makedirs('data', exist_ok=True)  # For the zip file
os.makedirs('data/data_2024', exist_ok=True)  # For the extracted files
os.makedirs('data/filtered', exist_ok=True)  # For the final filtered file

# Download and save the zip file
url = 'https://www.cms.gov/files/zip/rvu24b-updated-03/18/2024.zip'
save_path = os.path.join('data', '2024.zip')  # Use os.path.join for path concatenation
r = requests.get(url)
if r.status_code == 200:
    with open(save_path, 'wb') as f:
        f.write(r.content)
else:
    print("Failed to download the file. Status code:", r.status_code)
    exit()  # Stop the script if the file couldn't be downloaded

# Extract the zip file
folder_name_2024 = os.path.join('data', 'data_2024')
with zipfile.ZipFile(save_path, 'r') as zip_ref:
    zip_ref.extractall(folder_name_2024)

# Read the CSV file
data_2024_path = os.path.join(folder_name_2024, "PPRRVU24_APR.csv")

# Before proceeding, ensure the CSV file exists to avoid FileNotFoundError
if not os.path.exists(data_2024_path):
    print("The expected CSV file does not exist:", data_2024_path)
    exit()  # Stop the script if the CSV file doesn't exist

data_2024 = pd.read_csv(data_2024_path)

# Assuming the column headers are in the 9th row (index 8)
col_names = data_2024.iloc[8].to_numpy().tolist()  # Simplified version
df = data_2024.iloc[9:].reset_index(drop=True)
df.columns = col_names

# Filter for specific columns
cpt_codes = df[["HCPCS", "DESCRIPTION"]]

# Save the filtered data
filtered_save_path = os.path.join('data', 'filtered', 'cpt_codes_APR_2024.csv')
cpt_codes.to_csv(filtered_save_path, index=False)

print(cpt_codes.head(10))
