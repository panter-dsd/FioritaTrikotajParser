# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

from PyQt4 import QtCore, QtWebKit
import re


class LoveBunnyParser(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, page_url: str):
        super().__init__()

        self._page_url = page_url
        if not page_url:
            return

        self._web_view = QtWebKit.QWebView()
        self._web_view.loadFinished.connect(self._on_load_finished)
        self._web_view.setUrl(QtCore.QUrl(self._page_url))
        self._web_view.show()

    def page_url(self):
        return self._page_url

    def set_url(self, url: str):
        self._page_url = url
        self._web_view.setUrl(QtCore.QUrl(self._page_url))

    def set_page_source(self, text: str):
        self._page_source = text

    def _on_load_finished(self):
        print("On load finished")
        self._page_source = self._web_view.page().mainFrame().toHtml()
        print(self._page_source)
        self.finished.emit()


    def extract_name(self):
        h3str = "<h3>"
        start_index = self._page_source.index(h3str)

        start_index += len(h3str)

        end_index = self._page_source.index("</h3>", start_index)

        result = self._page_source[start_index:end_index]

        if result:
            result = self._remove_font(result)
        return result


    def extract_description(self):
        return str()


    def extract_colors(self):
        return []


    def extract_sizes(self):
        match_re = re.compile(
            "<option class=\"0\" value=\"\d+\" data-o-val=\"\d+\" ?>(\d+)</option>"
        )
        return match_re.findall(self._page_source)


    def extract_price(self):
        start_text = "<span class=\"item_price\">"
        start_index = self._page_source.index(start_text) + len(start_text)
        end_index = self._page_source.index("</span>", start_index)
        result = self._page_source[start_index:end_index]
        result = self._remove_span(result)
        match_re = re.compile("\d+.\d+")
        return match_re.findall(result)[0]

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

    @staticmethod
    def _remove_font(text: str):
        result = text
        try:
            start_index = result.index("<font")
            end_index = result.index(">", start_index)
        except ValueError:
            start_index = -1
            end_index = -1

        if (start_index >= 0) and (end_index > 0):
            result = result[:start_index] + result[end_index + 1:]
        return result.replace("</font>", "")

#koshka_as
#12m12m12