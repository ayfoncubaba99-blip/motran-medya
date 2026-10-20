# -*- coding: utf-8 -*-
"""3 Reels'in sahneleri. Zamanlar ms; ses OFF ms gecikmeyle başlar."""
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


def CTA(t0, sure):
    return (A('<div class="t" style="font-size:96px">Siz de <span class="o">deneyin.</span></div>', t0, None, 'blur', 'left:64px;top:560px')
            + A('<div class="dug" style="font-size:52px;padding:34px 48px">DM\'den MOTRAN yazın</div>', t0 + 350, None, 'pop', 'left:64px;top:760px', d=600, shake=1)
            + A('<div style="font-size:34px" class="gri">Ücretsiz tanıtım · @motranyazilim</div>', t0 + 700, None, 'up', 'left:70px;top:905px'))


def ALTYAZI(cumleler):
    return ''.join(A(f'<div>{m}</div>', a, b, 'fade', 'left:64px;right:230px;top:1250px', d=160, cls='alt-yazi') for a, b, m in cumleler)


def imlec(i, ta, tb, x0, y0, x1, y1, tc):
    return {'id': f'im{i}', 'v': [ta + OFF, tb + OFF, x0, y0, x1, y1, tc + OFF]}


# ---------------------------------------------------------------- R1 KAMYON
def r1():
    S = 20300
    FE = 8350 + OFF
    g = ''
    # HOOK (kare 0'da görünür)
    g += A('<div class="t" style="font-size:118px">Kamyon geldi.</div>', -2000, 2700, 'fade', 'left:64px;top:250px')
    g += A('<div class="t o" style="font-size:300px;line-height:.9">24</div><div class="t" style="font-size:110px">motosiklet.</div>', 1250, 2700, 'pop', 'left:64px;top:400px', d=520, shake=1)
    # her biri için
    g += A('<div class="t" style="font-size:76px">Her birinde:</div>', 2880, 5750, 'blur', 'left:64px;top:300px')
    alanlar = [('ŞASE NO', 'LBB•••••••01404', 2900), ('MOTOR NO', 'JN1P•••••60111', 3650), ('RENK', 'Siyah', 4500)]
    for i, (ad, deg, t) in enumerate(alanlar):
        g += A(f'<div class="kart" style="width:790px;padding:30px 36px;display:flex;justify-content:space-between;align-items:center">'
               f'<span style="font-size:34px;font-weight:800;letter-spacing:2px" class="o">{ad}</span>'
               f'<span style="font-size:38px;font-weight:600;font-family:monospace"><span class="yz"></span><span class="crs o">|</span></span></div>',
               t, 5750, 'left', f'left:64px;top:{430 + i * 165}px', yaz=deg, ys=t + 250, yh=45)
    # hepsi elle mi?
    g += A('<div class="t" style="font-size:120px">Hepsi</div><div class="t" style="font-size:120px">tek tek</div><div class="t o" style="font-size:150px">elle mi?</div>', 5850, 8250, 'blur', 'left:64px;top:300px')
    g += A('<div class="gri" style="font-size:36px">24 motosiklet × şase, motor no, renk</div>', 6500, 8250, 'up', 'left:68px;top:740px')
    # GEREK YOK
    g += A('<div class="t" style="font-size:190px">Gerek</div><div class="t o" style="font-size:190px">yok.</div>', 8450, 9350, 'stamp', 'left:90px;top:520px', d=380, shake=1)
    # GELEN FATURA
    g += A('<div class="t" style="font-size:76px">Faturayı açın,<br><span class="o">tek tuş.</span></div>', 9450, 13250, 'blur', 'left:64px;top:270px')
    kart = ('<div class="kart" style="width:810px;overflow:hidden">'
            '<div style="padding:26px 30px;font-size:26px;letter-spacing:3px;font-weight:800" class="gri">GELEN FATURALAR</div>'
            '<div class="sat" style="background:rgba(255,138,0,.10);border-left:6px solid #FF8A00"><div><div style="font-weight:800">Distribütör A</div>'
            '<div class="gri" style="font-size:26px;margin-top:6px">FTR2026000184 · 24 kalem</div></div>'
            '<div style="text-align:right"><div style="font-weight:800">1.736.400 ₺</div><div style="font-size:24px;margin-top:6px" class="o">Motosiklet</div></div></div>'
            '<div class="sat"><div><div style="font-weight:700">Distribütör B</div><div class="gri" style="font-size:26px;margin-top:6px">FTR2026000177 · 6 kalem</div></div>'
            '<div style="text-align:right;font-weight:700">412.800 ₺<div style="font-size:24px;margin-top:6px;color:#3DDC84">İşlendi</div></div></div>'
            '<div style="padding:30px"><div class="dug" style="width:100%;font-size:34px;padding:28px 0">ALIŞ FATURASI OLARAK İŞLE</div></div></div>')
    g += A(kart, 9750, 13250, 'up', 'left:64px;top:560px', d=500)
    g += A('<div class="t y" style="font-size:44px">✓ 24 araç işleniyor…</div>', 12050, 13250, 'pop', 'left:64px;top:1110px')
    # STOĞA ALINDI
    g += A('<div class="t" style="font-size:76px">Bilgiler<br><span class="o">faturadan gelir.</span></div>', 13350, 17150, 'blur', 'left:64px;top:270px')
    modeller = [('125cc Scooter', 'Siyah', '01404'), ('125cc Scooter', 'Beyaz', '01411'), ('150cc Naked', 'Kırmızı', '00387'),
                ('50cc Scooter', 'Gri', '02236'), ('250cc Enduro', 'Siyah', '00951'), ('125cc Scooter', 'Mavi', '01419')]
    g += A('<div class="kart" style="width:810px;height:640px"></div>', 13500, 17150, 'fade', 'left:64px;top:500px')
    satir = ''
    for i, (m, r, s) in enumerate(modeller):
        g += A(f'<div class="sat" style="width:810px"><div><div style="font-weight:700">{m}</div><div class="gri" style="font-size:24px;margin-top:4px">Şase …{s} · Motor no ✓</div></div>'
                   f'<div style="display:flex;align-items:center;gap:14px"><span style="font-size:28px">{r}</span><span class="y" style="font-size:34px">✓</span></div></div>',
                   13700 + i * 260, 17150, 'left', f'left:64px;top:{520 + i * 98}px', d=360)
    g += SAYAC(14900, 17150, 0, 24, 14950, 16700, 'left:64px;top:1150px;font-size:64px;color:#3DDC84', pre='Stokta: ', suf=' araç ✓', fx='up')
    g += CTA(17350, S)
    alt = ALTYAZI([(2880, 5700, 'Şase, motor numarası, renk…'), (9450, 13250, 'Gelen faturayı açın, alış faturası olarak işleyin.'),
                   (13350, 17150, 'Araçlar dakikalar içinde stokta.')])
    im = [imlec(1, 10700, 12300, 900, 1500, 470, 1000, 11700)]
    golge = [[2880 + OFF, FE, 0.62]]
    return dict(ad='r1_kamyon', sure=S, fe=FE, blur=(2.85 + OFF / 1000, FE / 1000), html=sayfa(g + alt, S, FE, golge, im),
                flow='flow/kamyon.mp4', ses='ses/r1.mp3',
                vurgu=[0, 1250, 2880, 5850, 8450, 9450, 13350, 14950, 17350], vurus=[8450], tiklar=[11700])


