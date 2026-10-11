# İnsan Fizyolojisi ve Robot Sistemleri — kurs dosyaları

Forenly AI Academy'deki **İnsan Fizyolojisi ve Robot Sistemleri** kursunun dosyaları. Derslerde ekranda gördüğünüz her Python oturumu, çizelge ve şekil bu betiklerle üretildi; her dersin görevinin yanıtını da buradaki denetim betiğiyle sınarsınız.

Kursu izlemek için program yazmanız gerekmez. Görevleri kâğıt, kalem ve hesap makinesiyle yaparsınız.

> Bu kurs sınav hazırlığı ve kavram öğretimi içindir. Tıbbi tavsiye, tanı, kişisel değer yorumu ya da beslenme önerisi içermez.

## Görevinizi denetleyin

Her dersin sonunda farklı sayılarla bir görev verilir. Yanıtınızı şöyle sınarsınız:

```
python gorev_denetle.py                 # 16 görevin listesi
python gorev_denetle.py 1.1 -79,2       # Ders 1.1 görevinin yanıtı (virgül ya da nokta)
python gorev_denetle.py 4.4 sekretin    # yazıyla yanıtlanan görev
```

Betik "DOĞRU" ya da "HENÜZ DEĞİL" der ve yanlışsa bir ipucu verir. Python kurmak istemezseniz beklenen yanıtlar `beklenen/GOREVLER.json` içinde yazılıdır; önce kendiniz hesaplayın, sonra bakın.

## Gerekenler

- **Python 3.10 veya üstü**, `numpy` (2.0 ya da üstü) ve `matplotlib`. Hepsi ücretsizdir. Kurs Python 3.12.3, NumPy 2.5.3 ve Matplotlib 3.11.2 ile 10 Ekim 2026'da denendi.
- Kurulum: `python -m pip install -r requirements.txt`
- Denetim betiği (`gorev_denetle.py`) yalnız Python ister, ek paket gerekmez.
- Bilgisayarınıza kurmak istemezseniz tarayıcıda çalışan bir not defterine (ör. Google Colab) bu klasörü yükleyip aynı betikleri çalıştırabilirsiniz.

## Hesapları yineleyin

1. Bu depoyu indirin (Code → Download ZIP) ve klasörde bir terminal açın.
2. Haftaları sırayla çalıştırın: `python hafta1.py`, `python hafta2.py`, `python hafta3.py`, `python hafta4.py` (hafta 1 zar modelini çalıştırdığı için yaklaşık on saniye sürer).
3. Betikler çalışınca `ekran/<ders>/` klasöründe şekiller (`.png`) ve Python oturum kayıtları (`.txt`), kökte de ölçülen sayılar (`OLCUMLER.json`) ve görev yanıtları (`GOREVLER.json`) oluşur.
4. İsteğe bağlı: `python komut_ciz.py` oturum kayıtlarını derslerdeki gibi resme çizer (Pillow gerekir).

`beklenen/OLCUMLER.json` ekibimizin 2026-10-10 koşumunda bulduğu sayılardır; `beklenen/ekran/` aynı koşumun şekilleri ve oturum kayıtlarıdır. Hesaplarda rastgele sayı yoktur; aynı sayıları bulmanız beklenir.

## Bitirme işi

