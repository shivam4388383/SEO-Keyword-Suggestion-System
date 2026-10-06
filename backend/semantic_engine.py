from sentence_transformers import SentenceTransformer, util


# ==========================================================
# SEMANTIC MODEL
# ==========================================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ==========================================================
# CALCULATE SEMANTIC SIMILARITY
# ==========================================================

def calculate_semantic_similarity(
    original_keyword,
    suggestions
):
    """
    Original keyword aur generated suggestions ke
    beech semantic similarity calculate karta hai.
    """

    if not original_keyword:
        return []

    if not suggestions:
        return []


    # Original keyword embedding
    original_embedding = model.encode(
        original_keyword,
        convert_to_tensor=True
    )


    # Suggestions embeddings
    suggestion_embeddings = model.encode(
        suggestions,
        convert_to_tensor=True
    )


    # Cosine similarity
    similarities = util.cos_sim(
        original_embedding,
        suggestion_embeddings
    )[0]


    results = []


    for suggestion, similarity in zip(
        suggestions,
        similarities
    ):

        score = float(
            similarity
        )

        # Convert -1 to +1 range
        # into 0 to 100
        percentage = round(
            max(
                0,
                min(
                    score * 100,
                    100
                )
            ),
            2
        )


        results.append({

            "keyword": suggestion,

            "semantic_score":
                percentage

        })


    return results


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    original = "car"


    suggestions = [

        "automobile",

        "vehicle",

        "car repair",

        "car insurance",

        "python programming",

        "digital marketing"

    ]


    results = calculate_semantic_similarity(
        original,
        suggestions
    )


    results.sort(
        key=lambda item:
        item["semantic_score"],
        reverse=True
    )


    print("\nSemantic Similarity Results\n")


    for item in results:

        print(
            f"{item['keyword']:<30}"
            f" | Semantic Score: "
            f"{item['semantic_score']}"
        )