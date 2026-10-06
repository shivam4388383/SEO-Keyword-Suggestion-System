import os
import pandas as pd

from sentiment_engine import analyze_sentiment


# ==================================================
# DATASET PATH
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "social_media_data.csv"
)


# ==================================================
# ANALYZE DATASET
# ==================================================

def analyze_dataset():

    if not os.path.exists(DATASET_PATH):

        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )


    df = pd.read_csv(
        DATASET_PATH
    )


    required_columns = {
        "text",
        "keyword"
    }


    missing_columns = (
        required_columns
        - set(df.columns)
    )


    if missing_columns:

        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(missing_columns)
        )


    results = []


    for _, row in df.iterrows():

        text = str(
            row["text"]
        )


        keyword = str(
            row["keyword"]
        )


        result = analyze_sentiment(
            text
        )


        results.append({

            "text": text,

            "keyword": keyword,

            "sentiment":
                result["sentiment"],

            "polarity":
                result["polarity"]

        })


    return pd.DataFrame(
        results
    )


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    df = analyze_dataset()


    print(
        "\nSentiment Analysis Results\n"
    )


    print(
        df.to_string(
            index=False
        )
    )


    print(
        "\nSentiment Summary:"
    )


    print(
        df["sentiment"]
        .value_counts()
    )