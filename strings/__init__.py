import os
from typing import List
import yaml

languages = {}
languages_present = {}

def get_string(lang: str):
    return languages[lang]

# First load Arabic as default language
if "ar" not in languages:
    languages["ar"] = yaml.safe_load(
        open(r"./strings/langs/ar.yml", encoding="utf8")
    )
    languages_present["ar"] = languages["ar"]["name"]

# Then load other languages
for filename in os.listdir(r"./strings/langs/"):
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "ar":  # Skip Arabic as it's already loaded
            continue
            
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        
        # Use Arabic as the base language for missing translations
        for item in languages["ar"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["ar"][item]
                
        try:
            languages_present[language_name] = languages[language_name]["name"]
        except:
            print("There is some issue with the language file inside bot.")
            exit()
