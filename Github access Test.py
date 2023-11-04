# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 14:05:28 2023

@author: layto
"""

import requests
import pandas as pd

# Define your authentication or access control headers
headers = {
    'Authorization': 'Bearer SHA256:22Uyl/hyLTJNhNaGTRuqqdQq3G+22qsLa7Yw0a0cFTw=',
    # Other headers if required
}

url = 'https://example.com/path/to/your/protected/excel-file.xlsx'

try:
    # Send a request with the appropriate headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Save the content to a temporary file
        with open('temp_file.xlsx', 'wb') as f:
            f.write(response.content)

        # Load the temporary file into a DataFrame
        df = pd.read_excel('temp_file.xlsx')

        # Now you have your data in the 'df' variable
        print(df)

    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
'''
from github import Github

g = Github('SHA256:22Uyl/hyLTJNhNaGTRuqqdQq3G+22qsLa7Yw0a0cFTw=')

repo = g.get_repo('laytonprend/POS-Solution')

with open('dataset.csv', 'r') as file:
    data = file.read()

repo.create_file('data/dataset.csv', 'upload csv', data, branch='main')
'''

'''from github import Github
g = Github("username", "password")

repo = g.get_user().get_repo(GITHUB_REPO)
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

with open('/tmp/file.txt', 'r') as file:
    content = file.read()

# Upload to github
git_prefix = 'folder1/'
git_file = git_prefix + 'file.txt'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, "committing files", content, branch="master")
    print(git_file + ' CREATED')'''
    