# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from unittest import TestCase

from stok_market_parser import StokMarketParser

class TestStokMarketParser(TestCase):
    def test_0(self):
        test_data = str()

        with open("test_data/stok-market/test0.html", encoding="utf-8") as f:
            test_data = f.read()

        parser = StokMarketParser()
        parser.set_page_source(test_data)

        self.assertEqual(
            parser.extract_name(),
            "Блуза"
        )
        self.assertEqual(parser.extract_price(), "322.00")
        self.assertEqual(
            parser.extract_main_image_url(),
            "http://stok-m.ru/image/cache/data-292-5576e8fe6dae1-177572-426x639.jpg"
        )
