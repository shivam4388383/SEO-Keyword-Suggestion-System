import re
from difflib import SequenceMatcher

from semantic_engine import calculate_semantic_similarity


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_words(text):
    normalized = normalize_text(text)

    if not normalized:
        return []

    return normalized.split()


# ============================================================
# WORD OVERLAP
# ============================================================

def calculate_word_overlap(original, suggestion):
    original_words = set(get_words(original))
    suggestion_words = set(get_words(suggestion))

    if not original_words:
        return 0

    common_words = original_words.intersection(
        suggestion_words
    )

    overlap_ratio = (
        len(common_words) /
        len(original_words)
    )

    return overlap_ratio * 100


# ============================================================
# TEXT SIMILARITY
# ============================================================

def calculate_similarity(original, suggestion):
    original_normalized = normalize_text(original)
    suggestion_normalized = normalize_text(suggestion)

    if not original_normalized:
        return 0

    similarity = SequenceMatcher(
        None,
        original_normalized,
        suggestion_normalized
    ).ratio()

    return similarity * 100


# ============================================================
# SEARCH INTENT
# ============================================================

def detect_intent(text):
    normalized = normalize_text(text)

    if not normalized:
        return "General"

    # Informational intent
    if (
        normalized.startswith("what ")
        or normalized.startswith("why ")
        or normalized.startswith("how ")
        or normalized.startswith("when ")
        or normalized.startswith("where ")
        or normalized.startswith("who ")
    ):
        return "Informational"

    learning_words = [
        "learn",
        "tutorial",
        "course",
        "guide",
        "beginner",
        "training",
        "examples"
    ]

    if any(
        word in normalized.split()
        for word in learning_words
    ):
        return "Informational"

    # Commercial intent
    commercial_words = [
        "best",
        "top",
        "compare",
        "comparison",
        "review",
        "price",
        "affordable",
        "cheap"
    ]

    if any(
        word in normalized.split()
        for word in commercial_words
    ):
        return "Commercial"

    # Transactional intent
    transactional_words = [
        "buy",
        "purchase",
        "order",
        "download",
        "subscribe",
        "hire"
    ]

    if any(
        word in normalized.split()
        for word in transactional_words
    ):
        return "Transactional"

    return "General"


def calculate_intent_score(original, suggestion):
    original_intent = detect_intent(original)
    suggestion_intent = detect_intent(suggestion)

    if original_intent == suggestion_intent:
        return 100

    if suggestion_intent == "General":
        return 65

    return 45


# ============================================================
# SEO MODIFIER SCORE
# ============================================================

def calculate_modifier_score(suggestion):
    normalized = normalize_text(suggestion)
    words = set(normalized.split())

    useful_modifiers = {
        "beginner": 6,
        "beginners": 6,
        "guide": 5,
        "tutorial": 6,
        "examples": 5,
        "tips": 5,
        "ideas": 5,
        "applications": 6,
        "tools": 6,
        "courses": 5,
        "course": 5,
        "meaning": 4,
        "definition": 4,
        "explained": 5,
        "comparison": 5,
        "compare": 5,
        "reviews": 4,
        "review": 4,
        "jobs": 4,
        "career": 4,
        "projects": 5,
        "skills": 4,
        "uses": 4,
        "benefits": 4
    }

    score = 0

    for word, value in useful_modifiers.items():
        if word in words:
            score += value

    return min(score, 15)


# ============================================================
# KEYWORD LENGTH SCORE
# ============================================================

def calculate_length_score(suggestion):
    word_count = len(get_words(suggestion))

    if word_count == 0:
        return 0

    if 2 <= word_count <= 5:
        return 10

    if word_count == 1:
        return 6

    if word_count == 6:
        return 7

    if word_count == 7:
        return 4

    return 2


# ============================================================
# OLD / TRADITIONAL RELEVANCE SCORE
# ============================================================

