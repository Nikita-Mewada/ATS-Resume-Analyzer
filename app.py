import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.pdf_parser import extract_text_from_pdf
from utils.text_processor import clean_text, preprocess_text
from utils.skill_extractor import load_skills, extract_skills
from utils.semantic_similarity import calculate_semantic_similarity

from utils.scorer import (
    calculate_skill_match,
    calculate_keyword_match,
    calculate_ats_score,
    get_recommendations
)

from database.database import (
    create_table,
    save_analysis,
    get_analysis_history
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

create_table()


# ============================================================
# LOAD SKILLS
# ============================================================

skills = load_skills()


# ============================================================
# HEADER
# ============================================================

st.title("📄 ATS Resume Analyzer")

st.write(
    "Analyze how well your resume matches a given job description."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("About")

    st.write(
        """
        This ATS Resume Analyzer compares a resume
        against a job description using:

        • Skill matching
        • Keyword matching
        • TF-IDF similarity
        • Cosine similarity
        """
    )

    st.divider()

    st.subheader("Scoring")

    st.write("Skill Match: 40%")
    st.write("Keyword Match: 20%")
    st.write("Semantic Similarity: 40%")


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("1. Upload Resume")

resume_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)


st.subheader("2. Job Description")

job_description = st.text_area(
    "Paste the job description below",
    height=250,
    placeholder=(
        "Example: We are looking for a Python Developer "
        "with experience in Python, SQL, FastAPI, Git..."
    )
)


analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if resume_file is None:

        st.warning(
            "Please upload a resume PDF."
        )

        st.stop()


    if not job_description.strip():

        st.warning(
            "Please enter a job description."
        )

        st.stop()


    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    with st.spinner("Extracting resume text..."):

        try:

            resume_text = extract_text_from_pdf(
                resume_file
            )

        except Exception as e:

            st.error(str(e))

            st.stop()


    if not resume_text:

        st.error(
            "Could not extract text from the PDF. "
            "Make sure the PDF contains selectable text."
        )

        st.stop()


    # --------------------------------------------------------
    # Clean text
    # --------------------------------------------------------

    cleaned_resume = clean_text(
        resume_text
    )

    cleaned_jd = clean_text(
        job_description
    )


    # --------------------------------------------------------
    # NLP preprocessing
    # --------------------------------------------------------

    processed_resume = preprocess_text(
        resume_text
    )

    processed_jd = preprocess_text(
        job_description
    )


    # --------------------------------------------------------
    # Extract skills
    # --------------------------------------------------------

    with st.spinner("Analyzing skills..."):

        resume_skills = extract_skills(
            cleaned_resume,
            skills
        )

        jd_skills = extract_skills(
            cleaned_jd,
            skills
        )


    # --------------------------------------------------------
    # Matched and missing skills
    # --------------------------------------------------------

    matched_skills = sorted(
        set(resume_skills).intersection(
            set(jd_skills)
        )
    )

    missing_skills = sorted(
        set(jd_skills).difference(
            set(resume_skills)
        )
    )


    # --------------------------------------------------------
    # Calculate scores
    # --------------------------------------------------------

    skill_score = calculate_skill_match(
        resume_skills,
        jd_skills
    )


    keyword_score = calculate_keyword_match(
        processed_resume,
        processed_jd
    )


    similarity_score = calculate_semantic_similarity(
    processed_resume,
    processed_jd
)


    ats_score = calculate_ats_score(
        skill_score,
        keyword_score,
        similarity_score
    )


    # --------------------------------------------------------
    # Save analysis
    # --------------------------------------------------------

    save_analysis(
        resume_file.name,
        ats_score,
        skill_score,
        keyword_score,
        similarity_score
    )


    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    st.divider()

    st.subheader("📊 ATS Analysis Results")


    # --------------------------------------------------------
    # Score display
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "ATS Score",
            f"{ats_score:.1f}/100"
        )


    with col2:

        st.metric(
            "Skill Match",
            f"{skill_score:.1f}%"
        )


    with col3:

        st.metric(
            "Keyword Match",
            f"{keyword_score:.1f}%"
        )


    with col4:

        st.metric(
            "Text Similarity",
            f"{similarity_score:.1f}%"
        )


    st.divider()


    # ========================================================
    # SKILLS
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("✅ Matched Skills")

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    skill.title()
                )

        else:

            st.info(
                "No matching skills found."
            )


    with col2:

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    skill.title()
                )

        else:

            st.success(
                "No missing skills detected!"
            )


    st.divider()


    # ========================================================
    # SCORE CHART
    # ========================================================

    st.subheader("📈 Score Breakdown")


    score_names = [
    "Skill Match",
    "Keyword Match",
    "Semantic Similarity"
]

    score_values = [
        skill_score,
        keyword_score,
        similarity_score
    ]


    fig = go.Figure(
        data=[
            go.Bar(
                x=score_names,
                y=score_values,
                text=[
                    f"{score:.1f}%"
                    for score in score_values
                ],
                textposition="auto"
            )
        ]
    )


    fig.update_layout(
        yaxis=dict(
            range=[0, 100],
            title="Score (%)"
        ),
        xaxis_title="Category",
        height=400
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # ATS SCORE GAUGE
    # ========================================================

    st.subheader("🎯 Overall ATS Score")


    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=ats_score,
            title={
                "text": "ATS Score"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                }
            }
        )
    )


    gauge.update_layout(
        height=350
    )


    st.plotly_chart(
        gauge,
        use_container_width=True
    )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.subheader("💡 Recommendations")


    recommendations = get_recommendations(
        missing_skills,        
        keyword_score,
        similarity_score
    )


    for recommendation in recommendations:

        st.info(
            recommendation
        )


    # ========================================================
    # EXTRACTED TEXT
    # ========================================================

    with st.expander(
        "View Extracted Resume Text"
    ):

        st.text_area(
            "Resume Text",
            resume_text,
            height=400
        )


# ============================================================
# HISTORY
# ============================================================

st.divider()

st.subheader("📚 Analysis History")


history = get_analysis_history()

if history:
    history_df = pd.DataFrame(
        history,
        columns=[
            "ID",
            "Resume",
            "ATS Score",
            "Skill Match",
            "Keyword Match",
            "Similarity",
            "Date"
        ]
    )

    # Convert byte values to valid text before displaying
    for column in history_df.columns:
        history_df[column] = history_df[column].apply(
            lambda value: (
                value.decode("utf-8", errors="replace")
                if isinstance(value, bytes)
                else value
            )
        )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "No previous analyses available."
    )