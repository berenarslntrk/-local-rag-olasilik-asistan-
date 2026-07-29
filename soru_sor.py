import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

# Kosinüs benzerliği hesaplayan fonksiyon (iki vektör ne kadar benzer?)
def kosinus_benzerligi(vektor1, vektor2):
    dot_product = sum(a * b for a, b in zip(vektor1, vektor2))
    norm_a = math.sqrt(sum(a * a for a in vektor1))
    norm_b = math.sqrt(sum(b * b for b in vektor2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

# Model baslatma - sadece 1 kez yapılır (singleton)
print("Model baslatiliyor, lutfen bekleyin...")
config = Configuration(app_name="YazKampiProjesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance
model = manager.catalog.get_model("qwen3-embedding-0.6b")
model.download()
model.load()
embedding_client = model.get_embedding_client()
print("Model hazir.\n")

def benzer_metinleri_bul(kullanici_sorusu, limit=2):
    print(f"\nSoru: '{kullanici_sorusu}'")
    print("Soru vektore donusturuluyor...")
    
    # 1. Soruyu vektöre (sayılara) çeviriyoruz
    soru_sonuc = embedding_client.generate_embedding(kullanici_sorusu)
    soru_vektoru = soru_sonuc.data[0].embedding
    
    # 2. Veritabanından tüm metinleri ve vektörleri çekiyoruz
    baglanti = sqlite3.connect("rag_veritabani.db")
    isaretci = baglanti.cursor()
    isaretci.execute("SELECT metin, vektor FROM belgeler")
    kayitlar = isaretci.fetchall()
    baglanti.close()
    
    if not kayitlar:
        print("Veritabani bos! Lutfen once veri_ekle.py dosyasini calistirin.")
        return []
        
    print("Veritabanindaki bilgilerle karsilastiriliyor...")
    
    # 3. Her bir metin için benzerlik skoru hesapla
    skorlar = []
    for metin, vektor_json in kayitlar:
        db_vektoru = json.loads(vektor_json)
        skor = kosinus_benzerligi(soru_vektoru, db_vektoru)
        skorlar.append((skor, metin))
        
    # 4. Skorları en yüksekten en düşüğe sırala
    skorlar.sort(key=lambda x: x[0], reverse=True)
    
    # Benzerlik eşiği: bu skorun altındaki sonuçlar "alakasız" sayılır
    ESIK = 0.35
    
    en_iyi_sonuclar = skorlar[:limit]
    
    # Eğer en iyi sonucun skoru bile eşiğin altındaysa, "bilmiyorum" de
    if en_iyi_sonuclar[0][0] < ESIK:
        print("\nBu konuda veritabaninda yeterli bilgi bulunamadi.")
        return []
    
    print("\n--- EN ALAKALI SONUCLAR ---")
    for i, (skor, metin) in enumerate(en_iyi_sonuclar, 1):
        if skor >= ESIK:
            print(f"{i}. Sonuc (Skor: {skor:.4f}): {metin}")
        
    return en_iyi_sonuclar

# Interaktif soru-cevap dongusu
if __name__ == "__main__":
    print("=" * 50)
    print("  RAG Soru-Cevap Sistemi")
    print("  Cikmak icin 'q' yazin")
    print("=" * 50)
    
    while True:
        soru = input("\nSorunuzu yazin: ").strip()
        if soru.lower() == 'q':
            print("Program sonlandirildi.")
            break
        if not soru:
            continue
        benzer_metinleri_bul(soru)
