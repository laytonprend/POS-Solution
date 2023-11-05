# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 17:03:15 2023

@author: layto
"""

from github import Github, Auth
#import urllib3
#from github import Auth
import requests  
# Create a custom Retry object
custom_retry = urllib3.util.Retry(    total=10, connect=None, read=None, redirect=None, status=None)

# using an access token
auth = Auth.Token("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")  # token expires in a year

# First create a Github instance with the custom retry object:
g = Github(auth=auth)#, retry=custom_retry)
user = g.get_user()
print(f"User: {user.login}")
print(g.get_user())
# Then play with your Github objects:
#for repo in g.get_user().get_repos():
 #   print(repo.full_name)

# To close connections after use
g.close()