from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

from utils import similarity


@st.cache_resource
def load_embedding_model():
    """
    Load the Sentence Transformer model once
    and cache it for the Streamlit application.
    """

    return SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, jd_text):
    """
    Calculate semantic similarity between
    resume and job description.

    Returns:
        float: similarity score between 0 and 100
    """

    if not resume_text or not jd_text:
        return 0.0

    model = load_embedding_model()

    # Convert resume and JD into embeddings
    resume_embedding = model.encode(
        resume_text,
        convert_to_numpy=True
    )

    jd_embedding = model.encode(
        jd_text,
        convert_to_numpy=True
    )

    # Calculate cosine similarity
    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    # Convert 0-1 similarity into 0-100 score
    score = float(similarity * 100)
    return round(score, 2)