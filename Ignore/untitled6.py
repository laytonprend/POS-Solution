# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:15:37 2023

@author: layto
"""

from github import Github
import pandas as pd
import requests
from io import StringIO
token='SHA256:PIVmphJed8RZBtFaSiEsT0Zi0g0gXAuRXj3dqY5Xw5U='#'SHA256:iNiOIQ9+/m+2Tk6seRKeTvr3YdAqdUy25iVAl+Ex6yM'

repo_for_upload='POS-Solution'
file_path='products.csv'
dest_path_on_github='products.csv'
commit_message='uploaded csv'
repo_owner='laytonprend'
repo_name='POS-Solution'

github = Github(token)
repo = github.get_user(repo_owner).get_repo(repo_name)

url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}'
response = requests.get(url)

df = pd.read_csv(StringIO(response.text))
df['test_col'] = "new_test_val"

content = repo.get_contents(file_path)

#df.to_csv(url, index=False)


with open(url, 'rb') as f:
    contents = f.read()




repo.update_file(file_path, commit_message, contents, content.sha)