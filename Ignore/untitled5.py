# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:37:55 2023

@author: layto
"""
import numpy as np
import pandas as pd
import requests
import io

# Create CSV file

# -> now upload file to private github repo

# define parameters for a request
token = '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'
owner = 'laytonprend'
repo = 'POS-Solution'
path = 'products.csv'
print(f'https://raw.githubusercontent.com/{owner}/{repo}/main/{path}')
f'https://raw.githubusercontent.com/{owner}/{repo}/main/{path}'
url='https://raw.githubusercontent.com/laytonprend/POS-Solution/main/products.csv?token=GHSAT0AAAAAACJ3ULJU47RQPVWBVCFS22EQZKGMZRA'
download=requests.get(url, auth=('laytonprend', token)).content

#download = requests.get(url).content
    
    # Reading the downloaded content and turning it into a pandas dataframe
    
df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    
    # Printing out the first 5 rows of the dataframe
    
print (df.head())  