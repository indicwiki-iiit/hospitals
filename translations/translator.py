import json
from google_trans_new import google_translator
import csv
import time
import sys
import os, pandas as pd

months_trans = {
    'january':'జనవరి', 'february':'ఫిబ్రవరి','march':'మార్చి','april': 'ఏప్రిల్',
    'may':'మే', 'june': 'జూన్','july': 'జూలై',    'august': 'ఆగస్టు', 'september': 'సెప్టెంబర్',
    'october': 'అక్టోబర్','november': 'నవంబర్','december': 'డిసెంబర్'
    }
caretype_trans = {
    'multi speciality hospital':'మల్టీస్పెషాలిటీ హాస్పిటల్',
    'small healthcare organization':'చిన్న ఆరోగ్య సంరక్షణ సంస్థ (SHCO)',
    'dental healthcare service provider':'దంత ఆరోగ్య సేవా కేంద్రం',
    'allopathic clinic':'అల్లోపతి క్లినిక్',
    'ayush hospital':'ఆయుష్ హాస్పిటల్ (AYUSH)',
    'panchakarma ayurvedic clinic':'పంచకర్మ క్లినిక్',
    'eye care organization': 'కంటి సంరక్షణ సంస్థ',
    'primary healthcare center':'ప్రాథమిక ఆరోగ్య కేంద్రం (PHC)',
    }
management_trans = {
    'public': 'ప్రభుత్వ',
    'private': 'ప్రైవేటు',
    'government': 'ప్రభుత్వ'}
systems_trans = {
    'allopathy':'అల్లోపతి',
    'homeopathy':'హోమియోపతి',
    'siddha':'సిద్ధ',
    'ayurvedic':'ఆయుర్వేద',
    'ayurveda':'ఆయుర్వేద',
    'unani':'యునాని'}
placetype_trans = {
    'city' : 'నగరం',
    'town' : 'పట్టణం',
    'village' :'గ్రామం',
}
trans= { **months_trans , **caretype_trans , **management_trans , **systems_trans, **placetype_trans }

acronym = ['ఏ','బీ', 'సీ', 'డీ', 'ఈ' ,'ఎఫ్', 'జీ', 'ఎచ్', 'ఐ', 'జె',
'కే', 'ఎల్', 'ఎమ్', 'ఎన్' ,'ఓ' ,'పీ' ,'క్యూ' ,'ఆర్', 'ఎస్', 'టీ', 'యూ', 'వీ', 'డబ్ల్యు', 'ఎక్స్' ,'వై' ,'జెడ్' ]
def hardcode(record):
    cols = ['Valid_From','Valid_Upto','Date_First']
    for col in cols:
        if col not in record:
            print('hardcode')
            print(record)
            print(col,record['Code']), exit()
        if record[col] is None or type(record[col]) != str or record[col] == 'None':
            continue
        try : 
            try :         month_date , year = record[col].split(',')
            except: month_date, year = record[col].split('.')
            month, date = month_date.split(' ')
        except: month, date, year = record[col].split()
    
        if not month.isalnum(): continue
        try  :       record[col] = trans[month.lower()]+' '+date+', '+year    
        except : print('month',month.lower()),print(col, record), exit()
       
    cols = ['Caretype','Management','Systems','Placetype']
    for col in cols:
        if record[col] is None or record[col] == '' or record[col] == 'None' : 
            continue
        if type(record[col]) != str or record[col].strip().lower() not in trans:
            #There has to be a typo => please check
            print('Typo:',record[col], type(record[col]))
            continue
        record[col] = trans[record[col].strip().lower()]

    return record

def telugu_acronym(text):
    telugu_text = ''
    for c in text.lower():
        if ord(c) >= ord('a') and ord(c) <= ord('z'):
            index = ord(c)-ord('a')
            telugu_text+=acronym[index]
        else:
            telugu_text+=c

    return telugu_text

exceptions = {
    'critical care' : 'క్లిష్టమైన సంరక్షణ',
    'x-ray' : 'ఎక్స్-రే',
    'ndmc':'ఎన్.డీ.ఎమ్.సీ (NDMC)',
    'door' : 'తలుపు',
    'plot' : 'ప్లాట్',
    'polysomnography (psg)' : 'పాలిసోమ్నోగ్రఫీ (PSG)',
    'garkheda' : 'గార్ఖేదా',
    'ophthalmology':'ఆప్తాల్మాలజీ',
    'opthalmology':'ఆప్తాల్మాలజీ',
    'boincheruvupalli': 'బోయిన్ చెరువుపల్లి',
    'mellacheruvu':'మెల్ల చెరువు',
    'pragnya' :'ప్రజ్ఞ',
    'mahindra world city':'మహీంద్రా వరల్డ్ సిటీ',
    'pragnya priya foundation (non-profit)' : 'ప్రజ్ఞ ప్రియ ఫౌండేషన్ (లాభాపేక్షలేనిది)',
    'cult.fit':'కల్ట్.ఫిట్'
}

