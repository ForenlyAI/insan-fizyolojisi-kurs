"""Hafta 3 · Solunum — Ders 3.1–3.4.
Fizyoloji sayıları kaynaklar.py'den, robot sayıları benzetim kaydından ve kol tablolarından gelir.
Spirometri izi tablodaki hacimlerden çizilmiş ŞEMATİK bir izdir (ölçüm değil). Hemoglobin derişimi ÖRNEK'tir (15 g/dL).
Kemorefleks hesabı MODEL HESABIDIR: denetleyicinin kazancı ÖRNEK; gerçek solunum denetiminde başka girdiler de vardır.
  python hafta3.py   → ekran/3.x/*.txt + *.png, OLCUMLER.json (d3_*), GOREVLER.json"""
import numpy as np
import matplotlib.pyplot as plt
from ortak import olc, oturum, sekil, gorev
from arac import (robot_ozet, doygunluk, kutu, ok, bos_eksen, cizelge, tr, sayi, TURUNCU, MAVI, YESIL, MOR, GRI, INSAN, ROBOT)
from kaynaklar import deger

ORNEK_HB = 15.0            # g/dL · ÖRNEK hemoglobin derişimi
ORNEK_DT = 10.0            # °C · ÖRNEK: soğutma havasının giriş ve çıkışı arasındaki sıcaklık farkı
ORNEK_KAZANC = 2.0         # L/dk/mmHg · ÖRNEK: kemorefleks modelinde denetleyici kazancı
ORNEK_BASINC = 523.0       # mmHg · ÖRNEK: görevde kullanılan düşük atmosfer basıncı


