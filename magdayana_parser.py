# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from html.parser import HTMLParser
from urllib import request

import xlrd

from abstract_parser import AbstractParser


class HtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self._tag_stack = []
        self._name = str()
        self._image_url = str()
        self._size_string = str()

    def feed(self, data):
        self._image_url = str()
        super().feed(data)

    def name(self):
        return self._name

    def image_url(self):
        return self._image_url

    def size_string(self):
        return self._size_string

    def handle_starttag(self, tag, attrs):
        if (not self._image_url
                and tag == "a"
                and ("rel", "example_group") in attrs):
            self._image_url = attrs[1][1]

        self._tag_stack.append((tag, attrs))

    def handle_endtag(self, tag):
        if self._tag_stack[-1][0] == tag:
            self._tag_stack.pop()

    def handle_data(self, data):
        if not self._tag_stack:
            return

        current_tag = self._tag_stack[-1][0]

        if current_tag == "h1":
            self._name = data

        if current_tag == "li" and "Размер:" in data:
            self._size_string = data.split(":")[1]


class MagdayanaParser(AbstractParser):
    _price_url = "http://www.magdayana.ru/assets/files/price_magdayana.xls"
    _price_data = bytes()

    def __init__(self):
        super().__init__("http://www.magdayana.ru")

        self._html_parser = HtmlParser()

        self._prices = dict()

    def name(self):
        return "Magdayana"

    def set_page_source(self, text: str):
        if not self._price_data and self.__download_prices():
            self.__parse_prices()

        self._html_parser.feed(text)
        super().set_page_source(text)

    def extract_price(self) -> str:
        try:
            return self._prices[self.extract_name()]
        except KeyError:
            return 0.0

    def extract_name(self) -> str:
        return self._html_parser.name()

    def extract_image_url(self) -> str:
        url = self._html_parser.image_url()

        if url and not url.startswith(self.main_url()):
            url = self.main_url() + url

        return url

    def __try_parse_sizes_list(self, sizes_str: str) -> list:
        result = sizes_str.split(",")
        for size in result:
            if len(size) > 3:
                return sizes_str
        return result

    def extract_sizes(self) -> list:
        sizes_str = self._html_parser.size_string().strip()
        if "," in sizes_str:
            return self.__try_parse_sizes_list(sizes_str)
        return [sizes_str]

    def __download_prices(self) -> bool:
        with request.urlopen(self._price_url) as f:
            self._price_data = f.read()

        return self._price_data

    def __parse_prices(self):
        book = xlrd.open_workbook(file_contents=self._price_data)
        sheet = book.sheet_by_index(0)

        for row in range(sheet.nrows):
            self._prices[sheet.cell(row, 0).value] = sheet.cell(row, 9).value

