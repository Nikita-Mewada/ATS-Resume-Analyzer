from utils.semantic_similarity import calculate_semantic_similarity


text1 = "Developed backend applications using Python and FastAPI."

text2 = "Experience building server-side software and REST APIs with Python."

text3 = "Designed marketing campaigns and created social media content."


score1 = calculate_semantic_similarity(
    text1,
    text2
)

score2 = calculate_semantic_similarity(
    text1,
    text3
)


print("Backend similarity:", score1)

print("Backend vs marketing:", score2)