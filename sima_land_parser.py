# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from html.parser import HTMLParser

from abstract_parser import AbstractParser


class HtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self._tag_stack = []
        self._name = str()
        self._price = str()
        self._image_url = str()
        self._minimum_order_quantity = 0

    def name(self):
        return self._name

    def price(self):
        return self._price

    def image_url(self):
        return self._image_url

    def minimum_order_quantity(self):
        return self._minimum_order_quantity

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

        if (current_tag == "div") and (("class", "actual") in current_attrs):
            for attr in current_attrs:
                if attr[0] == "data-price-value":
                    self._price = attr[1]
                    break

        if current_tag == "meta" and ("itemprop", "image") in current_attrs:
            self._image_url = current_attrs[1][1]

        if current_tag == "span":
            if (current_attrs
                and current_attrs[0]
                and (current_attrs[0][0] == "data-cart-min")):
                self._minimum_order_quantity = int(data)


class SimaLandParser(AbstractParser):
    def __init__(self):
        super().__init__("https://www.sima-land.ru/")

        self._html_parser = HtmlParser()

    def set_page_source(self, text: str):
        self._html_parser.feed(text)
        super().set_page_source(text)

    def name(self):
        return "Sima-Land"

    def extract_price(self) -> str:
        return self._html_parser.price()

    def extract_name(self) -> str:
        return self._html_parser.name()

    def extract_minimum_order_quantity(self) -> int:
        return self._html_parser.minimum_order_quantity()

    def extract_main_image_url(self) -> str:
        return self._html_parser.image_url()