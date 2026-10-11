#!/usr/bin/env python3
"""Ders görevlerinin yanıtını denetler (her dersin kazanımının kanıtı).
  python gorev_denetle.py                 görev listesini gösterir
  python gorev_denetle.py 1.1 -79,2       Ders 1.1 görevinin yanıtını denetler (virgül ya da nokta kullanılabilir)
  python gorev_denetle.py 4.4 sekretin    yazıyla yanıtlanan görev
Beklenen yanıtlar hafta1–4.py çalışınca GOREVLER.json'a yazılır; betikleri çalıştırmadıysanız beklenen/GOREVLER.json kullanılır."""
import json, pathlib, sys

K = pathlib.Path(__file__).resolve().parent
dosya = K / "GOREVLER.json" if (K / "GOREVLER.json").exists() else K / "beklenen" / "GOREVLER.json"
G = json.loads(dosya.read_text(encoding="utf-8"))


def liste():
    for ders in sorted(G, key=lambda k: tuple(map(int, k.split(".")))):
        print(f"Ders {ders}  {G[ders]['soru']}")
    print("\nYanıtınızı denetlemek için:  python gorev_denetle.py <ders> <yanıt>")


def denetle(ders, yanit):
    if ders not in G:
        print("Böyle bir ders yok:", ders); return 2
    g = G[ders]
    if isinstance(g["cevap"], str):
        dogru = yanit.strip().lower() == g["cevap"].lower()
    else:
        try:
            sayi = float(yanit.replace("−", "-").replace(",", "."))
        except ValueError:
            print("Sayı bekleniyordu, örnek: 12,5"); return 2
        dogru = abs(sayi - g["cevap"]) <= g["tolerans"]
    if dogru:
        print(f"DOĞRU · Ders {ders} · beklenen {str(g['cevap']).replace('.', ',')} {g['birim']}".rstrip())
        return 0
    print(f"HENÜZ DEĞİL · Ders {ders} · ipucu: {g['ipucu']}")
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        liste(); sys.exit(0)
    sys.exit(denetle(sys.argv[1], sys.argv[2]))
