from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, jd_text):
    """
    Calculate similarity between resume and job description
    using TF-IDF and cosine similarity.

    Returns:
        float: Similarity score from 0 to 100
    """

    if not resume_text or not jd_text:
        return 0.0

    documents = [
        resume_text,
        jd_text
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)