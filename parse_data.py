import requests
import urllib
import pandas as pd
from requests_html import HTMLSession, HTMLResponse, HTML
from tqdm import tqdm
from typing import List, Union
import os
from pathlib import PurePath
from bs4 import BeautifulSoup


class TextParser:
    def __init__(self, queries: List[str]):
        self.list_queries = queries
        self.__from_queries_to_files()

    def __get_source(self, url: str) -> HTMLResponse:
        """
        Return the source code for the provided URL
        """
        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)

    def __scrape_google(self, query: str) -> List[str]:
        """
        Extract links from query in google
        """
        query = urllib.parse.quote_plus(query)
        response = self.__get_source("https://www.google.ru/search?q=" + query)

        links = list(response.html.absolute_links)
        bad_domains = [
                    'translate.google',
                    'youtube',
                    'google.',
                    'webcache.googleusercontent'
                    ]

        for url in links[:]:
            if any([x in url for x in bad_domains]):
                links.remove(url)
        return list(set(links))

    def __extract_text_from_url(self, url: str) -> str:
        """
        Extract text from webpage via url
        """
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def __save_text_to_file(
        self,
        text: str,
        output_path: Union[str, PurePath]
    ) -> None:
        """
        Save text to txt file
        """
        text_file = open(output_path, "w")
        text_file.write(text)
        text_file.close()

    def __from_queries_to_files(self) -> None:
        """
        Main method to form folders of files for each query
        """
        for query in tqdm(self.list_queries):
            if not os.path.exists(query):
                os.mkdir(query)
            
            all_urls = self.__scrape_google(query)
            for i, url in enumerate(all_urls):
                try:
                    text_from_url = self.__extract_text_from_url(url)
                except:
                    print('\nError: ' + url)
                    continue
                
                path_for_file = PurePath(query, f'{i}.txt')
                self.__save_text_to_file(text_from_url, path_for_file)
