import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import schedule
import time

# === 📌 الخطوة 1: تحميل البيانات ===

# ✅ تعريف الدالة بحيث تستقبل اسم الملف
def load_data(filename):
    print("📥 جاري تحميل البيانات...")
    print("🚀 جاري تنفيذ باقي الخطوات...")
    data = pd.read_csv(filename)
    print("✅ تم تحميل البيانات بنجاح! 👇")
    print(data.head())  # عرض أول 5 صفوف للتأكد
    return data  # ✅ إرجاع البيانات لتتم معالجتها لاحقًا

# === 📌 الخطوة 2: تنظيف البيانات ===
def clean_data(data):
    print("🧹 تنظيف البيانات...")
    data.dropna(inplace=True)  # حذف القيم المفقودة
    data.drop_duplicates(inplace=True)  # إزالة التكرارات
    data['date'] = pd.to_datetime(data['date'])  # تحويل التاريخ
    return data

# === 📌 الخطوة 3: تحليل البيانات (EDA) ===
def eda(data):
    print("📊 تحليل البيانات الاستكشافي...")

    # إحصائيات وصفية
    print(data.describe())

    # خريطة الارتباط
    plt.figure(figsize=(8, 6))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
    plt.title("خريطة الارتباط")
    plt.show()

    # اتجاهات المبيعات عبر الزمن
    data.groupby('date')['sales'].sum().plot(kind='line', figsize=(10,5))
    plt.title('📈 اتجاهات المبيعات عبر الوقت')
    plt.xlabel('التاريخ')
    plt.ylabel('إجمالي المبيعات')
    plt.show()

    # أفضل المنتجات مبيعًا
    top_products = data.groupby('product')['sales'].sum().nlargest(10)
    top_products.plot(kind='bar', figsize=(10,5))
    plt.title('🏆 أفضل 10 منتجات من حيث المبيعات')
    plt.xlabel('المنتج')
    plt.ylabel('إجمالي المبيعات')
    plt.show()

# === 📌 الخطوة 4: تنفيذ K-Means يدويًا بدون مكتبة sklearn ===
def kmeans_manual(data, k=3, max_iters=100):
    print("🤖 تقسيم العملاء باستخدام K-Means يدويًا...")

    # اختيار مراكز عشوائية أولية
    np.random.seed(42)
    centroids = data[['sales', 'quantity']].sample(n=k).values

    for _ in range(max_iters):
        # حساب المسافات لكل نقطة إلى كل مركز
        distances = np.linalg.norm(data[['sales', 'quantity']].values[:, np.newaxis] - centroids, axis=2)
        clusters = np.argmin(distances, axis=1)

        # تحديث المراكز
        new_centroids = np.array([data[['sales', 'quantity']][clusters == i].mean() for i in range(k)])

        # التحقق من الاستقرار
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids

    data['customer_segment'] = clusters

    # رسم التجمعات
    plt.scatter(data['sales'], data['quantity'], c=clusters, cmap='viridis', alpha=0.6)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, label="Centroids")
    plt.title('📌 تقسيم العملاء إلى مجموعات')
    plt.xlabel('المبيعات')
    plt.ylabel('الكمية')
    plt.legend()
    plt.show()

    return data

# === 📌 الخطوة 5: تصدير البيانات إلى Power BI ===
def export_data(data, output_path):
    print(f"💾 تصدير البيانات إلى {output_path} ...")
    data.to_csv(output_path, index=False)

# === 📌 تشغيل جميع الخطوات ===
if __name__ == "__main__":
    # 1️⃣ تحميل البيانات
    data = load_data('data/sales_data.csv')

# 5️⃣ تصدير البيانات بعد التحليل إلى Power BI
export_data(data, "processed_sales_data.csv")

print("✅ تم تصدير البيانات بنجاح إلى processed_sales_data.csv!")
