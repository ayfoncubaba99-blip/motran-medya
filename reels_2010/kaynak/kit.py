# -*- coding: utf-8 -*-
"""MOTRAN Reels motoru (20.10.2026).
HTML sahne (deterministik zaman: window.__git(ms)) -> playwright şeffaf PNG kareler
-> ffmpeg: Flow klibi (alt katman) + kareler + ses.
"""
import os, json, subprocess, base64

W, H, FPS = 1080, 1920, 30
KOK = os.path.dirname(os.path.abspath(__file__))

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:'Inter',sans-serif;color:#fff}
#koyu{position:absolute;inset:0;background:#080706;opacity:0}
#isik{position:absolute;left:-300px;right:-300px;bottom:-500px;height:1300px;
 background:radial-gradient(closest-side,rgba(255,138,0,.38),rgba(255,138,0,.10) 55%,rgba(255,138,0,0));}
#isik2{position:absolute;left:300px;top:-420px;width:900px;height:900px;
 background:radial-gradient(closest-side,rgba(255,138,0,.20),rgba(255,138,0,0));}
#golge{position:absolute;inset:0;opacity:0}
#ust{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.78) 0%,rgba(0,0,0,.45) 30%,rgba(0,0,0,0) 48%);}
#alt{position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.75) 0%,rgba(0,0,0,0) 40%);}
#marka{position:absolute;left:64px;top:150px;display:flex;align-items:center;gap:14px;font-weight:800;letter-spacing:6px;font-size:26px;z-index:50}
#marka img{width:46px;height:46px;border-radius:50%}
#not{position:absolute;left:0;right:0;top:1452px;text-align:center;font-size:21px;color:rgba(255,255,255,.55);z-index:50}
#cubuk{position:absolute;left:64px;width:792px;top:1430px;height:5px;background:rgba(255,255,255,.12);border-radius:3px;z-index:50}
#cubuk i{display:block;height:100%;width:0;background:#FF8A00;border-radius:3px}
.a{position:absolute;opacity:0;will-change:transform,opacity}
.t{font-weight:800;letter-spacing:-2px;line-height:1.02;text-shadow:0 4px 30px rgba(0,0,0,.55)}
.o{color:#FF8A00}
.y{color:#3DDC84}
.k{color:#FF5A4F}
.kart{background:rgba(22,20,18,.92);border:1px solid rgba(255,255,255,.10);border-radius:30px;box-shadow:0 30px 80px rgba(0,0,0,.55)}
.cip{display:inline-flex;align-items:center;gap:12px;padding:16px 26px;border-radius:999px;background:rgba(255,138,0,.14);border:2px solid rgba(255,138,0,.55);font-weight:700;font-size:34px}
.dug{display:inline-flex;align-items:center;justify-content:center;gap:14px;background:#FF8A00;color:#111;font-weight:800;border-radius:22px}
.sat{display:flex;justify-content:space-between;align-items:center;padding:22px 30px;border-top:1px solid rgba(255,255,255,.08);font-size:30px}
.sat:first-child{border-top:none}
.gri{color:rgba(255,255,255,.55)}
.alt-yazi{position:absolute;left:64px;right:230px;top:1250px;font-size:40px;font-weight:700;line-height:1.18;z-index:40;text-shadow:0 3px 18px rgba(0,0,0,.9)}
.imlec{position:absolute;width:64px;height:64px;z-index:60;opacity:0}
.halka{position:absolute;border:4px solid #FF8A00;border-radius:50%;opacity:0}
"""

JS = r"""
const E=[...document.querySelectorAll('.a')];
const ez=(x)=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const ezio=(x)=>x<0?0:x>1?1:(x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2);
function sayi(n,tr){return tr?Math.round(n).toLocaleString('tr-TR'):Math.round(n)}
window.__git=function(t){
  const S=window.__SURE;
  // zemin
  const fe=window.__FLOW_END;
  document.getElementById('koyu').style.opacity = t<fe-350?0:Math.min(1,(t-(fe-350))/350);
  const ii=document.getElementById('isik'); ii.style.opacity=document.getElementById('koyu').style.opacity;
  ii.style.transform='translateY('+(Math.sin(t/1400)*40)+'px) scale('+(1+Math.sin(t/2100)*.05)+')';
  document.getElementById('isik2').style.opacity=document.getElementById('koyu').style.opacity;
  document.getElementById('ust').style.opacity=1-(+document.getElementById('koyu').style.opacity);
  const g=document.getElementById('golge'); // flow üstünde karartma
  let go=0; for(const [a,b,v] of window.__GOLGE){ if(t>=a&&t<b){ go=v*Math.min(1,(t-a)/300)*Math.min(1,(b-t)/300);} }
  g.style.background='rgba(8,7,6,'+go+')'; g.style.opacity=1;
  document.getElementById('cubuk').firstElementChild.style.width=(100*t/S)+'%';
  for(const e of E){
    const t0=+e.dataset.t0, t1=+(e.dataset.t1||1e9), d=+(e.dataset.d||420), fx=e.dataset.fx||'up';
    let p=ez((t-t0)/d), q=t1>=1e9?1:1-ez((t-t1)/320);
    let op=Math.min(p,q), tr='';
    if(t<t0){op=0}
    if(fx=='up') tr='translateY('+((1-p)*60)+'px)';
    else if(fx=='down') tr='translateY('+(-(1-p)*60)+'px)';
    else if(fx=='left') tr='translateX('+((1-p)*-120)+'px)';
    else if(fx=='right') tr='translateX('+((1-p)*120)+'px)';
    else if(fx=='pop') {const x=Math.min(1,(t-t0)/d); const s=x<0?0:(x<.6? .6+.55*ez(x/.6): 1.15-.15*ezio((x-.6)/.4)); tr='scale('+s+')'; op=Math.min(x<0?0:Math.min(1,x*3),q)}
    else if(fx=='stamp'){const x=Math.min(1,(t-t0)/d); const s=x<0?3:3-2*ez(x); tr='scale('+s+') rotate('+(-8)+'deg)'; op=Math.min(x<0?0:Math.min(1,x*2),q)}
    else if(fx=='zoom') tr='scale('+(1.25-.25*p)+')';
    else if(fx=='blur') {e.style.filter='blur('+((1-p)*18)+'px)'; tr='scale('+(1.08-.08*p)+')'}
    else if(fx=='fade') tr='';
    if(e.dataset.shake && t>=t0 && t<t0+260){const k=(t-t0)/260; tr+=' translate('+(Math.sin(t*.9)*14*(1-k))+'px,'+(Math.cos(t*1.1)*10*(1-k))+'px)'}
    if(t1<1e9 && t>t1 && fx!='pop') tr+=' translateY('+(-ez((t-t1)/320)*40)+'px)';
    e.style.opacity=op; e.style.transform=tr + (e.dataset.base||'');
    // sayaç
    if(e.dataset.c0!==undefined){const c0=+e.dataset.c0,c1=+e.dataset.c1,ct0=+(e.dataset.ct0||t0),ct1=+(e.dataset.ct1||t0+900);
      const x=ezio((t-ct0)/(ct1-ct0)); e.querySelector('.n').textContent=(e.dataset.pre||'')+sayi(c0+(c1-c0)*x,e.dataset.tr)+(e.dataset.suf||'');}
    // yazı makinesi
    if(e.dataset.yaz!==undefined){const full=e.dataset.yaz; const ys=+(e.dataset.ys||t0), yh=+(e.dataset.yh||28);
      const n=Math.max(0,Math.min(full.length,Math.floor((t-ys)/yh))); e.querySelector('.yz').textContent=full.slice(0,n);
      const c=e.querySelector('.crs'); if(c) c.style.opacity=(n<full.length||Math.floor(t/400)%2)?1:0;}
  }
  // imleç
  for(const m of window.__IMLEC){ const el=document.getElementById(m.id); const [ta,tb,x0,y0,x1,y1,tc]=m.v;
    if(t<ta||t>tb+300){el.style.opacity=0;const hh=document.getElementById(m.id+'h'); if(hh) hh.style.opacity=0; continue}
    const x=ezio((t-ta)/Math.max(1,(tc-ta)*.8)); el.style.opacity=Math.min(1,(t-ta)/200)*(t>tb?1-(t-tb)/300:1);
    const px=x0+(x1-x0)*x, py=y0+(y1-y0)*x; const pr=(t>=tc&&t<tc+180)?.82:1;
    el.style.transform='translate('+px+'px,'+py+'px) scale('+pr+')';
    const h=document.getElementById(m.id+'h'); if(h){const k=(t-tc)/450; if(k>=0&&k<=1){h.style.opacity=1-k;const r=20+80*k;h.style.width=h.style.height=(2*r)+'px';h.style.left=(x1+8-r)+'px';h.style.top=(y1+8-r)+'px'}else h.style.opacity=0}
  }
};
"""

IMLEC_SVG = ('<svg viewBox="0 0 24 24" width="64" height="64"><path d="M4 2l15 9-6.5 1.6L16 20l-3 1.5-3.4-7.3L4 18z" '
             'fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>')


def logo_b64():
    p = os.path.join(KOK, 'motran_logo.png')
    if os.path.exists(p):
        return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    return None


def sayfa(govde, sure, flow_end, golge=(), imlec=()):
    lg = logo_b64()
    marka = (f'<img src="{lg}">' if lg else '<span style="width:40px;height:40px;border-radius:50%;background:#FF8A00;display:inline-block"></span>') + 'MOTRAN'
    im_html = ''.join(f'<div class="imlec" id="{m["id"]}">{IMLEC_SVG}</div><div class="halka" id="{m["id"]}h"></div>' for m in imlec)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div id="koyu"><div id="isik"></div><div id="isik2"></div></div><div id="golge"></div><div id="ust"></div>
<div id="marka">{marka}</div>
{govde}
{im_html}
<div id="cubuk"><i></i></div><div id="not">Görseldeki veriler örnektir.</div>
<script>window.__SURE={sure};window.__FLOW_END={flow_end};window.__GOLGE={json.dumps(list(golge))};window.__IMLEC={json.dumps(list(imlec))};{JS}</script>
</body></html>"""


def kareler(html_yol, kls, sure_ms, bas=0, son=None):
    from playwright.sync_api import sync_playwright
    os.makedirs(kls, exist_ok=True)
    n = int(round(sure_ms / 1000 * FPS))
    son = n if son is None else son
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        hatalar = []
        pg.on('pageerror', lambda e: hatalar.append(str(e)))
        pg.goto('file://' + os.path.abspath(html_yol))
        pg.wait_for_timeout(400)
        for i in range(bas, son):
            yol = os.path.join(kls, f'{i:05d}.png')
            pg.evaluate(f'window.__git({i * 1000 / FPS})')
            pg.screenshot(path=yol, omit_background=True)
        b.close()
    if hatalar:
        print('JS HATA:', hatalar[:3])
    return n


def onizle(html_yol, zamanlar, cikti, flow=None):
    """Seçili anların PNG'si (flow klibinin karesi altta)."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    ims = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        hatalar = []
        pg.on('pageerror', lambda e: hatalar.append(str(e)))
        pg.goto('file://' + os.path.abspath(html_yol))
        pg.wait_for_timeout(400)
        for z in zamanlar:
            pg.evaluate(f'window.__git({z})')
            pg.screenshot(path='/tmp/_on.png', omit_background=True)
            ust = Image.open('/tmp/_on.png').convert('RGBA')
            alt = Image.new('RGBA', (W, H), (40, 40, 40, 255))
            if flow and os.path.exists(flow):
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(min(z / 1000, 7.9)), '-i', flow, '-frames:v', '1',
                                '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}', '/tmp/_fl.png'])
                alt = Image.open('/tmp/_fl.png').convert('RGBA')
            alt.alpha_composite(ust)
            ims.append(alt.convert('RGB').resize((W // 3, H // 3)))
        b.close()
    if hatalar:
        print('JS HATA:', hatalar[:3])
    cols = min(6, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new('RGB', (cols * W // 3, rows * H // 3), (0, 0, 0))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % cols) * W // 3, (i // cols) * H // 3))
    sh.save(cikti, quality=85)
