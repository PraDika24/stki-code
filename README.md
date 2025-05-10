# Resume Search with TF-IDF

Aplikasi ini adalah alat pencarian resume berbasis TF-IDF (Term Frequency-Inverse Document Frequency) untuk mencari CV yang paling relevan berdasarkan deskripsi pekerjaan yang dimasukkan. Aplikasi ini menggunakan FastAPI sebagai backend dan frontend sederhana dengan HTML dan JavaScript. Data resume diambil dari file CSV dan file PDF yang disimpan di direktori archive.

## Fitur

- Pencarian resume berdasarkan deskripsi pekerjaan menggunakan algoritma TF-IDF.
- Menampilkan ringkasan PDF dari CV.
- Tautan langsung untuk melihat file PDF CV.
- Antarmuka pengguna yang modern dan responsif menggunakan Tailwind CSS.

## Struktur Direktori

```
STKI-CODE/
├── .venv/                  # Virtual environment Python
├── archive/                # Direktori untuk data resume
│   ├── data/
│   │   ├── data/
│   │   │   ├── TEACHER/    # Contoh kategori, berisi file PDF (misalnya 28933005.pdf)
│   │   │   ├── ARTS/
│   │   │   └── ...
│   └── Resume/
│       └── Resume.csv      # File CSV berisi data resume
├── backend/                # Backend FastAPI
│   ├── __pycache__/
│   ├── main.py             # File utama FastAPI
│   └── tf_idf.py           # Logika TF-IDF dan pemrosesan data
├── frontend/               # Frontend aplikasi
│   └── index.html          # Halaman utama aplikasi
└── README.md               # Dokumentasi proyek (file ini)
```

## Prasyarat

- Python 3.8 atau lebih tinggi
- Virtual environment (opsional, tetapi direkomendasikan)
- Koneksi internet untuk CDN (Tailwind CSS dan FontAwesome)

## Instalasi

### 1. Clone atau Unduh Proyek
Pastikan Anda memiliki salinan proyek di direktori lokal Anda.

### 2. Buat Virtual Environment (Opsional)
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instal Dependensi
Pastikan Anda berada di direktori proyek (STKI-CODE), lalu instal dependensi:
```bash
pip install -r requirements.txt 
```

Catatan: Jika Anda menggunakan Windows, gunakan `pip` alih-alih `pip3`.

### 4. Unduh Data NLTK
Jalankan Python dan unduh data stopwords untuk NLTK:
```python
import nltk
nltk.download('stopwords')
```

### 5. Pastikan Data Resume Tersedia

- File `archive/Resume/Resume.csv` harus ada dan berisi kolom seperti ID, Category, dan Resume_str.
- File PDF CV harus ada di `archive/data/data/{Category}/{ID}.pdf` (misalnya, `archive/data/data/TEACHER/28933005.pdf`).

## Menjalankan Aplikasi

### 1. Jalankan Server FastAPI
Pastikan Anda berada di direktori proyek (STKI-CODE), lalu jalankan:
```bash
uvicorn backend.main:app --reload
```

Server akan berjalan di http://127.0.0.1:8000.

### 2. Akses Aplikasi
Buka browser dan kunjungi http://localhost:8000.

### 3. Gunakan Aplikasi

- Masukkan deskripsi pekerjaan di kolom pencarian.
- Klik tombol "Cari" untuk melihat hasil.
- Setiap hasil akan menampilkan nama file PDF (dapat diklik), ringkasan PDF, dan tautan untuk melihat CV.

## Contoh Penggunaan

1. Masukkan deskripsi pekerjaan seperti:
   ```
   We are looking for an enthusiastic, motivated, and experienced teacher to join our academic faculty.
   ```

2. Klik "Cari", dan aplikasi akan menampilkan daftar CV yang relevan dengan ringkasan PDF dan tautan untuk melihat file PDF.

## Teknologi yang Digunakan

- **Backend**: FastAPI, Python
- **Frontend**: HTML, JavaScript, Tailwind CSS, FontAwesome
- **Pemrosesan Data**: Pandas, Scikit-learn (TF-IDF), NLTK, pdfplumber

## Catatan

- Pastikan file PDF ada di direktori yang benar agar tautan berfungsi.
- Jika ikon PDF tidak muncul, pastikan koneksi internet aktif (karena menggunakan CDN FontAwesome).
- Untuk performa yang lebih baik, Anda bisa menambahkan indeks pada data atau mengoptimalkan algoritma TF-IDF.