def ders_3_1():
    """Akciğer hacim ve kapasiteleri ↔ eklemin kullandığı pay."""
    TV, IRV, ERV, RV = deger("TV_L"), deger("IRV_L"), deger("ERV_L"), deger("RV_L")
    FRC = ERV + RV; TLC = TV + IRV + ERV + RV
    t = np.linspace(0, 40, 2000)
    gecis = lambda t0, sure, v0, v1: v0 + (v1 - v0) * (1 - np.cos(np.pi * (t - t0) / sure)) / 2
    soluk = FRC + TV / 2 * (1 - np.cos(2 * np.pi * t / 4))
    v = np.select([t < 16, t < 20, t < 26, t < 28], [soluk, gecis(16, 4, FRC, TLC), gecis(20, 6, TLC, RV), gecis(26, 2, RV, FRC)], soluk)
    fig, ax = plt.subplots()
    ax.plot(t, v, color=INSAN, lw=4)
    for y, ls in [(RV, ":"), (FRC, "--"), (FRC + TV, "--"), (TLC, ":")]:
        ax.axhline(y, color=GRI, lw=1.5, ls=ls)
    x0 = 41.2
    def pay(y1, y2, ad, renk, x=x0):
        ax.annotate("", xy=(x, y1), xytext=(x, y2), arrowprops=dict(arrowstyle="<->", color=renk, lw=3))
        ax.text(x + 0.5, (y1 + y2) / 2, ad, fontsize=19, color=renk, va="center", weight="bold")
    pay(0, RV, f"artık hacim {tr(RV, 1)} L", GRI)
    pay(RV, FRC, f"soluk verme yedek hacmi {tr(ERV, 1)} L", MOR)
    pay(FRC, FRC + TV, f"soluk hacmi {tr(TV, 1)} L", TURUNCU)
    pay(FRC + TV, TLC, f"soluk alma yedek hacmi {tr(IRV, 1)} L", INSAN)
    ax.set_xlim(0, 58); ax.set_ylim(0, 6.6); ax.set_xticks([0, 10, 20, 30, 40]); ax.set_xlabel("zaman (s)"); ax.set_ylabel("akciğerdeki hava (L)")
    ax.text(1, TLC + 0.12, f"toplam akciğer kapasitesi {tr(TLC, 1)} L", fontsize=20, ha="left")
    ax.set_title("Dört hacim, dört kapasite · ŞEMATİK iz, hacimler ders kitabı tablosundan (yetişkin erkek ortalaması)")
    sekil("3.1", "spirometri")

    ns = oturum("3.1", "kapasiteler", """
from kaynaklar import deger
TV, IRV, ERV, RV = deger("TV_L"), deger("IRV_L"), deger("ERV_L"), deger("RV_L")
TV, IRV, ERV, RV
VC = TV + IRV + ERV
IC = TV + IRV
FRC = ERV + RV
TLC = VC + RV
round(VC, 1), round(IC, 1), round(FRC, 1), round(TLC, 1)
deger("VC_L"), deger("IC_L"), deger("FRC_L"), deger("TLC_L")
round(100 * TV / VC, 1)
from arac import robot_ozet
r = robot_ozet()
round(100 * r["hiz_en_buyuk"] / r["hiz_siniri"], 1)
round(100 * r["tutma_en_buyuk"] / r["efor"], 1)
""")
    r = robot_ozet(); VC = ns["VC"]
    hp = 100 * r["hiz_en_buyuk"] / r["hiz_siniri"]; tp = 100 * r["tutma_en_buyuk"] / r["efor"]
    fig, ax = cizelge("Soluk hacmi ve yedekler ↔ eklemin kullandığı pay", [
        ("Olağan iş", f"soluk hacmi {tr(TV, 1)} L", f"kayıtta en büyük dirsek hızı {tr(r['hiz_en_buyuk'])} rad/s"),
        ("Sınır", f"dirim kapasitesi {tr(VC, 1)} L", f"hız sınırı {tr(r['hiz_siniri'], 0)} rad/s, tork sınırı {tr(r['efor'], 0)} N·m (tablo)"),
        ("Kullanılan pay", f"yüzde {tr(100 * TV / VC, 0)}", f"hızın yüzde {tr(hp, 0)}'i, torkun yüzde {tr(tp, 0)}'si"),
        ("Hiç boşalmayan", f"artık hacim {tr(RV, 1)} L; spirometre ölçemez", "karşılığı yok"),
    ], "İki sistem de olağan işte sınırının küçük bir bölümünü kullanır. Akciğerde yedek, havanın gidip geldiği tek bir yolun hacmidir. Motorda sınır bir tasarım sayısıdır.",
        kaynak="İnsan: OpenStax Biology 2e 39.2 tablo (yetişkin erkek ortalaması) · Robot: benzetim kaydı ve kol tablosu")
    sekil("3.1", "karsilastirma")
    g = dict(TV=0.5, IRV=1.9, ERV=0.7, RV=1.1)
    gorev("3.1", "Soluk hacmi 0,5 L, soluk alma yedek hacmi 1,9 L, soluk verme yedek hacmi 0,7 L, artık hacim 1,1 L ise toplam akciğer kapasitesi kaç litredir? (hacimler ÖRNEK)",
          round(sum(g.values()), 1), "L", 0.05, "toplam akciğer kapasitesi = dört hacmin toplamı")
    olc(d3_1_hacimler_L=[TV, IRV, ERV, RV], d3_1_VC_L=VC, d3_1_IC_L=ns["IC"], d3_1_FRC_L=ns["FRC"], d3_1_TLC_L=ns["TLC"],
        d3_1_tablo_L=[deger("VC_L"), deger("IC_L"), deger("FRC_L"), deger("TLC_L")], d3_1_TV_payi_yuzde=100 * TV / VC,
        d3_1_hiz_payi_yuzde=hp, d3_1_tork_payi_yuzde=tp, d3_1_hiz_en_buyuk=r["hiz_en_buyuk"], d3_1_hiz_siniri=r["hiz_siniri"],
        d3_1_efor_Nm=r["efor"], d3_1_gorev_TLC_L=sum(g.values()), d3_1_gorev_VC_L=g["TV"] + g["IRV"] + g["ERV"])


