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

    def search_in_titles(self, list_soups):
        for soup in list_soups:
            title_article = soup.find('h2', class_='tm-title tm-title_h2').text
            set_words_title_article = set(title_article.split())
            if set_words_title_article & self.keywords:
                link_article = soup.find('a', class_='tm-title__link').get('href')
                self.articles.append(ArticleHabr(link=f"{self.link[0][:16]}{link_article}", features_output=self.features_output, session=self.session))
            if len(self.articles) >= self.numbers_articles:
                return True
        else:
            return False

    def find_objects(self, soup, common_feature):
        list_block_articles = soup.find_all(attrs=common_feature)
        return list_block_articles

    def get_request(self, *new_link):
        self.link = new_link

        for link in self.link:
            response = self.session.get(link, headers=self.headers)
            if response.status_code == 200:
                response = response.text
                soup = BeautifulSoup(response, 'lxml')

                list_block_articles = self.find_objects(soup, {"class": "tm-article-snippet tm-article-snippet"})
                if self.search_in_titles(list_block_articles):
                    break

            else:
                print(f"Ошибка: {response.status_code}")
        else:
            self.numbers_articles = len(self.articles)
            print(f"К сожалению, на сайте habr.com нашли только {self.numbers_articles} статей, содержащих ваши ключевые слова")

    def page_navigation(self, suffix, numbers_page):
        self.link = set([self.link + f"/{suffix}{number_page}/" for number_page in range(1, numbers_page)])

    def add_to_root_link(self, addition_link):
        self.link += addition_link
    
    def start_search(self):
        self.add_to_root_link('/ru/articles')
        self.page_navigation('page', 50)
        self.get_request(*self.link)

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

    with open('config.json', encoding="utf-8") as file:
        features_output = json.load(file)

    Articles = ArticlesHabrWithKeyword(features_output)
    Articles.start_search()
    Articles.parsing_all_articles_from_list()
    Articles.save_to_json(name_file='results.json')

if __name__ == '__main__':
    main()
