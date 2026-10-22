# -*- coding: utf-8 -*-
"""python3 yap.py r1 [kare|ses|video|hepsi]"""
import sys, os, subprocess, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from sahneler import REELS, OFF
import kit

SR = 44100


def wav_yaz(yol, x):
    import wave
    x = np.clip(x, -1, 1)
    d = (x * 32767).astype(np.int16)
    if d.ndim == 1:
        d = np.stack([d, d], 1)
    with wave.open(yol, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())


def ses_oku(yol):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', yol, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def lp(x, a):
    # tek kutuplu alçak geçiren
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s += a * (x[i] - s); y[i] = s
    return y


def muzik(sure_s, vo, seed=1):
    rng = np.random.default_rng(seed)
    n = int(sure_s * SR)
    t = np.arange(n) / SR
    bpm = 104; beat = 60 / bpm
    out = np.zeros(n)
    # akorlar Am F C G (kök frekanslar)
    kok = [110.0, 87.31, 130.81, 98.0]
    akor = [[220, 261.63, 329.63], [174.61, 220, 261.63], [261.63, 329.63, 392], [196, 246.94, 293.66]]
    bar = 4 * beat
    # kick + hat + bas
    kick_n = int(0.35 * SR); kt = np.arange(kick_n) / SR
    kick = np.sin(2 * np.pi * (45 * kt + (110 / 18) * (1 - np.exp(-18 * kt)))) * np.exp(-7 * kt)
    hat_n = int(0.05 * SR)
    hat = rng.standard_normal(hat_n) * np.exp(-np.arange(hat_n) / SR * 90)
    hat = np.diff(np.concatenate([[0], hat]))  # yüksek geçiren
    pompa = np.ones(n)
    b = 0
    while b * beat < sure_s:
        i = int(b * beat * SR)
        if i + kick_n < n:
            out[i:i + kick_n] += kick * 0.55
            pk = np.ones(kick_n); pk[:int(.25 * SR)] = 0.45 + 0.55 * np.linspace(0, 1, int(.25 * SR)) ** 2
            pompa[i:i + kick_n] = np.minimum(pompa[i:i + kick_n], pk)
        for off in (0.5,):
            j = int((b + off) * beat * SR)
            if j + hat_n < n:
                out[j:j + hat_n] += hat * 0.10
        b += 1
    # bas (8'lik) + pad
    bas = np.zeros(n); pad = np.zeros(n)
    k = 0
    while k * bar < sure_s:
        ci = k % 4
        for e in range(8):
            a = int((k * bar + e * beat / 2) * SR); L = int(beat / 2 * SR * 0.9)
            if a + L >= n: break
            tt = np.arange(L) / SR
            f = kok[ci] / 2 if e % 2 == 0 else kok[ci]
            sw = 2 * ((tt * f) % 1) - 1
            bas[a:a + L] += sw * np.exp(-tt * 6) * 0.22
        a = int(k * bar * SR); L = min(int(bar * SR), n - a)
        tt = np.arange(L) / SR
        env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3)
        for f in akor[ci]:
            for dt in (-0.6, 0.6):
                pad[a:a + L] += (2 * ((tt * (f + dt)) % 1) - 1) * env * 0.035
        k += 1
    bas = lp(bas, 0.06); pad = lp(pad, 0.04)
    out = out + bas + pad * pompa
    # sesin altında kıs (yan zincir)
    if vo is not None:
        v = np.zeros(n); m = min(n, len(vo)); v[:m] = np.abs(vo[:m])
        w = int(0.05 * SR)
        env = np.convolve(v, np.ones(w) / w, 'same')
        env = lp(env, 0.0008) * 25
        duck = 1 - 0.55 * np.clip(env, 0, 1)
        out *= duck
    fi = int(0.4 * SR); fo = int(1.2 * SR)
    out[:fi] *= np.linspace(0, 1, fi); out[-fo:] *= np.linspace(1, 0, fo)
    return out


