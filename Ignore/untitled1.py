# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:21:03 2023

@author: layto
"""

import requests
from requests.structures import CaseInsensitiveDict

# Variables
GH_PREFIX = "https://raw.githubusercontent.com"
ORG = "laytonprend"
REPO = "POS-Solution"
BRANCH = "main"
#FOLDER = "some-folder"
FILE = "products.csv"


token = 'SHA256:iNiOIQ9+/m+2Tk6seRKeTvr3YdAqdUy25iVAl+Ex6yM'
   # owner = 'laytonprend'
   # repo = 'POS-Solution'
    #path = file

URL = GH_PREFIX + "/" + ORG + "/" + REPO + "/" + BRANCH  + "/" + FILE
print(URL)
print('')
# Headers setup
headers = CaseInsensitiveDict()
headers["Authorization"] = "token " + token

# Execute and view status
resp = requests.get(URL, headers=headers)
if resp.status_code == 200:
   print(resp.content)
else:
   print("Request failed!",resp.status_code)