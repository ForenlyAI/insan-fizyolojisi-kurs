"""İnsan Fizyolojisi ve Robot Sistemleri — ortak hesaplar ve çizim yardımcıları.
  tablo(ad)                 : kol tablosunu okur ("sag_kol_kutle" ya da "sag_kol_parametre")
  on_kol()                  : dirsekten sonraki parçaların toplam kütlesi, kütle × uzaklık toplamı ve dönme eylemsizliği
  egim(k)                   : ön kolun yatayla yaptığı açı (kaba model: omuz açısı + dirsek açısı)
  geri_bildirim(...)        : tek eklemli geri bildirim döngüsünün model hesabı (kazançlar parametre tablosundan)
  evreler()                 : kayıtta kaldırma, taşıma ve bırakma evreleri (bardağın yatay hızından)
  cizelge(...)              : insan ile robotu yan yana koyan karşılaştırma çizelgesi
  zar_modeli(akim, ...)     : Hodgkin–Huxley zar modeli (mürekkep balığı dev aksonu, 6,3 °C; parametreler kaynaklar.py: pool2011)
  hill_hiz(F)               : Hill (1938) özgün uyumundan verilen kuvvette kısalma hızı
  doygunluk(P)              : Severinghaus (1979) denklemiyle hemoglobinin oksijen doygunluğu
  robot_ozet()              : derslerde yinelenen robot sayıları (kayıt süresi, adım, durgun pay, tutma torku, mekanik iş …)"""
import re, textwrap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from ortak import kayit, yumusat, LAB, g
from kaynaklar import deger

TURUNCU, MAVI, YESIL, MOR, GRI = "#C2410C", "#1D4ED8", "#0F766E", "#7E22CE", "#6B7280"
INSAN, ROBOT = YESIL, MAVI          # derslerde insan hep yeşil, robot hep mavi
EVRE_AD = ["kaldırma", "taşıma", "bırakma"]


def tablo(ad):
    return np.genfromtxt(LAB / f"veri/{ad}.csv", delimiter=",", names=True, dtype=None, encoding="utf-8")


def on_kol():
    """Dirsekten sonraki parçalar: (parçalar, toplam kütle kg, kütle × uzaklık kg·m, eylemsizlik kg·m²)."""
    T = tablo("sag_kol_kutle")
    dis = T[T["uzaklik_dirsek_m"] > 0]
    m, d = dis["kutle_kg"], dis["uzaklik_dirsek_m"]
    return dis, float(m.sum()), float((m * d).sum()), float((m * d ** 2).sum())


def dirsek_parametre():
    P = tablo("sag_kol_parametre")
    return P[P["ad"] == "dirsek"][0]


def egim(k):
    """Ön kolun yatayla açısı (rad). Kaba model: omuz ve dirsek aynı eksende döner, omzun yana açılması ve dönmesi ihmal edilir."""
    return k["omuz_pitch_rad"] + k["dirsek_rad"]


def tutma_torku(k):
    """Ön kolu ve eli yer çekimine karşı tutmak için dirsekte gereken tork (N·m), kaba model."""
    _, _, md, _ = on_kol()
    return g * md * np.cos(egim(k))


def geri_bildirim(kp, kd, eylemsizlik, baslangic=0.2, hedef=0.0, sure=1.5, adim=0.001, gecikme=0.0, isaret=-1):
    """Tek eklemli döngü: tork = isaret × (kp × sapma + kd × hız). isaret −1 negatif, +1 pozitif geri bildirim.
    gecikme: ölçümün denetleyiciye ulaşma süresi (s). Döndürür: zaman, açı."""
    n = int(round(sure / adim)); kayma = int(round(gecikme / adim))
    t = np.arange(n + 1) * adim
    q = np.empty(n + 1); w = np.empty(n + 1)
    q[0], w[0] = baslangic, 0.0
    for i in range(n):
        j = max(i - kayma, 0)
        tork = isaret * (kp * (q[j] - hedef) + kd * w[j])
        w[i + 1] = w[i] + tork / eylemsizlik * adim
        q[i + 1] = q[i] + w[i + 1] * adim
        if abs(q[i + 1]) > 1e3:
            q[i + 2:] = np.nan; w[i + 2:] = np.nan
            break
    return t, q


def evreler(esik=0.05):
    """Bardağın yatay hızı eşiği ilk ve son kez aştığı anlar arasında taşıma; öncesi kaldırma, sonrası bırakma."""
    k = kayit(); t = k["zaman_s"]
    p = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"], k["bardak_z_m"]]))
    v = np.gradient(p, t, axis=0)
    hiz = np.linalg.norm(v, axis=1)
    yatay = np.linalg.norm(v[:, :2], axis=1) > esik
    ilk, son = int(np.argmax(yatay)), int(len(t) - 1 - np.argmax(yatay[::-1]))
    sira = np.arange(len(t))
    evre = np.where(sira < ilk, 0, np.where(sira > son, 2, 1))
    return t, hiz, evre, ilk, son


