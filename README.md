# Parcer of Habr #

## Установка ##
1. Создание виртуального окружения
   ```python3 -m venv venv```
2. Активация виртуального окружения
   ```venv/Scripts/activate```
3. Установка зависимостей
   ```pip3 install -r requirements.txt```
## Инструкция по работе ##
Запрос на поиск осуществляется через файл конфигурации config.json  
В нем:
- "line_with_keywords" - строка, содержащая ключевые слова, по которым будет происходить поиск
- "numbers_articles" - количество статей, содержащих ключевые слова
- Далее соответсвующие ключам значения (true/false) определяют, какую информацию парсить с каждой статьи
- 2 аргумент значения, соответствующего ключу "all_images", определяет максимальное количество изображений, которое можно спарсить с одной статьи
- 2 аргумент значения, соответствующего ключу "text_on_page", определяет максимальноу количество символов текста, которое можно спарсить с одной статьи


При запуске файла ArticlesHabr.py результат сохраняется в файле results.json в виде списка словарей  
При запуске файла ArticleHabr.py результат сохраняется в файле result_one_article.json в виде словаря  
Изображения сохраняются в папке images, в которой создаются папки, названия которых в некоторой степени соответствуют названию статьи
