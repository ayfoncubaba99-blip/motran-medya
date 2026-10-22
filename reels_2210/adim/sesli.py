# Sesli Reels: sahneleri EDA ATLAS sesine gore yeniden zamanla, render, sesi muzigin ustune koy
import json, sys, subprocess, pathlib, asyncio
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import motor
K = pathlib.Path(__file__).parent
import os
DOSYA = os.environ.get("REELS","reels.json")
LST = json.loads((K/DOSYA).read_text())
reels = {r["id"]: r for r in LST}
ES = {"r1":"r1_excel","r2":"r2_5soru","r3":"r3_motorno","r4":"r4_saat19","r5":"r5_kask","r6":"r6_cumleler","r7":"r7_bayiler"}
if DOSYA!="reels.json": ES = {f"h{i+1}": r["id"] for i,r in enumerate(LST)}
for kisa in sys.argv[1:]:
    rid = ES[kisa]; r = json.loads(json.dumps(reels[rid]))
    ses = K/"ses"/f"{kisa}.mp3"
    vo = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(ses)]).decode())
    hedef = (vo + 1.3) * 1000
    top = sum(s["sure"] for s in r["sahneler"])
    k = hedef / top
    for s in r["sahneler"]: s["sure"] = int(s["sure"] * k)
    kls = K/"cikti_sesli"/rid; kls.mkdir(parents=True, exist_ok=True)
    for f in (kls/"kare").glob("*.jpg"): f.unlink()
    sure = asyncio.run(motor.kaydet(r, kls))
    gec=[]; a=0
    for s in r["sahneler"][:-1]: a+=s["sure"]; gec.append(a)
    motor.muzik(sure/1000, gec, kls/"muzik.wav")
    out = K/"cikti_sesli"/f"{rid}.mp4"
    flt = ("[1:a]volume=0.5[m];[2:a]adelay=150|150,apad,volume=1.5,asplit=2[v][vk];"
           "[m][vk]sidechaincompress=threshold=0.03:ratio=8:attack=60:release=500[md];"
           "[md][v]amix=inputs=2:weights='0.8 1':normalize=0,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",str(kls/"kare/%05d.jpg"),"-i",str(kls/"muzik.wav"),"-i",str(ses),
        "-filter_complex",flt,"-map","0:v","-map","[a]","-c:v","libx264","-pix_fmt","yuv420p","-crf","21","-preset","medium",
        "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(out)],check=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(kls/"kare/00000.jpg"),"-q:v","3",str(K/"cikti_sesli"/f"{rid}_kapak.jpg")])
    print(rid, "ses", round(vo,2), "video", round(sure/1000,2), flush=True)
