from flask import Flask, request, jsonify
from flask_cors import CORS

from keyword_engine import generate_keywords
from analyzer import analyze_keywords
from sentiment_analyzer import analyze_dataset
from sentiment_engine import analyze_sentiment

import sqlite3
from datetime import datetime


app = Flask(__name__)

CORS(app)


# ==================================================
# DATABASE - SAVE SEARCH
# ==================================================

def save_search(keyword, score):

    connection = sqlite3.connect("search_history.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            score INTEGER,
            searched_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO searches
        (
            keyword,
            score,
            searched_at
        )
        VALUES (?, ?, ?)
    """, (
        keyword,
        score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()

    connection.close()


# ==================================================
# HOME API
# ==================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "SEO Keyword Suggestion System API is running"
    })


# ==================================================
# SEARCH HISTORY API
# ==================================================

@app.route("/history", methods=["GET"])
def history():

    connection = sqlite3.connect(
        "search_history.db"
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            keyword,
            score,
            searched_at
        FROM searches
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    connection.close()

    return jsonify([
        dict(row)
        for row in rows
    ])


# ==================================================
# FALLBACK SENTIMENT
# ==================================================

def calculate_fallback_sentiment(keyword):

    """
    Used when no matching social-media
    records are available in the dataset.

    TextBlob analyzes the entered text itself.
    This is an estimated sentiment and is NOT
    presented as real social-media sentiment.
    """

    result = analyze_sentiment(keyword)

    sentiment = result["sentiment"]

    sentiment_percentage = {
        "Positive": 0,
        "Neutral": 0,
        "Negative": 0
    }

    sentiment_percentage[sentiment] = 100

    return {
        "percentage": sentiment_percentage,
        "source": "Estimated from input text",
        "matched_records": 0
    }


# ==================================================
# ANALYZE API
# ==================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # ------------------------------------------------
    # GET REQUEST DATA
    # ------------------------------------------------

    data = request.get_json()

    if not data or "keyword" not in data:

        return jsonify({
            "error": "Keyword is required"
        }), 400


    keyword = str(
        data["keyword"]
    ).strip()


    # ------------------------------------------------
    # EMPTY INPUT CHECK
    # ------------------------------------------------

    if not keyword:

        return jsonify({
            "error": "Keyword cannot be empty"
        }), 400


    # ------------------------------------------------
    # KEYWORD GENERATION
    # ------------------------------------------------

    keywords = generate_keywords(
        keyword
    )


    # ------------------------------------------------
    # KEYWORD ANALYSIS
    # ------------------------------------------------

    keyword_analysis = analyze_keywords(
        keywords,
        keyword
    )


    # ------------------------------------------------
    # RECOMMENDATION
    # ------------------------------------------------

    best_keyword = None

    if keyword_analysis:

        best_keyword = keyword_analysis[0]


    # ------------------------------------------------
    # SAVE SEARCH
    # ------------------------------------------------

    if best_keyword:

        save_search(
            keyword,
            best_keyword["score"]
        )


    # ------------------------------------------------
    # LOAD SENTIMENT DATASET
    # ------------------------------------------------

    sentiment_df = analyze_dataset()


    # ------------------------------------------------
    # SMART DATASET MATCHING
    # ------------------------------------------------

    input_keyword = keyword.lower().strip()


    matching_data = sentiment_df[
        sentiment_df["keyword"]
        .astype(str)
        .str.lower()
        .apply(
            lambda dataset_keyword:

            dataset_keyword in input_keyword
            or
            input_keyword in dataset_keyword
        )
    ]


    # ------------------------------------------------
    # DATASET MATCH FOUND
    # ------------------------------------------------

    if not matching_data.empty:

        sentiment_counts = (
            matching_data["sentiment"]
            .value_counts()
            .to_dict()
        )


        total = len(
            matching_data
        )


        sentiment_percentage = {

            "Positive": round(
                (
                    sentiment_counts.get(
                        "Positive",
                        0
                    )
                    / total
                ) * 100,
                2
            ),

            "Neutral": round(
                (
                    sentiment_counts.get(
                        "Neutral",
                        0
                    )
                    / total
                ) * 100,
                2
            ),

            "Negative": round(
                (
                    sentiment_counts.get(
                        "Negative",
                        0
                    )
                    / total
                ) * 100,
                2
            )
        }


        sentiment_source = (
            "Social media dataset"
        )


        matched_records = total


    # ------------------------------------------------
    # NO DATASET MATCH
    # ------------------------------------------------

    else:

        fallback = (
            calculate_fallback_sentiment(
                keyword
            )
        )


        sentiment_percentage = (
            fallback["percentage"]
        )


        sentiment_source = (
            fallback["source"]
        )


        matched_records = 0


    # ------------------------------------------------
    # FINAL RESPONSE
    # ------------------------------------------------

    return jsonify({

        "keyword": keyword,

        "suggestions": keyword_analysis,

        "sentiment": sentiment_percentage,

        "sentiment_source": sentiment_source,

        "matched_records": matched_records,

        "recommendation": best_keyword

    })


# ==================================================
# START SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )