# MOTRAN Reels: Nasıl Yapıldı? (20.10.2026)

> **"Kamyon geldi. 24 motosiklet."** Bu cümle videonun ilk karesinde, sesten önce ekranda.
> Bu belge 20 Ekim'de yapılan 7 Reels'in tarifidir: fikir, kanca, Flow görüntüsü, ses, animasyon ve birleştirme. Aynı yolla yeni Reels yapılabilir.

---

## 1. Kısaca boru hattı

```
Konu seç (daha önce paylaşılmamış)
   → Kanca (ilk 2 sn) + 15–20 sn'lik metin
   → Ses: ElevenLabs, EDA ATLAS (eleven_v4)
   → Açılış görüntüsü: Google Flow (Veo 3.1 Lite, 9:16, 8 sn, x1)
   → İndir (yan paneldeki tarayıcı → İndirilenler → buluta)
   → Sessizliklerden cümle zamanlarını bul
   → HTML sahneleri (kare kare animasyon) → playwright ile şeffaf PNG
   → ffmpeg: Flow klibi (alt) + PNG'ler (üst) + ses + müzik/efekt
   → Kontrol (kare özeti, ses seviyesi) → teslim
```

Bir Reels'in süresi yaklaşık 15–20 dk (render 2–3 dk; çoğu süre indirme ve kontrolde geçiyor).

---

## 2. Kanca: ilk 2 saniye her şey

Kural: **kanca 0. karede ekranda.** Sessiz izleyen kişi önce yazıyı okur. Selam yok, logo girişi yok, "bu videoda" yok.

Kullanılan kanca kalıpları (`instagram-agent-skill` → `ig-reel/hooks.json`):

| Reels | Kanca (ekranda, 0. sn) | Kalıp | Neden tutuyor |
| --- | --- | --- | --- |
| Kamyon Geldi | **Kamyon geldi. 24 motosiklet.** | Cold Open (olayın ortasından başla) | Her bayinin yaşadığı an + net sayı |
| Gece Mesajı | **Gece 23:30.** + "Son fiyat ne abi?" | Verbatim Question (müşterinin birebir sözü) | Bayi bu mesajı her gün görüyor |
| 7 Aydır Bekleyen | **Bu motosiklet 7 aydır satılmıyor.** + "STOKTA 214 GÜN" damgası | Cost Confession (kaybı söyle) | Acı veren gerçek, rakam |
| Müşteri Kapıda | **Müşteri kapıda. Teslime hazır.** | Cold Open + gerilim | "Ama önce…" ile bekleyiş başlıyor |
| Servis Bakım | **"En son ne zaman bakım yaptırmıştım?"** | Verbatim Question | Servisin en sık sorusu |
| Zam Geldi | **Zam geldi. 40 ilan fiyatı değişecek.** | The Deadline (değişim + iş yükü) | Sayaç 0'dan 40'a koşuyor |
| Personel Soruyor | **Yeni personel her şeyi size mi soruyor?** | The Callout (hedef kitleye seslen) | Patronun derdi, "abi" balonları |

Metin şablonu (her videoda aynı iskelet):

```
0–2 sn   KANCA     olay / soru / rakam (ekranda büyük, ilk karede)
2–7 sn   DERT      "Tek tek mi?", "Cevap yoksa başka bayiye yazar."
7–15 sn  ÇÖZÜM     MOTRAN ne yapar: tek cümle, ekranda o ekranın sade hali
15–17 sn VURUŞ     "Gerek yok." / "İlk cevap sizden." / "Müşteriyi bekletmeyin."
son 2 sn ÇAĞRI     "DM'den MOTRAN yazın" (tek çağrı)
```

Değişmeyen kurallar:
- **Programın yapmadığı şey söylenmez.** Örnek: Zam videosunda seste geçen "beş dakikada bitsin" cümlesi kesildi; 40 ilanın kaç dakikada güncelleneceğini bilmiyoruz.
- Sahibinden'de: giriş/doğrulama kullanıcıda; ödeme yapılmaz, doping seçilmez. GİB'de **ONAYLA'ya kullanıcı basar** (videoda yazıyor).
- Yalnız örnek veri: "Distribütör A/B", "125cc Scooter", FTR… fatura no, "Ahmet Y."; her karede **"Görseldeki veriler örnektir."**
- "motor" değil **"motosiklet"** (yalnız "motor numarası" kalır), "dükkân" değil **"mağaza"**.
- Yapay zekâ etiketi konmaz (Instagram kendisi koyarsa sorun değil).
- Sahibinden logosu yok. Bildirim simgesi de "S" harfi değil, genel konuşma balonu.

