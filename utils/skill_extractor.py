import pandas as pd
import re


def load_skills(path="data/skills.csv"):
    """
    Load skills from CSV file.
    """

    df = pd.read_csv(path)

    skills = (
        df["skill"]
        .dropna()
        .astype(str)
        .str.lower()
        .str.strip()
        .tolist()
    )

    return skills


def extract_skills(text, skills):
    """
    Extract skills present in the given text.
    """

    if not text:
        return []

    text = text.lower()

    found_skills = []

    for skill in skills:

        # Escape special regex characters
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))