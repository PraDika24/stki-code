from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import string
import nltk
import os
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download stopwords
nltk.download('stopwords')

# Inisialisasi FastAPI dan Middleware CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ganti sesuai kebutuhan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi stemmer
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Load CSV data
base_dir = os.path.dirname(os.path.abspath(__file__))
resume_csv_path = os.path.join(base_dir, "..", "archive", "Resume", "Resume.csv")
pdf_folder_path = os.path.join(base_dir, "..", "archive", "data", "data")

df = pd.read_csv(resume_csv_path)

# Preprocessing teks
def preprocess(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    tokens = text.split()
    filtered = [word for word in tokens if word not in stop_words]
    stemmed = [stemmer.stem(word) for word in filtered]
    return ' '.join(stemmed)

df['processed_cv'] = df['Resume_str'].apply(preprocess)

# Ekstrak ringkasan dari PDF
def extract_pdf_summary(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text[:300] + "..." if text else "No summary available"
    except Exception:
        return "Cannot extract PDF summary"

# # N-GRAM
# def get_similar_resumes(job_description_input: str):
#     job_description = preprocess(job_description_input)
#     documents = [job_description] + df['processed_cv'].tolist()

#     tfidf_vectorizer = TfidfVectorizer(
#         ngram_range=(1, 2),    # unigram dan bigram
#         min_df=2,              # minimal kata muncul di 2 dokumen
#         max_df=0.85,           # abaikan kata yang terlalu umum (>85% dokumen)
#         sublinear_tf=True,     # gunakan log-scaled term frequency
#         norm='l2'              # normalisasi vektor
#     )
#     tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

#     tfidf_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
#     df['tfidf_similarity'] = tfidf_sim

#     df_sorted = df.sort_values(by='tfidf_similarity', ascending=False)

#     results = df_sorted.head(10).copy()
#     results['csv_summary'] = results['Resume_str'].apply(lambda x: x[:300] + "..." if pd.notnull(x) else "No summary available")
#     results['pdf_summary'] = results.apply(
#         lambda row: extract_pdf_summary(os.path.join(pdf_folder_path, row['Category'], f"{row['ID']}.pdf")),
#         axis=1
#     )

#     return results[['ID', 'Category', 'tfidf_similarity', 'csv_summary', 'pdf_summary']].to_dict(orient='records')

# Tanpa N-GRAM
def get_similar_resumes(job_description_input):
    job_description = preprocess(job_description_input)
    documents = [job_description] + df['processed_cv'].tolist()

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    tfidf_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    df['tfidf_similarity'] = tfidf_sim

    df_sorted = df.sort_values(by='tfidf_similarity', ascending=False)

    # Pastikan ID dan Category diambil dari kolom asli
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archive_path = os.path.join(base_dir, "..", "archive", "data", "data")
    results = df_sorted.head(10).copy()
    results['csv_summary'] = results['Resume_str'].apply(lambda x: x[:300] + "..." if x else "No summary available")
    results['pdf_summary'] = results.apply(
        lambda row: extract_pdf_summary(os.path.join(archive_path, row['Category'], f"{row['ID']}.pdf")),
        axis=1
    )

    return results[['ID', 'Category', 'tfidf_similarity', 'csv_summary', 'pdf_summary']].to_dict(orient='records')

