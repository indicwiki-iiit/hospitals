import json
from google_trans_new import google_translator

months_trans = {
    'jan':'జనవరి', 'feb':'ఫిబ్రవరి','mar':'మార్చి','apr': 'ఏప్రిల్',
    'may':'మే', 'jun': 'జూన్','jul': 'జూలై',    'aug': 'ఆగస్టు', 'sep': 'సెప్టెంబర్',
    'oct': 'అక్టోబర్','nov': 'నవంబర్','dec': 'డిసెంబర్'
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
        if record[col] is None or type(record[col]) != str:
            continue
        date, month, year = record[col].split(' ')
        record[col] = date+' '+trans[month.lower()]+' '+year    
    
    cols = ['Caretype','Management','Systems','Placetype']
    for col in cols:
        if record[col] is None or record[col] == '' : 
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
}

def translate(record):
    cols = ['Name','District','State','Country','City','Location','Address']
    for col in cols:
        if record[col] is None or type(record[col]) != str:
            continue
        record[col] = translator.translate(record[col],lang_tgt='te')
        if acronym_translate:
            record[col] = telugu_acronym(record[col])

    cols = ['Services','Professions','Lab_Services','Diagnostic_Services','Other_Facilities']
    for col in cols:
        if record[col] is None or type(record[col]) != list or len(record[col])==0: 
            continue 
        after = []
        for ele in record[col]:
            if ele.strip().lower() in exceptions:
                after.append(exceptions[ele.strip().lower()])
                continue
            telugu_text = translator.translate(ele,lang_tgt = 'te')
            if acronym_translate:
                telugu_text = telugu_acronym(telugu_text)
            after.append(telugu_text)
        record[col] = after
    return record



translator = google_translator()
acronym_translate = True

filename = '../data/NABH_Accr_merge_cert.json'
with open(filename,'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)
#loop over the whole KB
for record_dict in data:
    record_dict = hardcode(record_dict)
    record_dict = translate(record_dict)

telugu_filename = '../data/NABH_Accr_merge_cert_telugu.json'
with open(telugu_filename,'w') as out_file:
    json.dump(data, out_file)
