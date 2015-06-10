# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

import re
from html.parser import HTMLParser

from abstract_parser import AbstractParser


class HtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self._tag_stack = []
        self._name = str()
        self._price = str()
        self._image_url = str()
        self._sizes = []

    def name(self):
        return self._name

    def price(self):
        return self._price

    def image_url(self):
        return self._image_url

    def sizes(self):
        return self._sizes

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append((tag, attrs))

        if (tag == "img") and (("id", "image") in attrs):
            for attr in attrs:
                if attr[0] == "src":
                    self._image_url = attr[1]

    def handle_endtag(self, tag):
        if self._tag_stack[-1][0] == tag:
            self._tag_stack.pop()

    def handle_data(self, data):
        if not self._tag_stack:
            return

        current_tag = self._tag_stack[-1][0]
        current_attrs = self._tag_stack[-1][1]

        if current_tag == "h1":
            self._name = data
            self.__remove_number_from_name()

        if (current_tag == "div") and (
            ("class", "price") in current_attrs) and not self._price:
            self._price = self.__extract_price(data)

        if current_tag == "label":
            size = self.__try_extract_size(current_attrs, data)
            if size:
                self._sizes.append(size)

    def __remove_number_from_name(self):
        splitted_name = self._name.split(' ')
        if splitted_name:
            try:
                int(splitted_name[-1])
                self._name = " ".join(splitted_name[:-1]).strip()
            except (TypeError, ValueError):
                pass

    @staticmethod
    def __extract_price(data: str) -> str:
        price_re = re.compile("(\d+\.\d+)")
        match = price_re.search(data)
        return match.group(0) if match else str()

    @staticmethod
    def __try_extract_size(attrs, data):
        return data.strip() if attrs and (attrs[0][0] == "for") else str()


class StokMarketParser(AbstractParser):
    def __init__(self):
        super().__init__("http://stok-m.ru/")

        self._html_parser = HtmlParser()

    def set_page_source(self, text: str):
        self._html_parser = HtmlParser()
        self._html_parser.feed(text)
        super().set_page_source(text)

    def name(self):
        return "Stok Market"

    def extract_price(self) -> str:
        return self._html_parser.price()

    def extract_name(self) -> str:
        return self._html_parser.name()

    def extract_minimum_order_quantity(self) -> int:
        return self._html_parser.minimum_order_quantity()

    def extract_main_image_url(self) -> str:
        return self._html_parser.image_url()

    def extract_sizes(self) -> list:
        return self._html_parser.sizes()
