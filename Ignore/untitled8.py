# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 14:31:35 2023

@author: layto
"""

from github import Github
import urllib3

# Authentication is defined via github.Auth
from github import Auth
import requests
username = 'laytonprend'
token = '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'

login = requests.get('https://raw.githubusercontent.com/laytonprend/POS-Solution/main/products.csv?token=GHSAT0AAAAAACJ4PLXTNBM26PVVIGSLDR4GZKHVAHA', auth = Auth.Token("token") )