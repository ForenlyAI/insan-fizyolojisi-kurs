"""Hafta 4 · Sindirim — Ders 4.1–4.4.
Fizyoloji sayıları kaynaklar.py'den, robot sayıları benzetim kaydından ve kol tablolarından gelir.
Enzim eğrisi Michaelis–Menten denklemidir; derişim, yarı hız derişimine bölünerek verilir (belirli bir enzimin ölçümü değil).
Kayıtta elektrik tüketimi ve pil verisi YOKTUR; enerji karşılaştırması dirseğin mekanik işi ve ders kitabındaki verim değerleriyle yapılır.
  python hafta4.py   → ekran/4.x/*.txt + *.png, OLCUMLER.json (d4_*), GOREVLER.json"""
import numpy as np
import matplotlib.pyplot as plt
from ortak import kayit, yumusat, olc, oturum, sekil, gorev
from arac import (robot_ozet, evreler, kutu, ok, bos_eksen, cizelge, tr, sayi, TURUNCU, MAVI, YESIL, MOR, GRI, INSAN, ROBOT)
from kaynaklar import deger


def bardak():
    """Kayıtta bardağın taşıma evresi: (süre s, ortalama hız m/s, en büyük hız m/s, kat edilen yol m)."""
    k = kayit(); t, hiz, evre, ilk, son = evreler()
    p = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"], k["bardak_z_m"]]))
    yol = float(np.sum(np.linalg.norm(np.diff(p[ilk:son + 1], axis=0), axis=1)))
    return float(t[son] - t[ilk]), float(hiz[evre == 1].mean()), float(hiz.max()), yol


