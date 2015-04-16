# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from unittest import TestCase

from magdayana_parser import MagdayanaParser


class TestMagdayanaParser(TestCase):
    def test_0(self):
        test_data = str()

        with open("test_data/magdayana/test0.html", encoding="utf-8") as f:
            test_data = f.read()

        parser = MagdayanaParser()
        parser.set_page_source(test_data)

        self.assertEqual(parser.extract_name(), "Бикини")
        self.assertEqual(parser.extract_price(), 685.0)
        self.assertEqual(parser.extract_image_url(),
            "http://www.magdayana.ru/assets/galleries/1001/1.jpg")
        self.assertEqual(parser.extract_sizes(), ["S", "M", "L"])

    def test_1(self):
        test_data = str()

        with open("test_data/magdayana/test1.html", encoding="utf-8") as f:
            test_data = f.read()

        parser = MagdayanaParser()
        parser.set_page_source(test_data)

        self.assertEqual(parser.extract_name(), "Купальник белый")
        self.assertEqual(parser.extract_price(), 509.0)
        self.assertEqual(parser.extract_image_url(),
            "http://www.magdayana.ru/assets/galleries/641/15.jpg")
        self.assertEqual(parser.extract_sizes(), ["унив. (42-46)"])

    def test_correct_load_image_url(self):
        test_data = str()

        with open("test_data/magdayana/test0.html", encoding="utf-8") as f:
            test_data = f.read()

        parser = MagdayanaParser()
        parser.set_page_source(test_data)

        with open("test_data/magdayana/test1.html", encoding="utf-8") as f:
            test_data = f.read()

        parser.set_page_source(test_data)
        self.assertEqual(parser.extract_image_url(),
            "http://www.magdayana.ru/assets/galleries/641/15.jpg"
        )



