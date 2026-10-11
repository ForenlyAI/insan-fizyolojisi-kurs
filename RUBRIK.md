# Bitirme işi ve ölçüt çizelgesi

**Bitirme işi: dört sistem karşılaştırma dosyası.** Sinir, kas, solunum ve sindirim için birer bölüm yazın (toplam en çok altı sayfa). Her bölümde:

1. O sistemin derslerinden birinin **hesabını kendi seçtiğiniz değerlerle** yeniden yapın (değerleri, birimleri ve adımları yazın).
2. En az dört satırlı bir **benzerlik ve fark çizelgesi** kurun: özellik, insan, insansı robot.
3. Robot sütununa **benzetim kaydından ya da kol tablosundan bir sayı** koyun (`beklenen/OLCUMLER.json` ya da ders şekilleri).
4. "Robot neden canlı sistemin aynısı değildir" sorusunu **en az iki farkla** yanıtlayın.

Sonuna kaynakça ekleyin. Teslim: tek PDF ya da ZIP. Her hafta sonunda doldurduğunuz çizelgeler (`CIZELGE.md`) bu dosyanın taslağıdır.

Her ölçütü teslimden önce kendiniz denetleyebilirsiniz; "nasıl denetlenir" sütunu ne yapacağınızı söyler.

| Ölçüt | Yeterli | Eksik | Nasıl denetlenir |
|---|---|---|---|
| Hesabın doğruluğu | Dört sistemin her birinde bir hesap var; formül, girilen değerler ve birimler yazılı; sonuç doğru | Bir sistemde hesap yok, birim yazılmamış ya da sonuç yanlış | Aynı formülü dersin görev değerleriyle çalıştırıp `python gorev_denetle.py <ders> <yanıt>` ile "DOĞRU" alın; sonra kendi değerlerinizle yineleyin |
| Kendi değerleri | Hesaplarda derste ve görevde kullanılmayan değerler seçilmiş ve neden seçildiği bir cümleyle yazılmış | Dersin çözülmüş örneği ya da görevin sayıları aynen kopyalanmış | Değerlerinizi `beklenen/GOREVLER.json` ve ders ekranlarındaki sayılarla karşılaştırın; aynıysa değiştirin |
| Kavramın doğru kullanımı | Her bölümde en az üç fizyoloji terimi yerinde kullanılmış (ör. denge potansiyeli, uç plak potansiyeli, alveoler ventilasyon, segmentasyon) ve basamaklar doğru sırada | Terim yanlış anlamda kullanılmış ya da sıra karışık | Terimi ve sırayı o haftanın "Uygulama ve Quiz" sayfasındaki kavram kartlarıyla karşılaştırın |
| Benzerlik ve fark | Her çizelgede en az dört satır, robot sütununda kayıttan ya da tablodan bir sayı ve en az iki açık fark var | Yalnız benzerlik yazılmış, robot sayısı yok ya da "aynısıdır" denmiş | Robot sayınızı `beklenen/OLCUMLER.json` içinde bulun; çizelgenizde "fark" sözcüğü geçen en az iki cümle sayın |
| Kaynak ve etiket | Kullanılan her fizyoloji sayısının kaynağı (kitap ve bölüm ya da yayın) yazılı; kaynağı olmayan sayı ÖRNEK diye işaretli; robot verisi "benzetim kaydı" diye anılmış | Kaynaksız sayı var ya da robot verisi gerçek ölçüm gibi sunulmuş | Her sayının yanına kaynak numarası koyup kaynakçayla eşleyin; `python kaynaklar.py` çıktısındaki künyeleri kullanabilirsiniz |
| Sınır ve dürüstlük | Dosyada tıbbi tavsiye, tanı ya da kişisel değer yorumu yok; model ve örnek olan yerler belirtilmiş; yapay zekâ aracı kullanıldıysa nerede kullanıldığı ve çıktının nasıl doğrulandığı yazılı | Kişiye özel sağlık ya da beslenme önerisi var; model hesabı ölçüm gibi sunulmuş; yapay zekâ kullanımı belirtilmemiş | Son sayfaya üç satırlık bir beyan yazın: model ve örnek olan yerler, kullanılan araçlar, doğrulama yolu |

**Geçme koşulu:** altı ölçütün en az beşi "yeterli"; "Hesabın doğruluğu" ölçütü mutlaka "yeterli" olmalı.

Not: bu kurs sınav hazırlığı ve kavram öğretimi içindir. Bitirme işi bir klinik değerlendirme ya da beslenme planı değildir.
