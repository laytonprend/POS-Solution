# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:34:06 2023

@author: layto
"""

import numpy as np
import pandas as pd
import requests
from io import StringIO

# Create CSV file
df = pd.DataFrame(np.random.randint(2,size=10_000).reshape(1_000,10))
df.to_csv('products.csv') 

# -> now upload file to private github repo

# define parameters for a request
token = "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"
owner = 'laytonprend'
repo = 'POS-Solution'
path = 'products.csv'

# send a request
r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
    owner=owner, repo=repo, path=path),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
            }
    )

# convert string to StringIO object
string_io_obj = StringIO(r.text)

# Load data to df
df = pd.read_csv(string_io_obj, sep=",", index_col=0)
print(df)