---

## 3. Ses: ElevenLabs

- Ses **EDA ATLAS** (`voice_id mBUB5zYuPwfVE6DTcEjf`), model **eleven_v4**, her metin için **1 üretim**.
- Etiketler: başta ve sonda `[excited]`, ortada `[playful]`.
- Okunuş: "Ö-Te-Ve", sayılar yazıyla ("yirmi dört", "on bir buçuk").
- 15–20 sn hedef: yaklaşık 40–45 kelime.

İndirme sorunu: Bulut makinesi `storage.googleapis.com`'a erişemiyor. Çözüm, yan paneldeki tarayıcıda o adresi açıp sayfanın içinden `fetch → blob → a.download` yapmak. Dosya İndirilenler'e düşüyor, buluta oradan alınıyor.

**Püf noktası:** Her indirme ayrı onay istiyor. Birkaç dosyayı **tek .bin içinde art arda** indirip (boyutlarını not ederek) bulutta byte'larından bölmek tek onaya indiriyor:

```js
const bl=[]; for(const u of URLS){ bl.push(await (await fetch(u)).blob()); }
const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob(bl));
a.download='motran_sesler_567.bin'; a.click(); bl.map(x=>x.size)   // boyutlar → bölme
```

---

## 4. Görüntü: Google Flow

- Ayar: **Video · Veo 3.1 Lite · 720p · 8 sn · 9:16 · x1** (x2 değil; video başı 10 kredi, günde 50 kredi).
- Her komutun sonu: **"photorealistic, vertical 9:16. No logos, no text, no signs, no people."**
- Komutta kamera hareketi şart: *slow push-in / dolly / orbit*. Görüntü durağan kalmasın.

Kullanılan komutlar (kısaltılmış):

| Reels | Flow komutu |
| --- | --- |
| Kamyon | Sunrise, delivery truck rear doors open, **uncrated** new motorcycles strapped inside, ramp, two already on concrete, slow dolly push-in. *No boxes, no crates…* |
| Gece Mesajı | Night, smartphone on dark wooden table next to motorcycle keys, screen lights up with notification, city bokeh, slow push-in |
| 7 Aydır | Single dusty motorcycle in dim showroom corner, **blank** paper price tag, sunbeam with dust particles, slow push-in |
| Müşteri Kapıda | Bright showroom, glossy red motorcycle, big red gift bow, keys on seat, slow orbit + push-in |
| Servis | Workshop, motorcycle on hydraulic lift, red tool cart, open logbook, slow push-in |
| Zam | Long row of new motorcycles, **blank** price tags swaying, dolly along the row |
| Personel | Sales counter, glowing monitor, helmet + keys, showroom blurred behind, slow push-in |

Dersler:
- İlk kamyon komutu kasalı geldi. Hasan: **"motorlar açık geliyor"** → *uncrated* + *No boxes, no crates* ile yeniden üretildi.
- "Dark bedroom" komutu reddedildi (Başarısız, kredi iade). "Night scene… wooden table" ile geçti.
- Fiyat etiketinde yazı çıkmasın diye **"blank paper price tag"** dendi.
- Veo bazen 8 sn içinde sahne değiştiriyor (Zam'da 4. sn'de monitöre geçti). Bulanıklık tam o anda başladığı için kesik göze batmadı.
- Video adresi `flow-content.google/...`; yine tarayıcı içinden `fetch` ile indiriliyor (videoyu açınca `document.querySelector('video').currentSrc`).

---

## 5. Zamanlama: ses neyse video o

Cümle başlangıçları sessizliklerden bulunuyor:

```bash
ffmpeg -i ses/r1.mp3 -af silencedetect=n=-32dB:d=0.09 -f null - 2>&1 | grep silence_
```

Örnek (Kamyon): "Kamyon geldi." 0.09–1.04 · "Yirmi dört motosiklet." 1.30–2.59 · "Gerek yok." 8.48–9.13 · "DM'den MOTRAN yazın." 17.30–18.91. Her sahnenin başı bu sürelere göre yazıldı. Ses videonun 0.12. sn'sinde başlıyor (`OFF = 120 ms`).

Ses içinden cümle kesme (Zam):

```bash
ffmpeg -i r5.mp3 -filter_complex "[0:a]atrim=0:12.70,asetpts=PTS-STARTPTS[a];[0:a]atrim=15.10,asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1" r5c.mp3
```

---

## 6. Animasyon: HTML sahneler (`kit.py` + `sahneler.py`)

