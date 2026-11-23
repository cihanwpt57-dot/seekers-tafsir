# Transkribiert alle NNN.mp3 aus dem eingebundenen Datensatz mit large-v3 auf 2x T4.
# Jede GPU bekommt jede zweite Datei. Fertige Dateien landen in /kaggle/working.
import glob
import json
import os
import subprocess
import sys
import time

OUT = "/kaggle/working"
MODEL = "large-v3"
TIME_BUDGET_S = 10.5 * 3600  # Sicherheitsgrenze unter Kaggles 12-h-Limit


def preload_cuda12():
    import ctypes
    import importlib.util
    for pkg in ("nvidia.cuda_runtime", "nvidia.cublas", "nvidia.cuda_nvrtc", "nvidia.cudnn"):
        spec = importlib.util.find_spec(pkg)
        if not spec:
            continue
        libdir = os.path.join(list(spec.submodule_search_locations)[0], "lib")
        libs = sorted(glob.glob(os.path.join(libdir, "*.so*")), key=lambda p: ("Lt" not in p, p))
        for _ in range(2):
            for lib in libs:
                try:
                    ctypes.CDLL(lib, mode=ctypes.RTLD_GLOBAL)
                except OSError:
                    pass


def worker(gpu, files, t_start):
    preload_cuda12()
    from faster_whisper import WhisperModel
    model = WhisperModel(MODEL, device="cuda", compute_type="float16")
    for f in files:
        if time.time() - t_start > TIME_BUDGET_S:
            print(f"GPU{gpu}: Zeitbudget erreicht, stoppe vor {f}", flush=True)
            break
        stem = os.path.splitext(os.path.basename(f))[0]
        t = time.time()
        try:
            segments, info = model.transcribe(
                f, language="en", beam_size=5, word_timestamps=True,
                condition_on_previous_text=False, vad_filter=False,
            )
            segs = [{
                "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text,
                "avg_logprob": round(s.avg_logprob, 3),
                "words": [{"w": w.word, "s": round(w.start, 2), "e": round(w.end, 2), "p": round(w.probability, 3)}
                          for w in (s.words or [])],
            } for s in segments]
        except Exception as e:  # eine kaputte Datei soll nicht den ganzen Lauf beenden
            print(f"GPU{gpu}: FEHLER {stem}: {e!r}", flush=True)
            continue
        secs = time.time() - t
        with open(f"{OUT}/{stem}.json", "w", encoding="utf-8") as fh:
            json.dump({"model": MODEL, "duration": info.duration, "segments": segs}, fh, ensure_ascii=False)
        with open(f"{OUT}/{stem}.txt", "w", encoding="utf-8") as fh:
            fh.write("\n".join(f"[{int(s['start']) // 60:02d}:{int(s['start']) % 60:02d}] {s['text'].strip()}" for s in segs))
        entry = {"datei": stem, "gpu": gpu, "modell": MODEL, "audio_s": round(info.duration, 1),
                 "rechen_s": round(secs, 1), "woerter": sum(len(s["text"].split()) for s in segs),
                 "zeit": time.strftime("%Y-%m-%d %H:%M:%S")}
        with open(f"{OUT}/laeufe.gpu{gpu}.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(entry, flush=True)


if __name__ == "__main__":
    import multiprocessing as mp
    t_start = time.time()
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "faster-whisper", "av<16",
                    "nvidia-cuda-runtime-cu12", "nvidia-cublas-cu12", "nvidia-cuda-nvrtc-cu12",
                    "nvidia-cudnn-cu12==9.*"], check=True)
    files = sorted(glob.glob("/kaggle/input/**/[0-9][0-9][0-9].mp3", recursive=True))
    print("Dateien:", len(files), flush=True)
    # Modell einmal vorab laden, damit nicht beide Prozesse gleichzeitig 3 GB herunterladen
    from faster_whisper import download_model
    download_model(MODEL)
    ctx = mp.get_context("fork")
    procs = []
    for gpu in (0, 1):
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)
        p = ctx.Process(target=worker, args=(gpu, files[gpu::2], t_start))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    print("Exit-Codes:", [p.exitcode for p in procs], "Dauer h:", round((time.time() - t_start) / 3600, 2))
