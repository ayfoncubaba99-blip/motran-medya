# 22.10.2026: "MOTRAN'ı denemek 4 adım" Reels, Flow açılışlı (hafta3 motor.py + flow/ yöntemi).
# 0 - FLOW_MS arası: Google Flow klibi altta (kancada net, sonra bulanık + koyu), sahneler şeffaf PNG olarak üstte.
# FLOW_MS sonrası: motor.py'nin koyu MOTRAN zemini. Ses: EDA ATLAS (ses/h1.mp3) + sentez müzik + Flow ortam sesi %30.
# python3 yap_flow.py [onizle 300,2500,...]
import json, subprocess, pathlib, asyncio, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import motor
from playwright.async_api import async_playwright

K = pathlib.Path(__file__).parent
FPS = 30
r = json.loads((K / "reels_demo.json").read_text())[0]
S = r["sahneler"]
HOOK_MS = S[0]["sure"]                 # kanca bitince Flow bulanıklaşır
FLOW_MS = S[0]["sure"] + S[1]["sure"]  # 1. adım bitince koyu zemine geçilir
FLOW = K / "flow" / "demo_kapi.mp4"


def seffaf_html():
    h = motor.html_yap(r)
    h = h.replace("html,body{width:1080px;height:1920px;background:#080706;", "html,body{width:1080px;height:1920px;background:transparent;")
    h = h.replace('<div id="isik"></div><div id="isik2"></div>',
                  '<div id="isik" style="display:none"></div><div id="isik2" style="display:none"></div>'
                  '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.78) 0%,rgba(0,0,0,.62) 45%,'
                  'rgba(0,0,0,.30) 72%,rgba(0,0,0,.12) 100%)"></div>')
    h = h.replace("#ornek{position:absolute;left:80px;top:1395px;font-size:22px;color:rgba(255,255,255,.4)",
                  "#ornek{position:absolute;left:80px;top:1395px;font-size:22px;color:rgba(255,255,255,.6);text-shadow:0 2px 8px #000")
    h = h.replace(".hook{", ".hook{text-shadow:0 6px 30px rgba(0,0,0,.6);").replace(".big{", ".big{text-shadow:0 6px 30px rgba(0,0,0,.6);")
    return h


async def seffaf_kareler(anlar, kls):
    kls.mkdir(parents=True, exist_ok=True)
    yol = kls.parent / "seffaf.html"
    yol.write_text(seffaf_html(), encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(yol.as_uri()); await pg.wait_for_timeout(400)
        for i, ms in enumerate(anlar):
            await pg.evaluate(f"window.__git({ms})")
            await pg.screenshot(path=str(kls / f"{i:05d}.png"), omit_background=True)
        await b.close()


def taban(out):
    hb = HOOK_MS / 1000
    flt = (f"[0:v]fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,split[a][b];"
           f"[b]boxblur=22:2,eq=brightness=-0.22,format=yuva420p,fade=t=in:st={hb:.2f}:d=0.45:alpha=1[bb];"
           f"[a][bb]overlay,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(FLOW), "-filter_complex", flt, "-map", "[v]", "-t", f"{FLOW_MS / 1000:.3f}",
                    "-c:v", "libx264", "-crf", "15", "-preset", "fast", str(out)], check=True)


def main():
    kls = K / "cikti" / (r["id"] + "_flow")
    kls.mkdir(parents=True, exist_ok=True)
    nf = int(FLOW_MS / 1000 * FPS)
    if len(sys.argv) > 2 and sys.argv[1] == "onizle":
        anlar = [int(x) for x in sys.argv[2].split(",")]
        on = kls / "on"; [f.unlink() for f in on.glob("*.png")] if on.exists() else None
        asyncio.run(seffaf_kareler(anlar, on))
        tb = kls / "taban.mp4"; taban(tb)
        parca = []
        for i, ms in enumerate(anlar):
            o = on / f"o{i}.jpg"
            if ms < FLOW_MS:
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ms / 1000:.3f}", "-i", str(tb), "-i", str(on / f"{i:05d}.png"),
                                "-filter_complex", "[0:v][1:v]overlay,scale=300:-1", "-frames:v", "1", str(o)], check=True)
            else:
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(K / "cikti" / r["id"] / "kare" / f"{int(ms / 1000 * FPS):05d}.jpg"),
                                "-vf", "scale=300:-1", str(o)], check=True)
            parca.append(str(o))
        subprocess.run(["ffmpeg", "-y", "-v", "error"] + sum([["-i", x] for x in parca], []) +
                       ["-filter_complex", "".join(f"[{i}:v]" for i in range(len(parca))) + f"hstack={len(parca)}", str(kls / "ozet.jpg")], check=True)
        print(kls / "ozet.jpg"); return
    # 1) koyu zeminli bütün kareler (motor.py)
    kd = kls / "kare"; kd.mkdir(exist_ok=True)
    import os
    if os.environ.get("KARE_VAR") and any(kd.glob("*.jpg")):     # koyu kareler zaten çekildiyse yeniden çekme
        sure = sum(s["sure"] for s in S)
    else:
        [f.unlink() for f in kd.glob("*.jpg")]
        sure = asyncio.run(motor.kaydet(r, kls))
    # 2) Flow süresince şeffaf kareler
    ks = kls / "seffaf"; [f.unlink() for f in ks.glob("*.png")] if ks.exists() else None
    asyncio.run(seffaf_kareler([f * 1000 / FPS for f in range(nf)], ks))
    tb = kls / "taban.mp4"; taban(tb)
    # 3) müzik
    gec = []; a = 0
    for s in S[:-1]: a += s["sure"]; gec.append(a)
    motor.muzik(sure / 1000, gec, kls / "muzik.wav", bpm=104)
    out = K / "cikti" / "MOTRAN_Demo_4_Adim_Reels_flow.mp4"
    fb = FLOW_MS / 1000
    flt = (f"[0:v][1:v]overlay=format=auto,format=yuv420p[ac];"
           f"[2:v]format=yuv420p[son];[ac][son]concat=n=2:v=1:a=0[v];"
           f"[3:a]volume=0.5[m];[4:a]adelay=120|120,apad,volume=1.5,asplit=2[vo][vk];"
           f"[5:a]volume=0.30,afade=t=out:st={fb - 1.0:.2f}:d=1.0,apad[fa];"
           f"[m][vk]sidechaincompress=threshold=0.03:ratio=8:attack=60:release=500[md];"
           f"[md][vo][fa]amix=inputs=3:weights='0.8 1 1':normalize=0,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tb), "-framerate", str(FPS), "-i", str(ks / "%05d.png"),
                    "-framerate", str(FPS), "-start_number", str(nf), "-i", str(kd / "%05d.jpg"),
                    "-i", str(kls / "muzik.wav"), "-i", str(K / "ses" / "h1.mp3"), "-i", str(FLOW),
                    "-filter_complex", flt, "-map", "[v]", "-map", "[a]", "-t", f"{sure / 1000:.3f}",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(out)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.5", "-i", str(out), "-frames:v", "1", "-q:v", "3",
                    str(K / "cikti" / "MOTRAN_Demo_4_Adim_kapak.jpg")])
    print("TAMAM", out, round(sure / 1000, 2))


if __name__ == "__main__":
    main()
