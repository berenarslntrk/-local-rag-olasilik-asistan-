import sqlite3

# Veritabanına bağlan
baglanti = sqlite3.connect("rag_veritabani.db")
isaretci = baglanti.cursor()

# Önce kaç kayıt var görelim
isaretci.execute("SELECT COUNT(*) FROM belgeler")
print(f"Toplam kayit sayisi: {isaretci.fetchone()[0]}")

# Tüm kayıtları görelim
isaretci.execute("SELECT id, metin FROM belgeler")
for satir in isaretci.fetchall():
    print(f"  ID {satir[0]}: {satir[1][:60]}...")

# Tekrarlanan kayıtları temizle (sadece benzersiz metinleri tut)
isaretci.execute('''
    DELETE FROM belgeler 
    WHERE id NOT IN (
        SELECT MIN(id) FROM belgeler GROUP BY metin
    )
''')
silinen = isaretci.rowcount

baglanti.commit()

print(f"\n{silinen} adet tekrarlanan kayit silindi.")
isaretci.execute("SELECT COUNT(*) FROM belgeler")
print(f"Kalan kayit sayisi: {isaretci.fetchone()[0]}")

baglanti.close()
