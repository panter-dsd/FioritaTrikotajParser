# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from unittest import TestCase

from sima_land_parser import SimaLandParser


class TestSimaLandParser(TestCase):
    def test_0(self):
        test_data = str()

        with open("test_data/sima-land/test0.html", encoding="utf-8") as f:
            test_data = f.read()

        parser = SimaLandParser()
        parser.set_page_source(test_data)

        self.assertEqual(
            parser.extract_name(),
            "Форма для яичницы и блинов 12х12 см \"Мишутка\", цвета МИКС"
        )
        self.assertEqual(parser.extract_price(), "20")
        self.assertEqual(parser.extract_minimum_order_quantity(), 10)
        self.assertEqual(
            parser.extract_image_url(),
            "https://st-cdn.r.worldssl.net/items/811/811916/0/400.jpg"
        )