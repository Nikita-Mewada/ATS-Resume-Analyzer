def calculate_skill_match(resume_skills, jd_skills):
    """
    Calculate the percentage of required job skills
    that are present in the resume.

    Args:
        resume_skills: Skills found in the resume
        jd_skills: Skills found in the job description

    Returns:
        float: Skill match percentage
    """

    if not jd_skills:
        return 0.0

    resume_skills = set(skill.lower() for skill in resume_skills)
    jd_skills = set(skill.lower() for skill in jd_skills)

    matched_skills = resume_skills.intersection(jd_skills)

    score = (len(matched_skills) / len(jd_skills)) * 100

    return round(score, 2)


def calculate_keyword_match(resume_text, jd_text):
    """
    Calculate keyword overlap between resume and job description.

    This is the Version 1 keyword matching approach.
    We will improve this further using TF-IDF in the next step.
    """

    if not resume_text or not jd_text:
        return 0.0

    resume_words = set(
        word.lower()
        for word in resume_text.split()
        if len(word) > 2
    )

    jd_words = set(
        word.lower()
        for word in jd_text.split()
        if len(word) > 2
    )

    if not jd_words:
        return 0.0

    matched_words = resume_words.intersection(jd_words)

    score = (len(matched_words) / len(jd_words)) * 100

    return round(score, 2)


def calculate_ats_score(
    skill_score,
    keyword_score,
    similarity_score
):
    """
    Calculate the final ATS score.

    Weight distribution:

        Skill Match          = 40%
        Keyword Match        = 20%
        Semantic Similarity  = 40%

    Args:
        skill_score: Skill matching percentage
        keyword_score: Keyword matching percentage
        similarity_score: Semantic similarity percentage

    Returns:
        float: Final ATS score
    """

    score = (
        0.40 * skill_score
        + 0.20 * keyword_score
        + 0.40 * similarity_score
    )

    return round(float(score), 2)


def get_recommendations(
    missing_skills,
    keyword_score,
    similarity_score
):
    """
    Generate recommendations for improving the resume.

    Args:
        missing_skills: Skills required by the JD but missing
                        from the resume
        keyword_score: Keyword matching score
        similarity_score: Semantic similarity score

    Returns:
        list: Resume improvement recommendations
    """

    recommendations = []

    # Missing skills
    if missing_skills:
        recommendations.append(
            "Consider adding relevant skills such as: "
            + ", ".join(missing_skills)
        )

    # Keyword score
    if keyword_score < 50:
        recommendations.append(
            "Improve keyword alignment by including "
            "important terms from the job description "
            "where they genuinely match your experience."
        )

    # Semantic similarity
    if similarity_score < 50:
        recommendations.append(
            "Your resume has relatively low semantic alignment "
            "with the job description. Consider highlighting "
            "projects and experience that are more relevant "
            "to the target role."
        )

    if not recommendations:
        recommendations.append(
            "Your resume has good alignment with the job description."
        )

    return recommendations