def ders_4_1():
    """Sindirim kanalı hareketleri ↔ bardağın taşınması."""
    bolum = [("yutma (yemek borusu)", deger("yutma_alt_s"), deger("yutma_ust_s"), INSAN),
             ("mide", 3600 * deger("mide_bosalma_alt_h"), 3600 * deger("mide_bosalma_ust_h"), MOR),
             ("ince bağırsak", 3600 * deger("ince_gecis_alt_h"), 3600 * deger("ince_gecis_ust_h"), TURUNCU),
             ("kalın bağırsak", 3600 * deger("kalin_bekleme_alt_h"), 3600 * deger("kalin_bekleme_ust_h"), GRI)]
    sure, ort, enb, yol = bardak()
    fig, ax = plt.subplots()
    for i, (ad, a, b, renk) in enumerate(bolum):
        y = 4 - i
        ax.barh(y, b - a, left=a, height=0.55, color=renk)
        yazi = f"{a:g}–{b:g} s" if b < 60 else f"{a / 3600:g}–{b / 3600:g} saat"
        ax.text(b * 1.25, y, f"{ad}: {yazi}", va="center", fontsize=24, weight="bold", color=renk)
    ax.barh(0, 1.0, left=sure - 0.5, height=0.55, color=ROBOT, hatch="//", edgecolor="#ffffff")
    ax.plot([sure], [0], "D", ms=18, color=ROBOT)
    ax.text(sure * 1.35, 0, f"robot: bardağın taşınması {tr(sure, 1)} s (benzetim kaydı)", va="center", fontsize=24, weight="bold", color=ROBOT)
    ax.set_xscale("log"); ax.set_xlim(1, 3e7); ax.set_yticks([]); ax.set_ylim(-0.7, 4.7); ax.set_xlabel("süre (saniye, logaritmik)")
    ax.set_title("Sindirim kanalında geçiş süreleri · ders kitabı aralıkları")
    sekil("4.1", "gecis-sureleri")

    ns = oturum("4.1", "iletim-hizi", """
from kaynaklar import deger
boru_cm = deger("yemek_borusu_cm")
round(boru_cm / deger("yutma_ust_s"), 1), round(boru_cm / deger("yutma_alt_s"), 1)
ince_cm = 100 * deger("ince_bagirsak_m")
round(ince_cm / (3600 * deger("ince_gecis_ust_h")), 3), round(ince_cm / (3600 * deger("ince_gecis_alt_h")), 3)
deger("segment_duodenum_dk"), deger("segment_ileum_dk"), round(60 / deger("mide_dalga_s"))
round(deger("segment_duodenum_dk") / 60, 2)
sure, ortalama, en_buyuk, yol = BARDAK
round(sure, 1), round(100 * ortalama, 1), round(yol, 2)
round(100 * ortalama / (boru_cm / deger("yutma_ust_s")), 1)
from arac import robot_ozet
robot_ozet()["saniyede"]
""", ns=dict(BARDAK=(sure, ort, enb, yol)))
    boru = deger("yemek_borusu_cm"); v_alt, v_ust = boru / deger("yutma_ust_s"), boru / deger("yutma_alt_s")
    ince = 100 * deger("ince_bagirsak_m"); i_alt, i_ust = ince / (3600 * deger("ince_gecis_ust_h")), ince / (3600 * deger("ince_gecis_alt_h"))
    r = robot_ozet()
    fig, ax = cizelge("Sindirim kanalı hareketleri ↔ bardağın taşınması", [
        ("İlerletme", "peristaltizm: kasılma dalgası içeriği iter", "kol bardağı tutar, robot onu taşır"),
        ("Karıştırma", f"segmentasyon: onikiparmak bağırsağında dakikada {deger('segment_duodenum_dk')}, ileumda {deger('segment_ileum_dk')}", "karıştırma yok; bardak dökülmeden taşınır"),
        ("Hız", f"yemek borusunda {tr(v_alt, 1)}–{tr(v_ust, 1)} cm/s; ince bağırsakta {tr(i_alt, 3)}–{tr(i_ust, 3)} cm/s", f"kayıtta ortalama {tr(100 * ort, 1)} cm/s, {tr(yol)} m yol"),
        ("Ritim", f"midede yaklaşık {deger('mide_dalga_s')} s'de bir dalga", f"denetim saniyede {r['saniyede']} ölçümle"),
    ], "Bağırsak içeriği bilerek yavaş taşır, çünkü asıl iş taşıma değil, karıştırma ve emilimdir. Robot yükü olduğu gibi ve hızla taşır. İkisinde de ilerleme sıralı kasılma ya da sıralı eklem hareketiyle olur.",
        kaynak="İnsan: OpenStax A&P 2e 23.2–23.5 · Robot: benzetim kaydı (taşıma evresi bardağın yatay hızından)")
    sekil("4.1", "karsilastirma")
    g = 100 * deger("ince_bagirsak_m") / (4 * 3600)
    gorev("4.1", "İnce bağırsak 3,05 m ve içerik 4 saatte geçiyor. Ortalama ilerleme hızı kaç cm/s'dir?",
          round(g, 3), "cm/s", 0.002, "hız = yol / süre; 4 saat = 14400 s")
    olc(d4_1_boru_cm=boru, d4_1_yutma_s=[deger("yutma_alt_s"), deger("yutma_ust_s")], d4_1_boru_hiz_cm_s=[v_alt, v_ust],
        d4_1_ince_hiz_cm_s=[i_alt, i_ust], d4_1_segment=[deger("segment_duodenum_dk"), deger("segment_ileum_dk")], d4_1_mide_dalga_s=deger("mide_dalga_s"),
        d4_1_mide_dalga_dk=60 / deger("mide_dalga_s"), d4_1_sureler_saat=[deger("mide_bosalma_alt_h"), deger("mide_bosalma_ust_h"), deger("ince_gecis_alt_h"),
                                                                     deger("ince_gecis_ust_h"), deger("kalin_bekleme_alt_h"), deger("kalin_bekleme_ust_h")],
        d4_1_kanal_m=deger("kanal_m"), d4_1_bardak_sure_s=sure, d4_1_bardak_hiz_cm_s=100 * ort, d4_1_bardak_en_buyuk_cm_s=100 * enb, d4_1_bardak_yol_m=yol,
        d4_1_hiz_orani=100 * ort / v_alt, d4_1_saniyede=r["saniyede"], d4_1_gorev_cm_s=g)


