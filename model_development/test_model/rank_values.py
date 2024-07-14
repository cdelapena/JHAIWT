from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def rank_on_values(user_text: List[str], match_text: List[str], top_n: int) -> str:
    print("Building the complete corpus...")
    corpus = user_text + match_text
    vectorizer = TfidfVectorizer(stop_words="english")

    print("Fitting and transforming the corpus...")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    print("Calculating the cosine similarity...")
    similarity_matrix = cosine_similarity(tfidf_matrix)

    print(f"Generating the top {top_n} recommendations...")
    similarity_df = pd.DataFrame(similarity_matrix, index=range(len(corpus)), columns=range(len(corpus)))
    rank_df = similarity_df.rank(ascending=False, method="min")

    pairs = []
    similarities = []
    ranks = []

    for i in range(len(corpus)):
        for j in range(i+1, len(corpus)):
            if j != 0 and i != 0:
                continue
            pairs.append(f"(corpus{i}, corpus{j})")
            similarities.append(similarity_matrix[i][j])
            ranks.append(rank_df.iloc[i,j])

    results_df = pd.DataFrame({
        "Pairs": pairs,
        "Similarities": similarities,
        "Rank": ranks
        })

    results_df = results_df.sort_values("Similarities", ascending=False).reset_index(drop=True)
    result = results_df.head(top_n).values.tolist()

    for n, i in enumerate(result):
        record = i[0].split(",")[1].split(")")[0]
        index = int(record.replace("corpus", ""))
        print(f"Rank {n}: {corpus[index]}")

    return

test_user_text = ["Chase leverage expertise in molecular biology and computer science to provide program solutions and data insights to our molecular geneticists. My goal is to join in the transformation of precision medicine by delivering robust laboratory results."]
test_match_texts = [
        "At PreventionGenetics, we are passionate about human genetics and its power to improve lives.", 
        "Chase serves millions of people with a broad range of banking products.",
        "At GeneDx, our mission is to deliver personalized and actionable health insights to inform diagnosis, direct treatment, and improve drug discovery."
        ]
test_top_n = 2

rank_on_values(test_user_text, test_match_texts, test_top_n)