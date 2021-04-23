import string
from collections import Counter

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def sentiment_analyse(sentiment_text):

    lower_case = sentiment_text.lower()
    cleaned_text = lower_case.translate(
        str.maketrans('', '', string.punctuation))
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    sentimentScore = score['pos'] - score['neg']
    if -1 <= sentimentScore < -0.5:
        return "1"
    elif -0.5 <= sentimentScore < 0:
        if(score['neu'] > 0.7):
            return "3"
        else:
            return "2"
    elif sentimentScore == 0:
        return "3"
    elif 0 < sentimentScore <= 0.6:
        if(score['neu'] > 0.7):
            return "3"
        else:
            return "4"
    elif 0.6 < sentimentScore <= 1:
        return "5"
    else:
        return None
