# 22.10.2026: "MOTRAN'ı denemek 4 adım" Reels — hafta3 motor.py (yerel kopya: liste maddelerine "zaman" eklendi) +
# EDA ATLAS sesi. Sahne süreleri sesteki cümle başlarına göre elle verildi (sesli.py'deki orantılı ölçek yerine).
import json, subprocess, pathlib, asyncio, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import motor
K = pathlib.Path(__file__).parent
r = json.loads((K / "reels_demo.json").read_text())[0]
kls = K / "cikti" / r["id"]; kls.mkdir(parents=True, exist_ok=True)
for f in (kls / "kare").glob("*.jpg"): f.unlink()
sure = asyncio.run(motor.kaydet(r, kls))
gec = []; a = 0
for s in r["sahneler"][:-1]: a += s["sure"]; gec.append(a)
motor.muzik(sure / 1000, gec, kls / "muzik.wav", bpm=104)
out = K / "cikti" / "MOTRAN_Demo_4_Adim_Reels.mp4"
flt = ("[1:a]volume=0.5[m];[2:a]adelay=120|120,apad,volume=1.5,asplit=2[v][vk];"
       "[m][vk]sidechaincompress=threshold=0.03:ratio=8:attack=60:release=500[md];"
       "[md][v]amix=inputs=2:weights='0.8 1':normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", str(kls / "kare/%05d.jpg"), "-i", str(kls / "muzik.wav"),
                "-i", str(K / "ses" / "h1.mp3"), "-filter_complex", flt, "-map", "0:v", "-map", "[a]", "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-shortest",
                "-movflags", "+faststart", str(out)], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(kls / "kare/00000.jpg"), "-q:v", "3", str(K / "cikti" / "MOTRAN_Demo_4_Adim_kapak.jpg")])
print("TAMAM", out, round(sure / 1000, 2))
