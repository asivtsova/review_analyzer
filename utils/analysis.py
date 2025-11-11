import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Инициализация NLTK
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
def get_tiktok_stopwords():
    """Стоп-слова для TikTok"""
    basic_stopwords = set(stopwords.words('english'))
    tiktok_specific = {'tiktok', 'app', 'update', 'video', 'videos',
                        'hello', 'hi', 'know', 'need', 'want', 'get',
                        'would', 'also', 'really', 'could', 'even', 'tik', 
                        'tok', 'people'}
    return basic_stopwords.union(tiktok_specific)

def get_word_frequencies(texts, top_n=20):
    """Подсчет частоты слов"""
    all_text = ' '.join(texts)
    words = word_tokenize(all_text)
    
    # Фильтрация стоп-слов
    stop_words = get_tiktok_stopwords()
    filtered_words = [word for word in words if word.lower() not in stop_words and len(word) > 2]
    
    word_freq = Counter(filtered_words)
    return dict(word_freq.most_common(top_n))

def create_wordcloud(text):
    """Создание облака слов"""
    stop_words = get_tiktok_stopwords()
    
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        stopwords=stop_words,
        max_words=100,
        colormap='viridis'
    ).generate(text)
    
    return wordcloud

def categorize_sentiment(score):
    """Категоризация отзыва по оценке"""
    if score <= 2:
        return 'negative'
    elif score >= 4:
        return 'positive'
    else:
        return 'neutral'

def analyze_sentiment_distribution(df):
    """Анализ распределения тональности"""
    if 'score' not in df.columns:
        return None
    
    df['sentiment'] = df['score'].apply(categorize_sentiment)
    sentiment_counts = df['sentiment'].value_counts()
    sentiment_stats = df.groupby('sentiment').agg({
        'score': 'mean',
        'thumbsUpCount': 'sum',
        'content': 'count'
    }).rename(columns={'content': 'count'})
    sentiment_stats['score'] = sentiment_stats['score'].round(2)
    
    return sentiment_counts, sentiment_stats