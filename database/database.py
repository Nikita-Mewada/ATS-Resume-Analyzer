import sqlite3
from datetime import datetime


DATABASE_NAME = "ats_analyzer.db"


def create_table():
    """
    Create analysis history table if it doesn't exist.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            ats_score REAL,
            skill_score REAL,
            keyword_score REAL,
            similarity_score REAL,
            analysis_date TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def save_analysis(
    resume_name,
    ats_score,
    skill_score,
    keyword_score,
    similarity_score
):
    """
    Save one analysis result.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history (
            resume_name,
            ats_score,
            skill_score,
            keyword_score,
            similarity_score,
            analysis_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            resume_name,
            float(ats_score),
            float(skill_score),
            float(keyword_score),
            float(similarity_score),
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    connection.commit()
    connection.close()

def get_analysis_history():
    """
    Retrieve previous analyses.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            resume_name,
            ats_score,
            skill_score,
            keyword_score,
            similarity_score,
            analysis_date
        FROM analysis_history
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows