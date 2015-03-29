# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

import urllib.request
import re

class PageParser(object):
    def __init__(self, page_url: str):
        super().__init__()

        self._page_url = page_url
        self._page_source = self._get_page_source()

        print(self.extract_name())
        print(self.extract_description())
        print(self.extract_colors())
        print(self.extract_sizes())
        print(self.extract_price())

    def page_url(self):
        return self._page_url

    def _get_page_source(self):
        result = str()

        with urllib.request.urlopen(self._page_url) as f:
            result = f.read().decode("utf-8")

        return result.replace("&quot;", "\"").replace("&nbsp;", " ")

    def extract_name(self):
        name_re = re.compile("<h1 itemprop=\"name\">(.*)</h1>")
        remove_re = re.compile(" F\w+ \d+")
        match = name_re.findall(self._page_source)

        result = match[0] if match else str()

        if result:
            remove_match = remove_re.search(result)
            if remove_match:
                result = result[:remove_match.start()] \
                         + result[remove_match.end():]

        return result

    def extract_description(self):
        h3str = "<h3>Описание товара</h3><p>"
        start_index = self._page_source.index(h3str)

        start_index += len(h3str)

        end_index = self._page_source.index("</p>", start_index)

        result = self._page_source[start_index:end_index]

        if result:
            result = self._remove_span(result)
        return result.replace("<br />", "").split("\n")[0]

    def extract_colors(self):
        begin_group_str = "<select id=\"select_color"
        end_group_str = "</select>"
        start_index = self._page_source.index(begin_group_str)
        end_index = self._page_source.index(end_group_str, start_index)

        match_re = re.compile("<option value=\"\d+\">([\w+\s\",-]+)</option>")

        match = match_re.findall(self._page_source, start_index, end_index)

        match.remove("Неважно")
        return match

    def extract_sizes(self):
        match_re = re.compile(
            "<tr class=\"catalog_size_count \"><td><span class=\"size-title\">([\d*]+)"
        )
        return match_re.findall(self._page_source)

    def extract_price(self):
        match_re = re.compile("<td>(\d+) <span class=\"rub\">a</span>")
        return match_re.findall(self._page_source)[0]

    def _remove_span(self, text: str):
        result = text
        start_index = result.index("<span")
        end_index = result.index(">", start_index)

        if (start_index >= 0) and (end_index > 0):
            result = result[:start_index] + result[end_index + 1:]
        return result.replace("</span>", "")