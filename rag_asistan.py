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
print("  IST1132 Olasılık Dersi Arama ve Yanıtlama Sistemi (RAG)")
print("  Microsoft Foundry Local Framework - On-Device Inference")
print("=" * 60)
print("\nModeller yükleniyor, lütfen bekleyin...")

config = Configuration(app_name="YazKampiOlasilikRAG")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Embedding Modelini Yükle
embed_model = manager.catalog.get_model("qwen3-embedding-0.6b")
embed_model.download()
embed_model.load()
embedding_client = embed_model.get_embedding_client()
print("[OK] Embedding Modeli Yuklendi (qwen3-embedding-0.6b)")

print("\nSistem hazir. Sorunuzu yazabilirsiniz.")
print("Çıkış yapmak için 'q' giriniz.\n")

def soru_cevapla(kullanici_sorusu, limit=3):
    print(f"\nSoru: '{kullanici_sorusu}'")
    print("Ders notlarinda semantik arama yapiliyor...")
    
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
        print("[HATA] Veritabanı bos! Lutfen önce veri_ekle.py dosyasini calistirin.")
        return
    
    # 3. Benzerlik Skorlarını Hesapla
    skorlar = []
    for metin, vektor_json in kayitlar:
        db_vektoru = json.loads(vektor_json)
        skor = kosinus_benzerligi(soru_vektoru, db_vektoru)
        skorlar.append((skor, metin))
        
    skorlar.sort(key=lambda x: x[0], reverse=True)
    en_iyi_sonuclar = skorlar[:limit]

    # En Alakalı 1. Sonuç Ana Cevap Olarak Sunulur
    ana_skor, ana_cevap = en_iyi_sonuclar[0]

    print("\n" + "=" * 60)
    print("YANIT (Ders Notlarindan Getirilen En Yüksek Benzerlikli Bilgi):")
    print("=" * 60)
    print(f"\n[Ana Bilgi]: {ana_cevap}")
    print(f"\n[Benzerlik Skoru]: %{ana_skor*100:.2f}")
    
    # Diğer Destekleyici Bilgiler (Varsa)
    if len(en_iyi_sonuclar) > 1:
        print("\n" + "-" * 60)
        print("Destekleyici / Iliskili Ek Notlar:")
        for i, (skor, metin) in enumerate(en_iyi_sonuclar[1:], 2):
            print(f"  * [Ek Not {i}] (Benzerlik: %{skor*100:.2f}): {metin[:110]}...")
    print("=" * 60)

if __name__ == "__main__":
    while True:
        try:
            soru = input("\nSorunuzu giriniz: ").strip()
            if soru.lower() == 'q':
                print("Program sonlandirildi.")
                break
            if not soru:
                continue
            soru_cevapla(soru)
        except (KeyboardInterrupt, EOFError):
            print("\nProgram sonlandirildi.")
            break
