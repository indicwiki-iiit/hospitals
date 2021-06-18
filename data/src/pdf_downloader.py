from urllib.request import urlretrieve
import pandas as pd

incorrect_files_count = 0


def download_file(download_code, url):
    global incorrect_files_count
    download_url = (
        "https://www.nabh.co/Documents/AccreditedList/"
        + url
        + "/"
        + download_code
        + ".pdf"
    )
    download_file = "../pdfs/" + download_code + ".pdf"
    print(download_url)
    try:
        urlretrieve(download_url, download_file)
        print("Completed")
    except Exception as error:
        print("Exception Occured")
        print(type(error))
        print(error)
        incorrect_files_count += 1


filename = "../data/NABH_Accr_merge.xlsx"
accr_hosp = pd.read_excel(filename)
folder = {
    "Multi Speciality Hospital": "Hospitals",
    "Eye Care Organization": "Eye%20Care%20Organisation",
    "Small Healthcare Organization": "SHCO",
    "Dental Healthcare Service Provider": "Dental%20Facilities",
    "Allopathic Clinic": "Allopathic%20Clinics",
    "AYUSH Hospital": "AYUSH%20Hospitals",
    "Panchakarma Ayurvedic Clinic": "Panchakarma%20Clinics",
    "Primary Healthcare Center": "PHC",
}
for index, entry in accr_hosp.iterrows():
    caretype = entry["Caretype"]
    code = entry["Code"]
    url = folder[caretype]
    if url in [
        "PHC",
        "Hospitals",
        "SHCO",
    ]:  # This is because certificates are not  available for PHCS
        incorrect_files_count += 1
        continue
    download_file(code, url)

print(incorrect_files_count)
