"""Hafta 1 · Sinir Sistemi — Ders 1.1–1.4 ve tanıtım haritası.
Fizyoloji sayıları kaynaklar.py'den, robot sayıları benzetim kaydından ve kol tablolarından gelir.
Zar modeli Hodgkin–Huxley modelidir (mürekkep balığı dev aksonu, 6,3 °C): insan nöronunun ölçümü DEĞİL, MODEL HESABI.
Ders 1.4'teki lif uzunlukları ve seçilen iletim hızları ÖRNEK'tir (aralık kaynaklı, seçilen değer örnek).
  python hafta1.py   → ekran/0.1, ekran/1.x/*.txt + *.png, OLCUMLER.json (d0_*, d1_*), GOREVLER.json"""
import math
import numpy as np
import matplotlib.pyplot as plt
from ortak import kayit, olc, oturum, sekil, gorev
from arac import (robot_ozet, zar_modeli, zar_dinlenim, vuru, sayim, kutu, ok, bos_eksen, cizelge, tr, sayi, DURGUN,
                  TURUNCU, MAVI, YESIL, MOR, GRI, INSAN, ROBOT)
from kaynaklar import deger

ISIK = 299792458          # m/s · ışık hızı (SI tanımı, kesin değer)
ORNEK_ON_M, ORNEK_ARD_M = 0.1, 0.9        # ÖRNEK: sempatik yolda gangliyon öncesi ve sonrası lif uzunluğu (toplam 1 m)
ORNEK_HIZ_MIYELINLI, ORNEK_HIZ_MIYELINSIZ = 10.0, 1.0   # ÖRNEK: kaynaktaki 0,1–100 m/s aralığından seçilen iki hız


def nernst_katsayisi(T=310.15):
    """Tek değerlikli iyon için 10 tabanlı Nernst katsayısı (mV). R ve F, SI tanımından kesin değerlerdir."""
    R, F = 8.314462618, 96485.33212
    return 1000 * R * T / F * math.log(10)


