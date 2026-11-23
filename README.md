# Seekers Complete Qur'an Tafsir – Transkripte

Automatische Transkripte der YouTube-Playlist
[Seekers Complete Qur'an Tafsir](https://www.youtube.com/playlist?list=PL4mTEQpP9b5EO4dxLRm6NsBDy8VoweKKQ)
von Shaykh Abdul-Rahim Reasat (SeekersGuidance), Sura al-Fatiha bis Anfang al-Shu'ara'.

- **723 Vorträge**, rund 385 Stunden Audio
- Transkribiert mit faster-whisper **large-v3** (Englisch, arabische Zitate teils in arabischer Schrift), November 2026
- Nur für den privaten Gebrauch. Die Rechte an den Vorträgen liegen bei SeekersGuidance.

## Aufbau

| Pfad | Inhalt |
|---|---|
| [INHALT.md](INHALT.md) | Alle Vorträge in Playlist-Reihenfolge, mit Links zu Text und Video |
| [vortraege/](vortraege/) | **Eine Datei pro Vortrag** (20–55 KB), in Ordnern pro Sure, z. B. `vortraege/024-al-nur/704-al-nur-56-58.md`. Durchsuchbar mit der GitHub-Suche. |
| [suren/](suren/) | Dieselben Texte, eine große Datei pro Sure zum Durchlesen (nicht von der GitHub-Suche erfasst) |
| [rohdaten/](rohdaten/) | Unveränderte Whisper-Ausgabe pro Vortrag (JSON): Segmente mit Start/Ende, `avg_logprob` und Wortzeiten (`w` Wort, `s`/`e` Start/Ende in s, `p` Wahrscheinlichkeit). Gleiche Ordner- und Dateinamen wie `vortraege/`. |
| [werkzeuge/](werkzeuge/) | `transcribe.py` (Kaggle-Skript, mit dem transkribiert wurde) und `build_repo.py` (erzeugt `vortraege/`, `suren/`, `INHALT.md` aus den Rohdaten) |
| [vortraege.json](vortraege.json) | Maschinenlesbare Liste: Playlist-Nr., Titel, Sure, Verse, Video-ID, Dauer, Datei, Rohdaten |
| [CLAUDE.md](CLAUDE.md) | Hinweise für Claude, wie Fragen zur Serie beantwortet werden sollen |

Jeder Absatz beginnt mit einem Zeitstempel, der direkt zur Stelle im YouTube-Video springt.
Die Ordnernummer ist die Surennummer (`000-sonstiges` = Live-Q&As u. a.), die Dateinummer die Playlist-Position.

## Entstehung

- Audio: yt-dlp 2026.10.26, `-x --audio-format mp3 --audio-quality 5` (48 kHz Stereo, ca. 106–136 kbit/s)
- Transkription: faster-whisper (Version nicht protokolliert), Modell large-v3, `compute_type="float16"`,
  Kaggle mit 2× Tesla T4
- Parameter: `language="en"`, `beam_size=5`, `word_timestamps=True`, `condition_on_previous_text=False`,
  `vad_filter=False`, kein `initial_prompt`, keine `hotwords`, `temperature` Standard
- Keine Nachkorrektur. Die Absätze in `vortraege/` und `suren/` fassen Segmente zusammen: Umbruch ab 60 s
  nach einem Satzende (`.?!`), spätestens nach 120 s; die Zeitmarke ist der Start des ersten Segments.
- Zeitraum: 22.11.2026, 01:59 bis 23.11.2026, 03:06; Nachlauf für die gegenphasigen Vorträge am 23.11.2026
  von 08:22 bis 08:41. Rechenzeit ca. 17,5 h.

## Hinweise zur Qualität

- Automatisch erzeugt, nicht korrekturgelesen. Eigennamen und arabische Begriffe sind oft
  lautschriftlich oder fehlerhaft geschrieben (z. B. „Alhamdulillahi Rabbil Alameen“).
- Playlist-Position 50 ist ein nicht mehr verfügbares Video; inhaltlich fehlt nichts.
- Die Vorträge 704–707, 709, 713, 715, 718, 723 und 724 haben im Original gegenphasige
  Stereokanäle; sie wurden nur aus dem linken Kanal transkribiert
  (`ffmpeg -i in.mp3 -af "pan=mono|c0=c0" -ar 16000 -b:a 64k out.mp3`).
- Automatisch geprüft: Wörter pro Minute (117–176), Lücken, `avg_logprob`, erfundene Schlusszeilen
  (keine gefunden), Wiederholungen. Einige kurze Wiederholungen bleiben stehen, z. B. 614 „Arabic“ 13×
  (Rezitation ab ca. 18:00), 439 „you“ 7×. Es wurde nichts angehört.
- Die Nummerierung in den Videotiteln weicht ab Position 50 um eins von der Playlist-Position ab.
