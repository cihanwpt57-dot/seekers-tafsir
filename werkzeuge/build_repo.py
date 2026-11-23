"""Baut aus den Whisper-Transkripten ein Markdown-Repo: eine Datei pro Sure, Absaetze mit YouTube-Zeitlinks."""
import glob, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
SRC = r"C:\Users\cihan\whisper\transkripte"
OUT = sys.argv[1]
PLAYLIST = "PL4mTEQpP9b5EO4dxLRm6NsBDy8VoweKKQ"

SUREN = {  # normalisierter Schluessel -> (Nummer, Anzeigename)
    "fatiha": (1, "al-Fatiha"), "baqara": (2, "al-Baqara"), "aliimran": (3, "Al 'Imran"),
    "nisa": (4, "al-Nisa'"), "maida": (5, "al-Ma'ida"), "anam": (6, "al-An'am"),
    "araf": (7, "al-A'raf"), "anfal": (8, "al-Anfal"), "tawba": (9, "al-Tawba"),
    "yunus": (10, "Yunus"), "hud": (11, "Hud"), "yusuf": (12, "Yusuf"), "rad": (13, "al-Ra'd"),
    "ibrahim": (14, "Ibrahim"), "hijr": (15, "al-Hijr"), "nahl": (16, "al-Nahl"),
    "isra": (17, "al-Isra'"), "kahf": (18, "al-Kahf"), "maryam": (19, "Maryam"),
    "taha": (20, "Ta Ha"), "anbiya": (21, "al-Anbiya'"), "hajj": (22, "al-Hajj"),
    "muminun": (23, "al-Mu'minun"), "nur": (24, "al-Nur"), "furqan": (25, "al-Furqan"),
    "shuara": (26, "al-Shu'ara'"),
}

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if c.isascii() and c.isalpha()).lower()
    return re.sub(r"^al", "", s) if not s.startswith("aliimran") else s

def ts(sec):
    sec = int(sec); h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def parse(base):
    m = re.match(r"^(\d{3}) - (\d+)\s*-\s*(.*) \[([\w-]{11})\]$", base)
    idx, nr, rest, vid = int(m.group(1)), m.group(2), m.group(3), m.group(4)
    titel = re.split(r"\s*-\s*Seekers Complete Qur'?an Tafsir", rest)[0].strip(" -")
    t = re.sub(r"^Sura[th]?\s+", "", titel)
    mm = re.match(r"^(.+?)[\s\-]+(\d+.*|end|End)?$", t)
    name, verse = (mm.group(1), mm.group(2) or "") if mm else (t, "")
    name = re.sub(r"\s*\(.*$", "", name)
    key = norm(name)
    sure = SUREN.get(key)
    verse = re.sub(r"\s*-\s*", "–", verse.strip()).replace("end", "Ende").replace("End", "Ende")
    first = re.match(r"\d+", verse)
    return dict(idx=idx, nr=nr, vid=vid, titel=titel, sure=sure, verse=verse,
                vers_start=int(first.group()) if first else 0)

def absaetze(segs, ziel=60):
    """Segmente zu Absaetzen von ~60 s zusammenfassen, Bruch bevorzugt nach Satzende."""
    out, cur, start = [], [], None
    for s in segs:
        t = s["text"].strip()
        if not t: continue
        if start is None: start = s["start"]
        cur.append(t)
        if s["end"] - start >= ziel and t[-1:] in ".?!" or s["end"] - start >= ziel * 2:
            out.append((start, " ".join(cur))); cur, start = [], None
    if cur: out.append((start, " ".join(cur)))
    return out

vortraege = []
for p in sorted(glob.glob(os.path.join(SRC, "*.json"))):
    base = os.path.basename(p)[:-5]
    v = parse(base)
    j = json.load(open(p, encoding="utf-8"))
    v["dauer"] = j["duration"]; v["segs"] = j["segments"]
    vortraege.append(v)

os.makedirs(os.path.join(OUT, "suren"), exist_ok=True)
gruppen = {}
for v in vortraege:
    k = v["sure"] or (0, "Sonstiges")
    gruppen.setdefault(k, []).append(v)

