# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

import re


class FioritaTrikotajParser(object):
    def __init__(self):
        super().__init__()

        self._main_url = "http://fiorita-trikotaj.ru/"

        self._page_source = str()

    def set_page_source(self, text: str):
        self._page_source = text

        self._page_source = self._page_source.replace("&quot;", "\"").replace(
            "&nbsp;", " ")

    def extract_name(self):
        start_str = "<h1 itemprop=\"name\">"
        end_str = "</h1>"

        try:
            start_index = self._page_source.index(start_str)
            start_index += len(start_str)
            end_index = self._page_source.index(end_str, start_index)
        except ValueError:
            return str()

        result = self._page_source[start_index:end_index]

        remove_re = re.compile("\w{2} \d[\d\w]+")
        remove_match = remove_re.search(result)
        if remove_match:
            result = result[:remove_match.start()] \
                     + result[remove_match.end():]

        return result

    def extract_description(self):
        h3str = "<h3>Описание товара</h3><p>"

        try:
            start_index = self._page_source.index(h3str)
            start_index += len(h3str)
            end_index = self._page_source.index("</p>", start_index)
        except ValueError:
            return str()

        result = self._page_source[start_index:end_index]

        if result:
            result = self._remove_span(result)
            result = result.replace("<br />", "")
        return result.split("\n")[0] if result else str()

    def extract_colors(self) -> list:
        begin_group_str = "<select id=\"select_color"
        end_group_str = "</select>"
        try:
            start_index = self._page_source.index(begin_group_str)
            end_index = self._page_source.index(end_group_str, start_index)
        except ValueError:
            return []

        match_re = re.compile("<option value=\"\d+\">([\w+\s\",-]+)</option>")

        match = match_re.findall(self._page_source, start_index, end_index)

        match.remove("Неважно")
        return match

    def extract_sizes(self) -> list:
        match_re = re.compile(
            "<tr class=\"catalog_size_count \"><td><span class=\"size-title\">([\d*]+)"
        )
        return match_re.findall(self._page_source)

    def extract_price(self) -> str:
        match_re = re.compile("<td>(\d+) <span class=\"rub\">a</span>")
        matches = match_re.findall(self._page_source)
        return matches[0] if matches else str()

    def extract_image_url(self):
        start_str = "big_pic"
        image_src_str = "src="
        try:
            start_index = self._page_source.index(start_str)
            image_url_start = self._page_source.index(image_src_str,
                                                      start_index)
            image_url_start += len(image_src_str) + 1
            image_url_end = self._page_source.index("\"", image_url_start)
        except ValueError:
            return str()

        return self._main_url + self._page_source[
                                image_url_start:image_url_end]

    @staticmethod
    def _remove_span(text: str):
        result = text
        try:
            start_index = result.index("<span")
            end_index = result.index(">", start_index)
        except ValueError:
            start_index = -1
            end_index = -1

        if (start_index >= 0) and (end_index > 0):
            result = result[:start_index] + result[end_index + 1:]
        return result.replace("</span>", "")