trans_count = 0
def translation_wrapper(text):
    global trans_count
    tel = translator.translate(text,lang_tgt='te')
    trans_count+=1
    if trans_count%10 == 0:
        time.sleep(2)
    return tel

all_cols = ['Code','Established_Year','Website', 'Opens_at','Closes_at','Num_Staff','Num_Beds', 'Operating_Rooms','Accredited'
            'Pharmacy','Ambulance','Medical_College', 'Vaccination','Bloodbank', 'Bloodtransfusion','Eyebank'
            'Valid_From','Valid_Upto', 'Date_First' 'Placetype','Management', 'Systems', 'Caretype'
            'Hospital_Name', 'Location','Address','District','State','Country','City', 'Managed_By',
            'Clinical_Services','Diagnostic_Services','Laboratory_Services','Professions','Other_Facilities']

def translate(record):
    cols = ['Hospital_Name','District','State','Country','City','Location','Address','Managed_By']
    for col in cols:
        if record[col] is None or type(record[col]) != str or record[col] == 'None':
            continue
        initial = record[col]
        if initial in current_translations:
            record[col] = current_translations[initial]
            continue
        record[col] = translation_wrapper(record[col])
        if acronym_translate:
            record[col] = telugu_acronym(record[col])
        current_translations[initial] = record[col]

    cols = ['Clinical_Services','Professions','Laboratory_Services','Diagnostic_Services','Other_Facilities']
    for col in cols:
        if record[col] is None or type(record[col]) != list or len(record[col])==0: 
            continue 
        after = []
        for ele in record[col]:
            if ele.strip().lower() in exceptions:
                after.append(exceptions[ele.strip().lower()])
                continue
            initial = ele.strip().lower()
            if initial in current_translations:
                after.append(current_translations[initial])
                continue
            telugu_text = translation_wrapper(ele)
            if acronym_translate:
                telugu_text = telugu_acronym(telugu_text)
            current_translations[initial] = telugu_text
            after.append(telugu_text)
        record[col] = after
    return record



translator = google_translator()
acronym_translate = False
current_translations = {}

translations_csv = './SHCO_english_telugu.csv'
if os.path.exists(translations_csv):
    df = pd.read_csv(translations_csv)
    print(df.columns)
    eng = df['english'].to_list()
    tel = df['current_telugu'].to_list()
    for i in range(len(df)):
        e, t = df.loc[i]
        current_translations[e] = t
print(len(current_translations.keys()))

filename = './Hospital_telugu_merged.json'
with open(filename,'r') as data_file:
    json_data = data_file.read()


data = json.loads(json_data)
print(len(data))
count = 0
#assert data[count]['Code'] == 'SHCO-2019-0263'
#loop over the whole KB
errors = [11]
for i in range(len(errors)):
    record_dict = data[i]
    # if count in errors:
    #     count+=1
    #     continue
    if count == 0:
        print('happening')
    try:
        print(' Processing '+str(count)+': '+record_dict['Code'])
        count+=1
        record_dict = hardcode(record_dict)
        record_dict = translate(record_dict)
    except:
        print('Error occured at '+record_dict['Code'])
        print('Exception : ',sys.exc_info())
        break
telugu_filename = './Hospital_telugu_merged.json'
# telugu_filename = './SHCO_telugu_merged.json'

# with open(telugu_filename,'r') as in_file:
#     data1 =  json.load(in_file)
#     data1.update(data)

with open(telugu_filename,'w') as out_file:
    json.dump(data, out_file)

translations_csv = './Hospital_english_telugu2.csv'
with open(translations_csv,'a+') as f:
    writer = csv.writer(f)
    writer.writerow(['english','current_telugu'])
    for key in current_translations:
        value = current_translations[key] 
        writer.writerow([key,value])

#If improvement file is added
# import pandas as pd
# improved = pd.read_excel('improvement_file')
# improved = improved['english','telugu_corrected']
# improved = improved.dropna(axis=0)
# exceptions = {}
# for i in range(len(improved)):
#     key, value = improved['english'][i], improved['telugu_corrected'][i]
#     exceptions[key] = value