DURGUN = 0.05     # rad/s: dirsek hızı bunun altındaysa "durgun" sayılır (tanım)


def robot_ozet():
    """Benzetim kaydından ve kol tablolarından derslerde yinelenen sayılar (hepsi hesapla; elle yazılmış sayı yok)."""
    k = kayit(); t = k["zaman_s"]; w = k["dirsek_hiz_rad_s"]
    P = dirsek_parametre(); kol = tablo("sag_kol_kutle")
    tork = tutma_torku(k)
    durgun = np.abs(w) < DURGUN
    adim = round(float(t[1] - t[0]), 3)
    return dict(sure=float(t[-1]), ornek=len(t), adim=adim, saniyede=round(1 / adim),
                kol_uzunluk=float(kol["uzaklik_omuz_pitch_m"].max()),
                durgun_pay=float(durgun.mean()), tutma_durgun=float(np.abs(tork[durgun]).mean()),
                tutma_en_buyuk=float(np.abs(tork).max()), tutma_yatay=float(g * on_kol()[2]),
                hiz_en_buyuk=float(np.abs(w).max()), hiz_siniri=float(P["hiz_rad_s"]), efor=float(P["efor_Nm"]),
                kp=float(P["kp"]), kd=float(P["kd"]), alt=float(P["alt_rad"]), ust=float(P["ust_rad"]),
                aci_kullanilan=float(np.degrees(k["dirsek_rad"].max() - k["dirsek_rad"].min())),
                mekanik_is=float(np.sum(np.abs(tork * w)) * adim),
                mekanik_guc_en_buyuk=float(np.abs(tork * w).max()))


# ---------- fizyoloji modelleri (parametreler kaynaklı: kaynaklar.py) ----------
def _oran(z, k):
    return k if abs(z) < 1e-7 else z / (1 - np.exp(-z / k))


def _hiz_fonksiyonlari(u):
    """Hodgkin–Huxley kapı hız fonksiyonları (1/ms), u mV. Kaynak: Pool ve Mato (2011), denklem A14–A19."""
    am = 0.1 * _oran(u + 40, 10); bm = 4 * np.exp(-(u + 65) / 18)
    ah = 0.07 * np.exp(-(u + 65) / 20); bh = 1 / (1 + np.exp(-(u + 35) / 10))
    an = 0.01 * _oran(u + 55, 10); bn = 0.125 * np.exp(-(u + 65) / 80)
    return am, bm, ah, bh, an, bn


def _iyon_akimi(u, m, h, n):
    return (deger("hh_gNa") * m ** 3 * h * (u - deger("hh_ENa_mV")) + deger("hh_gK") * n ** 4 * (u - deger("hh_EK_mV"))
            + deger("hh_gL") * (u - deger("hh_EL_mV")))


def zar_dinlenim():
    """Modelin dinlenim potansiyeli (mV): akımların toplamı sıfır olana kadar gevşetilir."""
    u = -65.0
    for _ in range(200000):
        am, bm, ah, bh, an, bn = _hiz_fonksiyonlari(u)
        du = -_iyon_akimi(u, am / (am + bm), ah / (ah + bh), an / (an + bn))
        u += 0.01 * du
        if abs(du) < 1e-10:
            break
    return u


def zar_modeli(akim, sure=40.0, adim=0.01):
    """Hodgkin–Huxley zar modeli. akim(t): uyarı akımı (µA/cm²), t ms. Döndürür: zaman (ms), zar potansiyeli (mV)."""
    u = zar_dinlenim(); C = deger("hh_C")
    am, bm, ah, bh, an, bn = _hiz_fonksiyonlari(u)
    m, h, n = am / (am + bm), ah / (ah + bh), an / (an + bn)
    N = int(round(sure / adim)); t = np.arange(N + 1) * adim
    U = np.empty(N + 1); U[0] = u
    for i in range(N):
        am, bm, ah, bh, an, bn = _hiz_fonksiyonlari(u)
        du = (akim(t[i]) - _iyon_akimi(u, m, h, n)) / C
        m += adim * (am * (1 - m) - bm * m); h += adim * (ah * (1 - h) - bh * h); n += adim * (an * (1 - n) - bn * n)
        u += adim * du; U[i + 1] = u
    return t, U


def vuru(genlik, bas=5.0, uzunluk=1.0):
    """Tek dikdörtgen uyarı vurusu: bas ms'de başlar, uzunluk ms sürer."""
    return lambda t: genlik if bas <= t < bas + uzunluk else 0.0


