"""
İzmir Ekonomi Üniversitesi
MBP 227 - Veri Bilimi ve Makine Öğrenmesi
1. Proje Ödevi

Hazırlayan: Ahmet Eren Yakut
Konu: Video Oyun Satışları ve Konsol Pazar Analizi (1980 - 2020)
Veri Seti: vgsales.csv (Kaggle)
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Çıktıların terminalde daha okunaklı durması için pandas ayarları
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# ==============================================================================
# 2.1 VERİ TOPLAMA
# ==============================================================================
"""
AÇIKLAMA:
Bu aşamada Kaggle platformundan elde edilen 'Video Game Sales' veri seti projeye dahil edilmiştir.
Veri seti 16.598 satır ve 11 sütun içermekte olup, yönergedeki 'en az 500 satır ve 6 sütun' kuralını
fazlasıyla sağlamaktadır. Veride hem sayısal (Satış rakamları, Yıl) hem de kategorik (Platform, Tür)
değişkenler bulunmaktadır.
"""
print("="*60)
print("--- 2.1 VERİ TOPLAMA ---")
df = pd.read_csv('vgsales.csv')
print("Veri Seti Yüklendi")
print("\nVeri Setinin Başı (df.head()):\n", df.head())
print("\nVeri Setinin Sonu (df.tail()):\n", df.tail())


# ==============================================================================
# 2.2 KEŞİFSEL VERİ ANALİZİ (EDA)
# ==============================================================================
"""
AÇIKLAMA:
Veri setinin yapısını anlamak için temel Keşifsel Veri Analizi adımları uygulanmıştır.
- df.shape ile satır/sütun hacmi,
- df.dtypes ile değişken tipleri,
- df.describe() ile sayısal sütunların istatistiksel dağılımları (ortalama, std, min, max),
- df.isnull().sum() ile veri setindeki eksik değerlerin tespiti yapılmıştır.
- Benzersiz değerler incelenmiş ve sayısal değişkenler arası korelasyon hesaplanmıştır.
"""
print("\n" + "="*60)
print("--- 2.2 KEŞİFSEL VERİ ANALİZİ (EDA) ---")
print(f"1. Veri Seti Boyutu: {df.shape[0]} Satır, {df.shape[1]} Sütun\n")
print("2. Veri Tipleri:\n", df.dtypes, "\n")
print("3. Temel İstatistiksel Özet:\n", df.describe(), "\n")
print("4. Eksik Değer Sayısı:\n", df.isnull().sum(), "\n")
print("5. Benzersiz Değer Sayısı:\n", df.nunique(), "\n")

print("6. Sayısal Değişkenler Arası Korelasyon Matrisi:")
# Sadece sayısal sütunları seçip korelasyon bakıyoruz
numeric_df = df.select_dtypes(include=['float64', 'int64'])
print(numeric_df.corr())


# ==============================================================================
# 2.3 EKSİK DEĞER ANALİZİ VE TEMİZLEME
# ==============================================================================
"""
AÇIKLAMA VE GEREKÇELENDİRME:
EDA aşamasında 'Year' sütununda 271, 'Publisher' sütununda 58 adet eksik değer bulunmuştur.
Bu değerler toplam 16.598 satırlık verinin sadece yaklaşık %1.9'unu oluşturmaktadır.
Oyunların çıkış yılları (Year) spesifik zaman verileri olduğu için ortalama (mean) veya 
medyan ile doldurmak analizde ciddi tarihsel sapmalara yol açacaktır. Bu gerekçeyle, 
eksik verilerin analizden tamamen çıkarılmasına (dropna) karar verilmiştir.
"""
print("\n" + "="*60)
print("--- 2.3 EKSİK DEĞER TEMİZLEME ---")
print(f"Temizlik Öncesi Satır Sayısı: {df.shape[0]}")

df.dropna(inplace=True) # Eksik satırlar kalıcı olarak siliniyor

print(f"Temizlik Sonrası Satır Sayısı: {df.shape[0]}")
print("Kalan Eksik Değerler:\n", df.isnull().sum())


# ==============================================================================
# 2.4 AYKIRI DEĞER (OUTLIER) ANALİZİ VE TEMİZLEME
# ==============================================================================
"""
AÇIKLAMA:
Veri setindeki 'Global_Sales' (Küresel Satışlar) sütununda "Wii Sports", "GTA V" gibi
standart dışı devasa satışlara ulaşmış hit oyunlar bulunmaktadır. Görselleştirmelerin 
çarpılmaması adına IQR (Çeyrekler Arası Aralık) yöntemi ile bu aykırı değerler tespit 
edilmiş ve temizlenmiştir.
"""
print("\n" + "="*60)
print("--- 2.4 AYKIRI DEĞER ANALİZİ (IQR) ---")

Q1 = df['Global_Sales'].quantile(0.25)
Q3 = df['Global_Sales'].quantile(0.75)
IQR = Q3 - Q1

alt_sinir = Q1 - 1.5 * IQR
ust_sinir = Q3 + 1.5 * IQR

aykiri_degerler = df[(df['Global_Sales'] < alt_sinir) | (df['Global_Sales'] > ust_sinir)]
print(f"Tespit edilen aykırı değer (hit oyun) sayısı: {aykiri_degerler.shape[0]}")

# Aykırı değer temizliği
df = df[(df['Global_Sales'] >= alt_sinir) & (df['Global_Sales'] <= ust_sinir)]
print(f"Aykırı değerler temizlendikten sonraki analiz edilebilir satır sayısı: {df.shape[0]}")


# ==============================================================================
# 2.5 SEABORN İLE GÖRSELLEŞTİRME (10 ADET)
# ==============================================================================
"""
AÇIKLAMA:
Bu bölümde veri setinden anlamlı çıkarımlar yapmak için Seaborn kütüphanesi ile 
10 farklı grafik oluşturulmuştur. Her grafikte başlıklar, eksen etiketleri ve 
gerekli renk paletleri (hue dahil edilerek) yönergeye uygun şekilde tanımlanmıştır.
NOT: Grafikler sırayla açılacaktır, kodu ilerletmek için açılan pencereyi kapatınız.
"""
print("\n" + "="*60)
print("--- 2.5 GÖRSELLEŞTİRMELER OLUŞTURULUYOR ---")
print("Lütfen açılan grafikleri inceledikten sonra kapatın ki kod devam etsin...")

sns.set_theme(style="whitegrid")

# Grafik 1: Countplot (Platform Dağılımı)
plt.figure(figsize=(10, 5))
sns.countplot(data=df, y='Platform', order=df['Platform'].value_counts().index[:10], hue='Platform', palette='viridis', legend=False)
plt.title('1. En Çok Oyun Üretilen 10 Platform')
plt.xlabel('Oyun Sayısı')
plt.ylabel('Platformlar')
plt.show()

# Grafik 2: Barplot (Türlere Göre Satış)
plt.figure(figsize=(12, 5))
sns.barplot(data=df, x='Genre', y='Global_Sales', errorbar=None, hue='Genre', palette='mako', legend=False)
plt.title('2. Oyun Türlerine Göre Ortalama Global Satışlar')
plt.xlabel('Oyun Türü')
plt.ylabel('Ortalama Satış (Milyon)')
plt.xticks(rotation=45)
plt.show()

# Grafik 3: Histplot (Yıllara Göre Dağılım)
plt.figure(figsize=(10, 5))
sns.histplot(df['Year'], bins=30, kde=True, color='purple')
plt.title('3. Oyunların Çıkış Yıllarına Göre Dağılımı')
plt.xlabel('Çıkış Yılı')
plt.ylabel('Frekans (Oyun Sayısı)')
plt.show()

# Grafik 4: Scatterplot (Bölgesel İlişki)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='NA_Sales', y='EU_Sales', alpha=0.5, color='red')
plt.title('4. Kuzey Amerika vs Avrupa Satışları İlişkisi')
plt.xlabel('Kuzey Amerika Satışları (Milyon)')
plt.ylabel('Avrupa Satışları (Milyon)')
plt.show()

# Grafik 5: Heatmap (Korelasyon Matrisi)
plt.figure(figsize=(8, 6))
sayisal_df = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']]
sns.heatmap(sayisal_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('5. Satış Bölgeleri Arası Korelasyon Matrisi')
plt.xlabel('Değişkenler')
plt.ylabel('Değişkenler')
plt.show()

# Grafik 6: Boxplot (Popüler Türlerin Dağılımı)
ilk_5_tur = df['Genre'].value_counts().index[:5]
df_ilk5 = df[df['Genre'].isin(ilk_5_tur)]
plt.figure(figsize=(10, 5))
sns.boxplot(data=df_ilk5, x='Genre', y='Global_Sales', hue='Genre', palette='Set2', legend=False)
plt.title('6. En Popüler 5 Türün Satış Dağılımı')
plt.xlabel('Oyun Türü')
plt.ylabel('Global Satışlar (Milyon)')
plt.show()

# Grafik 7: Lineplot (Yıllık Satış Trendi)
yillik_satis = df.groupby('Year')['Global_Sales'].sum().reset_index()
plt.figure(figsize=(12, 5))
sns.lineplot(data=yillik_satis, x='Year', y='Global_Sales', marker='o', color='green')
plt.title('7. Yıllara Göre Toplam Global Satış Trendi')
plt.xlabel('Yıl')
plt.ylabel('Toplam Satış (Milyon)')
plt.show()

# Grafik 8: Kdeplot (Japonya Yoğunluğu)
plt.figure(figsize=(8, 5))
sns.kdeplot(df['JP_Sales'], fill=True, color='blue')
plt.title('8. Japonya Satışları Yoğunluk Tahmini')
plt.xlabel('Japonya Satışları (Milyon)')
plt.ylabel('Yoğunluk')
plt.show()

# Grafik 9: Violinplot (Aksiyon vs Spor Dağılımı)
hedef_turler = df[df['Genre'].isin(['Action', 'Sports'])]
plt.figure(figsize=(8, 5))
sns.violinplot(data=hedef_turler, x='Genre', y='EU_Sales', hue='Genre', palette='muted', legend=False)
plt.title('9. Aksiyon ve Spor Oyunlarının Avrupa Satışları')
plt.xlabel('Tür')
plt.ylabel('Avrupa Satış (Milyon)')
plt.show()

# Grafik 10: Pairplot (Çoklu İlişki)
sns.pairplot(df.head(500)[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']])
plt.suptitle('10. İlk 500 Oyun İçin Satış Sütunları İlişkisi', y=1.02)
plt.show()


# ==============================================================================
# 2.6 GROUPBY & KOŞULLU SORGULAR
# ==============================================================================
"""
AÇIKLAMA:
Pandas kütüphanesinin groupby, agg, loc, query, filter gibi fonksiyonları 
kullanılarak veri seti üzerinden çeşitli filtrelemeler ve iş zekası sorguları 
çalıştırılmış ve ekrana yazdırılmıştır.
"""
print("\n" + "="*60)
print("--- 2.6 GROUPBY VE KOŞULLU SORGULAR ---")

# Sorgu 1
print("\n1. En Çok Satan İlk 5 Platform (groupby + sum):")
print(df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(5))

# Sorgu 2
print("\n2. Türlere Göre Çıkan Oyun Sayısı (groupby + count):")
print(df.groupby('Genre')['Name'].count().sort_values(ascending=False).head(5))

# Sorgu 3
print("\n3. En Yüksek Ortalama Satış Yapan 5 Yayıncı (groupby + mean):")
print(df.groupby('Publisher')['Global_Sales'].mean().sort_values(ascending=False).head(5))

# Sorgu 4
print("\n4. Türlerin Kuzey Amerika Satış İstatistikleri (groupby + agg):")
print(df.groupby('Genre')['NA_Sales'].agg(['min', 'max', 'mean']).head())

# Sorgu 5
print("\n5. 2015 Sonrası Çıkıp 1 Milyondan Fazla Satan İlk 5 Oyun (loc):")
print(df.loc[(df['Year'] >= 2015) & (df['Global_Sales'] > 1.0), ['Name', 'Year', 'Global_Sales']].head())

# Sorgu 6
print("\n6. Nintendo'nun Japonya'daki Popüler Oyunları (query):")
print(df.query("Publisher == 'Nintendo' and JP_Sales > 0.5")[['Name', 'JP_Sales']].head())

# Sorgu 7
print("\n7. Platformların Satış İstikrarsızlığı/Sapması (groupby + std):")
print(df.groupby('Platform')['Global_Sales'].std().sort_values(ascending=False).head())

# Sorgu 8
print("\n8. Toplam Satışı 50 Milyonu Geçen Platformların Listesi (groupby + filter):")
dev_platformlar = df.groupby('Platform').filter(lambda x: x['Global_Sales'].sum() > 50)
print(dev_platformlar['Platform'].unique())

# Sorgu 9
print("\n9. Avrupa'da En Çok Satan 5 PC Oyunu (sort_values + head):")
pc_avrupa = df[df['Platform'] == 'PC'].sort_values(by='EU_Sales', ascending=False)
print(pc_avrupa[['Name', 'EU_Sales']].head())

# Sorgu 10
print("\n10. Oyunların Kendi Tür Ortalamasına Göre Başarı Oranı (groupby + transform):")
df['Tur_Ortalamasi'] = df.groupby('Genre')['Global_Sales'].transform('mean')
df['Basari_Orani'] = df['Global_Sales'] / df['Tur_Ortalamasi']
print(df[['Name', 'Genre', 'Global_Sales', 'Basari_Orani']].head())

print("\n" + "="*60)
print("PROJE SONU")