def calculate_traditional_score(
    keyword,
    original_keyword
):
    keyword = normalize_text(keyword)
    original_keyword = normalize_text(
        original_keyword
    )

    if not keyword or not original_keyword:
        return 0

    word_overlap = calculate_word_overlap(
        original_keyword,
        keyword
    )

    similarity = calculate_similarity(
        original_keyword,
        keyword
    )

    intent_score = calculate_intent_score(
        original_keyword,
        keyword
    )

    modifier_score = calculate_modifier_score(
        keyword
    )

    length_score = calculate_length_score(
        keyword
    )

    base_score = (
        (word_overlap * 0.40)
        + (similarity * 0.25)
        + (intent_score * 0.15)
    )

    final_score = (
        base_score
        + (modifier_score * 0.75)
        + length_score
    )

    if keyword == original_keyword:
        final_score += 10

    if (
        original_keyword in keyword
        and keyword != original_keyword
    ):
        final_score += 5

    return max(
        0,
        min(round(final_score), 100)
    )


# ============================================================
# FINAL SEMANTIC + TRADITIONAL SCORE
# ============================================================

def calculate_keyword_score(
    keyword,
    original_keyword,
    semantic_score=0
):
    traditional_score = calculate_traditional_score(
        keyword,
        original_keyword
    )

    # Combine:
    # 65% traditional relevance
    # 35% semantic similarity
    final_score = (
        (traditional_score * 0.65)
        + (semantic_score * 0.35)
    )

    # Exact keyword should always remain highly relevant
    if (
        normalize_text(keyword)
        == normalize_text(original_keyword)
    ):
        final_score = 100

    return max(
        0,
        min(round(final_score), 100)
    )


# ============================================================
# COMPLETE KEYWORD ANALYSIS
# ============================================================

def analyze_keywords(keywords, original_keyword):

    if not keywords:
        return []

    # --------------------------------------------------------
    # Calculate semantic similarity
    # --------------------------------------------------------

    semantic_results = calculate_semantic_similarity(
        original_keyword,
        keywords
    )

    semantic_map = {
        item["keyword"]: item["semantic_score"]
        for item in semantic_results
    }

    # --------------------------------------------------------
    # Calculate final scores
    # --------------------------------------------------------

    results = []

    for keyword in keywords:

        semantic_score = semantic_map.get(
            keyword,
            0
        )

        final_score = calculate_keyword_score(
            keyword,
            original_keyword,
            semantic_score
        )

        results.append({
            "keyword": keyword,
            "word_count": len(
                get_words(keyword)
            ),
            "score": final_score,
            "semantic_score": round(
                semantic_score,
                2
            )
        })

    # --------------------------------------------------------
    # Sort by final relevance score
    # --------------------------------------------------------

    results.sort(
        key=lambda item: (
            item["score"],
            item["semantic_score"],
            -item["word_count"]
        ),
        reverse=True
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_cases = {

        "car": [
            "car",
            "automobile",
            "vehicle",
            "car repair",
            "car insurance",
            "python programming",
            "digital marketing"
        ],

        "python": [
            "python",
            "python programming",
            "learn python",
            "python tutorial",
            "python for beginners",
            "digital marketing"
        ],

        "quantum computing": [
            "quantum computing",
            "quantum computing applications",
            "quantum computing for beginners",
            "quantum computing tutorial",
            "quantum computing benefits",
            "python programming"
        ]
    }

    for original, keywords in test_cases.items():

        print("\n")
        print("=" * 80)
        print(
            f"ORIGINAL KEYWORD: {original}"
        )
        print("=" * 80)

        results = analyze_keywords(
            keywords,
            original
        )

        for item in results:

            print(
                f"{item['keyword']:<40}"
                f" | Final: {item['score']:>3}"
                f" | Semantic: "
                f"{item['semantic_score']:>6}"
                f" | Words: "
                f"{item['word_count']}"
            )