def ders_4_2():
    """Salgılar ve enzimler ↔ motorun doyması."""
    salgi = [("tükürük", deger("tukuruk_pH_alt"), deger("tukuruk_pH_ust"), INSAN), ("mide içeriği", deger("mide_pH_alt"), deger("mide_pH_ust"), TURUNCU),
             ("pankreas özsuyu", deger("pankreas_pH_alt"), deger("pankreas_pH_ust"), MOR), ("safra", deger("safra_pH_alt"), deger("safra_pH_ust"), GRI)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(19.2, 10.8))
    for i, (ad, a, b, renk) in enumerate(salgi):
        a1.barh(3 - i, b - a, left=a, height=0.5, color=renk)
        a1.text(0.3, 3 - i + 0.36, f"{ad}: pH {tr(a, 2 if a == 6.35 else 1)}–{tr(b, 2 if b == 6.85 else 1)}", ha="left", fontsize=20, weight="bold", color=renk)
    a1.axvline(deger("kan_pH"), color="#111111", lw=2.5, ls="--"); a1.text(deger("kan_pH") - 0.15, -0.55, f"kan pH {tr(deger('kan_pH'), 1)}", ha="right", fontsize=19)
    a1.set_xlim(0, 10); a1.set_ylim(-0.8, 3.9); a1.set_yticks([]); a1.set_xlabel("pH"); a1.set_title("Salgıların pH aralığı", fontsize=24)
    s = np.linspace(0, 12, 400); v = s / (1 + s)
    a2.plot(s, 100 * v, color=INSAN, lw=5)
    for x in [1, 3, 9]:
        a2.plot([x], [100 * x / (1 + x)], "o", ms=15, color=TURUNCU)
        a2.annotate(f"{x} kat → yüzde {tr(100 * x / (1 + x), 0)}", xy=(x, 100 * x / (1 + x)), xytext=(x + 0.8, 100 * x / (1 + x) - 13), fontsize=20,
                    arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    a2.axhline(100, color=GRI, ls="--", lw=2.5); a2.text(11.8, 101.5, "en büyük hız", ha="right", fontsize=19, color=GRI)
    a2.set_ylim(0, 110); a2.set_xlabel("substrat derişimi (yarı hız derişiminin katı)"); a2.set_ylabel("tepkime hızı (en büyüğün yüzdesi)")
    a2.set_title("Enzim doyar: Michaelis–Menten", fontsize=24)
    fig.suptitle("Her salgı kendi pH'ında çalışır, her enzim doyar · pH: ders kitabı, eğri: denklem", fontsize=24)
    sekil("4.2", "ph-ve-doyma")

    ns = oturum("4.2", "salgi-hesabi", """
from kaynaklar import deger
kan = deger("kan_pH")
round(10 ** (kan - deger("mide_pH_ust"))), round(10 ** (kan - deger("mide_pH_alt")))
def hiz_orani(kat):
    return kat / (1 + kat)
[round(100 * hiz_orani(k)) for k in (1, 3, 9)]
giren, icilen = deger("bagirsaga_giren_L"), deger("icilen_L")
round(giren - icilen, 1)
from arac import robot_ozet
import math
r = robot_ozet()
r["efor"], r["kp"]
doyma_rad = r["efor"] / r["kp"]
round(doyma_rad, 3), round(math.degrees(doyma_rad), 1)
round(100 * r["tutma_en_buyuk"] / r["efor"])
""")
    r = robot_ozet(); doy = ns["doyma_rad"]
    h_alt, h_ust = 10 ** (deger("kan_pH") - deger("mide_pH_ust")), 10 ** (deger("kan_pH") - deger("mide_pH_alt"))
    fig, ax = cizelge("Enzimin doyması ↔ motorun tork sınırı", [
        ("Dönüştürücü", "enzim: substratı ürüne çevirir; kendisi tükenmez", "motor: elektriği torka çevirir"),
        ("Doyma", "substrat arttıkça hız en büyük değere yaklaşır; dokuz katında yüzde 90", f"tork {tr(r['efor'], 0)} N·m'de kesilir (tablo)"),
        ("Doymanın nedeni", "enzim moleküllerinin hepsi dolu", f"MODEL: sapma {tr(np.degrees(doy), 1)}°'yi geçince komut sınıra dayanır"),
        ("Çalışma koşulu", f"pH: mide {tr(deger('mide_pH_alt'), 1)}–{tr(deger('mide_pH_ust'), 1)}, pankreas özsuyu {tr(deger('pankreas_pH_alt'), 1)}–{tr(deger('pankreas_pH_ust'), 1)}", f"kayıtta torkun en çok yüzde {tr(100 * r['tutma_en_buyuk'] / r['efor'], 0)}'si kullanıldı"),
    ], "İkisi de girdiyi ne kadar artırırsanız artırın belli bir hızın üstüne çıkamaz. Enzim kendi substratına ve pH'ına özgüdür, motor her komuta aynı yanıtı verir. Eğri bir denklemdir, belirli bir enzimin ölçümü değildir.",
        kaynak="İnsan: OpenStax A&P 2e 23.3–23.7; Michaelis–Menten denklemi (Johnson ve Goody, 2011) · Robot: kol tablosu ve benzetim kaydı")
    sekil("4.2", "karsilastirma")
    gorev("4.2", "Substrat derişimi yarı hız derişiminin 4 katıysa tepkime hızı en büyük hızın yüzde kaçıdır?",
          round(100 * 4 / 5, 0), "%", 1.0, "hız oranı = kat / (1 + kat)")
    olc(d4_2_pH=dict(tukuruk=[deger("tukuruk_pH_alt"), deger("tukuruk_pH_ust")], mide=[deger("mide_pH_alt"), deger("mide_pH_ust")],
                     pankreas=[deger("pankreas_pH_alt"), deger("pankreas_pH_ust")], safra=[deger("safra_pH_alt"), deger("safra_pH_ust")], kan=deger("kan_pH")),
        d4_2_hidrojen_kati=[h_alt, h_ust], d4_2_hiz_yuzde=[50.0, 75.0, 90.0], d4_2_salgi_L=deger("bagirsaga_giren_L") - deger("icilen_L"),
        d4_2_giren_L=deger("bagirsaga_giren_L"), d4_2_icilen_L=deger("icilen_L"), d4_2_tukuruk_L=[deger("tukuruk_alt_L"), deger("tukuruk_ust_L")],
        d4_2_safra_L=deger("safra_L"), d4_2_efor_Nm=r["efor"], d4_2_kp=r["kp"], d4_2_doyma_rad=doy, d4_2_doyma_derece=float(np.degrees(doy)),
        d4_2_tork_payi_yuzde=100 * r["tutma_en_buyuk"] / r["efor"], d4_2_gorev_yuzde=80.0)


def ders_4_3():
    """Emilim ve enerji dengesi ↔ enerji alımı ve dönüşüm verimi."""
    r = robot_ozet()
    gunluk_W = 1e6 * deger("gunluk_besin_MJ") / 86400
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(19.2, 10.8))
    besin = [("karbonhidrat", deger("karbonhidrat_kJ_g"), INSAN, ""), ("protein", deger("protein_kJ_g"), MOR, "//"), ("yağ", deger("yag_kJ_g"), TURUNCU, "xx")]
    for i, (ad, e, renk, desen) in enumerate(besin):
        a1.bar(i, e, color=renk, hatch=desen, edgecolor="#ffffff", width=0.65)
        a1.text(i, e + 0.8, f"{e} kJ", ha="center", fontsize=24, weight="bold", color=renk)
    a1.set_xticks(range(3)); a1.set_xticklabels([b[0] for b in besin]); a1.set_ylim(0, 46); a1.set_ylabel("bir gramın enerjisi (kJ)")
    a1.set_title("Besinin enerjisi", fontsize=24)
    guc = [("bazal", deger("bazal_guc_W")), ("otururken", deger("oturma_guc_W")), ("günlük besin\nortalaması", gunluk_W), ("yürürken", deger("yurume_guc_W"))]
    for i, (ad, w) in enumerate(guc):
        a2.bar(i, w, color=GRI if i == 2 else INSAN, hatch="//" if i == 2 else "", edgecolor="#ffffff", width=0.65)
        a2.text(i, w + 5, f"{tr(w, 0)} W", ha="center", fontsize=24, weight="bold")
    a2.set_xticks(range(4)); a2.set_xticklabels([g[0] for g in guc], fontsize=19); a2.set_ylim(0, 320); a2.set_ylabel("güç (W)")
    a2.set_title("Harcanan güç", fontsize=24)
    fig.suptitle("Enerji dengesi: alınan ve harcanan · değerler ders kitabı tablolarından", fontsize=24)
    sekil("4.3", "enerji-dengesi")

    ns = oturum("4.3", "enerji-hesabi", """
from kaynaklar import deger
deger("emilim_yuzeyi_m2"), deger("yuzey_kati")
round(deger("bagirsaga_giren_L") * deger("su_emilim_yuzde") / 100, 1)
gunluk_W = 1e6 * deger("gunluk_besin_MJ") / 86400
round(gunluk_W), deger("bazal_guc_W"), deger("oturma_guc_W")
from arac import robot_ozet
r = robot_ozet()
insan_kJ = deger("oturma_guc_W") * r["sure"] / 1000
round(insan_kJ, 1), round(insan_kJ / deger("karbonhidrat_kJ_g"), 2)
round(r["mekanik_is"], 1)
kas_J = r["mekanik_is"] / (deger("verim_kas_yuzde") / 100)
motor_J = r["mekanik_is"] / (deger("verim_motor_yuzde") / 100)
round(kas_J), round(motor_J, 1), round(kas_J / motor_J, 1)
ogun_kJ = 60 * deger("karbonhidrat_kJ_g") + 20 * deger("yag_kJ_g") + 25 * deger("protein_kJ_g")
ogun_kJ, round(ogun_kJ * 1000 / deger("oturma_guc_W") / 60)
""")
    ins = ns["insan_kJ"]; kas_J, mot_J = ns["kas_J"], ns["motor_J"]
    fig, ax = cizelge("Emilim ve enerji dengesi ↔ enerji alımı ve verim", [
        ("Enerjinin girişi", f"emilim yüzeyi yaklaşık {deger('emilim_yuzeyi_m2')} m²; besin önce parçalanır, sonra emilir", "pil doldurulur; dönüşüm gerekmez"),
        ("Depo", f"yağ gramı {deger('yag_kJ_g')} kJ, karbonhidrat {deger('karbonhidrat_kJ_g')} kJ", "pil verisi kayıtta yok"),
        (f"{tr(r['sure'], 1)} s içinde", f"oturan insan {tr(ins, 1)} kJ harcar: {tr(ins / deger('karbonhidrat_kJ_g'))} g karbonhidrat", f"dirseğin mekanik işi {tr(r['mekanik_is'], 1)} J (kaba model)"),
        ("Dönüşüm verimi", f"kas yüzde {deger('verim_kas_yuzde')}: aynı iş için {tr(kas_J, 0)} J", f"elektrik motoru yüzde {deger('verim_motor_yuzde')} (temsilî): {tr(mot_J, 1)} J"),
    ], "Beden yakıtını kendi sindirir, depolar ve dinlenirken bile harcar. Robotun enerjisi hazır gelir. Verim sayıları ders kitabı değerleridir; bu robotun elektrik tüketimi kayıtta bulunmadığı için ölçülmedi.",
        kaynak="İnsan: OpenStax A&P 2e 23.5, 23.7; College Physics 2e Tablo 7.1, 7.2, 7.4, 7.5 · Robot: benzetim kaydı (mekanik iş kaba model)")
    sekil("4.3", "karsilastirma")
    g_kJ = 50 * deger("karbonhidrat_kJ_g") + 10 * deger("yag_kJ_g") + 20 * deger("protein_kJ_g")
    gorev("4.3", "50 g karbonhidrat, 10 g yağ ve 20 g protein içeren bir öğünün enerjisi kaç kJ'dir?",
          g_kJ, "kJ", 10.0, "enerji = gram × (17, 39, 17) kJ toplamı")
    olc(d4_3_yuzey_m2=deger("emilim_yuzeyi_m2"), d4_3_yuzey_kati=deger("yuzey_kati"), d4_3_su_emilen_L=deger("bagirsaga_giren_L") * deger("su_emilim_yuzde") / 100,
        d4_3_besin_kJ_g=[deger("karbonhidrat_kJ_g"), deger("protein_kJ_g"), deger("yag_kJ_g")], d4_3_gunluk_W=gunluk_W, d4_3_gunluk_MJ=deger("gunluk_besin_MJ"),
        d4_3_guc_W=[deger("bazal_guc_W"), deger("oturma_guc_W"), deger("yurume_guc_W")], d4_3_insan_kJ=ins, d4_3_insan_karbonhidrat_g=ins / deger("karbonhidrat_kJ_g"),
        d4_3_mekanik_is_J=r["mekanik_is"], d4_3_kas_J=kas_J, d4_3_motor_J=mot_J, d4_3_kat=kas_J / mot_J, d4_3_ornek_ogun_kJ=ns["ogun_kJ"],
        d4_3_ornek_ogun_dk=ns["ogun_kJ"] * 1000 / deger("oturma_guc_W") / 60, d4_3_karbonhidrat_emilim=deger("karbonhidrat_emilim_g_saat"),
        d4_3_gorev_kJ=g_kJ, d4_3_gorev_dk=g_kJ * 1000 / deger("oturma_guc_W") / 60)


