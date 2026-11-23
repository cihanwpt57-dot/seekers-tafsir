# Hinweise für Claude

Dieses Repo enthält die Transkripte der Reihe *Seekers Complete Qur'an Tafsir* von
Shaykh Abdul-Rahim Reasat (723 Vorträge, Sura 1 bis Anfang Sura 26). Die Vorträge sind
englisch; der Nutzer fragt meist auf Deutsch.

## Wo was steht

- `vortraege/<NNN-sure>/<playlist-nr>-<sure>-<verse>.md` – ein Vortrag pro Datei.
  Ordnernummer = Surennummer, z. B. `002-al-baqara`, `024-al-nur`. `000-sonstiges` = Live-Q&As.
- `vortraege.json` – Liste aller Vorträge mit Sure, Versen, Video-ID und Dateipfad.
  Damit lässt sich zu „Sure X, Vers Y“ direkt der passende Vortrag finden.
- `suren/` enthält dieselben Texte als große Sammeldateien; zum Suchen `vortraege/` verwenden.

## Wie suchen

- Fragen zu einem Vers: in `vortraege.json` den Vortrag mit passender Sure und passendem
  Versbereich suchen und dessen Datei lesen.
- Fragen zu einem Thema: im Repo nach englischen Begriffen suchen (z. B. „patience“, „sabr“,
  „repentance“, „tawba“). Arabische Begriffe sind oft unterschiedlich transkribiert
  („Allah“/„Allāh“, „taqwa“/„taqwā“), daher mehrere Schreibweisen probieren.

## Wie antworten

- Antworte in der Sprache der Frage.
- Nenne zu jeder Aussage den Vortrag (Titel bzw. Sure und Verse) und den Zeitstempel als Link,
  so wie er im Transkript steht, z. B. [12:34](https://www.youtube.com/watch?v=ID&t=754s).
- Kurze wörtliche Zitate aus dem Transkript sind gut; kennzeichne sie als Zitat.
- Die Transkripte sind automatisch erzeugt (Whisper) und enthalten Hörfehler, besonders bei
  Namen und arabischen Begriffen. Erkennbare Fehler stillschweigend richtig deuten, bei
  Unklarheit darauf hinweisen. Nichts erfinden, was nicht im Transkript steht.
