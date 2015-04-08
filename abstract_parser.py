# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'


class AbstractParser(object):
    def __init__(self, main_url: str):
        super().__init__()

        self._main_url = main_url
        self._page_url = str()
        self._page_source = str()

    def name(self):
        return str()

    def can_parse(self, url: str) -> bool:
        return self._main_url in url

    def main_url(self):
        return self._main_url

    def page_url(self) -> str:
        return self._page_url

    def set_page_url(self, url: str):
        self._page_url = url

    def page_source(self) -> str:
        return self._page_source

    def set_page_source(self, text: str):
        self._page_source = text

        self._page_source = self._page_source.replace("&quot;", "\"").replace(
            "&nbsp;", " ")

    def extract_name(self) -> str:
        pass

    def extract_description(self) -> str:
        pass

    def extract_colors(self) -> list:
        pass

    def extract_sizes(self) -> list:
        pass

    def extract_price(self) -> str:
        pass

    def extract_image_url(self) -> str:
        pass

    def extract_minimum_order_quantity(self) -> int:
        return 1