def ders_4_4():
    """Sindirimin denetimi ↔ katmanlı denetim (hafta ürünü ve bitirme işi)."""
    fig, ax = bos_eksen("Sindirimin üç denetim katmanı ve robottaki karşılıkları")
    kat = [("Yerel", "enterik sinir sistemi\nkısa refleks", "eklem denetleyicisi\nher eklemde ayrı döngü", "en hızlı"),
           ("Merkezî", "otonom sinirler\nuzun refleks", "görev bilgisayarı\nhedefleri gönderir", "hızlı"),
           ("Yaygın", "hormonlar: gastrin,\nsekretin, kolesistokinin", "karşılığı zayıf:\nortak ayar değeri", "yavaş, kalıcı")]
    for i, (ad, ins, rob, hiz) in enumerate(kat):
        y = 0.68 - i * 0.24
        ax.text(0.01, y + 0.085, ad, fontsize=26, weight="bold", va="center")
        kutu(ax, 0.16, y, 0.32, 0.17, ins, INSAN, boy=22)
        kutu(ax, 0.54, y, 0.30, 0.17, rob, ROBOT, boy=22)
        ax.text(0.875, y + 0.085, hiz, fontsize=22, color=TURUNCU, weight="bold", va="center")
    ax.text(0.32, 0.93, "İnsan", ha="center", fontsize=26, weight="bold", color=INSAN)
    ax.text(0.69, 0.93, "İnsansı robot", ha="center", fontsize=26, weight="bold", color=ROBOT)
    ax.text(0.5, 0.06, f"Enterik sinir sisteminde yaklaşık {deger('enterik_noron_milyon')} milyon nöron bulunur. Kaynak: OpenStax A&P 2e 23.1–23.2.", ha="center", fontsize=20, color=GRI)
    sekil("4.4", "denetim-katmanlari")

    ns = oturum("4.4", "haberci-hizi", """
from kaynaklar import deger
hormonlar = [("gastrin", "mide", "midede asit salgısını artırır"),
             ("sekretin", "onikiparmak bağırsağı", "pankreastan bikarbonatlı salgıyı uyarır"),
             ("kolesistokinin", "onikiparmak bağırsağı", "pankreas enzimlerini ve safrayı uyarır"),
             ("mide baskılayıcı peptit", "onikiparmak bağırsağı", "mide salgısını ve boşalmasını yavaşlatır")]
for ad, kaynak, etki in hormonlar:
    print(f"{ad:24s} {kaynak:22s} {etki}")
sinir_ms = 1000 * 1.0 / deger("sinir_hizi_en_hizli")
dolasim_s = 60 * deger("kan_hacmi_L") / deger("kalp_debisi_L_dk")
sinir_ms, round(dolasim_s)
from arac import robot_ozet
adim_ms = 1000 * robot_ozet()["adim"]
adim_ms, round(1000 * dolasim_s / adim_ms)
deger("enterik_noron_milyon"), deger("mide_evresi_alt_h"), deger("mide_evresi_ust_h")
""")
    r = robot_ozet(); dol = ns["dolasim_s"]
    fig, ax = cizelge("Sindirimin denetimi ↔ katmanlı denetim · hafta ürünü", [
        ("Yerel döngü", f"enterik sinir sistemi: yaklaşık {deger('enterik_noron_milyon')} milyon nöron, kanalın duvarında", "eklem denetleyicisi: dört eklemde ayrı kazançlar (tablo)"),
        ("Merkezle bağ", "parasempatik uyarı artırır, sempatik uyarı azaltır", "görev bilgisayarı hedef açıları yollar"),
        ("Haberci hızı", f"sinir: 1 m yol {tr(ns['sinir_ms'], 0)} ms; hormon: kanın bir turu yaklaşık {tr(dol, 0)} s (hesap)", f"kayıtta {tr(1000 * r['adim'], 0)} ms'de bir ölçüm"),
        ("Geri bildirim", "bağırsak dolunca mide boşalması yavaşlar", "sapma büyüyünce düzeltme torku büyür"),
    ], "Bedende hızlı sinir ve yavaş hormon aynı işi birlikte ayarlar, yerel ağ merkez olmadan da çalışır. Robotta haberci tektir ve hep hızlıdır. Hormonun yavaşlığı kusur değil, etkinin uzun sürmesini sağlayan bir özelliktir.",
        kaynak="İnsan: OpenStax A&P 2e 18.1, 19.4, 23.1, 23.2, 23.4, 23.6 · Robot: kol tablosu ve benzetim kaydı")
    sekil("4.4", "karsilastirma")
    gorev("4.4", "Asitli mide içeriği onikiparmak bağırsağına girince salınan ve pankreastan bikarbonatlı salgıyı uyaran hormon hangisidir? (tek sözcük, küçük harf)",
          "sekretin", "", 0, "Hormon çizelgesinde hedefi pankreas, etkisi bikarbonat olan satır.")
    olc(d4_4_enterik_milyon=deger("enterik_noron_milyon"), d4_4_sinir_ms=ns["sinir_ms"], d4_4_dolasim_s=dol, d4_4_adim_ms=1000 * r["adim"],
        d4_4_dolasim_adim=1000 * dol / (1000 * r["adim"]), d4_4_mide_evresi_h=[deger("mide_evresi_alt_h"), deger("mide_evresi_ust_h")],
        d4_4_kan_L=deger("kan_hacmi_L"), d4_4_debi_L_dk=deger("kalp_debisi_L_dk"), d4_4_hormon_sayisi=len(ns["hormonlar"]), d4_4_eklem_sayisi=4)


if __name__ == "__main__":
    ders_4_1(); ders_4_2(); ders_4_3(); ders_4_4()
    print("hafta 4 tamam")
