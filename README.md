# Анализ отзывов TikTok

Веб-приложение для анализа текстовых отзывов на приложение TikTok из Google Play Store. Проект реализован в рамках студенческой работы по курсу "Разработка программных средств".

## Функциональность

- **Статистический анализ** - распределение оценок, базовая статистика
- **Визуализация текста** - облако слов из отзывов  
- **Анализ частот** - топ-15 самых употребляемых слов
- **Анализ тональности** - категоризация отзывов на положительные, нейтральные и отрицательные
- **Фильтрация** - интерактивные фильтры по оценкам

## Структура проекта

- `app.py` - Главная страница
- `pages/data_analyze.py` - Страница с аналитикой
- `utils/data_loader.py` - Загрузка и обработка данных
- `utils/analysis.py` - Функции анализа
- `data/tiktok_reviews.csv` - Данные отзывов (не включено в репозиторий)
- `docker-compose.yml` - Докер-файл
- `requirements.txt` - Зависимости
- `README.md` - Документация
- `tests/test_analysis.py` - Тесты функций анализа
- `tests/test_dataloader.py` - Тесты загрузки и обработки данных


## Данные

Проект использует датасет с отзывами на TikTok из Google Play Store:

- **Объем:** 119,733 отзывов
- **Поля данных:**
  - `content` - текст отзыва
  - `score` - оценка (1-5 звезд)
  - `thumbsUpCount` - количество лайков

  ## Установка и запуск

  ### Предварительные требования

- Python 3.8+
- pip (менеджер пакетов Python)

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/asivtsova/review_analyzer
cd review_analyzer

2. Создайте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Установите зависимости:
pip install -r requirements.txt

4. Поместите файл с данными в папку data/tiktok_reviews.csv

5. Запустите приложение:
streamlit run app.py

### Запуск c Docker

1. Клонируйте репозиторий:
```bash
git clone https://github.com/asivtsova/review_analyzer
cd review_analyzer

2. Поместите файл с данными в папку data/
3. Запустите с Docker Compose
docker-compose up -d

### Запуск тестов

```bash
# Установите зависимости для тестирования
pip install pytest

# Запустите все тесты
pytest