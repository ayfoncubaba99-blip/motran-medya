# MOTRAN kisa Reels uretici: sahne listesi (JSON) -> 1080x1920 30fps MP4 + sentez muzik
# Kullanim: python3 motor.py reels.json  [sadece_id]
import json, sys, math, pathlib, asyncio, subprocess, wave, struct, random
import numpy as np
from playwright.async_api import async_playwright

K = pathlib.Path(__file__).parent
LOGO = (K.parent / "logo.b64").read_text().strip()
FPS = 30

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;background:#080706;overflow:hidden;font-family:'Inter',sans-serif;color:#fff}
#isik{position:absolute;left:-300px;bottom:-500px;width:1700px;height:1300px;border-radius:50%;
 background:radial-gradient(circle,rgba(255,138,0,.34),rgba(255,138,0,0) 62%)}
#isik2{position:absolute;right:-420px;top:-380px;width:1100px;height:1100px;border-radius:50%;
 background:radial-gradient(circle,rgba(255,120,0,.20),rgba(255,120,0,0) 62%)}
.sc{position:absolute;left:80px;width:780px;top:230px;height:1210px;display:flex;flex-direction:column;justify-content:center;opacity:0}
.w{display:inline-block;opacity:0;transform:translateY(40px) scale(.96);filter:blur(10px);margin-right:.24em}
.hook{font-size:118px;line-height:1.02;font-weight:900;letter-spacing:-4px}
.big{font-size:92px;line-height:1.05;font-weight:850;letter-spacing:-3px}
.mid{font-size:64px;line-height:1.15;font-weight:750;letter-spacing:-1.5px}
.sub{font-size:44px;line-height:1.3;font-weight:500;color:rgba(255,255,255,.80);margin-top:34px}
.t{color:#FF8A00}
.kick{font-size:30px;font-weight:800;letter-spacing:6px;color:#FF8A00;margin-bottom:34px}
.li{display:flex;gap:26px;align-items:flex-start;font-size:52px;font-weight:750;line-height:1.18;padding:24px 0;
 border-bottom:2px solid rgba(255,255,255,.09);opacity:0;transform:translateX(-50px)}
.li b{color:#FF8A00;min-width:64px;font-weight:900}
.kart{background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);border-radius:34px;padding:30px 40px;margin-top:40px}
.sat{display:flex;justify-content:space-between;align-items:center;font-size:42px;padding:22px 0;border-bottom:2px solid rgba(255,255,255,.08);opacity:0}
.sat:last-child{border-bottom:0}
.sat .k{color:rgba(255,255,255,.62)}
.sat .v{font-weight:800}
.ok{color:#5be37f}.tr{color:#FFB347}
#logo{position:absolute;left:80px;top:150px;display:flex;align-items:center;gap:14px;opacity:.9}
#logo img{width:56px;height:56px}#logo b{font-size:30px;letter-spacing:6px;font-weight:800}
#ornek{position:absolute;left:80px;top:1395px;font-size:22px;color:rgba(255,255,255,.4);opacity:0}
.cta{background:#FF8A00;color:#150b00;border-radius:30px;padding:40px 44px;font-size:56px;font-weight:900;line-height:1.15;margin-top:50px;transform:scale(.9);opacity:0}
.cta small{display:block;font-size:34px;font-weight:700;margin-top:12px}
#bar{position:absolute;left:80px;top:1440px;width:780px;height:6px;background:rgba(255,255,255,.12);border-radius:3px}
#bar i{display:block;height:6px;width:0;background:#FF8A00;border-radius:3px}
"""

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def kelimeler(metin, cls):
    # *turuncu* isaretli kelimeler
    parts = []
    for i, w in enumerate(metin.split(" ")):
        t = w.startswith("*") or w.endswith("*")
        w2 = w.strip("*")
        parts.append(f'<span class="w{" t" if t else ""}">{esc(w2)}</span>')
    return f'<div class="{cls}">{"".join(parts)}</div>'

def sahne_html(i, s):
    tip = s["tip"]; ic = ""
    if s.get("kick"): ic += f'<div class="kick">{esc(s["kick"])}</div>'
    if tip == "hook":
        ic += kelimeler(s["metin"], "hook")
        if s.get("alt"): ic += kelimeler(s["alt"], "sub")
    elif tip in ("buyuk", "orta"):
        ic += kelimeler(s["metin"], "big" if tip == "buyuk" else "mid")
        if s.get("alt"): ic += kelimeler(s["alt"], "sub")
    elif tip == "liste":
        if s.get("baslik"): ic += kelimeler(s["baslik"], "mid")
        ic += '<div style="margin-top:30px">' + "".join(
            f'<div class="li"><b>{esc(str(n))}</b><span>{esc(x)}</span></div>' for n, x in s["maddeler"]) + "</div>"
    elif tip == "kart":
        if s.get("baslik"): ic += kelimeler(s["baslik"], "mid")
        rows = "".join(f'<div class="sat"><span class="k">{esc(k)}</span><span class="v {c}">{esc(v)}</span></div>'
                       for k, v, c in s["satirlar"])
        ic += f'<div class="kart">{rows}</div>'
    elif tip == "cta":
        ic += kelimeler(s["metin"], "big")
        ic += f'<div class="cta">{esc(s["dugme"])}<small>{esc(s.get("kucuk",""))}</small></div>'
    return f'<div class="sc" id="s{i}">{ic}</div>'

JS = r"""
const S = window.__S; let bas=[]; let a=0;
for(const s of S){bas.push(a); a+=s.sure;}
window.__SURE=a;
function ease(x){x=Math.max(0,Math.min(1,x));return 1-Math.pow(1-x,3)}
window.__git=function(ms){
  document.querySelector('#bar i').style.width=(100*Math.min(1,ms/window.__SURE))+'%';
  const ornekGoster = S.some((s,i)=>s.ornek && ms>=bas[i] && ms<bas[i]+s.sure);
  document.getElementById('ornek').style.opacity = ornekGoster?1:0;
  document.getElementById('isik').style.transform='translate('+(Math.sin(ms/2400)*60)+'px,'+(Math.cos(ms/3100)*40)+'px)';
  S.forEach((s,i)=>{
    const el=document.getElementById('s'+i); const L=ms-bas[i];
    const icinde = L>=-0 && L< s.sure;
    let op = 0;
    if(icinde){ op=1; const son=s.sure-L; if(son<260 && i<S.length-1) op=son/260; }
    el.style.opacity=op;
    el.style.transform = icinde? 'translateY('+((1-ease(L/400))*30)+'px)':'none';
    if(!icinde) return;
    const ilk = (i===0); // hook: ilk karede yazi tam gorunsun
    el.querySelectorAll('.w').forEach((w,k)=>{
      const t0 = ilk? 0 : 90+k*70; const p = ilk? 1 : ease((L-t0)/320);
      w.style.opacity=p; w.style.transform='translateY('+((1-p)*40)+'px) scale('+(0.96+0.04*p)+')'; w.style.filter='blur('+((1-p)*10)+'px)';
    });
    if(ilk){ const sc = 1.0 + 0.04*Math.sin(Math.min(1,L/600)*Math.PI); el.querySelector('.hook').style.transform='scale('+sc+')'; el.querySelector('.hook').style.transformOrigin='left center';}
    el.querySelectorAll('.li,.sat').forEach((r,k)=>{
      const p=ease((L-(s.zaman?s.zaman[k]:350+k*(s.aralik||520)))/350); r.style.opacity=p; r.style.transform='translateX('+((1-p)*-50)+'px)';
    });
    el.querySelectorAll('.cta').forEach(c=>{const p=ease((L-700)/380); c.style.opacity=p; c.style.transform='scale('+(0.9+0.1*p)+')';});
  });
};
"""

def html_yap(reel):
    S = reel["sahneler"]
    govde = "".join(sahne_html(i, s) for i, s in enumerate(S))
    return f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div id="isik"></div><div id="isik2"></div>
<div id="logo"><img src="data:image/png;base64,{LOGO}"><b>MOTRAN</b></div>
{govde}<div id="ornek">Görseldeki veriler örnektir.</div><div id="bar"><i></i></div>
<script>window.__S={json.dumps(S, ensure_ascii=False)};{JS}</script></body></html>"""

# ---------- ses: 100 BPM La minor, kick/hat/bas/pad + gecis "vuus"
def muzik(sure_s, gecisler_ms, yol, bpm=100):
    sr = 44100; n = int(sr * (sure_s + 0.3)); t = np.arange(n) / sr
    y = np.zeros(n)
    beat = 60 / bpm
    akor = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (261.63, 329.63, 392.0), (196.0, 246.94, 293.66)]
    bar = beat * 4
    for bi in range(int(sure_s / bar) + 2):
        a = akor[bi % 4]; t0 = bi * bar
        i0 = int(t0 * sr); i1 = min(n, int((t0 + bar) * sr))
        if i0 >= n: break
        tt = t[i0:i1] - t0
        env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3)
        for f in a:
            y[i0:i1] += 0.045 * env * (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt))
        # bas
        for k in range(4):
            b0 = t0 + k * beat; j0 = int(b0 * sr); j1 = min(n, int((b0 + beat*0.9) * sr))
            if j0 >= n: break
            tb = t[j0:j1] - b0
            y[j0:j1] += 0.12 * np.exp(-tb * 3) * np.sin(2*np.pi*(a[0]/2)*tb)
    for k in range(int(sure_s / beat) + 1):
        b0 = k * beat; j0 = int(b0 * sr); j1 = min(n, j0 + int(0.25 * sr))
        tk = t[j0:j1] - b0
        y[j0:j1] += 0.42 * np.exp(-tk * 18) * np.sin(2*np.pi*(55 + 90*np.exp(-tk*30))*tk)   # kick
        h0 = int((b0 + beat/2) * sr); h1 = min(n, h0 + int(0.05 * sr))
        if h0 < n:
            y[h0:h1] += 0.05 * np.random.randn(h1-h0) * np.exp(-np.arange(h1-h0)/sr*80)        # hat
    for g in gecisler_ms:
        j0 = int(g/1000 * sr) - int(0.18*sr); j1 = min(n, j0 + int(0.35*sr))
        if j0 < 0 or j0 >= n: continue
        m = j1 - j0; e = np.sin(np.linspace(0, np.pi, m))
        y[j0:j1] += 0.10 * np.random.randn(m) * e * np.linspace(0.3, 1, m)
    # giris vurusu
    m = int(0.5*sr); y[:m] += 0.35*np.exp(-np.arange(m)/sr*6)*np.sin(2*np.pi*48*np.arange(m)/sr)
    y[-int(0.8*sr):] *= np.linspace(1, 0, int(0.8*sr))
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.89
    with wave.open(str(yol), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((y * 32767).astype(np.int16).tobytes())

async def kaydet(reel, kls):
    html = kls / "reel.html"; html.write_text(html_yap(reel), encoding="utf-8")
    kare = kls / "kare"; kare.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(html.as_uri()); await pg.wait_for_timeout(500)
        sure = await pg.evaluate("window.__SURE")
        N = int(sure / 1000 * FPS)
        for f in range(N):
            await pg.evaluate(f"window.__git({f*1000/FPS})")
            await pg.screenshot(path=str(kare / f"{f:05d}.jpg"), type="jpeg", quality=92)
        await b.close()
    return sure

def main():
    reels = json.loads(pathlib.Path(sys.argv[1]).read_text())
    sadece = sys.argv[2] if len(sys.argv) > 2 else None
    for r in reels:
        if sadece and r["id"] != sadece: continue
        kls = K / "cikti" / r["id"]; kls.mkdir(parents=True, exist_ok=True)
        sure = asyncio.run(kaydet(r, kls))
        ac = 0; gec = []
        for s in r["sahneler"][:-1]:
            ac += s["sure"]; gec.append(ac)
        muzik(sure / 1000, gec, kls / "ses.wav")
        mp4 = K / "cikti" / f"{r['id']}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(kls / "kare/%05d.jpg"),
                        "-i", str(kls / "ses.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "medium",
                        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(mp4)], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(kls / "kare/00000.jpg"), "-q:v", "3", str(K / "cikti" / f"{r['id']}_kapak.jpg")])
        print(r["id"], round(sure/1000, 1), "sn", mp4.stat().st_size // 1024, "KB")

if __name__ == "__main__":
    main()
