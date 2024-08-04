from pathlib import Path
import sys
from typing import List, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommendation_engine(
    user_text: List[str], match_text: List[str], top_n: int
) -> List[int]:
    """Brute force cosine_similarities to compare similarity between
    a user text and job posting descriptions. Utilizes a TFIDF
    vectorizer, and limits to the top_n requested job postings.

    Args:
        user_text (List[str]): pass through user text
        match_text (List[str]): preprocessed job posting text
        top_n (int): requested number of recommend job postings

    Returns:
        List[int]: sorted match_text indecies as a list
    """
    print("\t-> Building the complete corpus...")
    corpus = user_text + match_text
    vectorizer = TfidfVectorizer(stop_words="english")

    print("\t-> Fitting and transforming the corpus...")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    print("\t-> Calculating the cosine similarity...")
    similarity_matrix = cosine_similarity(tfidf_matrix)

    print(f"\t-> Generating the top {top_n} recommendations...")
    similarity_df = pd.DataFrame(
        similarity_matrix, index=range(len(corpus)), columns=range(len(corpus))
    )
    rank_df = similarity_df.rank(ascending=False, method="min")

    pairs = []
    similarities = []
    ranks = []

    for i in range(len(corpus)):
        for j in range(i + 1, len(corpus)):
            if j != 0 and i != 0:
                continue
            pairs.append(f"(corpus{i}, corpus{j})")
            similarities.append(similarity_matrix[i][j])
            ranks.append(rank_df.iloc[i, j])

    results_df = pd.DataFrame(
        {"Pairs": pairs, "Similarities": similarities, "Rank": ranks}
    )

    results_df = results_df.sort_values("Similarities", ascending=False).reset_index(
        drop=True
    )
    result = results_df.head(top_n).values.tolist()

    result_index = [
        int(i[0].split(",")[1].split("corpus")[1].split(")")[0]) - 1 for i in result
    ]

    return result_index


def prefilter_data(category_id: int) -> Tuple[List[int], List[str]]:
    """Gathers model data by category from the db

    Args:
        category_id (int): [Job].categories.id

    Returns:
        Tuple[List[int], List[str]]: Tuple[[[posting].id, ...], [posting].preprocessed_data], ...]]
    """
    parent_path = str(Path.cwd().parent)
    sys.path.append(parent_path)
    from utils.sql.sprocs import get_model_data_by_category

    model_data = get_model_data_by_category(category_id, "Job.db")

    descriptions = [data.preprocessed_description for data in model_data]
    job_ids = [data.id for data in model_data]
    return job_ids, descriptions


def main(user_text: str, category_id: int, req_quant: int) -> List[int]:
    """Wrapper to prepare data for recommendation engine model

    Args:
        user_text (str): pass through text
        category_id (int): pass through [Job].category.id
        req_quant (int): user defined quantity of recommended results

    Returns:
        List[int]: [[posting].id, [posting].id, ...]
    """
    print("Filtering job data...")
    job_ids, input_job_data = prefilter_data(category_id)

    print("Sending data to recommendation engine...")
    engine_results = recommendation_engine([user_text], input_job_data, req_quant)

    print("Gathering job_ids from results")
    result = [job_ids[i] for i in engine_results]

    return result
