import json
import requests
from bs4 import BeautifulSoup
import os
from BaseParser import BaseParser

class ArticleHabr(BaseParser):

    def __init__(self, link, features_output, session=requests.Session()):
        super().__init__(link)
        self.session = session
        self.name_author = features_output['name_author']
        self.time_creation = features_output['time_creation']
        self.title_article = features_output['title_article']
        self.numbers_views = features_output['numbers_views']
        self.all_images = features_output['all_images']
        self.text_on_page = features_output['text_on_page']

    def _get_author(self, soup):
        block_author = soup.find('div', class_='tm-article-snippet__meta-container')
        name_author = block_author.find('a', class_='tm-user-info__username').text
        return name_author

    def _get_time_creation(self, soup):
        block_time_creation = soup.find('div', class_='tm-article-snippet__meta-container')
        time_creation = block_time_creation.find('time').get('title')
        return time_creation

    def _get_title(self, soup):
        block_title = soup.find('h1', class_='tm-title tm-title_h1')
        title = block_title.find('span').text
        return title

    def _get_numbers_views(self, soup):
        block_number_views = soup.find('div', class_='tm-article-snippet__stats')
        number_views = block_number_views.find('span', class_='tm-icon-counter__value').text
        return number_views

    def _get_images(self, soup, numbers_images):
        data = list()
        number_of_image = 1
        all_images = soup.find_all('img')

        try: os.mkdir('images')
        except FileExistsError: pass

        name_folder = '_'.join(self.title_article.split())
        try: os.mkdir(f'images/{name_folder}')
        except FileExistsError: pass
        except Exception: 
            try:
                name_folder = name_folder[:5]
                os.mkdir(f'images/{name_folder[:5]}')
            except: pass

        for image in all_images:
            if number_of_image < numbers_images:
                dowland_link = image.get('src')

                if (image_title := image.get('title')) != None:
                    name_jpg_file = image_title
                else:
                    name_jpg_file = str(number_of_image)

                response_dowland = self.session.get(dowland_link, headers=self.headers) #!!!!!!!!!!!!!

                if response_dowland.status_code == 200:
                    response_dowland = response_dowland.content
                    data.append(name_jpg_file)
                
                try:
                    with open(f'images/{name_folder}/{name_jpg_file}.jpg', 'wb') as file:
                        file.write(response_dowland)
                except:
                    with open(f'images/{name_folder}/{number_of_image}.jpg', 'wb') as file:
                        file.write(response_dowland)

                number_of_image += 1
            else:
                break

        return data

    def _get_text(self, soup, numbers_symbols):
        # Доработать функцию вывода текста

        block_text = soup.find('div', xmlns='http://www.w3.org/1999/xhtml')
        text = block_text.get_text()
        return text[:numbers_symbols]
    
    def get_request(self):
        response = self.session.get(self.link, headers=self.headers)
        if response.status_code == 200:
            response = response.text
            soup = BeautifulSoup(response, 'lxml')
    
            article = soup.find('article', class_ = 'tm-article-presenter__content tm-article-presenter__content_narrow')
            article_header = article.find('div', class_='tm-article-presenter__header')
            article_body = article.find('div', class_='tm-article-body')

            self.name_author = self._get_author(article_header) if self.name_author else None
            self.time_creation = self._get_time_creation(article_header) if self.time_creation else None
            self.title_article = self._get_title(article_header) if self.title_article else None
            self.numbers_views = self._get_numbers_views(article_header) if self.numbers_views else None
            self.all_images = self._get_images(article_body, self.all_images[1]) if self.all_images[0] else None
            self.text_on_page = self._get_text(article_body, self.text_on_page[1]) if self.text_on_page[0] else None


def main():
    link = input("Введите сслыку на статью: ")

    with open('config.json') as file:
        features_output = json.load(file)

    article = ArticleHabr(link, features_output)
    article.get_request()

    data_article = dict()
    data_article['link'] = article.link
    data_article['name_author'] = article.name_author
    data_article['time_creation'] = article.time_creation
    data_article['title_article'] = article.title_article
    data_article['numbers_views'] = article.numbers_views
    data_article['images_title'] = article.all_images
    data_article['text_on_page'] = article.text_on_page

    with open('result_one_article.json', 'w', encoding="utf-8") as file:
        json.dump(data_article, file, ensure_ascii=False)

if __name__ == '__main__':
    main()

    