def ders_3_2():
    """Ventilasyon ve ölü boşluk ↔ soğutma havası akışı."""
    VD = deger("olu_bosluk_mL"); f0 = deger("ornek_soluk_sayisi"); VT = 1000 * deger("TV_L")
    desen = [(f0, VT), (2 * f0, VT / 2)]
    fig, ax = plt.subplots()
    for i, (f, vt) in enumerate(desen):
        VE = f * vt / 1000; VA = f * (vt - VD) / 1000
        ax.bar(i * 3, VE, width=0.9, color=GRI, hatch="//", edgecolor="#ffffff")
        ax.bar(i * 3 + 1, VA, width=0.9, color=INSAN)
        ax.text(i * 3, VE + 0.12, f"dakika\n{tr(VE, 1)} L/dk", ha="center", fontsize=22)
        ax.text(i * 3 + 1, VA + 0.12, f"alveoler\n{tr(VA, 1)} L/dk", ha="center", fontsize=22, color=INSAN, weight="bold")
        ax.text(i * 3 + 0.5, -0.62, f"dakikada {f} soluk × {tr(vt, 0)} mL", ha="center", fontsize=23, weight="bold")
    ax.set_xlim(-0.9, 4.9); ax.set_ylim(0, 6.6); ax.set_xticks([]); ax.set_ylabel("ventilasyon (L/dk)")
    ax.set_title(f"Aynı dakika ventilasyonu, farklı alveoler ventilasyon · ölü boşluk {VD} mL (ders kitabı örneği)")
    sekil("3.2", "olu-bosluk")

    ns = oturum("3.2", "ventilasyon", """
from kaynaklar import deger
olu_bosluk = deger("olu_bosluk_mL")
def ventilasyon(soluk_sayisi, soluk_hacmi):
    return soluk_sayisi * soluk_hacmi, soluk_sayisi * (soluk_hacmi - olu_bosluk)
ventilasyon(10, 500)
ventilasyon(20, 250)
round(100 * olu_bosluk / 500)
ventilasyon(deger("soluk_sayisi_alt"), 500), ventilasyon(deger("soluk_sayisi_ust"), 500)
yogunluk, oz_isi = deger("hava_yogunluk"), deger("hava_oz_isi")
fark = ORNEK_DT                                   # ÖRNEK sıcaklık farkı (°C)
def tasinan_isi(litre_dakika):
    return yogunluk * oz_isi * (litre_dakika / 1000 / 60) * fark
round(tasinan_isi(6.0), 1)
from arac import robot_ozet
guc = robot_ozet()["mekanik_guc_en_buyuk"]
round(guc, 1)
gereken = guc / (yogunluk * oz_isi * fark) * 1000 * 60
round(gereken), round(gereken / 6.0, 1)
""", ns=dict(ORNEK_DT=ORNEK_DT))
    r = robot_ozet(); ven = ns["ventilasyon"]
    ve1, va1 = ven(10, 500); ve2, va2 = ven(20, 250)
    isi6 = ns["tasinan_isi"](6.0)
    fig, ax = cizelge("Ventilasyon ↔ soğutma havası akışı", [
        ("Akışın yönü", "gelgit: hava aynı yoldan girer ve çıkar", "tek yön: hava bir uçtan girer, öbür uçtan çıkar"),
        ("Boşa giden pay", f"ölü boşluk {VD} mL: {tr(VT, 0)} mL'lik soluğun yüzde {tr(100 * VD / VT, 0)}'u", "tek yönlü akışta ölü boşluk yok"),
        ("Taşınan şey", "oksijen ve karbondioksit; değişim yayılmayla", "ısı; değişim temasla"),
        ("Sayı", f"dakikada 6 L hava, ÖRNEK {tr(ORNEK_DT, 0)} °C farkla yalnız {tr(isi6, 1)} W ısı taşır", f"kayıttaki en büyük mekanik güç {tr(ns['guc'], 1)} W; o kadar ısı için {tr(ns['gereken'], 0)} L/dk gerekir"),
    ], "Solunum gaz taşır, soğutma havası ısı taşır. Gelgit akışı ölü boşluk bırakır, tek yönlü akış bırakmaz. Robotun ısı üretimi kayıtta yok; karşılaştırma mekanik güç üzerinden yapıldı.",
        kaynak="İnsan: Binks (2022) bölüm 3; OpenStax A&P 2e 22.3 · hava: College Physics 2e Tablo 11.1, 14.1 · Robot: benzetim kaydı (kaba model)")
    sekil("3.2", "karsilastirma")
    gorev("3.2", "Dakikada 15 soluk, soluk hacmi 400 mL, ölü boşluk 150 mL. Alveoler ventilasyon kaç mL/dk?",
          15 * (400 - VD), "mL/dk", 10.0, "alveoler ventilasyon = soluk sayısı × (soluk hacmi − ölü boşluk)")
    olc(d3_2_olu_bosluk_mL=VD, d3_2_ornek1=[ve1, va1], d3_2_ornek2=[ve2, va2], d3_2_olu_pay_yuzde=100 * VD / VT,
        d3_2_olagan_alt=list(ven(deger("soluk_sayisi_alt"), 500)), d3_2_olagan_ust=list(ven(deger("soluk_sayisi_ust"), 500)),
        d3_2_hava=[deger("hava_yogunluk"), deger("hava_oz_isi")], d3_2_ornek_dT=ORNEK_DT, d3_2_isi_6L_W=isi6,
        d3_2_mekanik_guc_en_buyuk_W=ns["guc"], d3_2_gereken_L_dk=ns["gereken"], d3_2_gereken_kat=ns["gereken"] / 6.0,
        d3_2_gorev_VA=15 * (400 - VD), d3_2_gorev_VE=15 * 400)


