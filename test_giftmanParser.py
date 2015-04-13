# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from unittest import TestCase

from giftman_parser import GiftmanParser


class TestGiftmanParser(TestCase):
    def test_0(self):
        test_data = str()

        with open("test_data/giftman/test0.html", encoding="cp1251") as f:
            test_data = f.read()

        parser = GiftmanParser()
        parser.set_page_source(test_data)

        self.assertEqual(parser.extract_name(),
            "Свеча \"Яйцо пасхальное\", парафин, "
            "красный, 4х6см, время горения 5 час"
        )
        self.assertEqual(parser.extract_price(), "35.74")
        self.assertEqual(parser.extract_minimum_order_quantity(), 1)
        self.assertEqual(parser.extract_image_url(),
            "http://www.giftman.ru/img/goods/photo/13140-b.1425997021.jpg")