def ders_1_1():
    """Dinlenim zar potansiyeli ↔ dururken tork üreten eklem."""
    ns = oturum("1.1", "nernst", """
import math
from kaynaklar import deger
R, F, T = 8.314462618, 96485.33212, 310.15
katsayi = 1000 * R * T / F * math.log(10)
round(katsayi, 1)
E_K = katsayi * math.log10(deger("K_dis_mM") / deger("K_ic_mM"))
E_Na = katsayi * math.log10(deger("Na_dis_mM") / deger("Na_ic_mM"))
E_Cl = -katsayi * math.log10(deger("Cl_dis_mM") / deger("Cl_ic_mM"))
round(E_K, 1), round(E_Na, 1), round(E_Cl, 1)
def goldman(oran):
    ust = deger("K_dis_mM") + oran * deger("Na_dis_mM")
    alt = deger("K_ic_mM") + oran * deger("Na_ic_mM")
    return katsayi * math.log10(ust / alt)
round(goldman(deger("gecirgenlik_orani")), 1)
r = 10 ** (deger("dinlenim_mV") / katsayi)
oran_70 = (r * deger("K_ic_mM") - deger("K_dis_mM")) / (deger("Na_dis_mM") - r * deger("Na_ic_mM"))
round(oran_70, 3), round(goldman(oran_70), 1)
""")
    EK, ENa, ECl = ns["E_K"], ns["E_Na"], ns["E_Cl"]
    g001 = ns["goldman"](deger("gecirgenlik_orani")); o70 = ns["oran_70"]
    din = deger("dinlenim_mV")

    fig, ax = plt.subplots()
    cizgi = [(ENa, f"sodyum denge potansiyeli  {tr(ENa, 1)} mV", MOR, "--"),
             (din, f"dinlenim zar potansiyeli  {tr(din, 0)} mV  (ders kitabı)", TURUNCU, "-"),
             (ECl, f"klor denge potansiyeli  {tr(ECl, 1)} mV", GRI, ":"),
             (EK, f"potasyum denge potansiyeli  {tr(EK, 1)} mV", INSAN, "-.")]
    for y, ad, renk, ls in cizgi:
        ax.axhline(y, color=renk, ls=ls, lw=5)
    ax.text(0.02, ENa - 9, cizgi[0][1], fontsize=26, color=MOR, weight="bold", va="top")
    ax.text(0.02, din + 4, cizgi[1][1], fontsize=26, color=TURUNCU, weight="bold", va="bottom")
    ax.text(0.98, ECl + 3, cizgi[2][1], fontsize=24, color=GRI, weight="bold", va="bottom", ha="right")
    ax.text(0.02, EK - 5, cizgi[3][1], fontsize=26, color=INSAN, weight="bold", va="top")
    ax.annotate("", xy=(0.42, din), xytext=(0.42, EK), arrowprops=dict(arrowstyle="<->", color="#111111", lw=3))
    ax.text(0.41, (din + EK) / 2 + 3, f"fark {tr(din - EK, 1)} mV", fontsize=24, va="center", ha="right")
    ax.axhline(0, color="#111111", lw=1.5)
    ax.set_xlim(0, 1); ax.set_xticks([]); ax.set_ylim(-125, 95); ax.set_ylabel("zar potansiyeli (mV)")
    ax.set_title("Dinlenim potansiyeli potasyumun dengesine yakındır · Nernst hesabı, derişimler ders kitabından")
    sekil("1.1", "denge-potansiyelleri")

    r = robot_ozet()
    fig, ax = cizelge("Dinlenim zar potansiyeli ↔ dururken tork üreten eklem", [
        ("Dinlenim değeri", f"zarın içi dışına göre {tr(din, 0)} mV; sıfır değil", f"dirsek dururken ortalama {tr(r['tutma_durgun'])} N·m tork (kaba model)"),
        ("Neden sıfır değil", "iyon derişimleri iki yanda farklı, zar en çok potasyuma geçirgen", "ön kolu yer çekimine karşı tutmak gerekir"),
        ("Bedeli", f"pompa her çevrimde {deger('pompa_Na')} sodyum atar, {deger('pompa_K')} potasyum alır; ATP harcar", f"kayıt süresinin yüzde {tr(100 * r['durgun_pay'], 0)}'inde dirsek durgun, motor yine de çalışır"),
        ("Hazır olma", "eşiğe yakın bekler: küçük uyarı yeter", "konumunu korur: komut gelince hemen döner"),
    ], "Zardaki fark iyon derişimlerinde depolanmış bir gerilimdir, pompa onu az enerjiyle korur. Motor ise durduğu sürece akım çeker. Yalnız 'dinlenim sıfır değildir' fikri ortaktır.",
        kaynak="İnsan: OpenStax Biology 2e 35.2, Anatomy and Physiology 2e 12.4 · Robot: benzetim kaydı ve kol tablosu")
    sekil("1.1", "karsilastirma")

    K2 = nernst_katsayisi() * math.log10(8 / deger("K_ic_mM"))
    gorev("1.1", "Hücre dışı potasyum 4 yerine 8 mM olursa potasyumun denge potansiyeli kaç mV olur? (37 °C, hücre içi 155 mM)",
          round(K2, 1), "mV", 0.5, "E = 61,5 × log10(dış / iç)")
    olc(d1_1_katsayi_mV=ns["katsayi"], d1_1_E_K_mV=EK, d1_1_E_Na_mV=ENa, d1_1_E_Cl_mV=ECl, d1_1_dinlenim_mV=din,
        d1_1_fark_K_mV=din - EK, d1_1_goldman_001_mV=g001, d1_1_oran_70=o70, d1_1_oran_kaynak=deger("gecirgenlik_orani"),
        d1_1_pompa=[deger("pompa_Na"), deger("pompa_K")], d1_1_durgun_yuzde=100 * r["durgun_pay"], d1_1_tutma_Nm=r["tutma_durgun"],
        d1_1_gorev_E_K_8mM=K2)


def esik_akimi():
    """1 ms'lik vuruda aksiyon potansiyeli başlatan en küçük akım (µA/cm²), ikiye bölerek."""
    alt, ust = 2.0, 30.0
    for _ in range(18):
        orta = (alt + ust) / 2
        if zar_modeli(vuru(orta), sure=30)[1].max() > 0:
            ust = orta
        else:
            alt = orta
    return alt, ust