def ders_3_3():
    """Gaz değişimi ve taşınması ↔ enerji akışı."""
    P = np.linspace(0, 120, 600); S = doygunluk(P)
    lo, hi = 10.0, 60.0
    for _ in range(50):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if doygunluk(m) < 0.5 else (lo, m)
    P50 = (lo + hi) / 2
    Sa, Sv = float(doygunluk(100.0)), float(doygunluk(deger("PvO2_mmHg")))
    fig, ax = plt.subplots()
    ax.plot(P, 100 * S, color=INSAN, lw=5)
    for p, s, ad, yer in [(100, Sa, "akciğerden çıkan kan", (72, 80)), (deger("PvO2_mmHg"), Sv, "dokudan dönen kan", (50, 55)), (P50, 0.5, "yarı doygunluk", (38, 30))]:
        ax.plot([p], [100 * s], "o", ms=16, color=TURUNCU)
        ax.annotate(f"{ad}\n{tr(p, 0 if p != P50 else 1)} mmHg → yüzde {tr(100 * s, 0)}", xy=(p, 100 * s), xytext=yer, fontsize=22,
                    arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    ax.axvspan(deger("PvO2_mmHg"), 100, color=INSAN, alpha=0.08)
    ax.set_xlim(0, 120); ax.set_ylim(0, 105); ax.set_xlabel("oksijenin kısmi basıncı (mmHg)"); ax.set_ylabel("hemoglobin doygunluğu (%)")
    ax.set_title("Oksijen–hemoglobin ayrışma eğrisi · Severinghaus (1979) denklemi, insan kanı")
    sekil("3.3", "ayrisma-egrisi")

    ns = oturum("3.3", "gaz-hesabi", """
from kaynaklar import deger
from arac import doygunluk
solunan = (deger("atmosfer_mmHg") - deger("su_buhari_mmHg")) * deger("oksijen_orani")
alveol = solunan - deger("PaCO2_mmHg") / deger("solunum_orani")
round(solunan, 1), round(alveol, 1)
hb = ORNEK_HB                                     # ÖRNEK hemoglobin (g/dL)
def icerik(basinc):
    return hb * deger("hb_kapasite") * float(doygunluk(basinc)) + basinc * deger("cozunurluk")
atardamar, toplardamar = icerik(100), icerik(deger("PvO2_mmHg"))
round(atardamar, 1), round(toplardamar, 1), round(atardamar - toplardamar, 1)
tuketim = (atardamar - toplardamar) * 10 * deger("kalp_debisi_L_dk")
round(tuketim), deger("oksijen_tuketimi_mL_dk")
round(tuketim / 1000 * deger("oksijen_kJ_litre") * 1000 / 60), deger("bazal_guc_W")
round(100 * (atardamar - toplardamar) / atardamar)
""", ns=dict(ORNEK_HB=ORNEK_HB))
    r = robot_ozet()
    Ca, Cv = ns["atardamar"], ns["toplardamar"]; tuk = ns["tuketim"]
    o2_kayit = deger("oksijen_tuketimi_mL_dk") * r["sure"] / 60
    e_kayit = o2_kayit / 1000 * deger("oksijen_kJ_litre")
    fig, ax = cizelge("Oksijen taşınması ↔ enerji akışı", [
        ("Taşıyıcı", f"hemoglobin: gramı {tr(deger('hb_kapasite'))} mL oksijen bağlar", "iletken: elektriği taşıyıcısız iletir"),
        ("Yükleme ve boşaltma", f"akciğerde yüzde {tr(100 * Sa, 0)}, dokuda yüzde {tr(100 * Sv, 0)} doygun; fark dokuya kalır", "pilden motora tek yönlü akış"),
        ("Akış", f"dakikada {tr(tuk, 0)} mL oksijen (hesap); tabloda {deger('oksijen_tuketimi_mL_dk')} mL", "elektrik gücü kayıtta yok"),
        (f"{tr(r['sure'], 1)} s içinde", f"{tr(o2_kayit, 0)} mL oksijen, yaklaşık {tr(e_kayit, 1)} kJ (dinlenim)", f"dirseğin mekanik işi {tr(r['mekanik_is'], 1)} J (kaba model)"),
    ], "Kan oksijeni bir taşıyıcıya yükler ve yalnız dörtte birini bırakır, kalanı yedektir. Telde taşıyıcı da yedek de yoktur. Hemoglobin derişimi ÖRNEK'tir; robotun elektrik tüketimi kayıtta bulunmaz.",
        kaynak="İnsan: Binks (2022) bölüm 14, 16; Severinghaus (1979); OpenStax A&P 2e 19.4, 22.4; College Physics 2e Tablo 7.4 · Robot: benzetim kaydı")
    sekil("3.3", "karsilastirma")
    g_alveol = (ORNEK_BASINC - deger("su_buhari_mmHg")) * deger("oksijen_orani") - deger("PaCO2_mmHg") / deger("solunum_orani")
    gorev("3.3", "Atmosfer basıncı 523 mmHg olan bir yükseklikte (ÖRNEK), karbondioksit basıncı 40 mmHg ve solunum değişim oranı 0,8 iken alveol oksijen basıncı kaç mmHg olur?",
          round(g_alveol, 1), "mmHg", 1.0, "alveol = (atmosfer − 47) × 0,21 − 40 / 0,8")
    olc(d3_3_solunan_mmHg=ns["solunan"], d3_3_alveol_mmHg=ns["alveol"], d3_3_tablo_alveol_mmHg=deger("PAO2_tablo_mmHg"), d3_3_P50_mmHg=P50,
        d3_3_doygunluk_100=100 * Sa, d3_3_doygunluk_40=100 * Sv, d3_3_ornek_hb=ORNEK_HB, d3_3_icerik_atardamar=Ca, d3_3_icerik_toplardamar=Cv,
        d3_3_icerik_fark=Ca - Cv, d3_3_tuketim_mL_dk=tuk, d3_3_tuketim_tablo=deger("oksijen_tuketimi_mL_dk"),
        d3_3_guc_W=tuk / 1000 * deger("oksijen_kJ_litre") * 1000 / 60, d3_3_bazal_W=deger("bazal_guc_W"), d3_3_birakilan_yuzde=100 * (Ca - Cv) / Ca,
        d3_3_co2=[deger("co2_bikarbonat_yuzde"), deger("co2_hb_yuzde"), deger("co2_cozunmus_alt"), deger("co2_cozunmus_ust")],
        d3_3_kayit_o2_mL=o2_kayit, d3_3_kayit_enerji_kJ=e_kayit, d3_3_mekanik_is_J=r["mekanik_is"], d3_3_ornek_basinc=ORNEK_BASINC,
        d3_3_gorev_alveol_mmHg=g_alveol)


def karbondioksit(kat, kazanc, VA0, P0):
    """Kemorefleks modeli: üretim 'kat' katına çıkınca yeni denge basıncı. P × (VA0 + kazanç × (P − P0)) = P0 × VA0 × kat."""
    if kazanc == 0:
        return P0 * kat
    a, b, c = kazanc, VA0 - kazanc * P0, -P0 * VA0 * kat
    return (-b + np.sqrt(b * b - 4 * a * c)) / (2 * a)


def ders_3_4():
    """Solunumun denetimi ↔ eklem denetim döngüsü (hafta ürünü: solunum denetim şeması)."""
    P0 = deger("PaCO2_mmHg"); VA0 = deger("ornek_soluk_sayisi") * (1000 * deger("TV_L") - deger("olu_bosluk_mL")) / 1000
    kat = deger("yurume_guc_W") / deger("oturma_guc_W")
    r = robot_ozet()
    G = np.linspace(0, 6, 300); Pg = np.array([karbondioksit(kat, g, VA0, P0) for g in G])
    P_ornek = float(karbondioksit(kat, ORNEK_KAZANC, VA0, P0)); VA_ornek = VA0 + ORNEK_KAZANC * (P_ornek - P0)
    kp = np.linspace(5, 120, 300); sapma = np.degrees(r["tutma_yatay"] / kp); sapma_tablo = float(np.degrees(r["tutma_yatay"] / r["kp"]))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(19.2, 10.8))
    a1.plot(G, Pg, color=INSAN, lw=5)
    a1.axhline(P0, color=GRI, lw=2.5, ls="--"); a1.text(5.9, P0 - 3.4, f"hedef {P0} mmHg", ha="right", fontsize=20, color=GRI)
    a1.plot([0, ORNEK_KAZANC], [P0 * kat, P_ornek], "o", ms=15, color=TURUNCU)
    a1.annotate(f"denetim yok\n{tr(P0 * kat, 0)} mmHg", xy=(0, P0 * kat), xytext=(0.9, 86), fontsize=20, arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    a1.annotate(f"ÖRNEK kazanç {tr(ORNEK_KAZANC, 0)}\n{tr(P_ornek, 1)} mmHg", xy=(ORNEK_KAZANC, P_ornek), xytext=(2.6, 62), fontsize=20, arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    a1.set_ylim(35, 100); a1.set_xlabel("denetleyici kazancı (L/dk/mmHg)"); a1.set_ylabel("atardamar karbondioksit basıncı (mmHg)")
    a1.set_title(f"Solunum: üretim {tr(kat)} katına çıkınca", fontsize=23)
    a2.plot(kp, sapma, color=ROBOT, lw=5)
    a2.plot([r["kp"]], [sapma_tablo], "o", ms=15, color=TURUNCU)
    a2.annotate(f"tablodaki kazanç {tr(r['kp'], 0)}\nkalıcı sapma {tr(sapma_tablo, 1)}°", xy=(r["kp"], sapma_tablo), xytext=(52, 14), fontsize=20, arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    a2.axhline(0, color=GRI, lw=2.5, ls="--")
    a2.set_ylim(-1, 36); a2.set_xlabel("eklem denetleyicisinin oransal kazancı (N·m/rad)"); a2.set_ylabel("kalıcı açı sapması (derece)")
    a2.set_title(f"Robot: {tr(r['tutma_yatay'], 1)} N·m yük altında", fontsize=23)
    fig.suptitle("Oransal denetim sapmayı küçültür, sıfırlamaz · MODEL HESABI, solunumda kazanç ÖRNEK", fontsize=24)
    sekil("3.4", "oransal-denetim")

    ns = oturum("3.4", "kemorefleks", """
from kaynaklar import deger
hedef = deger("PaCO2_mmHg")
alveoler = deger("ornek_soluk_sayisi") * (1000 * deger("TV_L") - deger("olu_bosluk_mL")) / 1000
kat = deger("yurume_guc_W") / deger("oturma_guc_W")
hedef, alveoler, round(kat, 2)
round(hedef * kat, 1)
kazanc = ORNEK_KAZANC                              # ÖRNEK denetleyici kazancı (L/dk/mmHg)
yeni = float(karbondioksit(kat, kazanc, alveoler, hedef))
round(yeni, 1), round(alveoler + kazanc * (yeni - hedef), 1)
round(hedef * 2, 1)
from arac import robot_ozet
import math
r = robot_ozet()
r["kp"], round(r["tutma_yatay"], 2)
round(math.degrees(r["tutma_yatay"] / r["kp"]), 1)
""", ns=dict(ORNEK_KAZANC=ORNEK_KAZANC, karbondioksit=karbondioksit))
    fig, ax = cizelge("Solunumun denetimi ↔ eklem denetim döngüsü · hafta ürünü", [
        ("Algılayıcı", f"merkezî ve çevresel kemoreseptörler; yanıtın yüzde {deger('merkezi_pay_yuzde')}'i merkezî", "eklemdeki açı algılayıcısı"),
        ("Denetleyici", "omurilik soğanındaki solunum merkezleri; ritim ve derinlik", f"eklem denetleyicisi; oransal kazanç {tr(r['kp'], 0)} (tablo)"),
        ("Etkileyici", "diyafram ve kaburga arası kaslar: ventilasyon", "motor: tork"),
        ("Kalan sapma", f"MODEL: üretim {tr(kat)} katına çıkınca {tr(P_ornek, 1)} mmHg; denetimsiz {tr(P0 * kat, 0)} mmHg", f"{tr(r['tutma_yatay'], 1)} N·m yük altında {tr(sapma_tablo, 1)}° (hesap)"),
    ], "İki döngü de sapmayı ölçer ve ters yönde düzeltir. Solunumda ritmi beyin sapı üretir ve egzersizde başka girdiler de devreye girer; bu model yalnız kemorefleksi gösterir. Robotun döngüsü tek bir sayıyı izler.",
        kaynak="İnsan: Binks (2022) bölüm 3, 14, 17; OpenStax A&P 2e 22.3; College Physics 2e Tablo 7.5 · Robot: kol tablosu · kazanç ÖRNEK")
    sekil("3.4", "karsilastirma")
    gorev("3.4", "Karbondioksit üretimi değişmeden alveoler ventilasyon yarıya inerse atardamar karbondioksit basıncı 40 mmHg'den kaç mmHg'ye çıkar?",
          round(P0 * 2, 1), "mmHg", 1.0, "basınç, üretim / alveoler ventilasyon ile orantılıdır")
    olc(d3_4_hedef_mmHg=P0, d3_4_alveoler_L_dk=VA0, d3_4_uretim_kati=kat, d3_4_denetimsiz_mmHg=P0 * kat, d3_4_ornek_kazanc=ORNEK_KAZANC,
        d3_4_model_mmHg=P_ornek, d3_4_model_alveoler_L_dk=VA_ornek, d3_4_merkezi_yuzde=deger("merkezi_pay_yuzde"), d3_4_periferik_esik=deger("periferik_esik_mmHg"),
        d3_4_kp=r["kp"], d3_4_tutma_yatay_Nm=r["tutma_yatay"], d3_4_kalici_sapma_derece=sapma_tablo, d3_4_gorev_mmHg=P0 * 2)


if __name__ == "__main__":
    ders_3_1(); ders_3_2(); ders_3_3(); ders_3_4()
    print("hafta 3 tamam")
