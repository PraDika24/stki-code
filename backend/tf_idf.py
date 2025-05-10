import pandas as pd
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import pdfplumber

nltk.download('stopwords')

stemmer = PorterStemmer()

file_path = 'archive/Resume/Resume.csv'
df = pd.read_csv(file_path)

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

df['processed_cv'] = df['Resume_str'].apply(preprocess)

def extract_pdf_summary(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text[:100] + "..." if text else "No summary available"
    except Exception:
        return "Cannot extract PDF summary"

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
    results['csv_summary'] = results['Resume_str'].apply(lambda x: x[:100] + "..." if x else "No summary available")
    results['pdf_summary'] = results.apply(
        lambda row: extract_pdf_summary(os.path.join(archive_path, row['Category'], f"{row['ID']}.pdf")),
        axis=1
    )

    return results[['ID', 'Category', 'tfidf_similarity', 'csv_summary', 'pdf_summary']].to_dict(orient='records')