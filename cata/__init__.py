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
        checksum = get_checksum(df, params["params"])
        params_str = json.dumps(params["params"])

        df.to_sql(checksum, self.db, if_exists='replace', index=False)

        c = self.db.cursor()
        c.execute(''' INSERT INTO catalog(ROWID, checksum, params) VALUES(?, ?, ?) ''',
            [None, checksum, params_str])
        self.db.commit()

        return(checksum)

    def read(self, checksum):
        try:
            return(pd.read_sql("select * from '{}'".format(checksum), self.db))
        except:
            return

    def get_params(self, checksum):
        c = self.db.cursor()
        c.execute(''' SELECT params FROM catalog WHERE checksum=? LIMIT 1''', (checksum,))
        result = c.fetchone()[0]
        return(json.loads(result))

    def find(self, **params):
        pass

    def update(self):
        pass

    def delete(self):
        pass


def get_checksum(df, params):
    # sha256(concatenated column names, serialized params, num_rows, num_cols, num_tables_in_cata)
    num_rows, num_cols = df.shape
    hash_values = {
        'columns': "".join(list(df.columns.values)),
        'params': json.dumps(params, sort_keys=True, separators=(',', ':')),
        'rows': num_rows,
        'cols': num_cols,
    }
    hash_fmt = "{rows} {cols} {columns} {params}"
    hash_str = hash_fmt.format(**hash_values)
    print(hash_str)
    checksum = hashlib.sha256(hash_str.encode('ascii')).hexdigest()
    print(checksum)

    # checksum = hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
    return(checksum)

if __name__ == '__main__':
    main(1)
