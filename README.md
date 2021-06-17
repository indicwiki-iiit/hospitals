# Tewiki Hospitals
Tewiki Hospital Bot is a Wikipedia bot that aims to generate wiki articles primarily in the hospitals and medical institutions domain. The bot currently focuses on articles in the Telugu language, however the system architecture is language-agnostic and can be easily extended to other languages such as Tamil, Hindi, etc. 

## Repository Structure
```
__ hospitals
	|__ data
		|__ code
		|__ 1135_hosp_eng.json
		
	|__ translations
		|__ code
		|__ 1135_hosp_telugu.json
	
	|__ template
		|__ telugu_hosp.j2
	
	|__ article_gen
		|__ xmlgenerator.py
		
	|__ outputs
		|__ 1135_hosp_tel.xml

```

## Architecture
The overall system architecture is divided into three steps : 
1. **KB creation**  : An enriched domain-specific knowledge base is created as the base for the bot. The KB design and enrichment process might involve domain expertise, human annotation, crowd sourcing and/or focused crawling.
2. **KB translation** : Translation and/or transliteration of the enriched KB to required language.
3. **Template creation** : The bot depends on human-written templates to generate meaningful and grammatically correct  articles in each domain. These templates are created for every domain-language pair and integrated with the domain-specific knowledge base to generate articles. 
4. **Wiki Article Generation** : The articles are then rendered in a human-consumable format, including support for  wiki references, infoboxes,  images, tables and other domain-specific features.

### Workflow
![[wikihospitals_workflow.svg]]
## KB Creation
An enriched knowledge base for Indian Hospitals domain should ideally include a comprehensive list of all the hospitals and healthcare institutions in the country, their geographical, historical and infrastructural details, and  medical services each institution offers. 

Since this data could not be extracted from a single source, there was a need to collect and combine information of different formats and from multiple websites.

The main sources that were referred to : 
1. **data.gov.in** : [Open  Government Data (OGD)](https://data.gov.in/resources/national-hospital-directory-geo-code-and-additional-parameters-updated-till-last-month) 
	
	- **Data format** : csv
	- Updated every month
	- **Records** :  30273  
	- **Attributes** : 30	(Contains geographical, infrastructural and some general details about management, established year, website, etc. )
		
2. **NABH** :  [Allopathic Clinics](https://www.nabh.co/Allopathic.aspx), [Hospitals](https://www.nabh.co/Hospitals.aspx), [SHCOs](https://www.nabh.co/SHCO.aspx)
	*  **Data format** : Scanned PDF certificates
	*  Updated yearly (new entries added)
	*  Contains details about the medical services and facilities offered
	*  **Records** : 1135 ( for allopathic medical institutions )

Since 90% of the records from [data.gov.in](data.gov.in) only contain Hospital name and Geographical details, their articles will only contain 30-50 words.  

So, for our database, we have only considered NABH accredited (notable) hospitals and combined the data from the above two sources. 

**Final attributes** considered :
Hospital_Name, System of Medicine, Management, Caretype, Website, Established Year, State, Coordinates, Location, District, Clinical Services, Bloodbank, Pharmacy, Ambulance, Eyebank, Support Services, Facilities,  Num staff, Num beds, opens at, closes at

The final KB is in json format with a dictionary for each hospital. Attributes such as Clinical Services, Facilities, etc are present as a list of strings.  

The KB generated might still have missing values for records. So we have used web crawling of google search results to fill the required information wherever possible. 

The individual data sources, their scraping, extracting and merging codes, Google answer crawling code and the final dataset are present in the **/data** folder. 

### Translation and Transliteration
To use the KB in a wiki article, the entries in the generated KB needs to be translated to the required languages. Numeric or time-based entries need not be translated, however since the hospitals data mainly consists of English-language strings, we use Google-trans-new library for translation of the entries. 

Errors are then manually corrected and the final translated eng-tel pairs are stored for further use. Storing the translations locally reduces the article generation time over sending requests to API every time. 

The translation code and the final xls file of eng-tel pairs are present in the **/translations** folder.

### Future Scope
* Currently, our final enriched database only consists of NABH approved hospitals (1135). 
	* From the OGD dataset, we can sample and use records of medium quality (that have some infrastructure details) to increase our KB size.
	* We can improve OGD dataset by filling the missing values using Google answer scraping.  
* Add support for images
* Refer to other sources such as practo, indiahelathcaretourism, JCL, etc to enrich our KB. 
* Automate periodic data collection 
## Template creation
We use Jinja2 template engine for creating templates for domain specific Wiki articles. Jinja2 is a powerful template engine which allows users to create diverse templates.

The domain expert must create a template for every target domain. The template contains variables whose values need to be supplied from a python program. 

The template must follow the language wikipedia guidelines, include references, categories and infobox. 

For this work, we created a template for Indian hospitals stored in **templates/hospitals.j2** 
## Wiki article generation
We then integrate the translated KB and template using a python program. This generates a wiki XML file, that can be imported to wikipedia.

Command to generate XML dump : 
```
python3 article_gen/xmlgenerator.py --data data/1135_hosp_telugu.json --template template/telugu_hosp.j2 --output output/1135_hosp_telugu.xml
```
## References
1. [wiki-ragas](https://github.com/nikhilpriyatam/wiki_ragas)

#tewiki #indicwiki #documentation