def ders_1_2():
    """Aksiyon potansiyeli ↔ sinyal hattındaki sayı."""
    alt, ust = esik_akimi()
    din = zar_dinlenim()
    kuvvetli = 2 * ust
    t, U_alt = zar_modeli(vuru(0.9 * ust), sure=25)
    _, U_ust = zar_modeli(vuru(1.1 * ust), sure=25)
    _, U_kuv = zar_modeli(vuru(kuvvetli), sure=25)
    tepe, tepe_k, dip = float(U_ust.max()), float(U_kuv.max()), float(U_kuv.min())
    yari = (tepe_k + din) / 2
    ust_idx = np.nonzero(U_kuv > yari)[0]
    genislik = float(t[ust_idx[-1]] - t[ust_idx[0]])

    fig, ax = plt.subplots()
    ax.plot(t, U_kuv, color=INSAN, lw=5, label=f"eşiğin iki katı uyarı: tepe {tr(tepe_k, 0)} mV")
    ax.plot(t, U_ust, color=MOR, lw=4, ls="--", label=f"eşiğin 1,1 katı uyarı: tepe {tr(tepe, 0)} mV")
    ax.plot(t, U_alt, color=TURUNCU, lw=4, ls=":", label=f"eşiğin 0,9 katı uyarı: aksiyon potansiyeli yok (en çok {tr(float(U_alt.max()), 0)} mV)")
    ax.axhline(din, color=GRI, lw=2, ls="-."); ax.text(24.8, din + 3, f"dinlenim {tr(din, 0)} mV", ha="right", fontsize=22, color=GRI)
    ax.axvspan(5, 6, color="#111111", alpha=0.12); ax.text(5.5, -92, "uyarı\n1 ms", ha="center", fontsize=20)
    ax.annotate(f"izleyen aşırı\npolarizasyon {tr(dip, 0)} mV", xy=(t[U_kuv.argmin()], dip), xytext=(13.5, -45), fontsize=22,
                arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    ax.set_ylim(-100, 62); ax.set_xlim(0, 25); ax.set_xlabel("zaman (ms)"); ax.set_ylabel("zar potansiyeli (mV)")
    ax.legend(loc="upper right", framealpha=1.0)
    ax.set_title("Ya hep ya hiç · MODEL HESABI: Hodgkin–Huxley, mürekkep balığı aksonu, 6,3 °C")
    sekil("1.2", "aksiyon-potansiyeli")

    # mutlak ve göreli dinlenmezlik: ikinci vuru (eşiğin iki katı) hangi aralıktan sonra yeniden ateşletir
    aralik = np.arange(2.0, 25.01, 0.5)
    ikinci = [sayim(zar_modeli(lambda x, g=g: kuvvetli if (5 <= x < 6 or 5 + g <= x < 6 + g) else 0.0, sure=45)[1]) for g in aralik]
    en_kisa = float(aralik[[i for i, s in enumerate(ikinci) if s >= 2][0]])
    # sıklık kodu: sürekli akımda saniyedeki aksiyon potansiyeli
    akimlar = [5.0, 7.0, 10.0, 20.0, 40.0]
    siklik = []
    for I in akimlar:
        tt, UU = zar_modeli(lambda x, I=I: I if x >= 10 else 0.0, sure=510, adim=0.02)
        siklik.append(sayim(UU) * 2)
    r = robot_ozet()
    ns = oturum("1.2", "esik-ve-siklik", """
from kaynaklar import deger
esik_alt, esik_ust = ESIK
round(esik_ust, 2)
round(DINLENIM, 1), round(TEPE, 1), round(DIP, 1), round(GENISLIK, 2)
deger("dinlenim_mV"), deger("esik_mV"), deger("tepe_mV"), deger("aksiyon_ms")
EN_KISA_ARALIK
for akim, hz in zip(AKIMLAR, SIKLIK):
    print(f"sürekli akım {akim:4.0f} µA/cm²  →  saniyede {hz:3d} aksiyon potansiyeli")
ADIM = 0.02
round(ADIM * max(SIKLIK), 1)
""", ns=dict(ESIK=(alt, ust), DINLENIM=din, TEPE=tepe_k, DIP=dip, GENISLIK=genislik, EN_KISA_ARALIK=en_kisa,
             AKIMLAR=akimlar, SIKLIK=siklik))
    fig, ax = cizelge("Aksiyon potansiyeli ↔ sinyal hattındaki sayı", [
        ("Bir işaret", f"hep aynı büyüklükte vuru; modelde tepe {tr(tepe_k, 0)} mV, ders kitabında +{deger('tepe_mV')} mV", "her ölçüm bir sayı; büyüklüğü bilgiyi taşır"),
        ("Şiddet bilgisi", f"vuru sıklaşır: modelde saniyede {min(s for s in siklik if s > 2)} ile {max(siklik)} arası", f"kayıtta saniyede {r['saniyede']} sayı, sıklık sabit"),
        ("En kısa aralık", f"dinlenmezlik: modelde ikinci vuru için en az {tr(en_kisa, 1)} ms", f"iki ölçüm arası {tr(1000 * r['adim'], 0)} ms (kayıttan)"),
        ("Eşik", f"ders kitabında {tr(deger('esik_mV'), 0)} mV; altında yanıt yok", "eşik yok: her değer iletilir"),
    ], "Nöron bilgiyi vuru sıklığıyla, sinyal hattı sayının büyüklüğüyle taşır. Model mürekkep balığı aksonudur ve soğuktur; insan nöronunun sayıları ders kitabı değerleridir.",
        kaynak="Model: Hodgkin ve Huxley (1952), parametreler Pool ve Mato (2011) · Ders kitabı: OpenStax A&P 2e 12.4 · Robot: benzetim kaydı")
    sekil("1.2", "karsilastirma")
    gorev("1.2", "Modelde eşiğin iki katı yerine dört katı uyarı verilirse tepe değeri yaklaşık kaç mV olur? (ya hep ya hiç)",
          round(float(zar_modeli(vuru(4 * ust), sure=25)[1].max()), 0), "mV", 8.0, "Tepe değeri uyarının büyüklüğüne neredeyse bağlı değildir.")
    olc(d1_2_esik_akim=ust, d1_2_model_dinlenim_mV=din, d1_2_model_tepe_mV=tepe_k, d1_2_model_tepe_11_mV=tepe, d1_2_model_dip_mV=dip,
        d1_2_model_alt_tepe_mV=float(U_alt.max()), d1_2_genislik_ms=genislik, d1_2_en_kisa_aralik_ms=en_kisa,
        d1_2_akimlar=akimlar, d1_2_siklik_hz=siklik, d1_2_adimda_vuru=r["adim"] * max(siklik),
        d1_2_kitap=[deger("dinlenim_mV"), deger("esik_mV"), deger("tepe_mV"), deger("aksiyon_ms")],
        d1_2_gorev_tepe_4kat=float(zar_modeli(vuru(4 * ust), sure=25)[1].max()))


def ders_1_3():
    """İletim hızı ve sinaps ↔ sinyal hattı ve gecikme."""
    hizli, yavas, sin = deger("sinir_hizi_en_hizli"), deger("sinir_hizi_en_yavas"), deger("sinaps_gecikmesi_ms")
    r = robot_ozet(); L = r["kol_uzunluk"]
    v = np.logspace(-1, 2, 200)
    fig, ax = plt.subplots()
    ax.loglog(v, 1000 * L / v, color=INSAN, lw=5, label=f"{tr(L)} m yol: iletim süresi")
    ax.loglog(v, 1000 * L / v + sin, color=MOR, lw=4, ls="--", label=f"iletim + bir sinaps ({sin} ms)")
    ax.axhline(1000 * r["adim"], color=ROBOT, lw=4, ls="-.")
    ax.text(0.11, 1000 * r["adim"] * 1.25, f"kayıtta iki ölçüm arası: {tr(1000 * r['adim'], 0)} ms", fontsize=24, color=ROBOT, weight="bold")
    for x, ad, sure_yazi, yer in [(hizli, "en hızlı sinir", f"{tr(1000 * L / hizli, 1)} ms", (5.0, 1.7)),
                                  (yavas, "en yavaş sinir", f"{tr(L / yavas, 1)} s", (0.28, 5200))]:
        ax.plot([x], [1000 * L / x], "o", ms=18, color=TURUNCU)
        ax.annotate(f"{ad}: {sayi(x)} m/s → {sure_yazi}", xy=(x, 1000 * L / x), xytext=yer,
                    fontsize=23, arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    ax.set_ylim(1, 20000)
    ax.set_xlabel("iletim hızı (m/s, logaritmik)"); ax.set_ylabel("süre (ms, logaritmik)")
    ax.legend(loc="center right", framealpha=1.0)
    ax.set_title("Hız düştükçe gecikme büyür · hız aralığı kaynaktan, yol robotun kol tablosundan")
    sekil("1.3", "iletim-suresi")

    ns = oturum("1.3", "gecikme-butcesi", """
from kaynaklar import deger
from arac import robot_ozet
r = robot_ozet()
yol = r["kol_uzunluk"]
hizli, yavas = deger("sinir_hizi_en_hizli"), deger("sinir_hizi_en_yavas")
sinaps = deger("sinaps_gecikmesi_ms")
yol, hizli, yavas, sinaps
round(1000 * yol / hizli, 1), round(yol / yavas, 1)
round(1000 * yol / hizli + sinaps, 1)
adim_ms = 1000 * r["adim"]
adim_ms, round(hizli * r["adim"], 1)
isik = 299792458
round(1e9 * yol / isik, 1)
deger("uc_plak_mV"), deger("uc_plak_esik_mV")
round(deger("uc_plak_mV") / deger("uc_plak_esik_mV"), 2)
""")
    guv = deger("uc_plak_mV") / deger("uc_plak_esik_mV")
    fig, ax = cizelge("Sinir yolu ↔ sinyal hattı", [
        ("Taşıyıcı", "aksiyon potansiyeli: akson boyunca kendini yeniler", "telde gerilim: sayı olarak kodlanmış veri"),
        (f"{tr(L)} m yol", f"en hızlı sinirde {tr(1000 * L / hizli, 1)} ms, en yavaşta {tr(L / yavas, 1)} s", f"en az {tr(1e9 * L / ISIK, 1)} ns (ışık hızı sınırı)"),
        ("Bağlantı noktası", f"kimyasal sinaps: yaklaşık {sin} ms gecikme, tek yön", "bağlantı ucu: gecikmesi ihmal edilir, iki yön"),
        ("Hattın ritmi", "sürekli; vuru geldiği an iletilir", f"kayıtta {tr(1000 * r['adim'], 0)} ms'de bir ölçüm"),
    ], "Sinirde gecikmeyi yolun kendisi üretir. Robotta kablo çok hızlıdır, gecikmeyi ölçüm ve hesap aralığı belirler. Hızlı olmak daha iyi denetim demek değildir.",
        kaynak="İnsan: Byrne, Neuroscience Online bölüm 3–4; OpenStax Biology 2e 35.2 · Robot: benzetim kaydı ve kol tablosu")
    sekil("1.3", "karsilastirma")
    gorev("1.3", "1 m uzunluğundaki bir yol 50 m/s hızla iletiyor ve yol üzerinde iki sinaps var. Toplam gecikme kaç ms?",
          round(1000 * 1.0 / 50 + 2 * sin, 1), "ms", 0.5, "gecikme = yol / hız + sinaps sayısı × sinaps gecikmesi")
    olc(d1_3_yol_m=L, d1_3_hizli_m_s=hizli, d1_3_yavas_m_s=yavas, d1_3_sinaps_ms=sin, d1_3_hizli_ms=1000 * L / hizli,
        d1_3_yavas_s=L / yavas, d1_3_hizli_sinaps_ms=1000 * L / hizli + sin, d1_3_adim_ms=1000 * r["adim"],
        d1_3_adimda_yol_m=hizli * r["adim"], d1_3_isik_ns=1e9 * L / ISIK, d1_3_cap_kati=deger("cap_kati"),
        d1_3_uc_plak=[deger("uc_plak_mV"), deger("uc_plak_esik_mV")], d1_3_guvenlik=guv, d1_3_gorev_ms=1000 * 1.0 / 50 + 2 * sin)


def en_uzun_durgun():
    """Kayıtta dirseğin kesintisiz en uzun süre durgun kaldığı aralık: (başlangıç s, süre s, ortalama açı °, sapma °)."""
    k = kayit(); t = k["zaman_s"]; d = np.abs(k["dirsek_hiz_rad_s"]) < DURGUN
    en, bas, i = (0, 0), None, 0
    for i, v in enumerate(d):
        if v and bas is None:
            bas = i
        if (not v or i == len(d) - 1) and bas is not None:
            if i - bas > en[1] - en[0]:
                en = (bas, i)
            bas = None
    a, b = en
    aci = np.degrees(k["dirsek_rad"][a:b])
    return float(t[a]), float(t[b - 1] - t[a]), float(aci.mean()), float(aci.std())


def ders_1_4():
    """Otonom sinir sistemi ↔ arka planda çalışan eklem denetimi (hafta ürünü: sinir yolu çizelgesi)."""
    fig, ax = bos_eksen("Somatik yol tek nöron, otonom yol iki nöron")
    yollar = [("Somatik (iskelet kası)", 0.74, [("omurilik", 0.20, 0.10), ("miyelinli akson · asetilkolin", 0.33, 0.42), ("iskelet kası", 0.78, 0.17)], INSAN),
              ("Sempatik", 0.45, [("omurilik\n(göğüs–bel)", 0.20, 0.10), ("kısa, miyelinli\nasetilkolin", 0.33, 0.13), ("gangliyon", 0.49, 0.10), ("uzun, miyelinsiz\nnoradrenalin", 0.62, 0.20), ("hedef organ", 0.85, 0.12)], TURUNCU),
              ("Parasempatik", 0.16, [("beyin sapı\nve sakral", 0.20, 0.10), ("uzun\nasetilkolin", 0.33, 0.24), ("gangliyon", 0.60, 0.10), ("kısa\nasetilkolin", 0.73, 0.09), ("hedef organ", 0.85, 0.12)], MOR)]
    for ad, y, parca, renk in yollar:
        ax.text(0.01, y + 0.07, ad.replace(" (", "\n("), fontsize=23, weight="bold", color=renk, va="center")
        for i, (m, x, w) in enumerate(parca):
            govde = i % 2 == 0
            kutu(ax, x, y + (0.0 if govde else 0.035), w, 0.14 if govde else 0.07, m, renk if govde else "#E5E7EB", boy=19 if govde else 17,
                 yazi="#ffffff" if govde else "#111111")
    ax.text(0.5, 0.045, f"Sempatik zincirde her yanda {deger('zincir_gangliyon')} gangliyon bulunur. Gangliyon öncesi lifler asetilkolin salar.",
            ha="center", fontsize=21, color=GRI)
    sekil("1.4", "iki-noronlu-yol")

    ns = oturum("1.4", "yol-gecikmesi", """
from kaynaklar import deger
sinaps = deger("sinaps_gecikmesi_ms")
somatik = 1000 * 1.0 / deger("sinir_hizi_en_hizli") + sinaps
round(somatik, 1)
on_m, ard_m = ORNEK_ON_M, ORNEK_ARD_M          # ÖRNEK lif boyları (m)
hiz_miyelinli, hiz_miyelinsiz = ORNEK_HIZ_MIYELINLI, ORNEK_HIZ_MIYELINSIZ    # ÖRNEK hızlar (m/s)
on_m, ard_m, hiz_miyelinli, hiz_miyelinsiz
sempatik = 1000 * on_m / hiz_miyelinli + sinaps + 1000 * ard_m / hiz_miyelinsiz + sinaps
round(sempatik, 1)
round(sempatik / somatik, 1)
from arac import robot_ozet
r = robot_ozet()
round(sempatik / (1000 * r["adim"]), 1)
""", ns=dict(ORNEK_ON_M=ORNEK_ON_M, ORNEK_ARD_M=ORNEK_ARD_M, ORNEK_HIZ_MIYELINLI=ORNEK_HIZ_MIYELINLI, ORNEK_HIZ_MIYELINSIZ=ORNEK_HIZ_MIYELINSIZ))
    r = robot_ozet(); bas, sure, aci, sapma = en_uzun_durgun()
    fig, ax = cizelge("Otonom sinir sistemi ↔ arka planda çalışan eklem denetimi", [
        ("İş", "kalp, damar, bez ve düz kası istem dışı ayarlar", "eklemi hedef açıda tutar; görev planı karışmaz"),
        ("Yol", "iki nöron ve bir gangliyon; ikinci lif miyelinsiz", "algılayıcı, denetleyici, motor; kablo"),
        ("Hız", f"ÖRNEK 1 m yol: {tr(ns['sempatik'], 0)} ms; somatik yol {tr(ns['somatik'], 0)} ms", f"kayıtta {tr(1000 * r['adim'], 0)} ms'de bir ölçüm"),
        ("Süreklilik", "iki bölüm birlikte, sürekli etkin; denge kayar", f"kayıtta dirsek {tr(sure, 1)} s boyunca {tr(aci, 1)}° ± {tr(sapma, 2)}°"),
    ], "Otonom sistem iki karşıt bölümün dengesiyle çalışır ve kimyasal habercisi hedefe göre değişir. Eklem denetleyicisi tek bir hedef sayıyı izler. Ortak yan, işin bilinçli plan dışında sürmesidir.",
        kaynak="İnsan: OpenStax A&P 2e 15.1 · seçilen lif boyları ve hızlar ÖRNEK · Robot: benzetim kaydı")
    sekil("1.4", "karsilastirma")
    para = 1000 * 0.9 / ORNEK_HIZ_MIYELINLI + 1000 * 0.1 / ORNEK_HIZ_MIYELINSIZ + 2 * deger("sinaps_gecikmesi_ms")
    gorev("1.4", "Parasempatik yolda gangliyon öncesi lif 0,9 m (10 m/s), sonrası 0,1 m (1 m/s) ve iki sinaps var. Toplam gecikme kaç ms? (hızlar ve boylar ÖRNEK)",
          round(para, 1), "ms", 1.0, "Her lif için yol / hız, üstüne iki sinaps gecikmesi.")
    olc(d1_4_somatik_ms=ns["somatik"], d1_4_sempatik_ms=ns["sempatik"], d1_4_oran=ns["sempatik"] / ns["somatik"],
        d1_4_ornek_on_m=ORNEK_ON_M, d1_4_ornek_ard_m=ORNEK_ARD_M, d1_4_ornek_hiz_miyelinli=ORNEK_HIZ_MIYELINLI,
        d1_4_ornek_hiz_miyelinsiz=ORNEK_HIZ_MIYELINSIZ, d1_4_sempatik_adim=ns["sempatik"] / (1000 * r["adim"]),
        d1_4_gangliyon=deger("zincir_gangliyon"), d1_4_durgun_bas_s=bas, d1_4_durgun_sure_s=sure, d1_4_durgun_aci=aci,
        d1_4_durgun_sapma=sapma, d1_4_gorev_parasempatik_ms=para)


def tanitim():
    """Tanıtım dersi: dört sistemin robot karşılıkları haritası."""
    fig, ax = bos_eksen("İnsan fizyolojisi ↔ insansı robot: dört sistemin haritası")
    satir = [("Hafta 1 · Sinir sistemi", "zar potansiyeli · iletim ·\nsinaps · otonom sistem", "sinyal hattı · gecikme ·\narka plan denetimi"),
             ("Hafta 2 · Kas", "sarkomer · eşleşme ·\nmotor birim · lif tipleri", "eklem motoru · tork ·\nhız sınırı"),
             ("Hafta 3 · Solunum", "hacimler · ventilasyon ·\ngaz taşınması · denetim", "hava akışı · enerji akışı ·\ndenetim döngüsü"),
             ("Hafta 4 · Sindirim", "hareket · salgı ·\nemilim · denetim", "taşıma · enerji alımı ·\ndönüşüm verimi")]
    for i, (h, ins, rob) in enumerate(satir):
        y = 0.76 - i * 0.2
        ax.text(0.01, y + 0.07, h, fontsize=24, weight="bold", va="center")
        kutu(ax, 0.27, y, 0.30, 0.14, ins, INSAN, boy=22)
        kutu(ax, 0.66, y, 0.32, 0.14, rob, ROBOT, boy=22)
        ax.annotate("", xy=(0.645, y + 0.07), xytext=(0.585, y + 0.07), arrowprops=dict(arrowstyle="<->", color="#111111", lw=3, mutation_scale=26))
    ax.text(0.42, 0.955, "İnsan", ha="center", fontsize=26, weight="bold", color=INSAN)
    ax.text(0.82, 0.955, "İnsansı robot", ha="center", fontsize=26, weight="bold", color=ROBOT)
    ax.text(0.5, 0.045, "Her eşleşme bir sayıyla sınanır: benzerlik kadar fark da söylenir.", ha="center", fontsize=23, color=TURUNCU, weight="bold")
    sekil("0.1", "harita")
    olc(d0_1_hafta=4, d0_1_ders=16)


if __name__ == "__main__":
    ders_1_1(); ders_1_2(); ders_1_3(); ders_1_4(); tanitim()
    print("hafta 1 tamam")
