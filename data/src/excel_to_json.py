import pandas as pd
import numpy as np

filename = "../data/NABH_Accr_merge_cert.xlsx"
accr_hosp = pd.read_excel(filename)
cols = [
    "Services",
    "Professions",
    "Lab_Services",
    "Diagnostic_Services",
    "Other_Facilities",
]
for col in cols:
    accr_hosp[col] = accr_hosp[col].replace(np.nan, "")
    accr_hosp[col] = accr_hosp[col].astype(str)
    accr_hosp[col] = [x.split(",") if x != "" else [] for x in accr_hosp[col].tolist()]

print(accr_hosp.columns)
accr_hosp["Established_Year"] = accr_hosp["Established_Year"].replace(np.nan, 0)
accr_hosp["Established_Year"] = accr_hosp["Established_Year"].astype(int)

accr_hosp["Num_Staff"] = accr_hosp["Num_Staff"].replace(np.nan, -1)
accr_hosp["Num_Staff"] = accr_hosp["Num_Staff"].astype(int)

accr_hosp["Num_Beds"] = accr_hosp["Num_Beds"].replace(np.nan, -1)
accr_hosp["Num_Beds"] = accr_hosp["Num_Beds"].astype(int)

accr_hosp = accr_hosp[accr_hosp["Accredited"] == True]
print(len(accr_hosp))
json_file = "../data/NABH_Accr_merge_cert.json"
accr_hosp.to_json(json_file, orient="records")
