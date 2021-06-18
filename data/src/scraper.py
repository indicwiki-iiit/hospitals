import pandas as pd
import numpy as np

# Hospitals
NABH_URL = "https://www.nabh.co/frmViewAccreditedHosp.aspx"  # 746 entries
NABH_filename = "NABH_Accr_Hosp.xlsx"

# SHCO - Small HealthCare Organisations
SHCO_URL = "https://www.nabh.co/frmViewAccreditedSHCO.aspx"  # 354 entries
SHCO_filename = "NABH_Accr_SHCO.xlsx"

# Blood Bank / Blood Center
BloodBank_URL = "https://www.nabh.co/frmViewAccreditedBloodBank.aspx"  # 91 entries
BloodBank_filename = "NABH_Accr_BloodBank.xlsx"

# Blood Storage Center
BloodStorage_URL = (
    "https://www.nabh.co/frmViewAccreditedBloodStorageCentre.aspx"
)  # 1 entry
BloodStorage_filename = "NABH_Accr_BloodStorage.xlsx"

# MIS - Medical Imaging Services
MIS_URL = "https://www.nabh.co/MIS.aspx"  # 118 entries
MIS_filename = "NABH_Accr_MIS.xlsx"

# Dental HealthCare Service Providers
Dental_URL = "https://www.nabh.co/frmViewAccreditedDentalFacilities.aspx"  # 122 entries
Dental_filename = "NABH_Accr_Dental.xlsx"

# Allopathic Clinics
AlloClinic_URL = (
    "https://www.nabh.co/frmViewAccreditedAllopathicClinics.aspx"
)  # 33 entries
AlloClinic_filename = "NABH_Accr_AlloClinic.xlsx"

# Ayush Accredited Hospitals
Ayush_URL = "https://www.nabh.co/frmViewAccreditedAyushHosp.aspx"  # 106 entries
Ayush_filename = "NABH_Accr_Ayush.xlsx"

# Panchkarma clinic
Panchkarma_URL = "https://www.nabh.co/frmViewAccreditedPanchkarma.aspx"  # 21 entries
Panchkarma_filename = "NABH_Accr_Panchkarma.xlsx"

# Clinical Trial (Ethics Committees)
Ethics_Comm_URL = (
    "https://www.nabh.co/frmViewAccreditedClinicalTrial.aspx"
)  # 170 entries
Ethics_filename = "NABH_Accr_Ethics.xlsx"

# Eye Care Organisation
Eye_URL = "https://www.nabh.co/frmViewAccreditedEyeCare.aspx"  # 164 entries
Eye_filename = "NABH_Accr_Eye.xlsx"

# OST Centre - Oral Substitution Therapy
# No certificates available here - Only List of centers
OSTC_URL = "https://www.nabh.co/ostc-accredited.aspx"  # 51 entries
OSTC_filename = "NABH_Accr_OSTC.xlsx"

# PHC - Primary HealthCare
PHC_URL = "https://www.nabh.co/frmViewAccreditedPHC.aspx"  # 31 entries
PHC_filename = "NABH_Accr_PHC.xlsx"

# Wellness Centers
Wellness_URL = "https://www.nabh.co/frmViewAccreditedWellnessCentre.aspx"  # 4 entries
Wellness_filename = "NABH_Accr_Wellness.xlsx"

# IRCA - Rehabilitation Center
# No list available

# EMPANELMENT
CGHS_Ayush_URL = "https://www.nabh.co/cghs_Ayush.aspx"  # 44 entries
CGHS_Ayush_filename = "CGHS_AYUSH_QCI_Recommendation.xlsx"

URLS = [
    (NABH_URL, NABH_filename),
    (SHCO_URL, SHCO_filename),
    (Dental_URL, Dental_filename),
    (AlloClinic_URL, AlloClinic_filename),
    (Ayush_URL, Ayush_filename),
    (Panchkarma_URL, Panchkarma_filename),
    (Eye_URL, Eye_filename),
    (PHC_URL, PHC_filename),
]

online = False
merge = []
for given_url, given_filename in URLS:

    if online:
        tables = pd.read_html(given_url)
        hosp = tables[0]
    else:
        hosp = pd.read_excel(given_filename)

    caretype = given_filename.split("_")[-1]
    caretype = caretype.split(".")[0]
    if caretype == "Hosp":
        caretype = "Multi Speciality Hospital"
    elif caretype == "SHCO":
        caretype = "Small Healthcare Organization"
    elif caretype == "Dental":
        caretype = "Dental Healthcare Service Provider"
    elif caretype == "AlloClinic":
        caretype = "Allopathic Clinic"
    elif caretype == "Ayush":
        caretype = "AYUSH Hospital"
    elif caretype == "Panchkarma":
        caretype = "Panchakarma Ayurvedic Clinic"
    elif caretype == "Eye":
        caretype = "Eye Care Organization"
    elif caretype == "PHC":
        caretype = "Primary Healthcare Center"
    hosp["Caretype"] = caretype

    full_name = hosp["Name"]
    dist, state, country, name, city = [], [], [], [], []
    for h_name in full_name:
        b, c, d = h_name.split(",")[-3:]
        a = ",".join(h_name.split(",")[:-3])
        e = b
        if b == "Hyderabad":
            # district is medchal malkajgiri
            b = "Medchal-Malkajgiri"
            e = "Hyderabad"
        elif b == "West Godavari":
            # city is different.
            e = "Tadipallegudem"
        name.append(a)
        dist.append(b)
        state.append(c)
        country.append(d)
        city.append(e)
    hosp["District"] = np.asarray(dist)
    hosp["State"] = np.asarray(state)
    hosp["Country"] = np.asarray(country)
    hosp["Name"] = np.asarray(name)
    hosp["City"] = np.asarray(city)
    print(hosp.columns)
    merge.append(hosp.copy())

extra_compulsory_cols = ["Placetype", "Location", "Address", "Management"]
drop_cols = ["S.N.", "Reference No."]
extra_additional_cols = [
    "Systems",
    "Date_First",
    "Medical_College",
    "Established_Year",
    "Services",
    "Professions",
    "Website",
    "Lab_Services",
    "Diagnostic_Services",
    "Num_Staff",
    "Num_Beds",
    "Bloodbank",
    "Ambulance",
    "Pharmacy",
    "Other_Facilities",
]


result = pd.concat(merge)
result = result.rename(
    columns={"Acc. No.": "Code", "Valid From": "Valid_From", "Valid Upto": "Valid_Upto"}
)
result["Accredited"] = "False"  # This should be true actually
result.drop_duplicates(subset="Code")
result.drop(drop_cols, axis=1)
result[extra_compulsory_cols] = ""
result[extra_additional_cols] = ""

result.to_excel("../data/NABH_Accr_merge.xlsx")
print(len(result))

# If given filename is CSV, use the below snippet
# hosp_csv = hosp.to_csv(index=False)
# csv_file = open('NABH_Accr_Hosp.csv',"w+")
# csv_file.write(hosp_csv)
# csv_file.close()

# Merge datasets; adding caretype and accredited == True ; systems also
# Pdf scraping
