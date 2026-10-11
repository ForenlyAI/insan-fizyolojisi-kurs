"""Hafta 2 · Kas Fizyolojisi — Ders 2.1–2.4.
Fizyoloji sayıları kaynaklar.py'den, robot sayıları benzetim kaydından ve kol tablolarından gelir.
Uzunluk–gerim eğrisinin platosu ve kırılma noktası kaynaklıdır (kurbağa kası lifi); eğrinin iki ucu ŞEMATİK'tir.
Kuvvet–hız eğrisi Hill (1938) özgün uyumudur (kurbağa kası); eksenler en büyük değere bölünmüştür.
Eklem döngüsü yanıtı MODEL HESABIDIR: kazançlar parametre tablosundan, başlangıç sapması ÖRNEK.
  python hafta2.py   → ekran/2.x/*.txt + *.png, OLCUMLER.json (d2_*), GOREVLER.json"""
import numpy as np
import matplotlib.pyplot as plt
from ortak import kayit, olc, oturum, sekil, gorev
from arac import (robot_ozet, on_kol, dirsek_parametre, geri_bildirim, tutma_torku, hill_sabitleri, hill_hiz, kutu, ok, bos_eksen,
                  cizelge, tr, sayi, TURUNCU, MAVI, YESIL, MOR, GRI, INSAN, ROBOT)
from kaynaklar import deger

SAPMA = 0.2                 # rad · ÖRNEK: eklemin hedefinden itildiği başlangıç sapması
SEMATIK_ALT_UM, SEMATIK_UST_UM, SEMATIK_KIRILMA = 1.27, 3.65, 0.84   # ŞEMATİK: eğrinin sıfıra indiği iki uç ve kırılmadaki gerim
ORNEK_LIF_CM, ORNEK_KISALMA = 10, 0.20     # ÖRNEK: lif boyu ve kısalma oranı


def yerlesme(t, q, bant=0.01):
    """Açının hedefin çevresindeki banda girip bir daha çıkmadığı an (s); çıkıyorsa None."""
    if np.isnan(q).any() or abs(q[-1]) > bant:
        return None
    dis = np.nonzero(np.abs(q) > bant)[0]
    return float(t[dis[-1] + 1]) if len(dis) else 0.0


