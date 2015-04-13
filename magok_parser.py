# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

import re

from abstract_parser import AbstractParser


class MagokParser(AbstractParser):
    def __init__(self):
        super().__init__("http://magok.ru")

    def name(self):
        return "MAG"

    def extract_sizes(self) -> list:
        return super().extract_sizes()

    def _extract_table(self) -> str:
        start_str = "<table class=\"goods_list\">"
        end_str = "</table>"

        try:
            start_index = self.page_source().index(start_str)
            end_index = self.page_source().index(end_str, start_index)
        except ValueError:
            return str()

        return self.page_source()[start_index:end_index]

    def extract_price(self) -> str:
        table_content = self._extract_table()

        prices = re.findall("(\d+,?\d*) руб", table_content)
        return prices[0] if prices else str()

    def extract_name(self) -> str:
        start_str = "<h1 itemprop=\"name\">"
        end_str = "</h1>"

        try:
            start_index = self.page_source().index(start_str)
            start_index += len(start_str)
            end_index = self.page_source().index(end_str, start_index)
        except ValueError:
            return str()

        result = self.page_source()[start_index:end_index]

        while "  " in result:
            result = result.replace("  ", " ")

        return result


    def extract_image_url(self) -> str:
        url_re = re.compile("href=\"(.*)\" class=\"highslide\"")
        result = url_re.findall(self.page_source())
        return self.main_url() + result[0] if result else str()

    def extract_description(self) -> str:
        return super().extract_description()

    def extract_colors(self) -> list:
        return super().extract_colors()

    def extract_minimum_order_quantity(self) -> int:
        table_content = self._extract_table()

        start_tag_str = "<td class="
        end_tag_str = "</td>"

        start_index = 0
        end_index = 0

        for i in range(4):
            try:
                start_index = table_content.index(start_tag_str, start_index + 1)
                end_index = table_content.index(end_tag_str, start_index)
            except ValueError:
                start_index = 0
                break

        result = super().extract_minimum_order_quantity()

        if start_index > 0:
            result_re = re.compile("\d+")
            numbers = result_re.findall(table_content, start_index, end_index)

            if numbers:
                result = int(numbers[-1])

        return result