def vuus(n_s=0.45, seed=2):
    rng = np.random.default_rng(seed)
    n = int(n_s * SR); t = np.linspace(0, 1, n)
    x = rng.standard_normal(n)
    # yükselen bant geçiren benzeri: iki lp farkı, katsayı zamanla artar
    y = np.empty(n); s1 = s2 = 0.0
    for i in range(n):
        a = 0.02 + 0.25 * t[i] ** 2
        s1 += a * (x[i] - s1); s2 += a * 0.3 * (s1 - s2); y[i] = s1 - s2
    return y * np.sin(np.pi * t) ** 1.5 * 0.9


def vurus_ses():
    n = int(0.9 * SR); t = np.arange(n) / SR
    b = np.sin(2 * np.pi * (38 * t + 60 / 10 * (1 - np.exp(-10 * t)))) * np.exp(-4 * t)
    nz = np.random.default_rng(5).standard_normal(n) * np.exp(-t * 25) * 0.4
    return (b + nz) * 0.8


def tik():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 300) * 0.5


def ses_yap(r):
    S = r['sure'] / 1000
    vo = ses_oku(r['ses'])
    vo_d = np.concatenate([np.zeros(int(OFF / 1000 * SR)), vo])
    n = int(S * SR)
    vo_d = np.pad(vo_d, (0, max(0, n - len(vo_d))))[:n]
    m = muzik(S, vo_d)
    sfx = np.zeros(n)
    wv = vuus()
    for z in r['vurgu'][1:]:
        a = int((z + OFF) / 1000 * SR) - len(wv) + int(0.05 * SR)
        if 0 <= a and a + len(wv) < n:
            sfx[a:a + len(wv)] += wv * 0.30
    for z in r.get('vurus', []):
        a = int((z + OFF) / 1000 * SR); v = vurus_ses()
        if a + len(v) < n:
            sfx[a:a + len(v)] += v * 0.45
    for im in r.get('tiklar', []):
        a = int((im + OFF) / 1000 * SR); v = tik()
        sfx[a:a + len(v)] += v
    wav_yaz(f'tmp_{r["ad"]}_muzik.wav', (m * 0.55 + sfx) * 0.9)


def video_yap(r, kls, cikti):
    S = r['sure'] / 1000
    b0, b1 = r['blur']
    fe = r['fe'] / 1000
    taban = f'tmp_{r["ad"]}_taban.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', r['flow'], '-an', '-vf',
                    f"fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
                    f"boxblur=luma_radius=22:luma_power=2:enable='between(t,{b0:.2f},{fe + 1:.2f})',"
                    f"tpad=stop_mode=clone:stop_duration={S + 1:.2f}", '-c:v', 'libx264', '-preset', 'fast', '-crf', '14', taban], check=True)
    flt = (f"[0:v][1:v]overlay=0:0[v0];[v0]format=yuv420p[v];"
           f"[2:a]adelay={OFF}|{OFF},volume=1.0[vo];"
           f"[4:a]atrim=0:{fe:.2f},afade=t=out:st={fe - 1.2:.2f}:d=1.2,volume=0.30[fl];"
           f"[3:a]volume=1.0[mz];"
           f"[vo][fl][mz]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.93,atrim=0:{S:.3f}[a]")
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', taban, '-framerate', '30', '-i', f'{kls}/%05d.png',
           '-i', r['ses'], '-i', f'tmp_{r["ad"]}_muzik.wav', '-i', r['flow'], '-filter_complex', flt, '-map', '[v]', '-map', '[a]',
           '-t', f'{S:.3f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', cikti]
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    r = REELS[sys.argv[1]]()
    is_ = sys.argv[2] if len(sys.argv) > 2 else 'hepsi'
    html = f'{r["ad"]}.html'
    open(html, 'w').write(r['html'])
    kls = f'kare_{r["ad"]}'
    if is_ in ('kare', 'hepsi'):
        kit.kareler(html, kls, r['sure'])
    if is_ in ('ses', 'hepsi', 'video'):
        ses_yap(r)
    if is_ in ('video', 'hepsi'):
        os.makedirs('cikti', exist_ok=True)
        video_yap(r, kls, f'cikti/MOTRAN_{r["ad"]}.mp4')
    print('TAMAM', r['ad'])
