import pandas as pd
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import pdfplumber

# Inisialisasi
nltk.download('stopwords')
stemmer = PorterStemmer()

# Load dataset
file_path = 'archive/Resume/Resume.csv'
df = pd.read_csv(file_path)

# Preprocessing
def preprocess(text):
    if pd.isnull(text):
        return ""
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    tokens = text.split()
    filtered = [word for word in tokens if word not in stop_words]
    stemmed = [stemmer.stem(word) for word in filtered]
    return ' '.join(stemmed)

df['processed_cv'] = df['Resume_str'].astype(str).apply(preprocess)

# Ekstraksi ringkasan dari PDF
def extract_pdf_summary(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text[:300] + "..." if text else "No summary available"
    except Exception:
        return "Cannot extract PDF summary"

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
    archive_path = os.path.join(base_dir, "..", "archive", "data", "data")

    results = df_sorted.head(10).copy()
    results['csv_summary'] = results['Resume_str'].apply(lambda x: x[:300] + "..." if x else "No summary available")
    results['pdf_summary'] = results.apply(
        lambda row: extract_pdf_summary(os.path.join(archive_path, row['Category'], f"{row['ID']}.pdf")),
        axis=1
    )

    return results[['ID', 'Category', 'tfp_similarity', 'csv_summary', 'pdf_summary']].to_dict(orient='records')
