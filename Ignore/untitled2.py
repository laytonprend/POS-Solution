# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:25:02 2023

@author: layto
"""

from requests import get as rget

token = 'SHA256:iNiOIQ9+/m+2Tk6seRKeTvr3YdAqdUy25iVAl+Ex6yM' 
owner = 'laytonprend'
repo = 'POS-Solution'
path = 'products.csv'

res = rget(f"https://{owner}:{token}@raw.githubusercontent.com/laytonprend/POS-Solution/main/products.csv")
with open('file.csv', 'wb+') as f:
        f.write(res.content)