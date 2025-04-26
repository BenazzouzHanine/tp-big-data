import requests
import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://www.wallpaperflare.com/search?wallpaper=anime&page=={}" 
total_pages = 180 # عدد الصفحات التي سنقوم بزيارتها

# قائمة لتخزين بيانات جميع الصور من جميع الصفحات
all_images_data = []

for page in range(1, total_pages + 1):
    print(f"معالجة الصفحة {page}...")
    url = base_url.format(page)
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"فشل تحميل الصفحة {page}، رمز الحالة: {response.status_code}")
            continue
    except Exception as e:
        print(f"حدث خطأ أثناء جلب الصفحة {page}: {e}")
        continue

    # تحليل محتوى الصفحة باستخدام BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # إيجاد جميع عناصر الصور (li التي تحمل itemprop="associatedMedia")
    image_items = soup.find_all('li', itemprop='associatedMedia')
    
    # استخراج البيانات من كل عنصر صورة
    for li in image_items:
        try:
            # استخراج رابط صفحة التفاصيل من وسم <a itemprop="url">
            a_tag = li.find('a', itemprop='url')
            image_page_link = a_tag.get('href') if a_tag else None
            
            # استخراج أبعاد الصورة من <span class="res">
            resolution_tag = li.find('span', class_='res')
            resolution = resolution_tag.get_text(strip=True) if resolution_tag else None

            # استخراج نوع الملف من <meta itemprop="fileFormat">
            file_format_tag = li.find('meta', itemprop='fileFormat')
            file_format = file_format_tag.get('content') if file_format_tag else None

            # استخراج الكلمات المفتاحية من <meta itemprop="keywords">
            keywords_tag = li.find('meta', itemprop='keywords')
            keywords = keywords_tag.get('content') if keywords_tag else None

            # استخراج الوصف من <meta itemprop="description">
            description_tag = li.find('meta', itemprop='description')
            description = description_tag.get('content') if description_tag else None

            # استخراج حجم الملف من <meta itemprop="contentSize">
            content_size_tag = li.find('meta', itemprop='contentSize')
            content_size = content_size_tag.get('content') if content_size_tag else None

            # استخراج بيانات صورة المعاينة من وسم <img> داخل <a>
            img_tag = a_tag.find('img') if a_tag else None
            if img_tag:
                # نستخدم data-src إذا كانت موجودة، وإلا نستخدم src
                preview_image = img_tag.get('data-src') if img_tag.has_attr('data-src') else img_tag.get('src')
                alt_text = img_tag.get('alt')
                title_text = img_tag.get('title')
            else:
                preview_image = alt_text = title_text = None

            # استخراج التسمية التوضيحية من <figcaption>
            caption_tag = li.find('figcaption')
            caption = caption_tag.get_text(strip=True) if caption_tag else None

            # تجميع البيانات في قاموس
            image_data = {
                "image_page_link": image_page_link,
                "resolution": resolution,
                "file_format": file_format,
                "keywords": keywords,
                "description": description,
                "content_size": content_size,
                "preview_image": preview_image,
                "alt_text": alt_text,
                "title_text": title_text,
                "caption": caption,
            }
            all_images_data.append(image_data)
        except Exception as e:
            print("حدث خطأ أثناء معالجة صورة:", e)
    
    # تأخير بسيط لتجنب الضغط على الخادم (اختياري)
    time.sleep(1)

# 3. حفظ النتائج في ملف CSV
csv_file = "images_data.csv"
fieldnames = [
    "image_page_link", 
    "resolution", 
    "file_format", 
    "keywords", 
    "description", 
    "content_size", 
    "preview_image", 
    "alt_text", 
    "title_text", 
    "caption"
]

try:
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_images_data)
    print(f"تم حفظ البيانات في الملف: {csv_file}")
except Exception as e:
    print("حدث خطأ أثناء حفظ البيانات في ملف CSV:", e)