"""İnsan Fizyolojisi ve Robot Sistemleri — fizyoloji tarafındaki sayıların kaynakları.
Buradaki her kaynak gerçektir (yazar, yıl, başlık, yayın yeri) ve 2026-10-10 tarihinde kaynağın kendi sayfasından, tam metninden
ya da yayın özetinden okunarak doğrulanmıştır; "dogrulama" alanı nereden okunduğunu söyler. Derslerde fizyolojiyle ilgili geçen
her sayı DEGER sözlüğünden gelir. Robot tarafındaki sayılar benzetim kaydından ve kol tablolarından gelir.
Bu dosya tıbbi tavsiye değildir; değerler sağlıklı yetişkinler için yayımlanmış ders kitabı değerleridir, kişiden kişiye değişir."""

ERISIM = "2026-10-10"

KAYNAKLAR = {
    "openstax_ap": dict(
        yazar="Betts, J. G., Young, K. A., Wise, J. A., et al.", yil=2022,
        baslik="Anatomy and Physiology 2e", yer="OpenStax, Rice University (açık ders kitabı)",
        adres="https://openstax.org/details/books/anatomy-and-physiology-2e",
        dogrulama="bölüm sayfaları tek tek okundu: 10.2, 10.3, 10.4, 10.5, 10.7, 10.8, 12.4, 12.5, 15.1, 18.1, 19.4, 22.3, 22.4, "
                  "22.5, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7"),
    "openstax_bio": dict(
        yazar="Clark, M. A., Douglas, M., & Choi, J.", yil=2018,
        baslik="Biology 2e", yer="OpenStax, Rice University (açık ders kitabı)",
        adres="https://openstax.org/details/books/biology-2e",
        dogrulama="bölüm 35.2 (Tablo 35.1: nöronun içinde ve dışında iyon derişimleri; sodyum potasyum pompası; sinaps gecikmesi) "
                  "ve bölüm 39.2 (akciğer hacim ve kapasiteleri tablosu, yetişkin erkek ortalaması; alveoler gaz denklemi örneği) okundu"),
    "openstax_fizik": dict(
        yazar="Urone, P. P., & Hinrichs, R.", yil=2022,
        baslik="College Physics 2e", yer="OpenStax, Rice University (açık ders kitabı)",
        adres="https://openstax.org/details/books/college-physics-2e",
        dogrulama="bölüm 7.6 (Tablo 7.1 besin enerjileri, Tablo 7.2 verimler), bölüm 7.8 (Tablo 7.4 bazal metabolizma, Tablo 7.5 "
                  "etkinliklere göre güç ve oksijen tüketimi), bölüm 11.2 (Tablo 11.1 yoğunluk) ve bölüm 14.2 (Tablo 14.1 öz ısı) okundu"),
    "byrne": dict(
        yazar="Byrne, J. H.", yil=2026,
        baslik="Neuroscience Online, Section 1: Chapter 1 (Resting Potentials and Action Potentials), Chapter 3 (Propagation of "
               "the Action Potential), Chapter 4 (Synaptic Transmission and the Skeletal Neuromuscular Junction)",
        yer="Neuroscience Online: An Electronic Textbook for the Neurosciences, UTHealth Houston (açık ders kitabı)",
        adres="https://nba.uth.tmc.edu/neuroscience/m/s1/chapter03.html",
        dogrulama="üç bölüm okundu: geçirgenlik oranı 0,01 (bölüm 1); iletim hızı saniyede 100 metreden 0,1 metrenin altına, hızı iki "
                  "katına çıkarmak için çap dört katına çıkmalı (bölüm 3); uç plak potansiyeli yaklaşık 50 mV, eşik için yaklaşık 30 mV "
                  "yeter (bölüm 4); sayfalar Ağustos–Eylül 2026'da gözden geçirilmiş"),
    "pool2011": dict(
        yazar="Pool, R. R., & Mato, G.", yil=2011,
        baslik="Inferring single neuron properties in conductance based balanced networks",
        yer="Frontiers in Computational Neuroscience, 5, 41 (açık erişim)", adres="https://doi.org/10.3389/fncom.2011.00041",
        dogrulama="tam metin Europe PMC'den okundu (PMC3191342), ek bölüm: Hodgkin ve Huxley (1952) modelinin mürekkep balığı dev "
                  "aksonu için 6,3 °C'deki parametreleri ve hız fonksiyonları (denklem A10–A19)"),
    "hodgkin1952": dict(
        yazar="Hodgkin, A. L., & Huxley, A. F.", yil=1952,
        baslik="A quantitative description of membrane current and its application to conduction and excitation in nerve",
        yer="The Journal of Physiology, 117, 500–544", adres="https://doi.org/10.1113/jphysiol.1952.sp004764",
        dogrulama="yayının künyesi Europe PMC kaydından okundu (PMID 12991237); modelin sayıları bu yayından değil, onları aynen "
                  "aktaran Pool ve Mato (2011) tam metninden alındı"),
    "binks2022": dict(
        yazar="Binks, A.", yil=2022,
        baslik="Pulmonary Physiology for Pre-Clinical Students", yer="Virginia Tech Publishing (açık ders kitabı, CC BY-NC-SA 4.0)",
        adres="https://pressbooks.lib.vt.edu/pulmonaryphysiology/",
        dogrulama="bölümler tam metin okundu: 3 (ölü boşluk 150 mL, dakika ve alveoler ventilasyon), 14 (alveoler gaz denklemi, "
                  "150 − 40 / 0,8 = 100), 16 (oksijen içeriği denklemi: 1,34 ve 0,003), 17 (solunumun denetimi, kemoreseptörler)"),
    "severinghaus1979": dict(
        yazar="Severinghaus, J. W.", yil=1979,
        baslik="Simple, accurate equations for human blood O2 dissociation computations",
        yer="Journal of Applied Physiology, 46(3), 599–602", adres="https://doi.org/10.1152/jappl.1979.46.3.599",
        dogrulama="yayın özeti Europe PMC kaydından okundu (PMID 35496): doygunluk denklemi S = 1 / (23400 / (P³ + 150 P) + 1), "
                  "insan kanının ölçünlü eğrisine ± 0,0055 içinde uyar"),
    "gordon1966": dict(
        yazar="Gordon, A. M., Huxley, A. F., & Julian, F. J.", yil=1966,
        baslik="The variation in isometric tension with sarcomere length in vertebrate muscle fibres",
        yer="The Journal of Physiology, 184, 170–192", adres="https://doi.org/10.1113/jphysiol.1966.sp007909",
        dogrulama="yayın özeti Europe PMC kaydından okundu (PMID 5921536): gerim eğrisinin tepesi 2,05 ile 2,2 mikrometre arasında "
                  "bir platodur; platonun altında düşüş yaklaşık 1,67 mikrometrede dikleşir (kurbağa kası lifi)"),
    "seow2013": dict(
        yazar="Seow, C. Y.", yil=2013,
        baslik="Hill's equation of muscle performance and its hidden insight on molecular mechanisms",
        yer="The Journal of General Physiology, 142(6), 561–573 (açık erişim)", adres="https://doi.org/10.1085/jgp.201311107",
        dogrulama="tam metin Europe PMC'den okundu (PMC3840917): Hill (1938) özgün uyumu (F + 14,35)(V + 1,03) = 87,6; en büyük güç "
                  "en büyük kuvvetin yaklaşık 0,3 katında"),
    "shishmarev2022": dict(
        yazar="Shishmarev, D., Rowland, E., Aditya, S., et al.", yil=2022,
        baslik="Molecular interactions of STAC proteins with skeletal muscle dihydropyridine receptor and excitation-contraction coupling",
        yer="Protein Science, 31, e4311 (açık erişim)", adres="https://doi.org/10.1002/pro.4311",
        dogrulama="yayın özeti Europe PMC kaydından okundu (PMID 35481653): iskelet kasında eşleşmenin kilit adımı iki kalsiyum "
                  "kanalının, dihidropiridin reseptörü ile riyanodin reseptörünün birlikte çalışmasıdır; bu kaynaktan sayı alınmadı"),
    "johnson2011": dict(
        yazar="Johnson, K. A., & Goody, R. S.", yil=2011,
        baslik="The original Michaelis constant: translation of the 1913 Michaelis–Menten paper",
        yer="Biochemistry, 50(39), 8264–8269", adres="https://doi.org/10.1021/bi201284u",
        dogrulama="yayın özeti Europe PMC kaydından okundu (PMID 21888353): tepkime hızı enzim–substrat bileşiğinin derişimiyle "
                  "orantılıdır (Michaelis–Menten denklemi); bu kaynaktan sayı alınmadı, yalnız denklemin künyesi"),
}