def ders_2_1():
    """Sarkomer ve kayan iplikler ↔ eklem motorunun tork sınırı."""
    pa, pu, kir = deger("plato_alt_um"), deger("plato_ust_um"), deger("kirilma_um")
    r = robot_ozet()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(19.2, 10.8))
    x = [SEMATIK_ALT_UM, kir, pa, pu, SEMATIK_UST_UM]; y = [0, SEMATIK_KIRILMA, 1, 1, 0]
    a1.plot(x, y, color=INSAN, lw=5, marker="o", ms=12)
    a1.axvspan(pa, pu, color=INSAN, alpha=0.18)
    a1.text((pa + pu) / 2, 1.06, f"plato\n{tr(pa)}–{tr(pu, 1)} µm", ha="center", fontsize=22, color=INSAN, weight="bold")
    a1.annotate(f"düşüş dikleşir\n{tr(kir)} µm", xy=(kir, SEMATIK_KIRILMA), xytext=(1.78, 0.36), fontsize=20,
                arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    a1.text(3.0, 0.62, "uçlar\nŞEMATİK", fontsize=20, color=GRI, ha="center")
    a1.set_ylim(0, 1.28); a1.set_xlabel("sarkomer boyu (µm)"); a1.set_ylabel("gerim (en büyüğe oranla)")
    a1.set_title("Kas: gerim boya bağlı", fontsize=24)
    aci = np.linspace(np.degrees(r["alt"]), np.degrees(r["ust"]), 200)
    a2.plot(aci, np.full_like(aci, r["efor"]), color=ROBOT, lw=5, label=f"motorun tork sınırı: {tr(r['efor'], 0)} N·m (tablo)")
    a2.plot(aci, r["tutma_yatay"] * np.abs(np.cos(np.radians(aci))), color=TURUNCU, lw=4, ls="--",
            label=f"ön kolu tutmak için gereken: en çok {tr(r['tutma_yatay'], 1)} N·m")
    a2.set_ylim(0, 31); a2.set_xlabel("dirsek açısı (derece)"); a2.set_ylabel("tork (N·m)")
    a2.legend(loc="center", framealpha=1.0, fontsize=18)
    a2.set_title("Motor: sınır açıya bağlı değil", fontsize=24)
    fig.suptitle("Uzunluk–gerim eğrisi ve motorun tork sınırı · kas: yayın, motor: kol tablosu ve kaba model", fontsize=24)
    sekil("2.1", "uzunluk-gerim")

    ns = oturum("2.1", "sarkomer-hesabi", """
from kaynaklar import deger
sarkomer_um, vuru_nm = deger("sarkomer_um"), deger("vuru_nm")
lif_cm, kisalma = ORNEK_LIF_CM, ORNEK_KISALMA        # ÖRNEK lif boyu ve kısalma oranı
lif_cm, kisalma
adet = lif_cm * 10000 / sarkomer_um
round(adet)
sarkomer_kisalma_nm = 1000 * sarkomer_um * kisalma
sarkomer_kisalma_nm, lif_cm * kisalma
round(sarkomer_kisalma_nm / 2 / vuru_nm)
deger("plato_alt_um"), deger("plato_ust_um")
dinlenim_um = 2.1                                    # ÖRNEK dinlenim boyu
alt = dinlenim_um * deger("ideal_alt_yuzde") / 100
ust = dinlenim_um * deger("ideal_ust_yuzde") / 100
round(alt, 2), round(ust, 2)
""", ns=dict(ORNEK_LIF_CM=ORNEK_LIF_CM, ORNEK_KISALMA=ORNEK_KISALMA))
    kat = r["efor"] / r["tutma_yatay"]
    fig, ax = cizelge("Sarkomer ↔ eklem motoru", [
        ("Kuvvetin kaynağı", f"çapraz köprüler; her vuruş ince ipliği yaklaşık {deger('vuru_nm')} nm kaydırır", "sargılardaki akım; rotor döner"),
        ("Konuma bağlılık", f"gerim sarkomer boyuna bağlı; plato {tr(pa)}–{tr(pu, 1)} µm", f"tork sınırı her açıda aynı: {tr(r['efor'], 0)} N·m (tablo)"),
        ("Hareket aralığı", f"en büyük gerim dinlenim boyunun yüzde {deger('ideal_alt_yuzde')}–{deger('ideal_ust_yuzde')}'sinde", f"kayıtta dirsek {tr(r['aci_kullanilan'], 1)}° aralık kullandı; sınır 180°"),
        ("Yön", "yalnız çeker; karşıt kas geri getirir", "iki yöne de döner"),
    ], "Kasın kuvveti iplik örtüşmesine, yani boya bağlıdır ve kas yalnız çeker. Motorun tork sınırı açıdan bağımsızdır. Ortak olan, küçük birimlerin kuvvetinin toplanmasıdır.",
        kaynak="İnsan: OpenStax A&P 2e 10.2–10.4; Gordon, Huxley ve Julian (1966) · Robot: benzetim kaydı ve kol tablosu")
    sekil("2.1", "karsilastirma")
    gorev("2.1", "Dinlenim boyu 2,0 µm olan bir sarkomerde en büyük gerim aralığının üst ucu kaç µm'dir? (dinlenim boyunun yüzde 120'si)",
          round(2.0 * deger("ideal_ust_yuzde") / 100, 2), "µm", 0.02, "üst uç = dinlenim boyu × 1,20")
    olc(d2_1_sarkomer_um=deger("sarkomer_um"), d2_1_vuru_nm=deger("vuru_nm"), d2_1_ornek_lif_cm=ORNEK_LIF_CM, d2_1_ornek_kisalma=ORNEK_KISALMA,
        d2_1_sarkomer_adet=ns["adet"], d2_1_sarkomer_kisalma_nm=ns["sarkomer_kisalma_nm"], d2_1_lif_kisalma_cm=ORNEK_LIF_CM * ORNEK_KISALMA,
        d2_1_vurus=ns["sarkomer_kisalma_nm"] / 2 / deger("vuru_nm"), d2_1_plato=[pa, pu], d2_1_kirilma_um=kir,
        d2_1_ideal=[ns["alt"], ns["ust"]], d2_1_ornek_dinlenim_um=ns["dinlenim_um"], d2_1_efor_Nm=r["efor"], d2_1_tutma_yatay_Nm=r["tutma_yatay"],
        d2_1_tork_kati=kat, d2_1_aci_kullanilan=r["aci_kullanilan"], d2_1_aci_siniri=float(np.degrees(r["ust"] - r["alt"])),
        d2_1_sematik=[SEMATIK_ALT_UM, SEMATIK_UST_UM, SEMATIK_KIRILMA], d2_1_miyozin=deger("miyozin_adet"), d2_1_gorev_ust_um=2.0 * 1.2)


def ders_2_2():
    """Uyarılma–kasılma eşleşmesi ↔ komuttan torka zincir."""
    fig, ax = bos_eksen("Uyarıdan kuvvete: iki zincir, aynı sıra")
    ust = ["motor nöron\naksiyon\npotansiyeli", "asetilkolin\nuç plak\npotansiyeli", "kas lifi\naksiyon\npotansiyeli", "T tüpü\nvoltaj\nalgılayıcısı",
           "sarkoplazmik\nretikulum\nkalsiyum salar", "troponin\nçapraz köprü\nkuvvet"]
    alt = ["görev\nbilgisayarı\nhedef açı", "sinyal hattı\nsayı", "eklem\ndenetleyicisi\nhata hesabı", "sürücü\nakım komutu", "motor\nsargısı\nakım", "rotor\ndişli\ntork"]
    for ad, liste, renk, y in [("İnsan", ust, INSAN, 0.58), ("İnsansı robot", alt, ROBOT, 0.18)]:
        ax.text(0.01, y + 0.25, ad, fontsize=26, weight="bold", color=renk, va="center")
        for i, m in enumerate(liste):
            x = 0.012 + i * 0.166
            kutu(ax, x, y, 0.135, 0.19, m, renk, boy=18)
            if i < 5:
                ok(ax, x + 0.146, y + 0.095, x + 0.163, y + 0.095)
    ax.text(0.5, 0.47, "elektrik işareti → kimyasal ya da elektriksel aktarım → kuvvet", ha="center", fontsize=23)
    ax.text(0.5, 0.06, "Kasta gevşeme de enerji ister: kalsiyum ATP harcayan pompalarla geri alınır.", ha="center", fontsize=21, color=GRI)
    sekil("2.2", "eslesme-zinciri")

    P = dirsek_parametre(); I = on_kol()[3] + float(P["armatur"]); kp, kd = float(P["kp"]), float(P["kd"])
    t, q = geri_bildirim(kp, kd, I, baslangic=SAPMA, sure=1.0)
    ty = yerlesme(t, q)
    r = robot_ozet()
    ns = oturum("2.2", "zamanlama", """
from kaynaklar import deger
uc_plak, gereken = deger("uc_plak_mV"), deger("uc_plak_esik_mV")
uc_plak, gereken, round(uc_plak / gereken, 2)
deger("sarsi_ms")
from arac import robot_ozet
r = robot_ozet()
r["efor"], round(r["tutma_yatay"], 2)
round(r["efor"] / r["tutma_yatay"], 1)
r["kp"], r["kd"], SAPMA_ORNEK_RAD
round(YERLESME_S, 2)
round(1000 * YERLESME_S / deger("sarsi_ms"), 1)
1000 * r["adim"]
""", ns=dict(SAPMA_ORNEK_RAD=SAPMA, YERLESME_S=ty))
    guv = deger("uc_plak_mV") / deger("uc_plak_esik_mV"); kat = r["efor"] / r["tutma_yatay"]
    fig, ax = cizelge("Uyarılma–kasılma eşleşmesi ↔ komuttan torka", [
        ("Aktarım", "sinir ucunda asetilkolin; lifin içinde kalsiyum", "telde sayı; sargıda akım"),
        ("Güvenlik payı", f"uç plak potansiyeli {deger('uc_plak_mV')} mV, eşik için {deger('uc_plak_esik_mV')} mV yeter: {tr(guv)} kat", f"tork sınırı {tr(r['efor'], 0)} N·m, tutma için {tr(r['tutma_yatay'], 1)} N·m yeter: {tr(kat, 1)} kat"),
        ("Yanıt süresi", f"tek sarsı kas tipine göre birkaç ms ile {deger('sarsi_ms')} ms arası", f"MODEL: eklem {tr(ty)} s'de hedefe yerleşir (sapma ÖRNEK)"),
        ("Kapatma", "kalsiyum geri pompalanır, asetilkolin parçalanır", "akım komutu sıfırlanır"),
    ], "Kasta işaret iki kez biçim değiştirir: elektrikten kimyasala, kimyasaldan mekaniğe. Robotta işaret baştan sona elektrikseldir. Güvenlik payları aynı türden büyüklükler değildir, yalnız fikir ortaktır.",
        kaynak="İnsan: OpenStax A&P 2e 10.2–10.4; Byrne, Neuroscience Online bölüm 4 · Robot: kol tablosu; döngü yanıtı MODEL HESABI")
    sekil("2.2", "karsilastirma")
    gorev("2.2", "Uç plak potansiyeli 40 mV'a düşerse ve eşik için 30 mV yetiyorsa güvenlik payı kaç kat olur?",
          round(40 / deger("uc_plak_esik_mV"), 2), "kat", 0.02, "pay = uç plak potansiyeli / eşik için gereken")
    olc(d2_2_uc_plak=[deger("uc_plak_mV"), deger("uc_plak_esik_mV")], d2_2_guvenlik=guv, d2_2_sarsi_ms=deger("sarsi_ms"),
        d2_2_efor_Nm=r["efor"], d2_2_tutma_yatay_Nm=r["tutma_yatay"], d2_2_tork_kati=kat, d2_2_kp=kp, d2_2_kd=kd,
        d2_2_sapma_ornek_rad=SAPMA, d2_2_sapma_ornek_derece=float(np.degrees(SAPMA)), d2_2_yerlesme_s=ty,
        d2_2_yerlesme_sarsi_kati=1000 * ty / deger("sarsi_ms"), d2_2_adim_ms=1000 * r["adim"], d2_2_gorev_pay=40 / deger("uc_plak_esik_mV"))


def ders_2_3():
    """Motor birim ve kuvvet–hız ↔ motorun tork–hız sınırı."""
    a, b, c, F0, V0, egri = hill_sabitleri()
    F = np.linspace(0, F0, 400); V = hill_hiz(F); G = F * V
    i_en = int(G.argmax()); yari = float(hill_hiz(0.5 * F0) / V0)
    k = kayit(); r = robot_ozet()
    tork = np.abs(tutma_torku(k)); hiz = np.abs(k["dirsek_hiz_rad_s"])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(19.2, 10.8))
    a1.plot(F / F0, V / V0, color=INSAN, lw=5, label="kısalma hızı")
    a1.plot(F / F0, G / G.max(), color=MOR, lw=4, ls="--", label="güç (en büyüğe oranla)")
    a1.plot([F[i_en] / F0], [1.0], "o", ms=16, color=TURUNCU)
    a1.annotate(f"en büyük güç\nkuvvet {tr(F[i_en] / F0)}, hız {tr(V[i_en] / V0)}", xy=(F[i_en] / F0, 1.0), xytext=(0.52, 1.02), fontsize=19,
                arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    a1.set_xlabel("kuvvet (en büyüğe oranla)"); a1.set_ylabel("hız ve güç (en büyüğe oranla)"); a1.set_ylim(0, 1.16)
    a1.legend(loc="center right", framealpha=1.0, fontsize=18); a1.set_title("Kas: yük arttıkça hız düşer", fontsize=24)
    a2.plot(tork[::3], hiz[::3], ".", color=ROBOT, ms=5, alpha=0.5)
    a2.plot([0, r["efor"], r["efor"]], [r["hiz_siniri"], r["hiz_siniri"], 0], color=TURUNCU, lw=4, ls="--")
    a2.text(r["efor"] * 0.5, r["hiz_siniri"] * 1.03, f"sınırlar (tablo): {tr(r['efor'], 0)} N·m, {tr(r['hiz_siniri'], 0)} rad/s", ha="center", fontsize=19, color=TURUNCU, weight="bold")
    a2.annotate(f"kayıttaki noktalar\nen büyük hız {tr(r['hiz_en_buyuk'])} rad/s", xy=(2.0, r["hiz_en_buyuk"]), xytext=(8, 17), fontsize=20,
                arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.5))
    a2.set_xlim(0, r["efor"] * 1.08); a2.set_ylim(0, r["hiz_siniri"] * 1.12); a2.set_xlabel("tork (N·m, kaba model)"); a2.set_ylabel("dirsek hızı (rad/s)")
    a2.set_title("Motor: sınırların çok içinde", fontsize=24)
    fig.suptitle("Kuvvet–hız eğrisi · kas: Hill (1938) özgün uyumu, kurbağa kası · robot: benzetim kaydı", fontsize=24)
    sekil("2.3", "kuvvet-hiz")

    ns = oturum("2.3", "hill-hesabi", """
from kaynaklar import deger
a, b, c = deger("hill_a"), deger("hill_b"), deger("hill_c")
a, b, c
F0 = c / b - a
V0 = c / a - b
round(F0, 1), round(V0, 2), round(a / F0, 2)
def hiz(F):
    return c / (F + a) - b
round(hiz(0.5 * F0) / V0, 3)
import numpy as np
F = np.linspace(0, F0, 2001)
guc = F * hiz(F)
round(float(F[guc.argmax()] / F0), 2), round(float(hiz(F[guc.argmax()]) / V0), 2)
deger("motor_birim_kucuk"), deger("motor_birim_kuvvet_kati")
from arac import robot_ozet
r = robot_ozet()
round(r["hiz_en_buyuk"], 2), r["hiz_siniri"], round(100 * r["hiz_en_buyuk"] / r["hiz_siniri"], 1)
""")
    pay = 100 * r["hiz_en_buyuk"] / r["hiz_siniri"]
    fig, ax = cizelge("Motor birim ve kuvvet–hız ↔ motorun sınırları", [
        ("Kuvvet ayarı", f"birimler küçükten büyüğe devreye girer; en büyüğü {deger('motor_birim_kuvvet_kati')} kat kuvvetli", "akım kesintisiz ayarlanır; basamak yok"),
        ("Hız ve yük", f"yük en büyük kuvvetin yarısıyken hız yüzde {tr(100 * yari, 0)}'e düşer", f"sınırlar tabloda: {tr(r['efor'], 0)} N·m ve {tr(r['hiz_siniri'], 0)} rad/s"),
        ("En büyük güç", f"en büyük kuvvetin {tr(F[i_en] / F0)} katında (hesap); kaynakta yaklaşık {tr(deger('hill_guc_kuvvet'), 1)}", "kayıtta böyle bir nokta aranmadı"),
        ("Kullanılan pay", "günlük işte motor birimlerin küçük bölümü çalışır", f"kayıtta en büyük hız sınırın yüzde {tr(pay, 1)}'i"),
    ], "Kasın eğrisi çapraz köprülerin kimyasından doğar ve kurbağa kasında ölçülmüştür. Motorun sınırları tasarım sayılarıdır. Kas kuvveti basamak basamak, motor kesintisiz ayarlar.",
        kaynak="İnsan: OpenStax A&P 2e 10.4; Hill (1938) uyumu, Seow (2013) içinde · Robot: benzetim kaydı ve kol tablosu")
    sekil("2.3", "karsilastirma")
    c25 = float(hill_hiz(0.25 * F0) / V0)
    gorev("2.3", "Hill uyumunda yük en büyük kuvvetin dörtte biriyken kısalma hızı en büyük hızın yüzde kaçıdır?",
          round(100 * c25, 1), "%", 1.0, "V = c / (F + a) − b; F = 0,25 × F0; sonucu V0'a bölün")
    olc(d2_3_hill=[a, b, c], d2_3_F0=F0, d2_3_V0=V0, d2_3_egrilik=egri, d2_3_yari_yukte_hiz=yari, d2_3_guc_kuvvet=float(F[i_en] / F0),
        d2_3_guc_hiz=float(V[i_en] / V0), d2_3_guc_kuvvet_kaynak=deger("hill_guc_kuvvet"), d2_3_motor_birim_kucuk=deger("motor_birim_kucuk"),
        d2_3_motor_birim_kat=deger("motor_birim_kuvvet_kati"), d2_3_tetanus=[deger("tetanus_kat_alt"), deger("tetanus_kat_ust")],
        d2_3_hiz_en_buyuk=r["hiz_en_buyuk"], d2_3_hiz_siniri=r["hiz_siniri"], d2_3_hiz_payi_yuzde=pay, d2_3_efor_Nm=r["efor"],
        d2_3_gorev_ceyrek_yuzde=100 * c25)


