import re


# ==========================================================
# INPUT CLEANING
# ==========================================================

def clean_keyword(keyword):
    """
    User ke input ko clean karta hai.
    Extra spaces aur unnecessary punctuation remove karta hai.
    """

    if not isinstance(keyword, str):
        raise ValueError("Keyword must be a string.")

    keyword = keyword.strip()

    # Multiple spaces ko single space mein convert karo
    keyword = re.sub(r"\s+", " ", keyword)

    return keyword


# ==========================================================
# NORMALIZE KEYWORD
# ==========================================================

def normalize_keyword(keyword):
    """
    Comparison ke liye keyword ko normalize karta hai.
    """

    text = keyword.lower().strip()

    # Question mark etc. remove
    text = re.sub(r"[^\w\s]", "", text)

    # Multiple spaces remove
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# QUESTION DETECTION
# ==========================================================

def is_question(keyword):

    text = keyword.lower().strip()

    question_words = [
        "who ",
        "what ",
        "when ",
        "where ",
        "why ",
        "how ",
        "which ",
        "can ",
        "could ",
        "should ",
        "would ",
        "is ",
        "are ",
        "am ",
        "do ",
        "does ",
        "did ",
        "will ",
        "have ",
        "has "
    ]

    return (
        text.endswith("?")
        or any(
            text.startswith(word)
            for word in question_words
        )
    )


# ==========================================================
# QUESTION KEYWORD GENERATOR
# ==========================================================

def generate_question_keywords(keyword):

    clean = normalize_keyword(keyword)

    suggestions = [
        keyword
    ]


    # ------------------------------------------------------
    # ARE YOU...
    # ------------------------------------------------------

    if clean.startswith("are you "):

        subject = clean[8:].strip()

        if subject:

            suggestions.extend([
                f"why are you {subject}",
                f"how to be {subject}",
                f"what makes you {subject}",
                f"ways to be {subject}",
                f"benefits of being {subject}",
                f"{subject} quotes",
                f"{subject} thoughts",
                f"{subject} life"
            ])

            return suggestions


    # ------------------------------------------------------
    # WHAT IS...
    # ------------------------------------------------------

    if clean.startswith("what is "):

        topic = clean[8:].strip()

        if topic:

            suggestions.extend([
                f"{topic} meaning",
                f"{topic} definition",
                f"{topic} explained",
                f"how does {topic} work",
                f"why is {topic} important",
                f"{topic} examples",
                f"{topic} benefits"
            ])

            return suggestions


    # ------------------------------------------------------
    # HOW TO...
    # ------------------------------------------------------

    if clean.startswith("how to "):

        topic = clean[7:].strip()

        if topic:

            suggestions.extend([
                f"how to {topic} for beginners",
                f"best way to {topic}",
                f"easy way to {topic}",
                f"steps to {topic}",
                f"{topic} tutorial",
                f"{topic} guide",
                f"{topic} tips"
            ])

            return suggestions


    # ------------------------------------------------------
    # WHY...
    # ------------------------------------------------------

    if clean.startswith("why "):

        topic = clean[4:].strip()

        if topic:

            suggestions.extend([
                f"why {topic}",
                f"reasons for {topic}",
                f"importance of {topic}",
                f"benefits of {topic}",
                f"advantages of {topic}",
                f"disadvantages of {topic}",
                f"{topic} explained"
            ])

            return suggestions


    # ------------------------------------------------------
    # GENERIC QUESTION
    # ------------------------------------------------------

    suggestions.extend([
        f"{keyword} meaning",
        f"{keyword} explained",
        f"{keyword} examples",
        f"{keyword} information",
        f"{keyword} guide"
    ])

    return suggestions


# ==========================================================
# SPECIAL TOPIC KNOWLEDGE
# ==========================================================

