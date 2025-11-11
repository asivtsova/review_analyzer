import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import logging

# Импортируем все из наших модулей
from utils.data_loader import load_data, clean_text
from utils.analysis import *

def main():
    st.title("📈 Анализ данных")
    
    # Загрузка данных
    try:
        df = load_data()
        logging.info("Данные успешно загружены")
        
        if df is None:
            st.error("Не удалось загрузить данные")
            return
            
        # Основная информация
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Всего отзывов", f"{len(df):,}")
        with col2:
            if 'score' in df.columns:
                avg_score = df['score'].mean()
                st.metric("Средняя оценка", f"{avg_score:.2f}")
        with col3:
            if 'thumbsUpCount' in df.columns:
                total_likes = df['thumbsUpCount'].sum()
                st.metric("Всего лайков", f"{total_likes:,}")
        
        # Боковая панель с фильтрами
        st.sidebar.header("Фильтры")
        
        if 'score' in df.columns:
            scores = st.sidebar.multiselect(
                "Оценки:",
                options=sorted(df['score'].unique()),
                default=sorted(df['score'].unique())
            )
            df = df[df['score'].isin(scores)]
        
        # Вкладки для разных анализов
        tab1, tab2, tab3, tab4 = st.tabs(["Статистика", "Облако слов", "Частота слов", "Анализ тональности"])
        
        with tab1:
            st.subheader("Распределение оценок")
            if 'score' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    score_counts = df['score'].value_counts().sort_index()
                    fig_bar = px.bar(score_counts, x=score_counts.index, y=score_counts.values,
                                    labels={'x': 'Оценка', 'y': 'Количество'},
                                    title="Количество отзывов по оценкам")
                    st.plotly_chart(fig_bar)
                
                with col2:
                    fig_pie = px.pie(values=score_counts.values, names=score_counts.index,
                                   title="Распределение оценок (%)")
                    st.plotly_chart(fig_pie)
                    
                # Топ отзывов по лайкам
                if 'thumbsUpCount' in df.columns:
                    st.subheader("Топ отзывов по лайкам")
                    top_liked = df.nlargest(5, 'thumbsUpCount')[['content', 'score', 'thumbsUpCount']]
                    for i, (_, row) in enumerate(top_liked.iterrows(), 1):
                        with st.expander(f"Отзыв #{i} - {row['thumbsUpCount']} лайков (оценка: {row['score']})"):
                            st.write(row['content'])
        
        with tab2:
            st.subheader("Облако слов")
            df['cleaned_content'] = df['content'].apply(clean_text)
            all_text = ' '.join(df['cleaned_content'].dropna())
            
            if all_text.strip():
                wordcloud = create_wordcloud(all_text)
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                ax.set_title('Облако слов из отзывов', fontsize=16)
                st.pyplot(fig)
        
        with tab3:
            st.subheader("Самые частые слова")
            df['cleaned_content'] = df['content'].apply(clean_text)
            texts_with_content = df[df['cleaned_content'].str.len() > 0]['cleaned_content']
            
            if len(texts_with_content) > 0:
                word_freq = get_word_frequencies(texts_with_content, top_n=15)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(x=list(word_freq.keys()), y=list(word_freq.values()),
                                labels={'x': 'Слова', 'y': 'Частота'},
                                title="Топ-15 самых частых слов")
                    st.plotly_chart(fig)
                
                with col2:
                    st.write("**Таблица частот:**")
                    freq_df = pd.DataFrame(list(word_freq.items()), columns=['Слово', 'Частота'])
                    st.dataframe(freq_df, use_container_width=True)
        
        with tab4:
            st.subheader("Анализ тональности отзывов")
            if 'score' in df.columns:
                sentiment_counts, sentiment_stats = analyze_sentiment_distribution(df)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_pie = px.pie(values=sentiment_counts.values, 
                                    names=sentiment_counts.index,
                                    title="Распределение тональности",
                                    color=sentiment_counts.index,
                                    color_discrete_map={'positive': 'green', 'negative': 'red', 'neutral': 'gray'})
                    st.plotly_chart(fig_pie)
                
                with col2:
                    st.write("**Статистика по категориям:**")
                    st.dataframe(sentiment_stats)
            
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")

    
    logging.info("Все страницы успешно загружены")

if __name__ == "__main__":
    main()