def ders_2_4():
    """Kas lif tipleri ve enerji ↔ motorun verimi (hafta ürünü: kas–motor çizelgesi)."""
    fig, ax = bos_eksen("İskelet kasının üç lif tipi")
    bas = ["", "Yavaş oksidatif", "Hızlı oksidatif", "Hızlı glikolitik"]
    sat = [("Kasılma", "yavaş", "hızlı", "hızlı"),
           ("Mitokondri", "çok", "çok", "az"),
           ("Miyoglobin", "var, kırmızı", "az", "az, beyaz"),
           ("Yorulma", "geç yorulur", "orta", "çabuk yorulur"),
           ("Çap ve gerim", "ince, düşük gerim", "orta, yüksek gerim", "kalın, en yüksek gerim"),
           ("Tipik iş", "duruş, tutma", "yürüme", "kısa, güçlü hareket")]
    xs = [0.01, 0.23, 0.49, 0.75]; ws = [0.19, 0.21, 0.21, 0.21]
    renk = [None, INSAN, MOR, TURUNCU]
    for j in range(1, 4):
        kutu(ax, xs[j], 0.86, ws[j], 0.08, bas[j], renk[j], boy=24)
    for i, s in enumerate(sat):
        y = 0.75 - i * 0.115
        if i % 2 == 0:
            ax.axhspan(y - 0.012, y + 0.085, color="#F3F4F6")
        ax.text(xs[0] + 0.005, y + 0.036, s[0], fontsize=23, weight="bold", va="center")
        for j in range(1, 4):
            ax.text(xs[j] + ws[j] / 2, y + 0.036, s[j], fontsize=22, va="center", ha="center")
    ax.text(0.5, 0.035, f"Hızlı lifler ATP'yi yavaş liflerden yaklaşık {deger('hizli_lif_kat')} kat hızlı parçalar. Kaynak: OpenStax A&P 2e 10.5.", ha="center", fontsize=20, color=GRI)
    sekil("2.4", "lif-tipleri")

    ns = oturum("2.4", "enerji-hesabi", """
from kaynaklar import deger
from arac import robot_ozet
r = robot_ozet()
round(r["sure"], 1), round(100 * r["durgun_pay"]), round(r["mekanik_is"], 1)
deger("kreatin_fosfat_s"), deger("glikoliz_s"), deger("oksijenli_pay_yuzde")
verim_kas, verim_motor = deger("verim_kas_yuzde") / 100, deger("verim_motor_yuzde") / 100
verim_kas, verim_motor
kas_enerji = r["mekanik_is"] / verim_kas
motor_enerji = r["mekanik_is"] / verim_motor
round(kas_enerji, 1), round(motor_enerji, 1)
round(1000 * kas_enerji / (1000 * deger("karbonhidrat_kJ_g")), 1)
""")
    r = robot_ozet(); kas_e, mot_e = ns["kas_enerji"], ns["motor_enerji"]
    fig, ax = cizelge("Kas ↔ eklem motoru · hafta ürünü", [
        ("Birim", f"sarkomer ≈ {tr(deger('sarkomer_um'), 0)} µm; kuvvet boya ve hıza bağlı", f"tek motor; sınırlar {tr(r['efor'], 0)} N·m ve {tr(r['hiz_siniri'], 0)} rad/s"),
        ("Çeşit", "üç lif tipi: yavaş oksidatif, hızlı oksidatif, hızlı glikolitik", "eklemde tek tip motor; iş bölümü yok"),
        ("Enerji kaynağı", f"kreatin fosfat ≈ {deger('kreatin_fosfat_s')} s, glikoliz ≈ {deger('glikoliz_s')} s, sonra oksijenli solunum", f"kayıt {tr(r['sure'], 1)} s; elektrik tüketimi kayıtta yok"),
        ("Verim", f"bisiklet ve tırmanmada yüzde {deger('verim_kas_yuzde')}: {tr(r['mekanik_is'], 1)} J iş için {tr(kas_e, 0)} J", f"elektrik motoru yüzde {deger('verim_motor_yuzde')} (temsilî): aynı iş için {tr(mot_e, 1)} J"),
    ], "Kas yakıtını kendi içinde üç yoldan üretir, yorulur ve onarılır. Motorun enerjisi dışarıdan gelir. Verim sayıları ders kitabı değerleridir, bu robotun ölçümü değildir.",
        kaynak="İnsan: OpenStax A&P 2e 10.3, 10.5; College Physics 2e Tablo 7.1–7.2 · Robot: benzetim kaydı (mekanik iş kaba model)")
    sekil("2.4", "karsilastirma")
    gorev("2.4", "Bir kas 150 J mekanik iş yapıyor ve verimi yüzde 20. Harcadığı toplam enerji kaç J?",
          round(150 / (deger("verim_kas_yuzde") / 100), 0), "J", 5.0, "enerji = iş / verim")
    olc(d2_4_sure_s=r["sure"], d2_4_durgun_yuzde=100 * r["durgun_pay"], d2_4_mekanik_is_J=r["mekanik_is"], d2_4_verim=[deger("verim_kas_yuzde"), deger("verim_motor_yuzde")],
        d2_4_kas_enerji_J=kas_e, d2_4_motor_enerji_J=mot_e, d2_4_karbonhidrat_mg=1000 * kas_e / (1000 * deger("karbonhidrat_kJ_g")),
        d2_4_kaynak_sure=[deger("kreatin_fosfat_s"), deger("glikoliz_s")], d2_4_oksijenli_yuzde=deger("oksijenli_pay_yuzde"),
        d2_4_hizli_lif_kat=deger("hizli_lif_kat"), d2_4_gorev_J=150 / (deger("verim_kas_yuzde") / 100))


if __name__ == "__main__":
    ders_2_1(); ders_2_2(); ders_2_3(); ders_2_4()
    print("hafta 2 tamam")
