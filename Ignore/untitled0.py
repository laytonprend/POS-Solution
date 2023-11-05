# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:00:04 2023

@author: layto
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import shutil
import numpy as np
import os
import requests
from io import StringIO
def _github(url: str, mode: str = "private"):
        url = url.replace("/blob/", "/")
        url = url.replace("/raw/", "/")
        url = url.replace("github.com/", "raw.githubusercontent.com/")

        if mode == "public":
            return requests.get(url)
        else:
            token = os.getenv('GITHUB_TOKEN', '...')
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3.raw'}
            return requests.get(url, headers=headers)
def load_data(file):
    #data = pd.read_excel(file)
    #return data.copy()
    # Define your authentication or access control headers
    headers = {
        'Authorization': 'Bearer SHA256:22Uyl/hyLTJNhNaGTRuqqdQq3G+22qsLa7Yw0a0cFTw=',
        # Other headers if required
    }
    url = 'https://raw.githubusercontent.com/laytonprend/POS-Solution/main/'+file#'https://github.com/laytonprend/POS-Solution/blob/main/'+file
    #https://raw.githubusercontent.com/laytonprend/POS-Solution/main/price.csv
    #if True:# temp 
    #try:
        # Send a request with the appropriate headers
    #download = requests.get(url,headers).content

# Reading the downloaded content and turning it into a pandas dataframe

    #df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    #url = 'https://raw.githubusercontent.com/laytonprend/POS-Solution/main/'+file#'https://github.com/laytonprend/POS-Solution/blob/main/'+file
    
    #if True:# temp 
    #try:
        # Send a request with the appropriate headers
    #download = requests.get(url).content
    
    # Reading the downloaded content and turning it into a pandas dataframe
    
    #df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    token = 'SHA256:22Uyl/hyLTJNhNaGTRuqqdQq3G+22qsLa7Yw0a0cFTw=' 
    owner = 'laytonprend'
    repo = 'POS-Solution'
    path = file
    
    r= _github('https://raw.githubusercontent.com/laytonprend/POS-Solution/main/products.csv?token=GHSAT0AAAAAACJ3ULJUK4XTFW35ORX3JE6UZKGMFPA','private')
    '''
    # send a request
    r = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
        owner=owner, repo=repo, path=path),
        headers={
            'accept': 'application/vnd.github.v3.raw',
            'authorization': 'token {}'.format(token)
                }
        )'''
   # convert string to StringIO object
    string_io_obj = StringIO(r.text)
    
    # Load data to df
    df = pd.read_csv(string_io_obj, sep=",", index_col=0)

    # Printing out the first 5 rows of the dataframe
    
    print (df.head())  
    # Printing out the first 5 rows of the dataframe
    
    print (df.head())    
            # Now you have your data in the 'df' variable
    print(df)    
     #   else:
      #      print(f"Failed to download the file. Status code: {response.status_code}")    
    #except Exception as e:
     #   print(f"An error occurred: {str(e)}")
    return df.copy()
def load_price():
    price_data = load_data("price.csv")
    print(price_data)
    # Filter price data
    date_format = "%d/%m/%Y"
    price_data['Date'] = pd.to_datetime(price_data['Date'], format=date_format, errors='coerce')
    price_data = price_data.sort_values(by=['Product_ID', 'Date'], ascending=[True, False])
    
    # Keep only the most recent entry for each product
    price_data = price_data.drop_duplicates(subset='Product_ID', keep='first')
    return price_data
def backup_data():
    backup_folder = "C:/Users/layto/OneDrive/Documents/GitHub/POS-Solution/backup_data"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    shutil.rmtree(backup_folder, ignore_errors=True)
    shutil.copy("products.csv", backup_folder)
    shutil.copy("price.csv", backup_folder)
    shutil.copy("transactions.csv", backup_folder)# acked up but not reinstated when reciver
    st.sidebar.success("Data backed up.")


product_data = load_data("products.csv")
#product_data = load_data("products.csv")
price_data=load_price()