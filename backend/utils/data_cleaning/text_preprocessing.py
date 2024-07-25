import pandas as pd
from utils.data_cleaning.reference_text import stopwords, punct_to_remove, punct_to_sub


def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", punct_to_remove))


def substitute_punctuation(text: str) -> str:
    for key, value in punct_to_sub.items():
        text = text.replace(key, value)
    return text


def remove_stopwords(text: str) -> str:
    return " ".join([word for word in text.split() if word.lower() not in stopwords])


def preprocess_text(data) -> list:
    """
    RETURNS: Preprocessed text data as-follows:
        - Stopwords removed
        - Lowercased
        - Punctuation removed
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data.copy()

    # Create intermediate columns for temp storage
    print("\n\tPreprocessing: Covert to lowercase...")
    df["description_lower"] = df["description"].str.lower()
    print("\tPreprocessing: Removing punctuation...")
    df["description_wo_punct"] = df["description_lower"].apply(remove_punctuation)
    print("\tPreprocessing: handling \\ and /...")
    df["description_punct_subbed"] = df["description_wo_punct"].apply(
        substitute_punctuation
    )
    print("\tPreprocessing: Removing stop words...\n")
    df["description_clean"] = df["description_punct_subbed"].apply(remove_stopwords)

    # Renaming the final cleaned column to 'preprocessed_description'
    df["preprocessed_description"] = df["description_clean"]

    # Remove intermediate columns
    df.drop(
        [
            "description_lower",
            "description_wo_punct",
            "description_punct_subbed",
            "description_clean",
        ],
        axis=1,
        inplace=True,
    )

    # Replace NaN values with None
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")