# ---------------------------------------------------------------- R2 GECE MESAJI
def r2():
    S = 20400
    FE = 8150 + OFF
    g = ''
    g += A('<div class="t" style="font-size:118px">Gece <span class="o">23:30.</span></div>', -2000, 4550, 'fade', 'left:64px;top:250px')
    bildirim = ('<div class="kart" style="width:810px;padding:30px 34px;display:flex;gap:26px;align-items:center;background:rgba(30,28,26,.94)">'
                '<div style="width:86px;height:86px;border-radius:50%;background:#FF8A00;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 24 24" width="46" height="46"><path d="M4 5h16v11H9l-5 4z" fill="#111"/></svg></div>'
                '<div><div class="gri" style="font-size:26px">Sahibinden · yeni mesaj · şimdi</div>'
                '<div style="font-size:44px;font-weight:800;margin-top:8px">"Son fiyat ne abi?"</div></div></div>')
    g += A(bildirim, 1500, 4550, 'down', 'left:64px;top:430px', d=500, shake=1)
    # başka bayi
    g += A('<div class="t" style="font-size:76px">Cevap yoksa<br><span class="o">başka bayiye</span> yazar.</div>', 4750, 8050, 'blur', 'left:64px;top:280px')
    bayi = [('Bayi A', 'Cevap verdi · 23:31', 'y', '✓'), ('Bayi B', 'Cevap verdi · 23:33', 'y', '✓'), ('Siz', 'Cevap yok', 'k', '✕')]
    for i, (b, d_, c, ik) in enumerate(bayi):
        vur = 'border:2px solid rgba(255,90,79,.7);' if b == 'Siz' else ''
        g += A(f'<div class="kart" style="width:790px;padding:30px 36px;display:flex;justify-content:space-between;align-items:center;{vur}">'
               f'<span style="font-size:42px;font-weight:800">{b}</span><span class="{c}" style="font-size:34px;font-weight:700">{d_}  {ik}</span></div>',
               5200 + i * 650, 8050, 'left', f'left:64px;top:{560 + i * 160}px', shake=(1 if b == 'Siz' else ''))
    # MOTRAN hazırlar
    g += A('<div class="t" style="font-size:72px">MOTRAN<br><span class="o">cevabı hazırlar.</span></div>', 8250, 12900, 'blur', 'left:64px;top:270px')
    g += A('<div class="kart" style="width:810px;height:690px"></div>', 8350, 12900, 'fade', 'left:64px;top:500px')
    g += A('<div class="gri" style="font-size:26px;letter-spacing:3px;font-weight:800">SAHİBİNDEN MESAJLARI</div>', 8350, 12900, 'fade', 'left:100px;top:530px')
    g += A('<div style="background:#2A2724;border-radius:28px 28px 28px 8px;padding:22px 28px;font-size:36px;font-weight:600">Son fiyat ne abi?</div>', 8550, 12900, 'left', 'left:100px;top:590px')
    g += A('<div style="font-size:32px;font-weight:700"><span class="y">✓</span> Stok: 125cc Scooter · 2024 · 3 adet</div>', 9850, 12900, 'up', 'left:100px;top:705px')
    g += A('<div style="font-size:32px;font-weight:700"><span class="y">✓</span> Fiyat listesi: nakit 72.350 ₺</div>', 10650, 12900, 'up', 'left:100px;top:765px')
    cevap = 'Merhaba, 2024 model 125cc Scooter stokta var. Nakit fiyatı 72.350 TL. Taksit seçeneklerini de yazabilirim.'
    g += A('<div style="background:#FF8A00;color:#111;border-radius:28px 28px 8px 28px;padding:24px 30px;font-size:34px;font-weight:700;line-height:1.25;width:690px">'
           '<span class="yz"></span><span class="crs">|</span></div>', 11300, 12900, 'right', 'left:150px;top:850px', yaz=cevap, ys=11350, yh=14)
    # gönder
    g += A('<div class="t" style="font-size:76px">Siz bakıp<br><span class="o">gönderirsiniz.</span></div>', 13000, 15700, 'blur', 'left:64px;top:280px')
    g += A('<div class="dug" style="font-size:46px;padding:30px 60px">GÖNDER</div>', 13100, 15700, 'pop', 'left:64px;top:560px')
    g += A('<div class="t y" style="font-size:52px">✓ Gönderildi · 23:31</div>', 14250, 15700, 'pop', 'left:64px;top:720px')
    g += A('<div class="cip">Telefondan bile.</div>', 14650, 15700, 'up', 'left:64px;top:830px')
    g += A('<div class="t" style="font-size:150px">İlk cevap</div><div class="t o" style="font-size:150px">sizden.</div>', 15850, 17350, 'stamp', 'left:80px;top:520px', d=380, shake=1)
    g += CTA(17550, S)
    alt = ALTYAZI([(4750, 8050, 'Cevap vermezseniz, o müşteri başka bayiye yazar.'),
                   (8250, 12900, 'MOTRAN mesajı okur, stoğa ve fiyat listesine bakıp cevabı hazırlar.')])
    im = [imlec(1, 13150, 14400, 860, 1450, 330, 600, 13950)]
    golge = [[4700 + OFF, FE, 0.62]]
    return dict(ad='r2_gece_mesaj', sure=S, fe=FE, blur=(4.7 + OFF / 1000, FE / 1000), html=sayfa(g + alt, S, FE, golge, im),
                flow='flow/telefon.mp4', ses='ses/r2.mp3',
                vurgu=[0, 1500, 4750, 8250, 9850, 10650, 11300, 13100, 13950, 15850, 17550], vurus=[1500, 15850], tiklar=[13950])