def sayim(U):
    """Zar potansiyelinin sıfırı aşağıdan yukarı kaç kez geçtiği = aksiyon potansiyeli sayısı."""
    return int(np.sum((U[1:] > 0) & (U[:-1] <= 0)))


def hill_sabitleri():
    """Hill (1938) özgün uyumundan en büyük kuvvet, en büyük hız ve eğrilik (a / en büyük kuvvet)."""
    a, b, c = deger("hill_a"), deger("hill_b"), deger("hill_c")
    F0 = c / b - a; V0 = c / a - b
    return a, b, c, F0, V0, a / F0


def hill_hiz(F):
    """Verilen kuvvette kısalma hızı (özgün uyumun birimleriyle)."""
    a, b, c = deger("hill_a"), deger("hill_b"), deger("hill_c")
    return c / (np.asarray(F, float) + a) - b


def doygunluk(P):
    """Hemoglobinin oksijen doygunluğu (0–1), P mmHg. Severinghaus (1979), denklem 1."""
    P = np.asarray(P, float)
    with np.errstate(divide="ignore"):
        return 1 / (23400 / (P ** 3 + 150 * P) + 1)


# ---------- çizim ----------
def kutu(ax, x, y, w, h, metin, renk, boy=24, yazi="#ffffff"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", fc=renk, ec="none"))
    ax.text(x + w / 2, y + h / 2, metin, ha="center", va="center", color=yazi, fontsize=boy, linespacing=1.4)


def ok(ax, x1, y1, x2, y2, renk="#111111"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=renk, lw=3, mutation_scale=28))


def bos_eksen(baslik):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_title(baslik)
    return fig, ax


def tr(x, basamak=2):
    return f"{x:.{basamak}f}".replace(".", ",").replace("-", "−")


def sayi(x):
    """Gereksiz sıfır basmadan Türkçe ondalık: 100, 0,1, 2,5."""
    return f"{x:g}".replace(".", ",").replace("-", "−")


def sar(s, en):
    """Satıra böler; sayı ile birimi ('−70 mV', '20 ms') ayırmaz."""
    if not s:
        return ""
    s = re.sub(r"(\d) (?=(mV|ms|ns|s|m|cm|mm|µm|nm|N·m|W|J|kJ|L|mL|mmHg|°C|m/s|rad/s|Hz|kat|g)\b)", "\\1\u00a0", s)
    return "\n".join(textwrap.wrap(s, en))


def cizelge(baslik, satirlar, fark, basliklar=("", "İnsan", "İnsansı robot"), kaynak=""):
    """Karşılaştırma çizelgesi. satirlar: (özellik, insan, robot) · fark: alttaki 'aynısı değil' cümlesi."""
    fig, ax = bos_eksen(baslik)
    x0, w = [0.01, 0.25, 0.63], [0.22, 0.36, 0.36]
    for j, b in enumerate(basliklar):
        if b:
            kutu(ax, x0[j] + 0.03, 0.885, w[j] - 0.07, 0.055, b, [None, INSAN, ROBOT][j], boy=27)
    n = len(satirlar); ust, alt = 0.84, 0.17
    h = (ust - alt) / n
    for i, (oz, ins, rob) in enumerate(satirlar):
        y = ust - (i + 0.5) * h
        if i % 2 == 0:
            ax.add_patch(FancyBboxPatch((0.0, y - h / 2 + 0.006), 1.0, h - 0.012, boxstyle="round,pad=0.0,rounding_size=0.015", fc="#F3F4F6", ec="none"))
        ax.text(x0[0] + 0.01, y, sar(oz, 14), fontsize=25, weight="bold", va="center", ha="left", linespacing=1.25)
        ax.text(x0[1] + 0.01, y, sar(ins, 27), fontsize=25, va="center", ha="left", color="#111111", linespacing=1.25)
        ax.text(x0[2] + 0.01, y, sar(rob, 27), fontsize=25, va="center", ha="left", color="#111111", linespacing=1.25)
    ax.add_patch(FancyBboxPatch((0.0, 0.02), 1.0, 0.115, boxstyle="round,pad=0.0,rounding_size=0.02", fc="#FFF7ED", ec=TURUNCU, lw=3))
    uzun = len(fark) > 160
    ax.text(0.02, 0.0775, sar("Fark: " + fark, 112 if uzun else 84), fontsize=20 if uzun else 23, va="center", ha="left", color="#111111",
            linespacing=1.25 if uzun else 1.3)
    if kaynak:
        ax.text(0.99, -0.012, kaynak, fontsize=15, va="top", ha="right", color=GRI)
    return fig, ax
