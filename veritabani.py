import sqlite3

# Veritabanına bağlan (eğer klasörde böyle bir dosya yoksa, otomatik olarak sıfırdan yaratır)
baglanti = sqlite3.connect("rag_veritabani.db")
isaretci = baglanti.cursor()

# Dokümanları ve vektörleri (embedding) tutacağımız tabloyu oluştur
isaretci.execute('''
CREATE TABLE IF NOT EXISTS belgeler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metin TEXT,
    vektor TEXT
)
''')

# Yaptığımız değişiklikleri kaydet ve bağlantıyı kapat
baglanti.commit()
baglanti.close()

print("Harika! Veritabanı ve belgeler tablosu başarıyla oluşturuldu.")