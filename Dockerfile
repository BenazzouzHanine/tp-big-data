# استخدم صورة Python الرسمية
FROM python:3.9-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ الملفات المطلوبة فقط
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# تشغيل كود التحليل تلقائيًا
CMD ["python", "scripts/tp.py"]
