# -*- coding: utf-8 -*-
# catalog (c) Ian Dennis Miller

import os
import csv
import json
from shutil import copyfile
import hashlib
import pandas
from pandas.util import hash_pandas_object

class Cata:
    def __init__(self, root_path=".cata"):
        self.root_path = root_path
        if not os.path.exists(root_path):
            os.makedirs(root_path)

    def create(self, df=None, csv_filename=None, **params):
        created = False
        if csv_filename and os.path.exists(csv_filename):
            checksum = sha256(csv_filename)
            destination = os.path.join(self.root_path, checksum)
            copyfile(csv_filename, destination)
            created = True
        elif df is not None:
            checksum = get_checksum(df, params)
            destination = os.path.join(self.root_path, checksum)
            df.to_csv(destination, sep='\t', encoding='utf-8')
            created = True
            
        if created:
            # add to the catalog
            destination = os.path.join(self.root_path, ".cata.csv")
            try:
                with open(destination, 'r') as csvfile:
                    row_count = sum(1 for row in csvfile)
            except:
                row_count = 0

            with open(destination, 'a') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar="'",
                    quoting=csv.QUOTE_NONNUMERIC)
                spamwriter.writerow([row_count+1, checksum, json.dumps(params["params"], sort_keys=True, separators=(',', ':'))])
        
        return(checksum)

    def read(self, checksum):
        source = os.path.join(self.root_path, checksum)
        return(pandas.read_csv(source))

    def get_params(self, checksum):
        pass

    def find(self, **params):
        checksum = self.search(**params)
        if checksum:
            return(self.read(checksum))

    def search(self, **params):
        destination = os.path.join(self.root_path, ".cata.csv")
        with open(destination, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar="'")
            for row in csvreader:
                [idx, checksum, params_json] = row
                print(params_json)
                params_loads = json.loads(params_json)
                match = True
                for k, v in params.items():
                    print(params_loads)
                    if k in params_loads.keys():
                        if params_loads[k] != v:
                            match = False
                    else:
                        match = False
                if match:
                    return(checksum)

    def update(self):
        pass

    def delete(self):
        pass

def get_checksum(df, params):
    num_rows, num_cols = df.shape
    hash_values = {
        'columns': "".join(list(df.columns.values)),
        'params': json.dumps(params, sort_keys=True, separators=(',', ':')),
        'rows': num_rows,
        'cols': num_cols,
    }
    hash_fmt = "{rows} {cols} {columns} {params}"
    hash_str = hash_fmt.format(**hash_values)
    checksum = hashlib.sha256(hash_str.encode('ascii')).hexdigest()

    return(checksum)

def sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return(hash_sha256.hexdigest())

if __name__ == '__main__':
    main(1)
