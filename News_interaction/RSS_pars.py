# Importing inbuilt modules
import re
import json
import logging
from os import path
from itertools import zip_longest
from collections import deque


# Importing external modules
import aiohttp


# Importing custom modules
import config


# Class for parsing news with RSS channel
class RSS_pars():
    def __init__(self):
        self.news_agregators = [(news_agregator[0].replace(' ', '_').lower(), news_agregator[1]) \
                               for news_agregator in config.news_agregators] # List of tuples that contains: [0] - news aggregator name, [1] - URL on news aggregator
        
        self.old_news = {} # Creating dict-cache for collection of old news

        # Headers that provide requests to aggregators' sites without blocking 
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

        # Importing old news from the backup file if something gets wrong with the program or creating a new deque if the backup file doesn't exist
        for news_agregator in self.news_agregators:
            try:
                with open(path.join('.', 'temp', f'{news_agregator[0]}_old_news.json'), 'r', encoding='utf-8') as old_news_file:
                    self.old_news[news_agregator[0]] = json.load(old_news_file)
            # If the file does not exist, create a clear deque
            except FileNotFoundError:
                self.old_news[news_agregator[0]] = deque([], 10)    
            except Exception as e:
                logging.critical(f"Something went wrong with unloading data from temp files.\n\n{e}")
            # If the file exists, create a deque and add the cache news
            else:   
                self.old_news[news_agregator[0]] = deque(self.old_news[news_agregator[0]], 10)
                

    '''---------------NEWS PARS FUNCTION---------------'''


    # Parsing news resource and yielding [image, title, link, description]
    async def news_pars(self, url: str) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    news_response = await response.text()   # Formating response to text format

                    news_title = await self.get_title(news_response)
                    news_link = await self.get_link(news_response)
                    news_description = await self.get_description(news_response)
                    preview_image = await self.get_preview_image(news_link)

                    news_iter = zip_longest(preview_image, news_title, news_link, news_description, fillvalue='')  # Combining images, titles, links and descriptions

                    for news in news_iter:
                        yield list(news)
                else:
                    logging.critical(f"Can't get news from {url} with code {response.status}")

    
    '''---------------CHECKING FUNCTION ON NEWS EXISTING IN CACHE---------------'''


    # Checking news on existing in old news
    async def is_news_in_old_news(self, news: list, news_agregator: str) -> bool:
        if news not in self.old_news[news_agregator]:
            self.old_news[news_agregator].append(news)
            return False
        return True
    

    '''---------------BACKUP FILE OF CACHE NEWS CREATE FUNCTION---------------'''


    # Recreating backup file with old news
    async def recreate_old_news_backup_file(self, news_agregator: str):
        try:
            with open(fr"./temp/{news_agregator}_old_news.json", 'w') as old_news_file_back:
                json.dump(list(self.old_news[news_agregator]), old_news_file_back)
        except Exception as e:
            logging.critical(f"Can't recreate backup file with old news.\n\n{e}")


    '''---------------TITLE FUNCTION---------------'''


    # Getting titles of news from RSS HTTP response
    async def get_title(self, news_response: str) -> list:
        titles = []
        for index, title in enumerate(re.finditer(r"<item>.*?<title>(?P<start>&lt;p&gt;|<!\[CDATA\[)?(?P<title>.*?)(?P<end>&lt;/p&gt;|\]\]>)?</title>", \
                                                  news_response, re.DOTALL)):
            titles.append(title.group('title'))

            # Function only gets first 3 news and doesn't read others for fast work
            if index == 2:
                break
        return titles
    

    '''---------------LINK FUNCTION---------------'''


    # Getting links of news from RSS HTTP response
    async def get_link(self, news_response: str) -> list:
        links = []
        for index, link in enumerate(re.finditer(r"<item>.*?<link>(?P<start>&lt;p&gt;|<!\[CDATA\[)?(?P<link>http.+?)(?P<end>&lt;/p&gt;|\]\]>)?</link>", \
                                                  news_response, re.DOTALL)):
            links.append(link.group('link'))

            # Function only gets first 3 news and doesn't read others for fast work
            if index == 2:
                break
        return links
    

    '''---------------DESCRIPTION FUNCTION---------------'''


    # Getting a description of news from RSS HTTP response
    async def get_description(self, news_response: str) -> list:
        descriptions = []
        for index, description in enumerate(re.finditer(r"<item>.*?<description>(?P<start>&lt;p&gt;|<!\[CDATA\[)?(?P<description>.*?)(?P<end>&lt;/p&gt;|\]\]>)?</description>", \
                                                  news_response, re.DOTALL)):
            descriptions.append(description.group('description'))

            # Function only gets first 3 news and doesn't read others for fast work
            if index == 2:
                break
        return descriptions
    

    '''---------------PREVIEW IMAGE FUNCTION---------------'''


    # Getting a preview image with an open graph from a URL link
    async def get_preview_image(self, urls: tuple):
        preview_images = [] # Initializating a clear list of possible images of news
        async with aiohttp.ClientSession() as session:
            for url in urls:
                # Getting response from new's link
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        url_response = await response.text(encoding='utf-8')
                        image_url = re.search(r'<meta.*?property="og:image" content="(http.*?)".*?>', url_response, re.DOTALL)

                        # If there is an image in opengraph, so we append the image to the list
                        if image_url:
                            preview_images.append(image_url.group(1))
                        else:
                            preview_images.append('')
                    else:
                        preview_images.append('')
        return preview_images
