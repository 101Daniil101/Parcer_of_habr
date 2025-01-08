import requests
from bs4 import BeautifulSoup
import abc
import fake_useragent

class BaseParser(abc.ABC):

    user = fake_useragent.UserAgent().random

    def __init__(self, link):
        self.headers = {'user-agent': self.user}
        self.link = link
        self.session = requests.Session()

    def get_title_website(self):
        response = self.session.get(self.link, headers=self.headers).text
        soup = BeautifulSoup(response, 'lxml')
        title_website = soup.find('head').find('title').text
        return title_website

    def get_html_code(self):
        response = self.session.get(self.link, headers=self.headers).text
        soup = BeautifulSoup(response, 'lxml')
        block_html_code = soup['html']
        return block_html_code

    def check_status_code_200(self):
        response = self.session.get(self.link)
        if response.status_code == 200:
            return True
        else:
            return False

    @abc.abstractmethod
    def get_request(self): pass


    