# ---------------------------------------------------------------- R3 BEKLEYEN MOTOSİKLET
MOTO_SVG = ('<svg viewBox="0 0 64 40" width="{w}" height="{h}">'
            '<g fill="none" stroke="{c}" stroke-width="5"><circle cx="12" cy="29" r="8"/><circle cx="52" cy="29" r="8"/></g>'
            '<g fill="{c}" stroke="{c}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
            '<path d="M19 24 L28 15 L43 15 L47 21 L38 25 L24 26 Z"/><path d="M27 13 L38 13" stroke-width="5" fill="none"/>'
            '<path d="M12 29 L22 24" fill="none"/><path d="M52 29 L45 11 L50 8" fill="none"/></g></svg>')


def r3():
    S = 20800
    FE = 7700 + OFF
    g = ''
    g += A('<div class="t" style="font-size:96px">Bu motosiklet</div>', -2000, 2500, 'fade', 'left:64px;top:250px')
    g += A('<div class="t o" style="font-size:170px">7 aydır</div>', -2000, 2500, 'fade', 'left:64px;top:360px')
    g += A('<div class="t" style="font-size:96px">satılmıyor.</div>', -2000, 2500, 'fade', 'left:64px;top:545px')
    g += A('<div style="border:6px solid #FF5A4F;color:#FF5A4F;border-radius:18px;padding:14px 30px;font-size:58px;font-weight:900;letter-spacing:3px">STOKTA 214 GÜN</div>',
           900, 2500, 'stamp', 'left:120px;top:1020px', d=360, shake=1, base=' rotate(-6deg)')
    # parası
    g += A('<div class="t" style="font-size:80px">Parası</div><div class="t o" style="font-size:80px">rafta bekliyor.</div>', 2650, 4700, 'blur', 'left:64px;top:280px')
    g += SAYAC(2800, 4700, 0, 68400, 2850, 4200, 'left:64px;top:520px;font-size:170px', suf=' ₺', fx='pop')
    # kaç tane
    g += A('<div class="t" style="font-size:96px">Sizde</div><div class="t o" style="font-size:96px">kaç tane var?</div>', 4950, 7600, 'blur', 'left:64px;top:280px')
    izgara = ''
    turuncu = {3, 9, 14, 18}
    for i in range(20):
        x, y = 64 + (i % 5) * 160, 560 + (i // 5) * 130
        renk = '#FF8A00' if i in turuncu else 'rgba(255,255,255,.35)'
        izgara += A(MOTO_SVG.format(w=128, h=80, c=renk), 5200 + i * 60 + (900 if i in turuncu else 0), 7600, 'pop', f'left:{x}px;top:{y}px', d=380)
    g += izgara
    g += A('<div class="t" style="font-size:150px;color:#fff">?</div>', 6900, 7600, 'pop', 'left:760px;top:250px')
    # stok raporu
    g += A('<div class="t" style="font-size:72px">MOTRAN<br><span class="o">listeler.</span></div>', 7950, 14200, 'blur', 'left:64px;top:270px')
    g += A('<div class="kart" style="width:810px;height:520px"></div>', 8050, 14200, 'fade', 'left:64px;top:500px')
    g += A('<div class="gri" style="font-size:26px;letter-spacing:3px;font-weight:800">STOK RAPORLARI · 6+ AY STOKTA</div>', 8050, 14200, 'fade', 'left:100px;top:530px')
    satirlar = [('150cc Naked', 'Siyah', 214), ('125cc Scooter', 'Beyaz', 201), ('50cc Scooter', 'Kırmızı', 188), ('250cc Enduro', 'Gri', 183)]
    for i, (m, r, gun) in enumerate(satirlar):
        vur = 'background:rgba(255,138,0,.13);border-radius:18px;' if i == 0 else ''
        g += A(f'<div class="sat" style="width:770px;{vur}"><div><div style="font-weight:700">{m}</div><div class="gri" style="font-size:24px;margin-top:4px">{r}</div></div>'
               f'<div class="o" style="font-weight:800">{gun} gün</div></div>', 8350 + i * 380, 14200, 'left', f'left:84px;top:{590 + i * 100}px', d=360)
    kp = ('<div class="kart" style="width:810px;padding:30px 36px;display:flex;align-items:center;gap:30px;border:2px solid rgba(255,90,79,.6)">'
          '<div style="width:110px;height:110px;border-radius:50%;background:rgba(255,90,79,.18);border:4px solid #FF5A4F;display:flex;align-items:center;justify-content:center;font-size:58px;font-weight:900;color:#FF5A4F">3</div>'
          '<div><div class="gri" style="font-size:26px;letter-spacing:3px;font-weight:800">KONTROL PANELİ</div><div style="font-size:48px;font-weight:800;margin-top:6px">ZARARDA</div></div></div>')
    g += A(kp, 11500, 14200, 'pop', 'left:64px;top:1010px', d=500, shake=1)
    g += A('<div class="t" style="font-size:80px">Hangisini<br>öne çıkaracağınızı<br><span class="o">ilk bakışta görün.</span></div>', 14350, 17550, 'blur', 'left:64px;top:300px')
    g += A('<div class="kart" style="width:810px;padding:30px 36px;display:flex;justify-content:space-between;align-items:center;border:3px solid #FF8A00">'
           '<div><div style="font-size:40px;font-weight:800">150cc Naked</div><div class="gri" style="font-size:28px;margin-top:6px">Siyah · 214 gün stokta</div></div>'
           '<div class="o" style="font-size:34px;font-weight:800">EN ESKİ</div></div>', 15000, 17550, 'pop', 'left:64px;top:720px', d=500)
    g += CTA(17750, S)
    alt = ALTYAZI([(7950, 11400, 'Altı aydan uzun stokta bekleyenleri listeler.'), (11450, 14200, 'Zararda olanları kontrol panelinde sayar.')])
    golge = [[2600 + OFF, FE, 0.6]]
    return dict(ad='r3_bekleyen', sure=S, fe=FE, blur=(2.6 + OFF / 1000, FE / 1000), html=sayfa(g + alt, S, FE, golge, []),
                flow='flow/tozlu.mp4', ses='ses/r3.mp3',
                vurgu=[0, 900, 2650, 4950, 7950, 8350, 11500, 14350, 15000, 17750], vurus=[900, 11500])


REELS = {'r1': r1, 'r2': r2, 'r3': r3}


# ---------------------------------------------------------------- R4 TESLİM (ÖTV / FATURA / GARANTİ)
def r4():
    S = 20000
    FE = 9300 + OFF
    g = ''
    g += A('<div class="t" style="font-size:118px">Müşteri kapıda.</div>', -2000, 2950, 'fade', 'left:64px;top:250px')
    g += A('<div class="t o" style="font-size:132px">Teslime hazır.</div>', 1230, 2950, 'pop', 'left:64px;top:390px', d=520, shake=1)
    # ama önce
    g += A('<div class="t" style="font-size:96px">Ama <span class="o">önce…</span></div>', 3070, 7150, 'blur', 'left:64px;top:290px')
    isler = [('ÖTV BEYANNAMESİ', 'GİB', 3600), ('FATURA', 'e-Fatura / e-Arşiv', 4900), ('GARANTİ', 'Tedarikçi portalı', 5800)]
    for i, (ad, yer, t) in enumerate(isler):
        g += A(f'<div class="kart" style="width:790px;padding:30px 36px;display:flex;justify-content:space-between;align-items:center">'
               f'<div><div style="font-size:40px;font-weight:800">{ad}</div><div class="gri" style="font-size:28px;margin-top:6px">{yer}</div></div>'
               f'<div style="font-size:30px;font-weight:700;color:#FFB347">bekliyor</div></div>', t, 7150, 'left', f'left:64px;top:{470 + i * 175}px')
    # ayrı ekran ayrı giriş
    g += A('<div class="t" style="font-size:110px">Hepsi</div><div class="t" style="font-size:110px">ayrı ekran,</div><div class="t o" style="font-size:110px">ayrı giriş.</div>', 7310, 9250, 'blur', 'left:64px;top:300px')
    for i, (ad, x, y, r) in enumerate([('GİB', 120, 760, -7), ('e-Fatura', 380, 820, 5), ('Garanti portalı', 200, 930, -3)]):
        g += A(f'<div class="kart" style="width:420px;overflow:hidden"><div style="background:#2A2724;padding:14px 20px;font-size:26px;font-weight:700;display:flex;gap:10px;align-items:center">'
               f'<span style="width:14px;height:14px;border-radius:50%;background:#FF5A4F;display:inline-block"></span>{ad}</div>'
               f'<div style="padding:22px 20px"><div style="height:16px;background:rgba(255,255,255,.12);border-radius:8px;margin-bottom:14px"></div>'
               f'<div style="height:16px;width:70%;background:rgba(255,255,255,.12);border-radius:8px"></div></div></div>',
               7700 + i * 380, 9250, 'pop', f'left:{x}px;top:{y}px', d=420, base=f' rotate({r}deg)')
    # şaseyi yazın
    g += A('<div class="t" style="font-size:80px">Şaseyi yazın,<br><span class="o">HEPSİNİ ÇALIŞTIR.</span></div>', 9520, 12500, 'blur', 'left:64px;top:280px')
    g += A('<div class="kart" style="width:810px;padding:34px 36px;display:flex;align-items:center;gap:20px"><span class="gri" style="font-size:30px;font-weight:800;letter-spacing:2px">ŞASE</span>'
           '<span style="font-size:46px;font-weight:700;font-family:monospace"><span class="yz"></span><span class="crs o">|</span></span></div>',
           9700, 12500, 'up', 'left:64px;top:540px', yaz='LBB•••••••01404', ys=9900, yh=55)
    g += A('<div class="dug" style="width:810px;font-size:46px;padding:34px 0">▶  HEPSİNİ ÇALIŞTIR</div>', 10500, 12500, 'pop', 'left:64px;top:720px', d=450)
    # adımlar
    g += A('<div class="t" style="font-size:80px">Formlar dolar,<br><span class="o">onay sizde.</span></div>', 12650, 15500, 'blur', 'left:64px;top:280px')
    adim = [('1', 'ÖTV', 'GİB formu dolduruldu', 12900), ('2', 'FATURA', 'Fatura bilgileri hazır', 13500), ('3', 'GARANTİ', 'Portal formu dolduruldu', 14100)]
    for i, (n, ad, ac, t) in enumerate(adim):
        g += A(f'<div class="kart" style="width:810px;padding:26px 32px;display:flex;align-items:center;gap:26px">'
               f'<div style="width:74px;height:74px;border-radius:50%;background:rgba(61,220,132,.16);border:3px solid #3DDC84;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:900;color:#3DDC84">✓</div>'
               f'<div><div style="font-size:38px;font-weight:800">{n} · {ad}</div><div class="gri" style="font-size:28px;margin-top:4px">{ac}</div></div></div>',
               t, 15500, 'left', f'left:64px;top:{530 + i * 165}px')
    g += A('<div class="cip">GİB\'de ONAYLA\'ya siz basarsınız.</div>', 14600, 15500, 'up', 'left:64px;top:1040px')
    g += A('<div class="t" style="font-size:132px">Müşteriyi</div><div class="t o" style="font-size:132px">bekletmeyin.</div>', 15660, 16950, 'stamp', 'left:70px;top:520px', d=380, shake=1)
    g += CTA(17150, S)
    alt = ALTYAZI([(3070, 7150, 'ÖTV beyannamesi, fatura, garanti…'), (9520, 12500, 'MOTRAN\'da şaseyi yazın, hepsini çalıştır deyin.')])
    im = [imlec(1, 10700, 12200, 900, 1450, 470, 760, 11400)]
    golge = [[3050 + OFF, FE, 0.62]]
    return dict(ad='r4_teslim', sure=S, fe=FE, blur=(3.05 + OFF / 1000, FE / 1000), html=sayfa(g + alt, S, FE, golge, im),
                flow='flow/teslim.mp4', ses='ses/r4.mp3',
                vurgu=[0, 1230, 3070, 7310, 9520, 12650, 15660, 17150], vurus=[1230, 15660], tiklar=[11400])


REELS['r4'] = r4
