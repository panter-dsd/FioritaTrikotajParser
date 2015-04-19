# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from unittest import TestCase

from magok_parser import MagokParser


class TestMagokParser(TestCase):
    def setUp(self):
        super().setUp()
        self._test_data = str()

        with open("test_data/magok/test0.html", "r", encoding="utf-8") as f:
            self._test_data = f.read()

    def test_0(self):
        parser = MagokParser()
        parser.set_page_source(self._test_data)

        self.assertEqual(parser.extract_name(), "Молния джинсовая золото №4 10см замок М-4002 цв.310 черный")
        self.assertEqual(parser.extract_price(), "8,24")
        self.assertEqual(parser.extract_minimum_order_quantity(), 50)
        self.assertEqual(parser.extract_main_image_url(), "http://magok.ru/img/preview/big/5/53888.jpg")
