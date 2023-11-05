# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:29:30 2023

@author: layto
"""

import requests
from requests.structures import CaseInsensitiveDict

url = "https://raw.githubusercontent.com/organization/repo/branch/folder/file"

# If repo is private - we need to add a token in header:
headers = CaseInsensitiveDict()
headers["Authorization"] = "token SHA256:iNiOIQ9+/m+2Tk6seRKeTvr3YdAqdUy25iVAl+Ex6yM"

resp = requests.get(url, headers=headers)
print(resp.status_code)