def dateiname(k):
    n, name = k
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower().replace("'", "") if n else "sonstiges").strip("-")
    return f"{n:03d}-{slug}.md"

index_rows, meta = [], []
for k in sorted(gruppen):
    n, name = k
    vs = sorted(gruppen[k], key=lambda v: (v["vers_start"], v["idx"]))
    fn = dateiname(k)
    kopf = f"Sura {n} – {name}" if n else "Sonstiges (Live SeekersAnswers u. a.)"
    lines = [f"# {kopf}", "",
             f"Seekers Complete Qur'an Tafsir – Shaykh Abdul-Rahim Reasat. {len(vs)} Vorträge, "
             f"automatisch transkribiert (Whisper large-v3). Zeitstempel sind Links zur Stelle im Video.", "",
             "## Vorträge", ""]
    for v in vs:
        anker = f"v{v['idx']:03d}"
        lines.append(f"- [{v['titel']}](#{anker}) · {ts(v['dauer'])}")
    lines.append("")
    for v in vs:
        url = f"https://www.youtube.com/watch?v={v['vid']}"
        lines += [f'<a id="v{v["idx"]:03d}"></a>', "",
                  f"## {v['titel']}", "",
                  f"Playlist-Nr. {v['idx']} · Vortrag {v['nr']} · Dauer {ts(v['dauer'])} · [Video]({url})", ""]
        body = []
        for start, text in absaetze(v["segs"]):
            body += [f"**[{ts(start)}]({url}&t={int(start)}s)** {text}", ""]
        lines += body
        # Einzeldatei pro Vortrag (klein genug fuer die GitHub-Codesuche)
        ordner = fn[:-3]
        vslug = re.sub(r"[^a-z0-9]+", "-", (f"{name} {v['verse']}" if n else v["titel"]).lower()
                       .replace("'", "").replace("–", " ")).strip("-")[:60]
        vfn = f"{v['idx']:03d}-{vslug}.md"
        os.makedirs(os.path.join(OUT, "vortraege", ordner), exist_ok=True)
        vk = [f"# {v['titel']}", "",
              f"- Reihe: Seekers Complete Qur'an Tafsir – Shaykh Abdul-Rahim Reasat",
              f"- Sure: {n} – {name}" if n else "- Sure: – (kein Tafsir-Vortrag)",
              f"- Verse: {v['verse'] or '–'}",
              f"- Playlist-Nr.: {v['idx']} · Vortrag {v['nr']} · Dauer {ts(v['dauer'])}",
              f"- Video: {url}", "", "## Transkript", ""]
        open(os.path.join(OUT, "vortraege", ordner, vfn), "w", encoding="utf-8", newline="\n").write("\n".join(vk + body))
        v["vdatei"] = f"vortraege/{ordner}/{vfn}"
        index_rows.append((v["idx"], v["nr"], v["titel"], n, ts(v["dauer"]), v["vdatei"], v["idx"], url))
        meta.append(dict(playlist_nr=v["idx"], vortrag_nr=v["nr"], titel=v["titel"], sure=n or None,
                         sure_name=name if n else None, verse=v["verse"], video_id=v["vid"],
                         dauer_s=round(v["dauer"]), datei=v["vdatei"], suren_datei=f"suren/{fn}"))
    open(os.path.join(OUT, "suren", fn), "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(fn, len(vs))

idx = ["# Inhaltsverzeichnis", "", "Alle Vorträge in Playlist-Reihenfolge.", "",
       "| Nr. | Vortrag | Titel | Sure | Dauer | Text | Video |", "|---:|---:|---|---:|---:|---|---|"]
for i, nr, titel, n, dauer, fn, a, url in sorted(index_rows):
    idx.append(f"| {i} | {nr} | {titel} | {n or '–'} | {dauer} | [lesen]({fn}) | [▶]({url}) |")
open(os.path.join(OUT, "INHALT.md"), "w", encoding="utf-8", newline="\n").write("\n".join(idx) + "\n")
json.dump(meta, open(os.path.join(OUT, "vortraege.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Vortraege:", len(vortraege), " ohne Sure:", [v["titel"] for v in vortraege if not v["sure"]])
