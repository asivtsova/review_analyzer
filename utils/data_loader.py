# utils/data_loader.py
import pandas as pd
import re
import logging

def load_data(file_path='data/tiktok_reviews.csv'):
    """Загрузка и предобработка данных"""
    df = pd.read_csv(file_path)
    
    logging.info("Загружен файл")
    
    # Удаляем ненужные колонки
    columns_to_drop = ['userName', 'at', 'reviewId', 'reviewCreatedVersion', 'appVersion']
    existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df = df.drop(columns=existing_columns_to_drop)
    
    # Очистка текста
    if 'content' in df.columns:
        df['content'] = df['content'].astype(str).apply(clean_text)
    
    return df

def clean_text(text):
    """Очистка текста от специальных символов"""
    text = re.sub(r'[^\w\s]', '', text)  # Удаляем пунктуацию
    text = re.sub(r'\d+', '', text)      # Удаляем цифры
    text = text.lower().strip()          # Приводим к нижнему регистру
    return text

def get_basic_stats(df):
    """Базовая статистика"""
    stats = {
        'total_reviews': len(df),
        'columns': df.columns.tolist(),
        'reviews_with_text': df['content'].str.len().gt(0).sum() if 'content' in df.columns else 0
    }
    
    logging.info("Очищен текст от спец.символов")

    return stats