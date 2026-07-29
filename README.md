# IST1132 Olasılık Dersi Yerel RAG Asistanı

![Microsoft Foundry Local](https://img.shields.io/badge/Microsoft-Foundry%20Local-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![RAG](https://img.shields.io/badge/Architecture-RAG-purple)

Bu proje, **Microsoft Foundry Local** altyapısı kullanılarak tamamen **yerel (local/offline)** çalışan, internete bağımlılığı olmayan bir **Olasılık Dersi Yapay Zeka Asistanı** (Retrieval-Augmented Generation - RAG) uygulamasıdır.

Yıldız Teknik Üniversitesi **IST1132 Olasılık** dersi 1-5. hafta konularını (Kesikli Düzgün, Bernoulli, Binom, Hipergeometrik, Geometrik, Negatif Binom, Poisson ve Normal Dağılımlar) kapsayan ders notları üzerinde semantik arama ve soru-cevaplama gerçekleştirir.

---

## Sistem Mimarisi

```
[ Kullanıcı Sorusu ]
        |
        v
[ Foundry Local Embedding Modeli ] (qwen3-embedding-0.6b)
        |
        v (Soru Vektörü)
[ Vektör Benzerlik Araması ] (Kosinüs Benzerliği - Cosine Similarity)
        |
        v (İlgili Notlar / Bağlam)
[ SQLite Vektör Veritabanı ] (rag_veritabani.db)
        |
        v
[ Kanıta Dayalı Doğru Yanıt ]
```

---

## Özellikler

- **%100 Yerel ve Çevrimdışı (Offline):** Hiçbir veri dışarıya aktarılmaz, bulut/internet bağlantısına ihtiyaç duymaz.
- **Hallusinasyon Önleyici (Grounded Answers):** Yapay zeka bilmiyorsa uydurmaz, sadece ders notlarındaki bilgiye dayanarak cevap verir.
- **Hızlı Vektör Arama:** SQLite üzerinde saklanan sayısal vektörler (embeddings) ile milisaniyeler içinde anlamsal arama.
- **Kapsamlı Müfredat:** IST1132 Olasılık dersi 1-5. Hafta tüm teorik konular, formüller ve dağılım özellikleri eklenmiştir.

---

## Kurulum ve Çalıştırma

### 1. Gereksinimleri Yükleyin
```bash
pip install -r requirements.txt
```

### 2. Veri Tabanını Oluşturun ve Ders Notlarını Yükleyin
```bash
python veri_ekle.py
```
*Bu komut, ders notlarını vektörlere dönüştürerek `rag_veritabani.db` veritabanına kaydeder.*

### 3. Asistanı Çalıştırın
```bash
python rag_asistan.py
```

---

## Örnek Test Soruları

| Soru | Beklenen Yanıt Türü |
|------|---------------------|
| *Bernoulli dağılımının beklenen değeri nedir?* | E(X) = p, Varyans V(X) = p * q |
| *Binom dağılımı hangi koşullarda kullanılır?* | n bağımsız deneme, 2 olası sonuç, p sabit olasılık |
| *Poisson dağılımı hangi durumlarda tercih edilir?* | Nadir (ender) olaylar, n >= 20, p <= 0.05 |
| *Normal dağılımın %68 kuralı nedir?* | Ortalama etrafında mu +- 1*sigma %68 alan kaplar |

---

## Proje Yapısı

| Dosya | Açıklama |
|-------|----------|
| `veri_ekle.py` | Ders notlarını vektörleştirip SQLite veritabanına aktaran veri yükleme betiği |
| `rag_asistan.py` | Kullanıcı sorularını alıp semantik arama yapan ana RAG uygulaması |
| `soru_sor.py` | Vektör arama ve benzerlik skorlama modülü |
| `rag_veritabani.db` | Notların ve embeddinglerin saklandığı yerel veritabanı |
| `requirements.txt` | Proje bağımlılıkları |

---

## Lisans ve Teşekkür
Bu proje Microsoft Foundry Local yaz kampı kapsamında geliştirilmiştir. Ders materyalleri YTÜ İstatistik Bölümü IST1132 Olasılık müfredatına dayanmaktadır.
