from foundry_local_sdk import Configuration, FoundryLocalManager

ornek_metin = "Evimde 6 tane kedim var ve onlarla vakit geçirmeyi çok seviyorum."

print("Model hazırlanıyor ve metin vektöre dönüştürülüyor. Lütfen bekleyin...")

# 1. Foundry Local altyapısını başlatıyoruz
config = Configuration(app_name="YazKampiProjesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# 2. Embedding (Vektör) modelini seçip yüklüyoruz
model = manager.catalog.get_model("qwen3-embedding-0.6b")
model.load()

# 3. Vektör dönüştürücü aracı alıyoruz
embedding_client = model.get_embedding_client()

# 4. Metnimizi sayısal vektöre (embedding) çeviriyoruz
sonuc = embedding_client.generate_embedding(ornek_metin)

# Elde ettiğimiz matematiksel diziyi (vektörü) alalım
vektor = sonuc.data[0].embedding

print("\n--- SONUÇLAR ---")
print(f"Orijinal Metin: '{ornek_metin}'")
print(f"Bu metnin uzaydaki boyutu (koordinat sayısı): {len(vektor)}")
print(f"İşte yapay zekanın anladığı sayılar (sadece ilk 5 tanesi): {vektor[:5]}")