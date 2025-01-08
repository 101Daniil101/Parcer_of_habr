import requests
from bs4 import BeautifulSoup
import json
from BaseParser import BaseParser
from ArticleHabr import ArticleHabr

class ArticlesHabrWithKeyword(BaseParser):
    def __init__(self, features_output):
        super().__init__('https://habr.com')
        self.keywords = set(features_output['line_with_keywords'].split())
        self.articles = list()
        self.numbers_articles = features_output['numbers_articles']
        self.features_output = features_output

    def _check_article(self, block_article):
        # Улучшить поиск
        title_article = block_article.find('h2', class_='tm-title tm-title_h2').text
        set_words_title_article = set(title_article.split())
        if set_words_title_article & self.keywords:
            return True
        else:
            return False
        
    def search_in_titles(self):
        ...

    def get_request(self):
        number_page = 0
        numbers_articles = 0

        while numbers_articles < self.numbers_articles:
            number_page += 1

            if number_page < 50:
                response = self.session.get(f"{self.link}/ru/articles/page{number_page}/", headers=self.headers)
                if response.status_code == 200:
                    response = response.text
                    soup = BeautifulSoup(response, 'lxml')
                    list_block_articles = soup.find_all('div', class_='tm-article-snippet tm-article-snippet')

                    for block_article in list_block_articles:
                        if numbers_articles < self.numbers_articles:

                            if self._check_article(block_article):
                                link_article = block_article.find('a', class_='tm-title__link').get('href')
                                self.articles.append(ArticleHabr(link=f"{self.link}{link_article}", features_output=self.features_output, session=self.session))
                                numbers_articles += 1
                        else:
                            break
                    else:
                        continue
                    break
            else:
                self.numbers_articles = numbers_articles
                print(f"К сожалению, на сайте habr.com нашли только {numbers_articles} статей, содержащих ваши ключевые слова")

    def parsing_all_articles_from_list(self):
        for article in self.articles:
            article.get_request()
        
    def save_to_json(self, name_file):
        result_data = list()

        for article in self.articles:
            data_article = dict()

            data_article['link'] = article.link
            data_article['name_author'] = article.name_author
            data_article['time_creation'] = article.time_creation
            data_article['title_article'] = article.title_article
            data_article['numbers_views'] = article.numbers_views
            data_article['images_title'] = article.all_images
            data_article['text_on_page'] = article.text_on_page
        
            result_data.append(data_article)

        with open(name_file, 'w', encoding='utf=8') as file:
            json.dump(result_data, file, ensure_ascii=False)


def main():
    #Добавь поиск по другим элементам

    with open('config.json', encoding="utf-8") as file:
        features_output = json.load(file)

    Articles = ArticlesHabrWithKeyword(features_output)
    Articles.get_request()
    Articles.parsing_all_articles_from_list()
    Articles.save_to_json(name_file='result.json')

if __name__ == '__main__':
    main()
