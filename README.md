# Spotify Downloader (Tkinter + Selenium) — **Read‑me**

> **Purpose & scope**  
> This repository contains a small desktop utility that **automates a third‑party website (spotifydown.com)** with **Selenium** and provides a simple **Tkinter GUI** for progress/cover‑art display. It also **renames audio files** using embedded tags via **eyeD3**.  
> 
> **Legal use only:** Use this tool **only** with content you created/own, that is in the **public domain**, or that you are **explicitly licensed** to download. Respect the Terms of Service of all services you access. This documentation intentionally avoids any instructions that would facilitate unauthorized access to copyrighted works.

---

## Features (from code)

- **Headless Firefox automation** using Selenium to interact with **https://spotifydown.com/** (input field `searchInput`, buttons labeled **“Download”**, optional **“Load More”** pagination).  
- **Cookie/consent click‑through** handled by a helper that clicks a button labeled **“Souhlas”** (Czech “Consent”).  
- **Ad/iframe hider** that removes `<iframe>` elements from the page to reduce interference.  
- **GUI preview**: shows **track/playlist title** parsed with **BeautifulSoup**, and **album art** fetched via `requests` then rendered with **Pillow**.  
- **Post‑processing**: uses **eyeD3** to read tags and **rename output files** to `Artist - Title.mp3`, with **character sanitization**.  
- **Background worker thread** for the download workflow; GUI elements (progress label/bar, artwork) update from that thread.  
- **Default output location**: the script points to the user’s **Downloads** folder by default (`~/Downloads`).

_Source: `SpotifyDownloader.py` (imports, helper functions, UI wiring, and the `download_task` flow)._

---

## How it works (high‑level)

1. Launches **headless Firefox** (`selenium.webdriver.Firefox`) and opens `https://spotifydown.com/`.  
2. Enters the provided URL into the **search** field (`class="searchInput"`), acknowledges **cookies/consent**, and clicks **“Download”**.  
3. Waits for the **result section** to load, extracts a **display name** (e.g., track/playlist header), and fetches **cover art** for the GUI.  
4. Collects the available **“Download”** buttons (optionally clicking **“Load More”** to expand lists).  
5. As the browser saves files, the script uses **eyeD3** to read tags and **rename** the resulting `.mp3` files to `Artist - Title.mp3` (with special‑character cleanup).

> Note: The website’s structure, DOM classes, consent flow, or anti‑automation behavior may change; adjust the XPaths/class names accordingly if something breaks.

---

## Requirements

- **Python** 3.9+  
- **Firefox** and **GeckoDriver** available on the system PATH  
- Python packages: `selenium`, `beautifulsoup4`, `Pillow`, `requests`, `eyed3`  
- Tkinter (usually included with Python on Windows/macOS; on some Linux distros install `python3-tk`)

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install selenium beautifulsoup4 Pillow requests eyed3
```

> If Firefox/GeckoDriver are not installed, add them first (e.g., package manager or vendor installers) and ensure `geckodriver` is on PATH.

---

## Quick start (responsible use)

```bash
# from the repository root
python SpotifyDownloader.py
```

- When prompted, paste a **URL you are authorized to process** (e.g., your own work or public‑domain content).  
- The app opens a small window showing **title** and **cover art**; progress text updates as the background task runs.  
- Output files land under your **Downloads** directory by default. You can change this path in code (see `file_path = os.path.expanduser("~/Downloads")`).

> This README intentionally avoids operational instructions aimed at acquiring copyrighted content you are not licensed to download.

---

## Configuration & customization

- **Headless mode**: controlled via `Options()` for Firefox. Remove `--headless` for visual browser debugging.  
- **Download directory**: edit `file_path` to your preferred folder.  
- **Consent UI**: the helper searches for a button with `aria-label="Souhlas"`. If your local consent text differs, update the XPath in `click_consent_button(...)`.  
- **Site layout changes**: if `searchInput`, **“Download”**, or **“Load More”** controls change, update the locators in `download_task(...)`.  
- **Filename policy**: adjust `remove_special_characters(...)` and the tag fields used in `process_file(...)` to match your needs.

---

## Project layout

```
spotify-downloader/
├─ SpotifyDownloader.py   # Tkinter UI + Selenium automation + post-processing
├─ dist/                  # (Optional) packaged builds if you create them locally
└─ .gitignore
```

---

## Known limitations

- **Third‑party dependency**: relies on a public website; availability and markup may change at any time.  
- **Browser downloads**: headless browsers may require profile prefs for fully automatic save behavior on some platforms.  
- **Tagging edge cases**: if tags are missing/invalid, the post‑processing step falls back and may delete a partially written file (see exception handling).

---

## Roadmap ideas

- Configurable output directory and **non‑headless** debug mode toggle.  
- A small **settings** dialog for locale, selectors, and download behavior.  
- Optional switch to **explicit APIs** (where permitted) or a pluggable backend.

---

## License

_No license file is present at the time of writing._

---

## Ethical & legal notice

This project and its documentation are provided **for lawful and responsible use** only. Always follow the licenses and Terms of Service associated with the content and services you use. The authors and contributors are **not responsible** for how third parties use this code.
