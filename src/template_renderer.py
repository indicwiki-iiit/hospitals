from jinja2 import Template, Environment, BaseLoader, FileSystemLoader
import gettext
import json

#jinja_env = Environment(loader = BaseLoader(), extensions=['jinja2.ext.do','jinja2.ext.i18n'])

template_path = 'telugu_hospitals.j2'
#template_file = open(template_path,'r')
#template_text = template_file.read()
#template = jinja_env.from_string(template_text)
ENV = Environment(loader=FileSystemLoader('../../jinja-templates')) # Global variable
template = ENV.get_template(template_path)

filename = '../data/NABH_Accr_merge_cert_telugu.json'
with open(filename,'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)
#loop over the whole KB
for record_dict in data:
    article = template.render(**record_dict)
    print(article) #store each article
    print("#################")