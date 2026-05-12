# 🎮 Video Oyun Satışları ve Konsol Pazar Analizi

 Proje Özeti
Bu proje, 1980 - 2020 yılları arasındaki küresel video oyunu satış verilerini inceleyerek; platform rekabetleri, türlerin bölgesel popülaritesi ve yayıncı başarıları üzerine derinlemesine veri analizi (Data Analysis) yapan bir Python çalışmasıdır. Kaggle üzerinden alınan 16.598 satırlık geniş bir veri seti kullanılmıştır.

 Teknik Özellikler ve Sorgular
Proje kapsamında `Pandas` kütüphanesi kullanılarak gerçekleştirilen bazı temel analizler:
* **Filtreleme & Sıralama (`loc`, `query`, `sort_values`):** 2015 sonrası çıkan ve 1 milyondan fazla satan oyunların, Nintendo'nun Japonya'daki popüler oyunlarının ve Avrupa'da en çok satan PC oyunlarının tespit edilmesi.
* **Gruplama ve Kümeleme (`groupby`, `agg`):** Platformların satış istikrarsızlığının (standart sapma) ölçülmesi, oyun türlerine göre Kuzey Amerika satış istatistiklerinin (min, max, mean) hesaplanması.
* **Veri Temizleme:** Eksik verilerin (NaN) tespiti ve veri setinin analize uygun hale getirilmesi.

## 🛠 Kullanılan Teknolojiler
* **Programlama Dili:** Python 3.x
* **Veri Analizi ve Manipülasyonu:** Pandas
* **Veri Seti Kaynağı:** `vgsales.csv` (Kaggle)
