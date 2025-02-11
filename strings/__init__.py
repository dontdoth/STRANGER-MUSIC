import os
from typing import List
import yaml

languages = {}
languages_present = {}

def get_string(lang: str):
    return languages[lang]

# First load Persian (Farsi) as default language
if "fa" not in languages:
    languages["fa"] = yaml.safe_load(
        open(r"./strings/langs/fa.yml", encoding="utf8")
    )
    languages_present["fa"] = languages["fa"]["name"]

# Then load other languages
for filename in os.listdir(r"./strings/langs/"):
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "fa":  # Skip Persian as it's already loaded
            continue
            
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        
        # Use Persian as the base language for missing translations
        for item in languages["fa"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["fa"][item]
                
        try:
            languages_present[language_name] = languages[language_name]["name"]
        except:
            print("مشکلی در فایل زبان ربات وجود دارد.")
            exit()
