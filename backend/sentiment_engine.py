from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyze sentiment of given text.
    Returns Positive, Negative, or Neutral.
    """

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "text": text,
        "sentiment": sentiment,
        "polarity": round(polarity, 2)
    }


if __name__ == "__main__":

    test_texts = [
        "This AI tool is amazing and very useful.",
        "I hate this complicated software.",
        "AI tools are available online."
    ]

    for text in test_texts:

        result = analyze_sentiment(text)

        print("\nText:", result["text"])
        print("Sentiment:", result["sentiment"])
        print("Polarity:", result["polarity"])