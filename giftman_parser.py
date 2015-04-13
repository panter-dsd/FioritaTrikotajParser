# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"


from html.parser import HTMLParser
import re

from abstract_parser import AbstractParser


class HtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self._tag_stack = []
        self._name = str()
        self._price = str()
        self._image_url = str()

    def name(self):
        return self._name

    def price(self):
        return self._price

    def image_url(self):
        return self._image_url

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append((tag, attrs))

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

        if current_tag == "span" and current_attrs == [("class", "price")]:
            self._price = data

        if current_tag == "meta" and ("property", "og:image") in current_attrs:
            self._image_url = current_attrs[1][1]

class GiftmanParser(AbstractParser):
    def __init__(self):
        super().__init__("http://www.giftman.ru/")

        self._html_parser = HtmlParser()

    def name(self):
        return "Giftman"

    def set_page_source(self, text: str):
        self._html_parser.feed(text)
        super().set_page_source(text)

    def extract_price(self) -> str:
        return self._html_parser.price()

    def extract_name(self) -> str:
        return re.sub("\s+", " ", self._html_parser.name()).strip()

    def extract_image_url(self) -> str:
        return self._html_parser.image_url()