TOPIC_PATTERNS = {

    "python": [
        "python programming",
        "learn python",
        "python tutorial",
        "python for beginners",
        "python projects",
        "python examples",
        "python course",
        "python applications",
        "python interview questions"
    ],

    "java": [
        "java programming",
        "learn java",
        "java tutorial",
        "java for beginners",
        "java projects",
        "java examples",
        "java course",
        "java applications",
        "java interview questions"
    ],

    "javascript": [
        "javascript programming",
        "learn javascript",
        "javascript tutorial",
        "javascript for beginners",
        "javascript projects",
        "javascript examples",
        "javascript course",
        "javascript applications"
    ],

    "cyber security": [
        "cyber security courses",
        "cyber security tools",
        "cyber security jobs",
        "cyber security certification",
        "cyber security for beginners",
        "cyber security projects",
        "cyber security tutorial",
        "cyber security skills",
        "cyber security career"
    ],

    "artificial intelligence": [
        "artificial intelligence tools",
        "artificial intelligence courses",
        "artificial intelligence projects",
        "artificial intelligence for beginners",
        "learn artificial intelligence",
        "artificial intelligence applications",
        "artificial intelligence examples",
        "artificial intelligence tutorial"
    ],

    "ai": [
        "AI tools",
        "AI courses",
        "AI projects",
        "AI for beginners",
        "learn AI",
        "AI applications",
        "AI examples",
        "AI tutorial"
    ],

    "ai tools": [
        "best AI tools",
        "free AI tools",
        "AI tools for students",
        "AI tools for productivity",
        "AI tools for business",
        "AI tools for beginners",
        "latest AI tools",
        "AI tools comparison"
    ],

    "digital marketing": [
        "digital marketing courses",
        "digital marketing tools",
        "digital marketing strategy",
        "digital marketing for beginners",
        "learn digital marketing",
        "digital marketing jobs",
        "digital marketing skills",
        "digital marketing trends"
    ],

    "beautiful": [
        "beautiful quotes",
        "beautiful images",
        "beautiful captions",
        "beautiful meaning",
        "beautiful synonyms",
        "beautiful wallpaper",
        "beautiful ideas",
        "beautiful places",
        "beautiful words"
    ],

    "happy": [
        "happy quotes",
        "happy thoughts",
        "happy life",
        "happy moments",
        "how to be happy",
        "ways to be happy",
        "happy captions",
        "happy mindset",
        "happiness tips"
    ],

    "love": [
        "love quotes",
        "love captions",
        "love messages",
        "love songs",
        "love stories",
        "love poems",
        "love meaning",
        "romantic ideas",
        "relationship advice"
    ],

    "fitness": [
        "fitness tips",
        "fitness exercises",
        "fitness for beginners",
        "fitness plan",
        "home fitness",
        "fitness workout",
        "fitness diet",
        "fitness goals",
        "fitness training"
    ],

    "business": [
        "business ideas",
        "business strategy",
        "business plan",
        "small business ideas",
        "online business",
        "business tips",
        "business growth",
        "business management"
    ]
}


# ==========================================================
# GENERIC TOPIC GENERATOR
# ==========================================================

def generate_generic_keywords(keyword):

    suggestions = [
        keyword,

        f"{keyword} meaning",

        f"{keyword} definition",

        f"{keyword} examples",

        f"{keyword} benefits",

        f"{keyword} uses",

        f"{keyword} types",

        f"{keyword} guide",

        f"{keyword} tips",

        f"{keyword} ideas",

        f"{keyword} for beginners",

        f"learn {keyword}",

        f"{keyword} tutorial",

        f"{keyword} applications",

        f"{keyword} explained"
    ]

    return suggestions


# ==========================================================
# NORMAL TOPIC GENERATOR
# ==========================================================

def generate_topic_keywords(keyword):

    clean = normalize_keyword(keyword)


    # Exact known topic
    if clean in TOPIC_PATTERNS:

        return [
            keyword
        ] + TOPIC_PATTERNS[clean]


    # ------------------------------------------------------
    # Partial known topic matching
    # ------------------------------------------------------

    for topic, suggestions in TOPIC_PATTERNS.items():

        if topic in clean or clean in topic:

            return [
                keyword
            ] + suggestions


    # ------------------------------------------------------
    # Unknown topic
    # ------------------------------------------------------

    return generate_generic_keywords(
        keyword
    )


# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

def remove_duplicates(suggestions):

    unique = []

    seen = set()


    for suggestion in suggestions:

        suggestion = suggestion.strip()

        if not suggestion:
            continue


        key = suggestion.lower()


        if key not in seen:

            seen.add(key)

            unique.append(
                suggestion
            )


    return unique


# ==========================================================
# MAIN INTELLIGENT KEYWORD ENGINE
# ==========================================================

def generate_keywords(keyword):

    keyword = clean_keyword(keyword)


    if not keyword:

        return []


    # ------------------------------------------------------
    # QUESTION
    # ------------------------------------------------------

    if is_question(keyword):

        suggestions = (
            generate_question_keywords(
                keyword
            )
        )


    # ------------------------------------------------------
    # NORMAL TOPIC
    # ------------------------------------------------------

    else:

        suggestions = (
            generate_topic_keywords(
                keyword
            )
        )


    # Remove duplicates
    suggestions = remove_duplicates(
        suggestions
    )


    # Maximum 12 suggestions
    return suggestions[:12]


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    test_keywords = [

        "python",

        "quantum computing",

        "cyber security",

        "beautiful",

        "are you happy?",

        "best laptop for students"

    ]


    for keyword in test_keywords:

        print("\n" + "=" * 60)

        print(
            f"INPUT: {keyword}"
        )

        print("=" * 60)


        results = generate_keywords(
            keyword
        )


        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"{index}. {result}"
            )