# ad: (değer, birim, kaynak anahtarı, kaynaktaki yer, açıklama)
DEGER = {
    # Hafta 1 · sinir sistemi
    "Na_dis_mM": (145, "mM", "openstax_bio", "Tablo 35.1", "hücre dışı sodyum derişimi"),
    "Na_ic_mM": (12, "mM", "openstax_bio", "Tablo 35.1", "hücre içi sodyum derişimi"),
    "K_dis_mM": (4, "mM", "openstax_bio", "Tablo 35.1", "hücre dışı potasyum derişimi"),
    "K_ic_mM": (155, "mM", "openstax_bio", "Tablo 35.1", "hücre içi potasyum derişimi"),
    "Cl_dis_mM": (120, "mM", "openstax_bio", "Tablo 35.1", "hücre dışı klor derişimi"),
    "Cl_ic_mM": (4, "mM", "openstax_bio", "Tablo 35.1", "hücre içi klor derişimi"),
    "pompa_Na": (3, "iyon", "openstax_bio", "35.2", "pompanın bir çevrimde dışarı attığı sodyum sayısı"),
    "pompa_K": (2, "iyon", "openstax_bio", "35.2", "pompanın bir çevrimde içeri aldığı potasyum sayısı"),
    "dinlenim_mV": (-70, "mV", "openstax_ap", "12.4", "dinlenim zar potansiyeli"),
    "esik_mV": (-55, "mV", "openstax_ap", "12.4", "eşik değer"),
    "tepe_mV": (30, "mV", "openstax_ap", "12.4", "aksiyon potansiyelinin tepe değeri"),
    "aksiyon_ms": (2, "ms", "openstax_ap", "12.4", "bir aksiyon potansiyelinin yaklaşık süresi"),
    "gecirgenlik_orani": (0.01, "oran", "byrne", "bölüm 1", "sodyum geçirgenliğinin potasyum geçirgenliğine oranı (mürekkep balığı aksonuna uyum)"),
    "hh_ENa_mV": (50.0, "mV", "pool2011", "ek, A13 sonrası", "model: sodyum denge potansiyeli"),
    "hh_EK_mV": (-77.0, "mV", "pool2011", "ek, A13 sonrası", "model: potasyum denge potansiyeli"),
    "hh_EL_mV": (-54.4, "mV", "pool2011", "ek, A13 sonrası", "model: sızıntı denge potansiyeli"),
    "hh_gNa": (120.0, "mS/cm²", "pool2011", "ek, A13 sonrası", "model: en büyük sodyum iletkenliği"),
    "hh_gK": (36.0, "mS/cm²", "pool2011", "ek, A13 sonrası", "model: en büyük potasyum iletkenliği"),
    "hh_gL": (0.3, "mS/cm²", "pool2011", "ek, A13 sonrası", "model: sızıntı iletkenliği"),
    "hh_C": (1.0, "µF/cm²", "pool2011", "ek, A13 sonrası", "model: zar sığası"),
    "hh_sicaklik_C": (6.3, "°C", "pool2011", "ek, A13 sonrası", "model parametrelerinin ölçüldüğü sıcaklık"),
    "sinir_hizi_en_hizli": (100.0, "m/s", "byrne", "bölüm 3", "sinirlerde en hızlı iletim"),
    "sinir_hizi_en_yavas": (0.1, "m/s", "byrne", "bölüm 3", "sinirlerde en yavaş iletim (bunun altı da var)"),
    "cap_kati": (4, "kat", "byrne", "bölüm 3", "hızı iki katına çıkarmak için aksonun çapının çıkması gereken kat"),
    "sinaps_gecikmesi_ms": (1, "ms", "openstax_bio", "35.2", "kimyasal sinapsta yaklaşık gecikme"),
    "ranvier_um": (1, "µm", "openstax_bio", "35.2", "miyelinsiz boğumun yaklaşık uzunluğu"),
    "uc_plak_mV": (50, "mV", "byrne", "bölüm 4", "sinir–kas kavşağında uç plak potansiyelinin yaklaşık büyüklüğü"),
    "uc_plak_esik_mV": (30, "mV", "byrne", "bölüm 4", "kas lifini eşiğe ulaştırmaya yeten yaklaşık büyüklük"),
    "zincir_gangliyon": (23, "adet", "openstax_ap", "15.1", "omurganın her yanındaki sempatik zincirde gangliyon sayısı"),
    # Hafta 2 · kas
    "sarkomer_um": (2.0, "µm", "openstax_ap", "10.2", "bir sarkomerin yaklaşık boyu"),
    "vuru_nm": (10, "nm", "openstax_ap", "10.3", "bir çapraz köprü vuruşunda ince ipliğin kaydığı yaklaşık yol"),
    "miyozin_adet": (300, "molekül", "openstax_ap", "10.3", "bir kalın iplikteki yaklaşık miyozin molekülü sayısı"),
    "plato_alt_um": (2.05, "µm", "gordon1966", "özet", "gerim platosunun alt ucu (kurbağa kası lifi)"),
    "plato_ust_um": (2.2, "µm", "gordon1966", "özet", "gerim platosunun üst ucu (kurbağa kası lifi)"),
    "kirilma_um": (1.67, "µm", "gordon1966", "özet", "platonun altında düşüşün dikleştiği sarkomer boyu"),
    "ideal_alt_yuzde": (80, "%", "openstax_ap", "10.4", "en büyük gerim için sarkomer boyunun dinlenim boyuna oranı, alt sınır"),
    "ideal_ust_yuzde": (120, "%", "openstax_ap", "10.4", "en büyük gerim için sarkomer boyunun dinlenim boyuna oranı, üst sınır"),
    "sarsi_ms": (100, "ms", "openstax_ap", "10.4", "tek sarsının kas tipine göre ulaşabildiği süre (birkaç milisaniye ile 100 ms arası)"),
    "motor_birim_kucuk": (6, "lif", "openstax_ap", "10.4", "göz kaslarında bir motor nöronun uyardığı yaklaşık lif sayısı"),
    "motor_birim_kuvvet_kati": (50, "kat", "openstax_ap", "10.4", "en büyük motor birimin en küçüğe göre üretebildiği kuvvet"),
    "tetanus_kat_alt": (3, "kat", "openstax_ap", "10.4", "tam olmayan tetanusta gerimin tek sarsıya oranı, alt"),
    "tetanus_kat_ust": (4, "kat", "openstax_ap", "10.4", "tam olmayan tetanusta gerimin tek sarsıya oranı, üst"),
    "hill_a": (14.35, "kuvvet birimi", "seow2013", "Şekil 2 açıklaması", "Hill (1938) özgün uyumunda a sabiti"),
    "hill_b": (1.03, "hız birimi", "seow2013", "Şekil 2 açıklaması", "Hill (1938) özgün uyumunda b sabiti"),
    "hill_c": (87.6, "kuvvet × hız", "seow2013", "Şekil 2 açıklaması", "Hill (1938) özgün uyumunda sağ taraf"),
    "hill_guc_kuvvet": (0.3, "oran", "seow2013", "metin", "en büyük gücün alındığı kuvvetin en büyük kuvvete yaklaşık oranı"),
    "hizli_lif_kat": (2, "kat", "openstax_ap", "10.5", "hızlı liflerin ATP'yi yavaş liflere göre parçalama hızı"),
    "kreatin_fosfat_s": (15, "s", "openstax_ap", "10.3", "kreatin fosfatın enerji sağlayabildiği yaklaşık süre"),
    "glikoliz_s": (60, "s", "openstax_ap", "10.3", "yalnız glikolizle sürdürülebilen yaklaşık kas etkinliği"),
    "oksijenli_pay_yuzde": (95, "%", "openstax_ap", "10.3", "dinlenen ya da orta etkinlikteki kasın ATP'sinde oksijenli solunumun payı"),
    "verim_kas_yuzde": (20, "%", "openstax_fizik", "Tablo 7.2", "bisiklet sürme ve tırmanmada insan bedeninin verimi"),
    "verim_motor_yuzde": (98, "%", "openstax_fizik", "Tablo 7.2", "elektrik motorunun verimi (temsilî değer)"),
    # Hafta 3 · solunum
    "TV_L": (0.5, "L", "openstax_bio", "39.2 tablo", "soluk hacmi (yetişkin erkek ortalaması)"),
    "IRV_L": (3.1, "L", "openstax_bio", "39.2 tablo", "soluk alma yedek hacmi"),
    "ERV_L": (1.2, "L", "openstax_bio", "39.2 tablo", "soluk verme yedek hacmi"),
    "RV_L": (1.2, "L", "openstax_bio", "39.2 tablo", "artık hacim"),
    "VC_L": (4.8, "L", "openstax_bio", "39.2 tablo", "dirim kapasitesi"),
    "IC_L": (3.6, "L", "openstax_bio", "39.2 tablo", "soluk alma kapasitesi"),
    "FRC_L": (2.4, "L", "openstax_bio", "39.2 tablo", "işlevsel artık kapasite"),
    "TLC_L": (6.0, "L", "openstax_bio", "39.2 tablo", "toplam akciğer kapasitesi"),
    "soluk_sayisi_alt": (12, "soluk/dk", "openstax_ap", "22.3", "olağan soluk sayısının alt sınırı"),
    "soluk_sayisi_ust": (18, "soluk/dk", "openstax_ap", "22.3", "olağan soluk sayısının üst sınırı"),
    "olu_bosluk_mL": (150, "mL", "binks2022", "bölüm 3", "anatomik ölü boşluk"),
    "ornek_soluk_sayisi": (10, "soluk/dk", "binks2022", "bölüm 3", "kitaptaki çözümlü örnekte soluk sayısı"),
    "atmosfer_mmHg": (760, "mmHg", "openstax_ap", "22.3", "deniz düzeyinde atmosfer basıncı"),
    "su_buhari_mmHg": (47, "mmHg", "openstax_ap", "22.4 Tablo 22.3", "alveol havasında su buharı basıncı"),
    "oksijen_orani": (0.21, "oran", "openstax_bio", "39.2", "kuru havada oksijenin payı (denklemde kullanılan)"),
    "PaCO2_mmHg": (40, "mmHg", "binks2022", "bölüm 14", "atardamar kanında olağan karbondioksit basıncı"),
    "solunum_orani": (0.8, "oran", "binks2022", "bölüm 14", "solunum değişim oranı (üretilen karbondioksit / tüketilen oksijen)"),
    "PAO2_tablo_mmHg": (104, "mmHg", "openstax_ap", "22.4 Tablo 22.3", "alveol havasında oksijen basıncı (tablo değeri)"),
    "PvO2_mmHg": (40, "mmHg", "openstax_ap", "22.4", "dokudan dönen kanda oksijen basıncı"),
    "PvCO2_mmHg": (45, "mmHg", "openstax_ap", "22.4", "dokudan dönen kanda karbondioksit basıncı"),
    "hb_kapasite": (1.34, "mL/g", "binks2022", "bölüm 16", "bir gram hemoglobinin taşıyabildiği oksijen"),
    "cozunurluk": (0.003, "mL/dL/mmHg", "binks2022", "bölüm 16", "oksijenin kanda çözünme katsayısı"),
    "co2_bikarbonat_yuzde": (70, "%", "openstax_ap", "22.5", "karbondioksitin bikarbonat olarak taşınan payı"),
    "co2_hb_yuzde": (20, "%", "openstax_ap", "22.5", "karbondioksitin hemoglobine bağlı taşınan payı"),
    "co2_cozunmus_alt": (7, "%", "openstax_ap", "22.5", "karbondioksitin çözünmüş taşınan payı, alt"),
    "co2_cozunmus_ust": (10, "%", "openstax_ap", "22.5", "karbondioksitin çözünmüş taşınan payı, üst"),
    "kalp_debisi_L_dk": (5.25, "L/dk", "openstax_ap", "19.4", "dinlenimde ortalama kalp debisi"),
    "oksijen_tuketimi_mL_dk": (250, "mL/dk", "openstax_fizik", "Tablo 7.4", "dinlenimde oksijen tüketimi (tablo toplamı)"),
    "oksijen_kJ_litre": (20, "kJ/L", "openstax_fizik", "7.8", "tüketilen bir litre oksijen başına açığa çıkan enerji"),
    "bazal_guc_W": (85, "W", "openstax_fizik", "Tablo 7.4", "dinlenimde bazal metabolizma gücü (tablo toplamı)"),
    "oturma_guc_W": (120, "W", "openstax_fizik", "Tablo 7.5", "otururken toplam güç"),
    "yurume_guc_W": (280, "W", "openstax_fizik", "Tablo 7.5", "saatte beş kilometre yürürken toplam güç"),
    "hava_yogunluk": (1.29, "kg/m³", "openstax_fizik", "Tablo 11.1", "havanın yoğunluğu"),
    "hava_oz_isi": (1015, "J/kg·°C", "openstax_fizik", "Tablo 14.1", "kuru havanın sabit basınçta öz ısısı"),
    "periferik_esik_mmHg": (60, "mmHg", "openstax_ap", "22.3", "çevresel kemoreseptörlerin solunumu artırdığı oksijen basıncı (yaklaşık ve altı)"),
    "merkezi_pay_yuzde": (80, "%", "binks2022", "bölüm 17", "karbondioksit yanıtında merkezî kemoreseptörlerin payı"),
    # Hafta 4 · sindirim
    "yemek_borusu_cm": (25.4, "cm", "openstax_ap", "23.3", "yemek borusunun yaklaşık uzunluğu"),
    "yutma_alt_s": (4, "s", "openstax_ap", "23.3", "katı lokmanın yutulma süresi, alt"),
    "yutma_ust_s": (8, "s", "openstax_ap", "23.3", "katı lokmanın yutulma süresi, üst"),
    "mide_dalga_s": (20, "s", "openstax_ap", "23.4", "midede karıştırma dalgalarının aralığı"),
    "mide_bosalma_alt_h": (2, "saat", "openstax_ap", "23.4", "midenin boşalma süresi, alt"),
    "mide_bosalma_ust_h": (4, "saat", "openstax_ap", "23.4", "midenin boşalma süresi, üst"),
    "segment_duodenum_dk": (12, "1/dk", "openstax_ap", "23.5", "onikiparmak bağırsağında segmentasyon sıklığı"),
    "segment_ileum_dk": (8, "1/dk", "openstax_ap", "23.5", "ileumda segmentasyon sıklığı"),
    "ince_bagirsak_m": (3.05, "m", "openstax_ap", "23.5", "ince bağırsağın canlıdaki yaklaşık uzunluğu"),
    "ince_gecis_alt_h": (3, "saat", "openstax_ap", "23.5", "kimusun ince bağırsaktan geçiş süresi, alt"),
    "ince_gecis_ust_h": (5, "saat", "openstax_ap", "23.5", "kimusun ince bağırsaktan geçiş süresi, üst"),
    "kalin_bekleme_alt_h": (12, "saat", "openstax_ap", "23.5", "artığın kalın bağırsakta kalma süresi, alt"),
    "kalin_bekleme_ust_h": (24, "saat", "openstax_ap", "23.5", "artığın kalın bağırsakta kalma süresi, üst"),
    "kanal_m": (7.62, "m", "openstax_ap", "23.1", "sindirim kanalının canlıdaki yaklaşık uzunluğu"),
    "tukuruk_alt_L": (1.0, "L/gün", "openstax_ap", "23.3", "günlük tükürük, alt"),
    "tukuruk_ust_L": (1.5, "L/gün", "openstax_ap", "23.3", "günlük tükürük, üst"),
    "tukuruk_pH_alt": (6.35, "pH", "openstax_ap", "23.3", "tükürüğün pH değeri, alt"),
    "tukuruk_pH_ust": (6.85, "pH", "openstax_ap", "23.3", "tükürüğün pH değeri, üst"),
    "mide_pH_alt": (1.5, "pH", "openstax_ap", "23.4", "mide içeriğinin pH değeri, alt"),
    "mide_pH_ust": (3.5, "pH", "openstax_ap", "23.4", "mide içeriğinin pH değeri, üst"),
    "pankreas_pH_alt": (7.1, "pH", "openstax_ap", "23.6", "pankreas özsuyunun pH değeri, alt"),
    "pankreas_pH_ust": (8.2, "pH", "openstax_ap", "23.6", "pankreas özsuyunun pH değeri, üst"),
    "safra_L": (1.0, "L/gün", "openstax_ap", "23.6", "günlük safra (yaklaşık)"),
    "safra_pH_alt": (7.6, "pH", "openstax_ap", "23.6", "safranın pH değeri, alt"),
    "safra_pH_ust": (8.6, "pH", "openstax_ap", "23.6", "safranın pH değeri, üst"),
    "kan_pH": (7.4, "pH", "openstax_ap", "18.1", "kanın ortalama pH değeri"),
    "bagirsaga_giren_L": (9, "L/gün", "openstax_ap", "23.7", "ince bağırsağa günde giren sıvı"),
    "icilen_L": (2.3, "L/gün", "openstax_ap", "23.7", "bunun yiyecek ve içecekten gelen payı"),
    "su_emilim_yuzde": (90, "%", "openstax_ap", "23.7", "suyun ince bağırsakta emilen payı"),
    "emilim_yuzeyi_m2": (200, "m²", "openstax_ap", "23.5", "ince bağırsağın emilim yüzeyi (yaklaşık)"),
    "yuzey_kati": (600, "kat", "openstax_ap", "23.5", "kıvrım, villus ve mikrovillusun yüzeyi artırma katı (en az)"),
    "karbonhidrat_emilim_g_saat": (120, "g/saat", "openstax_ap", "23.7", "karbonhidrat emiliminin tahmini üst hızı"),
    "karbonhidrat_kJ_g": (17, "kJ/g", "openstax_fizik", "Tablo 7.1", "bir gram karbonhidratın enerjisi"),
    "protein_kJ_g": (17, "kJ/g", "openstax_fizik", "Tablo 7.1", "bir gram proteinin enerjisi"),
    "yag_kJ_g": (39, "kJ/g", "openstax_fizik", "Tablo 7.1", "bir gram yağın enerjisi"),
    "gunluk_besin_MJ": (12, "MJ", "openstax_fizik", "Tablo 7.1", "önerilen günlük yetişkin besin enerjisi"),
    "enterik_noron_milyon": (100, "milyon", "openstax_ap", "23.1", "enterik sinir sistemindeki yaklaşık nöron sayısı"),
    "mide_evresi_alt_h": (3, "saat", "openstax_ap", "23.4", "mide salgısının mide evresinin süresi, alt"),
    "mide_evresi_ust_h": (4, "saat", "openstax_ap", "23.4", "mide salgısının mide evresinin süresi, üst"),
    "kan_hacmi_L": (5, "L", "openstax_ap", "18.1", "yetişkin erkekte kan hacmi (5 ile 6 litre arası, alt değer)"),
}


def deger(ad):
    """Kaynaklı bir fizyoloji değerini sayı olarak döndürür."""
    return DEGER[ad][0]


def kunye(ad):
    """Değerin kısa künyesi: yazar (yıl), kaynaktaki yer."""
    d = DEGER[ad]
    k = KAYNAKLAR[d[2]]
    return f'{k["yazar"].split(",")[0]} ({k["yil"]}), {d[3]}'


def kaynakca():
    """Kaynakça satırları (yazar soyadına göre sıralı)."""
    return [f'{k["yazar"]} ({k["yil"]}). {k["baslik"]}. {k["yer"]}. Erişim: {ERISIM}.'
            for k in sorted(KAYNAKLAR.values(), key=lambda k: k["yazar"])]


if __name__ == "__main__":
    print(len(KAYNAKLAR), "kaynak ·", len(DEGER), "değer")
    for s in kaynakca():
        print(" ", s)
