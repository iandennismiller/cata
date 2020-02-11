# -*- coding: utf-8 -*-
# catalog (c) Ian Dennis Miller

import os
import json
import sqlite3
import hashlib
import pandas as pd
from pandas.util import hash_pandas_object

class Cata:
    def __init__(self, filename=None, overwrite=False):
        if not filename:
            self.filename = os.path.expanduser("~/.cata")
        else:
            self.filename = filename

        if overwrite and os.path.isfile(self.filename):
            os.remove(self.filename)

        self.db = sqlite3.connect(self.filename)

        # if there is no table called catalog, create it

        # count how many tables have the name 'catalog'
        c = self.db.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='catalog' ''')

        # if the count is 0, then table does not exist
        if c.fetchone()[0] == 0:
            c.execute(''' CREATE TABLE catalog (id INTEGER PRIMARY KEY AUTOINCREMENT, checksum TEXT NOT NULL, params TEXT NOT NULL) ''')
            self.db.commit()

    def create(self, df, **params):
        checksum = hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
        df.to_sql(checksum, self.db, if_exists='replace', index=False)

        params_str = json.dumps(params["params"])

        c = self.db.cursor()
        c.execute(''' INSERT INTO catalog(ROWID, checksum, params) VALUES(?, ?, ?) ''',
            [None, checksum, params_str])
        self.db.commit()

        return(checksum)

    def read(self, checksum):
        return(pd.read_sql("select * from '{}'".format(checksum), self.db))

    def find(self, **params):
        pass

    def update(self):
        pass

    def delete(self):
        pass


if __name__ == '__main__':
    main(1)
