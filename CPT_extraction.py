# source 
# https://www.cms.gov/medicare/medicare-fee-service-payment/physicianfeesched/pfs-relative-value-files/rvu23d
# https://www.cms.gov/medicare/payment/fee-schedules/physician/pfs-relative-value-files/rvu24b
# https://www.reddit.com/r/datasets/comments/d3mbev/hcpcs_level_i_cpt_codes_full_list/

import pandas as pd
import requests
import zipfile

# path_2023 = "https://www.cms.gov/files/zip/rvu23d.zip"
fname = "2024.zip"
url = 'https://www.cms.gov/files/zip/rvu24b-updated-03/18/' + fname
r = requests.get(url)
with open(fname, 'wb') as f:
    f.write(r.content)

folder_name_2024 = "data_2024"
with zipfile.ZipFile(fname, 'r') as zip_ref:
    zip_ref.extractall(folder_name_2024)

data_2024_path = folder_name_2024 + "/PPRRVU24_APR.csv"

data_2024 = pd.read_csv(data_2024_path)

print(data_2024.head())


# cols_all = data_2024.iloc[8].tolist()
# data_2024.columns = cols_all
df = data_2024.iloc[9:].reset_index(drop=True)
cpt_codes = df[["HCPCS", "DESCRIPTION"]]
cpt_codes.to_csv("cpt_codes_APR_2024.csv", index=False)