import sqlite3
import json
from foundry_local_sdk import Configuration, FoundryLocalManager

# IST1132 Olasılık Dersi Ders Notları (Öğrenci Çalışma Notları Formatında)
ders_notlari = [
    # Genel Bilgiler
    "Ders Bilgisi: IST1132 Olasılık, Prof. Dr. Fatma NOYAN TEKELİ. Değerlendirme: 2 Vize (%60) + 1 Final (%40). Not hesabı: Dönem içi %60, final %40.",

    # Genel Dağılım Kavramları ve Farkları
    "Kesikli ve Sürekli Dağılım Farkı: 1) Kesikli Dağılım: Sayılabilir ayrık değerler alır (zar atışı, tura sayısı, hatalı parça sayısı). Olasılık fonksiyonu f(x)=P(X=x) ile hesaplanır. Örnek: Bernoulli, Binom, Poisson. 2) Sürekli Dağılım: Aralıktaki tüm reel değerleri alabilir, ölçülür (zaman, boy, kilo, sıcaklık). Nokta olasılığı 0'dır P(X=a)=0, alan (integral) hesaplanır. Örnek: Normal Dağılım.",

    # Hafta 1: Kesikli Düzgün & Bernoulli
    "Kesikli Düzgün (Uniform) Dağılım: n farklı sonucun hepsinin olasılığı eşittir. f(x) = 1/n. Ortalaması E(X) = (n+1)/2, Varyansı V(X) = (n^2 - 1)/12. Örnek: Hilesiz tavla zarı atışında her yüzün olasılığı 1/6'dır.",

    "Bernoulli Dağılımı: Tek bir denemede sadece 2 olası sonuç vardır (Başarı 1, Başarısızlık 0). f(x) = (p^x) * (q^(1-x)). Ortalaması E(X) = p, Varyansı V(X) = p*q (q = 1-p).",

    # Hafta 2: Binom Dağılımı
    "Binom Dağılımı: n bağımsız Bernoulli denemesinde x başarı alma olasılığıdır. Koşulları: n deneme var, 2 sonuç var, p sabit, denemeler bağımsız. Olasılık Formülü: f(x) = P(X=x) = C(n,x) * (p^x) * (q^(n-x)) = [n! / (x! * (n-x)!)] * (p^x) * (q^(n-x)). Ortalaması E(X) = n*p, Varyansı V(X) = n*p*q.",

    # Hafta 3: Hipergeometrik, Geometrik, Negatif Binom
    "Hipergeometrik Dağılım: İadesiz (tekrarsız) çekimlerde kullanılır, denemeler bağımsız değildir. N toplam nesne, 'a' ilgilenilen nesne, n seçilen örneklem. Formül: f(x) = [C(a,x) * C(N-a, n-x)] / C(N,n). E(X) = n*(a/N). n/N <= 0.05 ise Binom'a yaklaşır.",

    "Geometrik Dağılım: İlk başarıyı elde edene kadar yapılan deneme sayısı X'tir. Formül: f(x) = (q^(x-1)) * p (x=1,2,3...). Ortalaması E(X) = 1/p, Varyansı V(X) = (1-p)/(p^2). Dağılım daima sağa çarpıktır.",

    "Negatif Binom (Paskal) Dağılımı: r. başarıyı elde edene kadar yapılan deneme sayısı X'tir. Formül: f(x) = C(x-1, r-1) * (p^r) * (q^(x-r)). Ortalaması E(X) = r/p, Varyansı V(X) = r*q/(p^2). r=1 olursa Geometrik dağılım olur.",

    # Hafta 4: Poisson & Çok Terimli Dağılım
    "Poisson Dağılımı: Belirli zaman veya alanda nadir (ender) gerçekleşen olayların sayısıdır (n çok büyük, p çok küçük). λ (lambda) birim zamandaki ortalama olay sayısıdır. Formül: f(x) = (e^(-λ) * λ^x) / x!. Ortalaması E(X) = λ, Varyansı V(X) = λ.",

    "Binom'dan Poisson'a Yakınsama: Deney sayısı n >= 20 ve p <= 0.05 olduğunda Binom yerine λ = n*p kullanılarak Poisson dağılımı hesaplanır.",

    "Çok Terimli (Multinomial) Dağılım: Binom'un k > 2 sonuçlu halidir. Formül: f(x1..xk) = [n! / (x1! * x2! * ... * xk!)] * (p1^x1 * p2^x2 * ... * pk^xk). Ortalaması E(Xi) = n*pi, Varyansı V(Xi) = n*pi*(1-pi).",

    # Hafta 5: Normal Dağılım ve Yakınsamalar
    "Normal Dağılım (Çan Eğrisi): Sürekli değişkenler için N(μ, σ^2) dağılımıdır. Ortalama μ etrafında simetriktir. Ortalama = Mod = Medyan'dır. Toplam alan 1'dir. μ±1σ %68, μ±2σ %95, μ±3σ %99.7 alan kaplar.",

    "Standart Normal Dağılım (Z Dönüşümü): Ortalaması 0, varyansı 1 olan N(0,1) dağılımıdır. Dönüşüm Formülü: Z = (X - μ) / σ. Olasılıklar Z tablosundan bulunur.",

    "Binom ve Poisson'un Normal'e Yakınsaması (Süreklilik Düzeltmesi): Kesikli dağılımlar sürekli Normal dağılıma yakınsadığında ±0.5 Süreklilik Düzeltmesi (Continuity Correction) yapılır. Formül: Z = (x ± 0.5 - np) / sqrt(npq)."
]

print("Veritabanı sıfırlanıyor ve yeniden oluşturuluyor...")
baglanti = sqlite3.connect("rag_veritabani.db")
isaretci = baglanti.cursor()
isaretci.execute("DROP TABLE IF EXISTS belgeler")
isaretci.execute('''
CREATE TABLE belgeler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metin TEXT,
    vektor TEXT
)
''')
baglanti.commit()

print("Foundry Local Embedding modeli yükleniyor...")
config = Configuration(app_name="YazKampiProjesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("qwen3-embedding-0.6b")
model.download()
model.load()
embedding_client = model.get_embedding_client()

print("IST1132 Olasılık Dersi notları veritabanına ekleniyor...")
for i, metin in enumerate(ders_notlari, 1):
    sonuc = embedding_client.generate_embedding(metin)
    vektor = sonuc.data[0].embedding
    vektor_json = json.dumps(vektor)
    isaretci.execute("INSERT INTO belgeler (metin, vektor) VALUES (?, ?)", (metin, vektor_json))
    print(f"[{i}/{len(ders_notlari)}] Eklendi: {metin[:50]}...")

baglanti.commit()
baglanti.close()

print("\nIST1132 Olasılık Dersi Bilgi Tabanı başarıyla güncellendi.")
