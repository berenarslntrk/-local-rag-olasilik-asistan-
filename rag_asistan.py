import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

def kosinus_benzerligi(vektor1, vektor2):
    dot_product = sum(a * b for a, b in zip(vektor1, vektor2))
    norm_a = math.sqrt(sum(a * a for a in vektor1))
    norm_b = math.sqrt(sum(b * b for b in vektor2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

print("=" * 60)
print("   IST1132 Olasılık Dersi Yapay Zeka Asistanı (RAG)")
print("  Microsoft Foundry Local ile Çevrimdışı / Yerel Çalışır")
print("=" * 60)
print("\nYapay zeka modelleri hazırlanıyor, lütfen bekleyin...")

config = Configuration(app_name="YazKampiOlasilikRAG")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Embedding Modelini Yükle
embed_model = manager.catalog.get_model("qwen3-embedding-0.6b")
embed_model.download()
embed_model.load()
embedding_client = embed_model.get_embedding_client()
print("✓ Embedding Modeli Hazır (qwen3-embedding-0.6b)")

print("\n Sistem hazır! Olasılık dersi hakkındaki sorularınızı yazabilirsiniz.")
print("  (Çıkmak için 'q' yazabilirsiniz)")

def soru_cevapla(kullanici_sorusu, limit=3, esik=0.25):
    print(f"\n Soru: '{kullanici_sorusu}'")
    print("⏳ Sorunuz vektöre çevrilip ders notlarında semantik arama yapılıyor...")
    
    # 1. Soruyu Vektöre Çevir
    soru_sonuc = embedding_client.generate_embedding(kullanici_sorusu)
    soru_vektoru = soru_sonuc.data[0].embedding
    
    # 2. SQLite Veritabanından Notları Çek
    baglanti = sqlite3.connect("rag_veritabani.db")
    isaretci = baglanti.cursor()
    isaretci.execute("SELECT metin, vektor FROM belgeler")
    kayitlar = isaretci.fetchall()
    baglanti.close()
    
    if not kayitlar:
        print("Veritabanı boş! Lütfen önce veri_ekle.py çalıştırarak ders notlarını yükleyin.")
        return
    
    # 3. Benzerlik Skorlarını Hesapla
    skorlar = []
    for metin, vektor_json in kayitlar:
        db_vektoru = json.loads(vektor_json)
        skor = kosinus_benzerligi(soru_vektoru, db_vektoru)
        skorlar.append((skor, metin))
        
    skorlar.sort(key=lambda x: x[0], reverse=True)
    en_iyi_sonuclar = skorlar[:limit]
    
    # Eşik Kontrolü
    if en_iyi_sonuclar[0][0] < esik:
        print("\n Bu konuda IST1132 Olasılık ders notlarında yeterli bilgi bulunamadı.")
        return

    print("\n------------------------------------------------------------")
    print(" ASİSTAN YANITI (Ders Notlarından Bulunan Formüller ve Açıklamalar):")
    print("------------------------------------------------------------")
    bulunan_sayi = 0
    for i, (skor, metin) in enumerate(en_iyi_sonuclar, 1):
        if skor >= esik:
            bulunan_sayi += 1
            print(f"\n Not Parçası [{i}] (Uyum Skoru: %{skor*100:.1f}):")
            print(f"   {metin}")
    print("------------------------------------------------------------")

if __name__ == "__main__":
    while True:
        try:
            soru = input("\n Sorunuzu yazın: ").strip()
            if soru.lower() == 'q':
                print("İyi çalışmalar, başarılar! ")
                break
            if not soru:
                continue
            soru_cevapla(soru)
        except (KeyboardInterrupt, EOFError):
            print("\nÇıkış yapıldı.")
            breakbinom dağı
