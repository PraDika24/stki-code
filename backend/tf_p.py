import pandas as pd
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import re
import pdfplumber

# Inisialisasi
nltk.download('stopwords')
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Load dataset
file_path = 'archive/Resume/Resume.csv'
df = pd.read_csv(file_path)

# Preprocessing
def preprocess(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

df['processed_cv'] = df['Resume_str'].astype(str).apply(preprocess)

# Ekstraksi ringkasan dari PDF
def extract_pdf_summary(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text[:300] + "..." if text else "No summary available"
    except Exception:
        return "Cannot extract PDF summary"
    

# Menggunakan N-GRAM
# def get_similar_resumes_tfp(job_description_input):
#     # Pra-pemrosesan job description
#     job_description = preprocess(job_description_input)

#     # Gabungkan job description dan semua CV yang telah diproses
#     documents = [job_description] + df['processed_cv'].tolist()


#     # Buat vectorizer dengan n-gram dan filter dokumen
#     vectorizer = CountVectorizer(
#         ngram_range=(1, 1),  # N-gram bisa disesuaikan (misalnya: (1, 2) untuk unigram dan bigram)
#         min_df=2,            # Hanya term yang muncul di >=2 dokumen
#         max_df=0.85          # Hapus term yang sangat umum
#     )

#     # Transformasi teks menjadi matriks count
#     vector_matrix = vectorizer.fit_transform(documents).toarray()

#     # Pisahkan vektor job description dan resume
#     jd_count = vector_matrix[0]
#     resume_counts = vector_matrix[1:]

#     # Hitung TF-P untuk job description dan resume
#     jd_tfp = jd_count / (jd_count.sum() + 1e-9)
#     resume_tfp = resume_counts / (resume_counts.sum(axis=1, keepdims=True) + 1e-9)

#     # Hitung cosine similarity
#     similarity_scores = cosine_similarity(resume_tfp, [jd_tfp]).flatten()
#     df['tfp_similarity'] = similarity_scores

#     # Urutkan berdasarkan similarity tertinggi
#     df_sorted = df.sort_values(by='tfp_similarity', ascending=False)

#     # Path ke folder resume PDF
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     pdf_base_path = os.path.join(base_dir, "..", "archive", "data", "data")

#     # Ambil 10 resume teratas
#     results = df_sorted.head(10).copy()
#     results['csv_summary'] = results['Resume_str'].apply(lambda x: x[:300] + "..." if x else "No summary available")
#     results['pdf_summary'] = results.apply(
#         lambda row: extract_pdf_summary(os.path.join(pdf_base_path, row['Category'], f"{row['ID']}.pdf")),
#         axis=1
#     )

#     return results[['ID', 'Category', 'tfp_similarity', 'csv_summary', 'pdf_summary']].to_dict(orient='records')

# Tanpa N-GRAM
# Fungsi utama: mencari kemiripan dengan TF-P
def get_similar_resumes_tfp(job_description_input):
    job_description = preprocess(job_description_input)
    documents = [job_description] + df['processed_cv'].tolist()

    vectorizer = CountVectorizer()
    vector_matrix = vectorizer.fit_transform(documents).toarray()

    jd_vector = vector_matrix[0]
    resume_vectors = vector_matrix[1:]

    # Hitung TF-P
    jd_tfp = jd_vector / (jd_vector.sum() + 1e-9)
    resume_tfp = resume_vectors / (resume_vectors.sum(axis=1, keepdims=True) + 1e-9)

    similarity_scores = cosine_similarity(resume_tfp, [jd_tfp]).flatten()
    df['tfp_similarity'] = similarity_scores

    df_sorted = df.sort_values(by='tfp_similarity', ascending=False)

    # Path ke PDF resume
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_base_path = os.path.join(base_dir, "..", "archive", "data", "data")

    # Ambil hasil teratas
    results = df_sorted.head(10).copy()
    results['csv_summary'] = results['Resume_str'].apply(lambda x: x[:300] + "..." if x else "No summary available")
    results['pdf_summary'] = results.apply(
        lambda row: extract_pdf_summary(os.path.join(pdf_base_path, row['Category'], f"{row['ID']}.pdf")),
        axis=1
    )

    return results[['ID', 'Category', 'tfp_similarity', 'csv_summary', 'pdf_summary']].to_dict(orient='records')
