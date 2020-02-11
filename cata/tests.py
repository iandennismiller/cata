# -*- coding: utf-8 -*-
# catalog (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from unittest import TestCase as BaseCase
import pandas as pd
from . import Cata

df = pd.DataFrame(data={
    "id": [1, 2, 3],
    "value": [1, 4, 9] 
})

class BasicTestCase(BaseCase):
    def setUp(self):
        self.cata = Cata("/tmp/test.cata", overwrite=True)

    def tearDown(self):
        pass

    def test_create(self):
        "ensure an entry can be created"
        result = self.cata.create(df, params={"lr": 0.01, "momentum": 0.9})
        self.assertNotEqual(result, None)

    def test_read(self):
        "ensure an entry can be read"
        result = self.cata.create(df, params={"lr": 0.01, "momentum": 0.9})

        checksum = "639d93806424326a5438a16132c1eb911faf9879cb57c6f3f6d2553d1c564cb4"
        result = self.cata.read(checksum=checksum)
        self.assertIsNotNone(result)
