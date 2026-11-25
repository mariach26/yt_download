# 🛠️ My Tools

Μια web εφαρμογή πολλαπλών εργαλείων φτιαγμένη με **Python** και **Streamlit**, που συγκεντρώνει σε ένα απλό περιβάλλον εργαλεία για λήψη περιεχομένου από το YouTube και επεξεργασία εγγράφων PDF & Word.

##  Λειτουργίες

Η εφαρμογή περιλαμβάνει 3 βασικά εργαλεία, προσβάσιμα από το πλευρικό μενού:

1. **YouTube Downloader**
   - Λήψη βίντεο από YouTube στην καλύτερη διαθέσιμη ποιότητα **MP4**.
   - Εξαγωγή ήχου σε μορφή **MP3 (192kbps)** μέσω FFmpeg.
   - Αυτόματη αφαίρεση παραμέτρων playlist (`&list=`) ώστε να κατεβαίνει μόνο το επιλεγμένο βίντεο.
   - Αυτόματος καθαρισμός των προσωρινών αρχείων από τον φάκελο `downloads/` αμέσως μετά την προετοιμασία της λήψης.

2. **PDF Split & Merge**
   - **Split (Διαχωρισμός):** Ανέβασμα ενός αρχείου PDF και διαχωρισμός του σε 2 μέρη με βάση τη σελίδα που επιλέγει ο χρήστης.
   - **Merge (Συγχώνευση):** Ένωση 2 ή περισσότερων αρχείων PDF σε ένα ενιαίο έγγραφο.

3. **Μετατροπέας Αρχείων (PDF <-> Word)**
   - **PDF σε Word (`.docx`):** Μετατροπή αρχείων PDF σε επεξεργάσιμα έγγραφα Word.
   - **Word σε PDF (`.pdf`):** Μετατροπή αρχείων `.docx` σε PDF.

---

## Τεχνολογίες & Βιβλιοθήκες

- [Streamlit](https://streamlit.io/) — Διεπαφή χρήστη (UI)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Λήψη βίντεο και εξαγωγή ήχου από YouTube
- [PyPDF2](https://pypi.org/project/PyPDF2/) — Διαχωρισμός και συγχώνευση αρχείων PDF
- [pdf2docx](https://pypi.org/project/pdf2docx/) — Μετατροπή PDF σε Word
- [docx2pdf](https://pypi.org/project/docx2pdf/) — Μετατροπή Word σε PDF

---

## Εγκατάσταση & Εκτέλεση

### Προαπαιτούμενα
- **Python 3.8+**
- **FFmpeg:** Απαραίτητο για τη μετατροπή ήχου σε MP3 και τη συγχώνευση βίντεο/ήχου σε MP4 από το `yt-dlp`. Βεβαιώσου ότι είναι εγκατεστημένο και προσβάσιμο στο `PATH` του συστήματος.
- **Microsoft Word:** Απαιτείται από τη βιβλιοθήκη `docx2pdf` (σε Windows/macOS) για τη μετατροπή αρχείων Word σε PDF.

### Βήματα

1. **Κλωνοποίηση του repository:**
   ```bash
   git clone https://github.com/mariach26/yt_download.git
   cd yt_download
   ```

2. **Δημιουργία και ενεργοποίηση εικονικού περιβάλλοντος (προτείνεται):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

3. **Εγκατάσταση εξαρτήσεων:**
   ```bash
   pip install streamlit yt-dlp PyPDF2 pdf2docx docx2pdf
   ```
 

4. **Εκτέλεση της εφαρμογής:**
   ```bash
   streamlit run app.py
   ```

Η εφαρμογή θα ανοίξει αυτόματα στον browser σου (συνήθως στο `http://localhost:8501`).

---

##  Δομή Project

```text
yt_download/
├── app.py              # Κύριο αρχείο της εφαρμογής Streamlit (UI & εργαλεία PDF/Word)
├── dl_config.py        # Ρυθμίσεις yt-dlp και λογική λήψης βίντεο/ήχου
├── downloads/          # Προσωρινός φάκελος λήψεων (δημιουργείται αυτόματα)
└── README.md           # Τεκμηρίωση του project
```