Kursun sonunda **dört sistem karşılaştırma dosyası** teslim edersiniz. Ne isteneceği ve nasıl ölçüleceği `RUBRIK.md` içinde; her haftanın son dersinde dolduracağınız çizelgelerin boş kalıbı `CIZELGE.md` içinde.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `gorev_denetle.py` | 16 dersin görev yanıtını denetler |
| `RUBRIK.md` | Bitirme işi ve ölçüt çizelgesi |
| `CIZELGE.md` | Hafta ürünleri ve bitirme dosyası için boş kalıp |
| `ortak.py` | Kaydı okuma (`kayit`), ölçüm ve görev yanıtı yazma, oturum kaydı ve şekil kaydetme |
| `arac.py` | Ortak hesaplar: robot sayıları, zar modeli, Hill denklemi, hemoglobin doygunluğu, karşılaştırma çizelgesi çizimi |
| `kaynaklar.py` | Fizyolojiyle ilgili her sayının kaynağı: 12 kaynak, 128 değer; her kaynağın nasıl doğrulandığı (`python kaynaklar.py` kaynakçayı yazar) |
| `hafta1.py` | Sinir sistemi: Nernst ve Goldman, zar modeliyle aksiyon potansiyeli, iletim ve sinaps gecikmesi, otonom yol |
| `hafta2.py` | Kas: sarkomer ve uzunluk–gerim, eşleşme zinciri, Hill kuvvet–hız eğrisi, lif tipleri ve enerji |
| `hafta3.py` | Solunum: hacim ve kapasiteler, ventilasyon ve ölü boşluk, alveoler gaz denklemi ve ayrışma eğrisi, kemorefleks modeli |
| `hafta4.py` | Sindirim: geçiş süreleri ve hızlar, pH ve enzim doyması, emilim ve enerji dengesi, denetim katmanları |
| `komut_ciz.py` | Oturum kayıtlarını resme çizer (isteğe bağlı) |
| `veri/cay_servisi_kaydi.csv` | Çay servisi benzetim kaydı: zaman, dört eklem açısı, dirsek hızı, bardağın konumu × 5666 örnek (saniyede 50) |
| `veri/sag_kol_kutle.csv` | Robotun sağ kol parçalarının kütlesi ve eklemlere uzaklığı (el kütlesi VARSAYIM) |
| `veri/sag_kol_parametre.csv` | Dört eklemin denetim kazançları, tork ve hız sınırları, açı sınırları |

## Veri ve kaynaklar hakkında

Robot verisi **benzetim kaydıdır**, gerçek robot ölçümü değildir. Kayıt, Forenly AI'nin bir insansı robota bir kafede çay servisini benzetimde yaptırdığı bir bölümden alınmıştır. Kayıtta elektrik tüketimi, pil, sıcaklık ve hava akışı verisi yoktur.

Fizyolojiyle ilgili her sayı `kaynaklar.py` içindeki ders kitaplarından ve hakemli yayınlardan gelir; değerler yayımlanmış ortalamalardır, kişiden kişiye değişir.

Şunlar **ÖRNEK**, **ŞEMATİK** ya da **MODEL HESABI**'dır, ölçüm değildir (kodda adlarında `ORNEK` ya da `SEMATIK` geçer):

- Zar modeli (Ders 1.2): Hodgkin–Huxley modeli, mürekkep balığı dev aksonu, 6,3 °C. İnsan nöronunun ölçümü değildir; sınav için ders kitabı değerleri ayrıca verilir.
- Otonom yolun lif boyları ve seçilen hızlar (Ders 1.4); lif boyu ve kısalma oranı (Ders 2.1); hemoglobin derişimi 15 g/dL (Ders 3.3); soğutma havasının 10 °C sıcaklık farkı (Ders 3.2); kemorefleks kazancı (Ders 3.4); örnek öğün (Ders 4.3).
- Uzunluk–gerim eğrisinin iki ucu şematiktir; platosu ve kırılma noktası yayından alınmıştır (kurbağa kası). Kuvvet–hız eğrisi Hill'in kurbağa kasındaki özgün uyumudur.
- Eklem döngüsü yanıtı, kalıcı sapma ve doyma açısı (Ders 2.2, 3.4, 4.2): kazançlar tablodan, hesap bir model.
- Tutma torku ve mekanik iş: ön kolun yatayla açısı = omuz açısı + dirsek açısı kabul eden kaba bir model.
- Verimler (kas yüzde 20, elektrik motoru yüzde 98) ders kitabının temsilî değerleridir; bu robotun ölçümü değildir.

Robot canlı sistemin aynısı değildir; derslerde her karşılaştırma benzerlik kadar farkla yapılır.

## Yapay zekâ beyanı

Anlatım metni, seslendirme, şekiller ve bu betikler yapay zekâ araçlarıyla üretildi. Her hesap gerçekten çalıştırıldı, her fizyoloji sayısı kaynağından okunarak doğrulandı. Siz de bir yapay zekâ aracı kullanırsanız aynı yolu izleyin: verdiği her sayıyı bir ders kitabında bulun, hesabı kendiniz yineleyin ve `gorev_denetle.py` ile sınayın; kaynağını bulamadığınız sayıyı kullanmayın.
