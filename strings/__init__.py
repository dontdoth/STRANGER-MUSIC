import os
from typing import List
import yaml

# دیکشنری برای نگهداری زبان‌ها
languages = {}
# دیکشنری برای نگهداری نام زبان‌های موجود
languages_present = {}

def get_string(lang: str):
    """دریافت رشته‌های زبان مورد نظر"""
    return languages[lang]

# پیمایش فایل‌های زبان در پوشه
for filename in os.listdir(r"./strings/langs/"):
    # اگر زبان انگلیسی هنوز بارگذاری نشده
    if "fa" not in languages:  # تغییر به فارسی به عنوان زبان پیش‌فرض
        languages["fa"] = yaml.safe_load(
            open(r"./strings/langs/fa.yml", encoding="utf8")  # تغییر به فایل فارسی
        )
        languages_present["fa"] = languages["fa"]["name"]
        
    # بررسی فایل‌های yml
    if filename.endswith(".yml"):
        language_name = filename[:-4]  # حذف پسوند .yml
        if language_name == "fa":  # رد کردن فایل فارسی
            continue
            
        # بارگذاری فایل زبان
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        
        # اضافه کردن کلیدهای موجود در فارسی که در زبان فعلی نیستند
        for item in languages["fa"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["fa"][item]
    
    try:
        # ذخیره نام زبان
        languages_present[language_name] = languages[language_name]["name"]
    except:
        print("مشکلی در فایل زبان ربات وجود دارد.")
        exit()
