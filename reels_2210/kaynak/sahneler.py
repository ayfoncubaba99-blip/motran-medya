# -*- coding: utf-8 -*-
"""22.10.2026 Reels: MOTRAN demosu yayında. reels_2010/kaynak/sahneler.py kalıbı (A, SAYAC, ALTYAZI, imleç).
Zamanlar ms; ses OFF ms gecikmeyle başlar. Ses: EDA ATLAS (eleven_v4), 18,3 sn.
Cümleler (ses içinde): 0.00 "Programı bir deneyebilir miyim?" · 1.95 "Bu soruyu çok duyduk." · 3.53 "Artık cevabı evet:"
· 5.28 "MOTRAN demosu yayında." · 6.98 "Kurulum yok," · 7.85 "kart bilgisi yok." · 9.13 "Araç ekleyin, satın;"
· 10.8 "stok, kontrol paneli, kâr zarar anında değişsin." · 14.20 "Yedi gün ücretsiz." · 15.68 "DM'den DEMO yazın, linki gönderelim."
"""
from kit import sayfa

OFF = 120


def A(ic, t0, t1=None, fx='up', st='', d=None, cls='', **kw):
    at = f' data-t0="{t0 + OFF}"'
    if t1 is not None:
        at += f' data-t1="{t1 + OFF}"'
    if d:
        at += f' data-d="{d}"'
    at += f' data-fx="{fx}"'
    for k, v in kw.items():
        if k in ('ct0', 'ct1', 'ys') and isinstance(v, (int, float)):
            v = v + OFF
        at += f' data-{k}="{v}"'
    return f'<div class="a {cls}"{at} style="{st}">{ic}</div>'


def SAYAC(t0, t1, c0, c1, ct0, ct1, st, pre='', suf='', tr=1, fx='pop', cls='t'):
    return A('<span class="n"></span>', t0, t1, fx=fx, st=st, cls=cls, c0=c0, c1=c1, ct0=ct0, ct1=ct1, pre=pre, suf=suf, tr=tr)


def ALTYAZI(cumleler):
    return ''.join(A(f'<div>{m}</div>', a, b, 'fade', 'left:64px;right:230px;top:1250px', d=160, cls='alt-yazi') for a, b, m in cumleler)


def imlec(i, ta, tb, x0, y0, x1, y1, tc):
    return {'id': f'im{i}', 'v': [ta + OFF, tb + OFF, x0, y0, x1, y1, tc + OFF]}


BALON = ('<div class="kart" style="width:{w}px;padding:24px 30px;display:flex;gap:22px;align-items:center;background:rgba(30,28,26,.94)">'
         '<div style="width:70px;height:70px;border-radius:50%;background:#FF8A00;display:flex;align-items:center;justify-content:center;flex:0 0 70px">'
         '<svg viewBox="0 0 24 24" width="38" height="38"><path d="M4 5h16v11H9l-5 4z" fill="#111"/></svg></div>'
         '<div><div class="gri" style="font-size:24px">DM · {saat}</div><div style="font-size:38px;font-weight:800;margin-top:6px">{m}</div></div></div>')

CHECK = ('<div style="width:64px;height:64px;border-radius:50%;background:rgba(61,220,132,.16);border:3px solid #3DDC84;display:flex;'
         'align-items:center;justify-content:center;font-size:32px;font-weight:900;color:#3DDC84;flex:0 0 64px">✓</div>')