- 1080×1920, 30 fps. Her öğe tek satır: `A(html, başla, bitir, efekt)`.
  Efektler: `up`, `left`, `right`, `pop`, `stamp` (büyükten oturan damga), `blur` (bulanıktan netleşen), `fade`; `shake=1` titreme.
- Hazır parçalar: `SAYAC` (0→24, 0→68.400 ₺), yazı makinesi (`yaz=`), imleç + tık halkası, `CTA` (Siz de deneyin + DM düğmesi), `ALTYAZI` (sessiz izleyen için alt yazı), `QR_SVG`, motosiklet simgesi.
- Zemin mantığı: Flow süresince HTML **şeffaf** (altta video görünüyor). Kancadan sonra video **bulanıklaşıp kararıyor** (`golge` + ffmpeg `boxblur`), Flow bitince koyu MOTRAN zemini (turuncu ışık) geliyor.
- Güvenli alan: yazılar x 64–850, y 230–1440 arası (Instagram'ın düğmeleri ve açıklaması altta/sağda).
- Okunurluk: üstte koyu degrade (`#ust`) + yazılara gölge.

Önizleme, render öncesi kontrol:

```bash
python3 onizle.py r1 0,1500,2000,9000,13600,15500   # seçilen anlar, Flow karesi altta
```

---

## 7. Birleştirme (`yap.py`)

```bash
python3 yap.py r1            # kare + ses + video
python3 yap.py r1 video      # yalnız yeniden kodla
```

1. **Kareler:** playwright her karede `window.__git(ms)` çağırıp şeffaf PNG alıyor (~600 kare, 2–3 dk).
2. **Müzik + efekt (numpy, tamamen sentez):** 104 BPM, Am–F–C–G; kick, hat, bas, pad. Ses varken müzik %55 kısılıyor (yan zincir). Sahne geçişlerinde "vuuş", vuruş anlarında (Gerek yok., İlk cevap sizden.) alçak darbe, tıklamada "tik".
3. **Taban video:** Flow klibi 1080×1920'ye büyütülüyor, bulanıklık penceresi ekleniyor, `tpad` ile video süresine uzatılıyor. **Ayrı dosyaya** yazılıyor.
4. **Son:** taban + PNG'ler (overlay) + ses + Flow'un kendi ortam sesi (%30, Flow bitince sönüyor) + müzik → `-t <süre>`, crf 19, AAC 192k.

**Yaşanan hata ve çözüm:** `tpad` ile `overlay` aynı filtre zincirinde olunca video 8,5 sn'de kesildi. Önce taban videoyu ayrı üretmek ve `trim` yerine `-t` kullanmak çözdü.

Kontrol: `ffprobe` (video ve ses süresi eşit mi), `volumedetect` (ortalama ≈ −16,5 dB, tepe ≈ −0,7 dB), 1,5 sn aralıklı kare özeti.

---

## 8. Teslim ve yedek

- Sohbete gönderildi ve mağaza PC'sinde `İndirilenler\MOTRAN_Reels_*.mp4` olarak duruyor.
- Yedek: GitHub `motran-medya` deposu → `reels_2010/` (7 mp4) + `reels_2010/kaynak/` (`kit.py`, `sahneler.py`, `yap.py`, `onizle.py`).
- Paylaşım **elle** (Metricool değil). Açıklama: tek çağrı ("DM'den MOTRAN yazın"), link yok, 5 hashtag (ASCII: `#motosikletbayisi #bayiprogrami … #motran`).

---

## 9. Yeni Reels için kontrol listesi

- [ ] Konu daha önce paylaşılmadı mı? (`motran-medya`: hafta2, hafta3, biliyor, flow, reels_2010)
- [ ] Kanca 0. karede ekranda mı, 6–8 kelimeden kısa mı?
- [ ] Metindeki her cümleyi program gerçekten yapıyor mu? Süre/sayı vaadi yok mu?
- [ ] Flow komutunda "No logos, no text, no signs, no people" var mı?
- [ ] Görüntüde yazı/logo/marka çıktıysa bulanık bölgede mi kalıyor?
- [ ] Her karede "Görseldeki veriler örnektir."
- [ ] Ses 15–20 sn, video sesten ~1 sn uzun, ortalama ≈ −16 dB
- [ ] Yapay zekâ etiketi yok, "motosiklet" ve "mağaza" kelimeleri doğru

Bugünkü 7 Reels: Kamyon Geldi · Gece Mesajı · 7 Aydır Bekleyen · Müşteri Kapıda · Servis Bakım · Zam Geldi · Personel Soruyor.
