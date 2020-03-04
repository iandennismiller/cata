# -*- coding: utf-8 -*-
# catalog (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from unittest import TestCase as BaseCase
import pandas as pd
from . import Cata, get_checksum

df = pd.DataFrame(data={
    "id": [1, 2, 3],
    "value": [1, 4, 9] 
})
params = {"lr": 0.01, "momentum": 0.9}
checksum_good = "5c7dfb0fb299fb8adf71ed3f53c65ef185aebd53451a949cc71b79d124b91125"

class BasicTestCase(BaseCase):
    def setUp(self):
        self.cata = Cata()

    def tearDown(self):
        pass

    def test_create(self):
        "ensure an entry can be created"
        checksum = self.cata.create(df, params=params)
        self.assertEqual(checksum, checksum_good)

    def test_read(self):
        "ensure an entry can be read"
        checksum = self.cata.create(df, params=params)
        df_test = self.cata.read(checksum=checksum)
        self.assertIsNotNone(df_test)

        params_test = self.cata.get_params(checksum=checksum)
        #print(params)
        self.assertIsNotNone(params_test)

        self.assertEqual(get_checksum(df_test, params_test), checksum_good)

    def test_find(self):
        "ensure a table checksum works"
        df_test = self.cata.find(lr=0.01)
        self.assertIsNotNone(df_test)

    def test_search(self):
        "ensure a table checksum works"
        checksum = self.cata.search(lr=0.01)
        self.assertEqual(checksum, checksum_good)