def demo():
    S = 19600
    FE = 7800 + OFF
    g = ''
    # KANCA (kare 0'da ekranda): müşterinin birebir sorusu
    g += A('<div class="t o" style="font-size:200px;line-height:.6;height:90px">“</div>', -2000, 1850, 'fade', 'left:58px;top:250px')
    g += A('<div class="t" style="font-size:112px">Programı bir</div><div class="t o" style="font-size:132px">deneyebilir</div>'
           '<div class="t" style="font-size:112px">miyim?”</div>', -2000, 1850, 'fade', 'left:64px;top:345px')
    g += A('<div class="cip">Bayilerin en sık sorusu</div>', 700, 1850, 'up', 'left:64px;top:760px')
    # BU SORUYU ÇOK DUYDUK: DM balonları
    g += A('<div class="t" style="font-size:84px">Bu soruyu</div><div class="t o" style="font-size:84px">çok duyduk.</div>', 1950, 3400, 'blur', 'left:64px;top:280px')
    for i, (saat, m, t) in enumerate([('09:12', 'Abi deneyebilir miyim?', 2150), ('13:40', 'Önce bi görsem olur mu?', 2500),
                                      ('21:05', 'Deneme sürümü var mı?', 2850)]):
        g += A(BALON.format(w=760, saat=saat, m=m), t, 3400, 'pop', f'left:{64 + (i % 2) * 50}px;top:{520 + i * 170}px', d=420)
    # CEVAP: EVET + DEMO YAYINDA
    g += A('<div class="t" style="font-size:76px">Artık cevabı:</div>', 3530, 6850, 'blur', 'left:64px;top:270px')
    g += A('<div style="border:10px solid #FF8A00;color:#FF8A00;border-radius:26px;padding:6px 40px 14px;font-size:170px;font-weight:900;letter-spacing:-4px">EVET.</div>',
           4350, 6850, 'stamp', 'left:90px;top:390px', d=380, shake=1, base=' rotate(-4deg)')
    g += A('<div class="t" style="font-size:84px">MOTRAN demosu</div><div class="t o" style="font-size:84px">yayında.</div>', 5280, 6850, 'up', 'left:64px;top:700px')
    tar = ('<div class="kart" style="width:810px;overflow:hidden">'
           '<div style="display:flex;align-items:center;gap:12px;padding:20px 26px;background:#1d1a17">'
           '<i style="width:16px;height:16px;border-radius:50%;background:#3a3530;display:inline-block"></i>'
           '<i style="width:16px;height:16px;border-radius:50%;background:#3a3530;display:inline-block"></i>'
           '<i style="width:16px;height:16px;border-radius:50%;background:#3a3530;display:inline-block"></i>'
           '<div style="flex:1;margin-left:12px;background:#0e0c0b;border-radius:14px;padding:10px 20px;font-size:26px" class="gri">motranyazilim.com · demo</div>'
           '<div class="y" style="font-size:24px;font-weight:800;letter-spacing:2px">● CANLI</div></div>'
           '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:24px">'
           + ''.join(f'<div style="background:#1b1815;border-radius:18px;padding:16px 20px"><div class="gri" style="font-size:20px;letter-spacing:2px;font-weight:800">{k}</div>'
                     f'<div style="font-size:44px;font-weight:900;margin-top:4px">{v}</div></div>' for k, v in (('STOK', '100'), ('BU AY', '18'), ('BUGÜN', '0')))
           + '</div></div>')
    g += A(tar, 5800, 6850, 'up', 'left:64px;top:930px', d=480)
    # KURULUM YOK / KART YOK
    g += A('<div class="t" style="font-size:120px">Kurulum</div><div class="t o" style="font-size:120px">yok.</div>', 6980, 8950, 'blur', 'left:64px;top:300px')
    g += A('<div class="t" style="font-size:120px">Kart bilgisi</div><div class="t o" style="font-size:120px">yok.</div>', 7850, 8950, 'blur', 'left:64px;top:600px')
    g += A('<div class="cip">Tarayıcıda açılır, hemen başlarsınız.</div>', 8250, 8950, 'up', 'left:64px;top:900px')
    # ARAÇ SATIN, HER ŞEY DEĞİŞSİN
    g += A('<div class="t" style="font-size:80px">Araç ekleyin,</div><div class="t o" style="font-size:80px">satın.</div>', 9130, 14050, 'blur', 'left:64px;top:270px')
    g += A('<div class="kart" style="width:810px;height:640px"></div>', 9300, 14050, 'fade', 'left:64px;top:480px')
    g += A('<div class="gri" style="font-size:24px;letter-spacing:3px;font-weight:800">DEMO MAĞAZA · STOK</div>', 9300, 14050, 'fade', 'left:100px;top:510px')
    g += SAYAC(9450, 14050, 100, 99, 10250, 10550, 'left:96px;top:555px;font-size:190px;line-height:1', suf='', fx='up')
    g += A('<div class="gri" style="font-size:40px;font-weight:800">araç</div>', 9450, 14050, 'up', 'left:420px;top:680px')
    g += A('<div style="border:6px solid #3DDC84;color:#3DDC84;border-radius:16px;padding:6px 22px;font-size:50px;font-weight:900;letter-spacing:2px">SATILDI</div>',
           10300, 14050, 'stamp', 'left:560px;top:600px', d=340, shake=1, base=' rotate(-8deg)')
    for i, (ad, ac, t) in enumerate([('Stok', '100 → 99', 10800), ('Kontrol paneli', 'güncellendi', 11360), ('Kâr / zarar', 'yeniden hesaplandı', 12400)]):
        g += A(f'<div class="sat" style="width:770px"><div style="display:flex;align-items:center;gap:20px">{CHECK}<span style="font-weight:700">{ad}</span></div>'
               f'<span class="y" style="font-weight:800">{ac}</span></div>', t, 14050, 'left', f'left:84px;top:{800 + i * 100}px', d=360)
    # 7 GÜN ÜCRETSİZ
    g += A('<div class="t o" style="font-size:300px;line-height:.9">7 gün</div><div class="t" style="font-size:150px;margin-top:30px">ücretsiz.</div>',
           14200, 15550, 'pop', 'left:64px;top:430px', d=520, shake=1)
    # ÇAĞRI: DM'den DEMO
    g += A('<div class="t" style="font-size:96px">DM\'den <span class="o">DEMO</span></div><div class="t" style="font-size:96px">yazın.</div>', 15680, None, 'blur', 'left:64px;top:520px')
    g += A('<div class="dug" style="font-size:56px;padding:34px 56px">✉  DEMO</div>', 16030, None, 'pop', 'left:64px;top:780px', d=600, shake=1)
    g += A('<div style="font-size:34px" class="gri">Linki gönderelim · @motranyazilim</div>', 16380, None, 'up', 'left:70px;top:930px')
    alt = ALTYAZI([(1950, 3400, 'Bayilerden her gün aynı soru geliyor.'),
                   (9130, 14050, 'Stok, kontrol paneli, kâr / zarar anında değişir.')])
    im = [imlec(1, 9600, 10900, 900, 1450, 640, 650, 10200)]
    golge = [[1950 + OFF, FE, 0.62]]
    return dict(ad='demo_yayinda', sure=S, fe=FE, blur=(1.95 + OFF / 1000, FE / 1000), html=sayfa(g + alt, S, FE, golge, im),
                flow='flow/demo.mp4', ses='ses/demo.mp3',
                vurgu=[0, 1950, 3530, 5280, 6980, 7850, 9130, 10800, 14200, 15680], vurus=[4350, 14200], tiklar=[10200])


REELS = {'demo': demo}
