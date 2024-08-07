# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:25:49 2023

@author: layto
"""
# requirments file
import streamlit as st
import pandas as pd
from datetime import datetime
import shutil
import numpy as np
import os
import requests
from io import StringIO
from github import Github, Auth



# change to github URL

# Load the product and price data from Excel files

#@st.cache_data # is decorator only 1 function-yes
def download_data(file):
  url = 'https://raw.githubusercontent.com/laytonprend/POS-Solution/main/' + file
  print(url)
  download = requests.get(url)

  if download.status_code == 200:
      # Check file extension for appropriate read method 
      if file.endswith('.csv'):
          df = pd.read_csv(StringIO(download.content.decode('utf-8')))
      else:
          df = pd.read_excel(StringIO(download.content))  # Assuming Excel if not CSV
      return df.copy()
  else:
      print(f"Error downloading file: {download.status_code}")
      return None  # Handle download error
def upload_data(df,file_path):
    #tried cmd setx GITHUB_PAT "PAT token"
    #forced in local and system env variables now
    owner='laytonprend'
    access_token= os.getenv('GITHUB_PAT')  #os.environ.get("GITHUB_PAT")
    branch_name = 'main'  # Replace with your desired branch name
    repo='POS-Solution'
    repo_name=f'{owner}/{repo}'
    print(repo_name)
    
    g = Github(access_token)
    repo = g.get_repo(repo_name)
    df_content = df.to_csv(index=False)

    #print('midway success')
    # Create or update the file, including the existing SHA
    commit_message = f"Updating {file_path} data"
    contents = repo.get_contents(file_path, ref=branch_name)  # Get file contents
    #print(contents)
    #st.title(access_token)
    #repo.update_file(contents.path, "more tests", "more tests", contents.sha, branch="main")

    repo.update_file(file_path, "Updated transaction data", df_content, contents.sha, branch=branch_name)

    # {'commit': Commit(sha="b06e05400afd6baee13fff74e38553d135dca7dc"), 'content': ContentFile(path="test.txt")}
    
    #repo.create_file(file_path, "Creating file from URL", df_content, branch=branch_name)
    print(f'File at "{file_path}" CREATED in the repository')

def load_price():
    price_data = download_data('price.csv')#?token=GHSAT0AAAAAACUX2PDDRBOAKGVADX3TQMBYZUQGKCA')#'price.csv?token=GHSAT0AAAAAACUX2XWMPFXQN44LBUFCRE6QZUQF7ZA')#'price.csv?token=GHSAT0AAAAAACJ3ULJVDU4IL7Q6DBGQOJ7MZKGM3XQ')
    #https://raw.githubusercontent.com/laytonprend/POS-Solution/main/price.csv?token=GHSAT0AAAAAACUX2XWMPFXQN44LBUFCRE6QZUQF7ZA
    # Filter price data
    print(price_data.head())
    date_format = "%d/%m/%Y %H:%M" #%H:%M"#"%d/%m/%Y"
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

st.session_state.product_data = download_data('products.csv')#?token=GHSAT0AAAAAACUX2XWMSFK6S4Q3A4GH23OUZUQGAQQ')#'products.csv?token=GHSAT0AAAAAACJ3ULJU47RQPVWBVCFS22EQZKGMZRA')
#product_data = load_data("products.csv")
st.session_state.price_data=load_price()
#backup_data() # auto backs up at the start of the code # if backed up then any faults cant be recovered

#product_data=product_data.merge(price_data,by='Product_ID',how='left')


# Streamlit app
st.title("Restaurant POS System")

# Shopping cart
st.header("Shopping Cart")
def init_cart():
     return {
        "product_id": [],
        "product_name": [],
        "price": [],
        "quantity": []
    }
    
cart = st.session_state.cart if "cart" in st.session_state else init_cart()
# Number of buttons to display per row
buttons_per_row = 5
button_columns = st.columns(buttons_per_row)
#def callback():#buttonw as clicked
 #   st.session_state.button_clicked=True
    #cart
# Loop through the Product_IDs to create buttons
for product_id, product_name in zip(st.session_state.product_data['Product_ID'], st.session_state.product_data['Product_Name']):
    product_id = int(product_id)  # Convert product_id to an integer
    if button_columns[(product_id-1) % buttons_per_row].button(f"Add to Cart Product {product_id}, {product_name}", key=f"button_add_{product_id}, {product_name}"):
        product_index = cart["product_id"].index(product_id) if product_id in cart["product_id"] else -1

        if product_index != -1:
            # Update quantity and price for existing product
            cart["quantity"][product_index] += 1
        else:
            # Add new product to cart
            
            try:
                cart["price"].append(st.session_state.price_data.loc[st.session_state.price_data['Product_ID'] == product_id, 'Price'].values[-1]) # price first as may not be in
                cart["product_id"].append(product_id)
                cart["product_name"].append(st.session_state.product_data.loc[st.session_state.product_data['Product_ID'] == product_id, 'Product_Name'].values[-1])
                cart["quantity"].append(1)
            except IndexError:
                st.title(f'Please add price data for {product_name}, unable to add to cart')
            
            
        st.session_state.cart=cart # key to write back to session state



# Display items in the cart
remove_indices = []
for i, product_id in enumerate(cart["product_id"]):
    if st.button(f"Remove from Cart (Product_ID {product_id})", key=f"button_remove_{product_id}"):
        if cart["quantity"][i] > 1:
            cart["quantity"][i] -= 1
        else:
            remove_indices.append(i)

# Remove items marked for removal
for i in reversed(remove_indices):
    del cart["product_id"][i]
    del cart["product_name"][i]
    del cart["price"][i]
    del cart["quantity"][i]
    st.session_state.cart=cart # key to write back to session state

# Calculate total price
total_price = sum([price * quantity for price, quantity in zip(cart["price"], cart["quantity"])])

# Display the cart contents
st.write("Cart Items:")
for product_id, product_name, price, quantity in zip(cart["product_id"],cart["product_name"], cart["price"], cart["quantity"]):
    st.write(f"Product_ID: {product_id}, Product_Name: {product_name}, Price: ${price:.2f}, Quantity: {quantity}")
st.write(f"Total Price: ${total_price:.2f}")

if st.button("Checkout"):
    #download_data.clear() # clear function so reload raw data
    transactions_prev = download_data('transactions.csv')#?token=GHSAT0AAAAAACUX2XWM36QGCSK7KFGRMQKQZUQGBCA')#"transactions.csv?token=GHSAT0AAAAAACJ3ULJUSULGHYXPQDJGVUQUZKGM4YQ")
    transaction_id=np.max(transactions_prev['Transaction_ID'])+1#new transaction ID
    transactions = []
    for product_id, product_name, product_price, product_quantity in zip(cart["product_id"], cart["product_name"], cart["price"], cart["quantity"]):# in cart.items():
        #item_price=product_data.loc[]
        transactions.append({"Transaction_ID":transaction_id, "Date": datetime.now(), "Total_Price":product_price*product_quantity, 'Unit_Price':product_price ,"Quantity":product_quantity ,
                             "Product_ID": product_id, "Product_Name": product_name})

        
        #for i in range(product_info["quantity"]):
         #   transactions.append({"Product_ID": product_id, "Price": product_info["price"], "Date": datetime.now()})
    #transactions = load_data("transactions.csv")
    st.session_state.transactions_data = pd.concat([transactions_prev, pd.DataFrame(transactions)])
    #transactions_df.to_csv("transactions.csv", index=False)
    upload_data(st.session_state.transactions_data,'transactions.csv')
    cart=init_cart()
    st.session_state.cart=init_cart()
    st.success("Checkout successful. Transaction data saved to 'transactions.csv'")

# Developer Options
def update_product_data(product_data,new_product_id,new_product_name):
    backup_data() # can recover if faulty
    new_product_entry = {"Product_ID": [product_id], "Product_Name": [new_product_name], "Date": [datetime.now()]}
    new_product_df = pd.DataFrame(new_product_entry)
    # Load the existing price data
    #product_data = load_data("products.csv")
    # Append the new data to the existing data
    updated_product_data = pd.concat([product_data, new_product_df], ignore_index=True)
    # Save the updated price data to the Excel file
    updated_product_data.to_excel("products.csv", index=False)
    

st.sidebar.header("Developer Options")
##product update
UpdateProduct = st.session_state.UpdateProduct if "UpdateProduct" in st.session_state else False
ProductSubmission = st.session_state.ProductSubmission if "ProductSubmission" in st.session_state else []
if st.sidebar.button("Update Product Data") or UpdateProduct:
    st.session_state.UpdateProduct=True
    #download_data.clear() # clear function so reload raw data
    st.session_state.product_data = download_data("products.csv")
    
    
    
    #issue when adding new products
    new_product_id = np.max(st.session_state.product_data['Product_ID'])+1 # +1 doesnt work but it should#st.sidebar.number_input("Product_ID:",step=1)
    new_product_name = st.sidebar.text_input("New Product Name:")
    if st.sidebar.button("Submit New Product") and ProductSubmission!=[new_product_id,new_product_name]:# maybe block duplicates too
        st.session_state.ProductSubmission=[new_product_id,new_product_name]
        
        #update_product_data(product_data,new_product_id,new_product_name)
        st.sidebar.success("Product data updated.")
        #download_data.clear() # clear function so reload raw data
        st.session_state.product_data = download_data("products.csv")
        
# Function to update price data
def update_price_data(new_price, product_id):
    backup_data() # can recover if faulty
    new_price_entry = {"Product_ID": [product_id], "Price": [new_price], "Date": [datetime.now()]}
    new_price_df = pd.DataFrame(new_price_entry)
    # Load the existing price data
    price_data = load_price()
    # Append the new data to the existing data
    updated_price_data = pd.concat([price_data, new_price_df], ignore_index=True)
    # Save the updated price data to the Excel file
    #return updated_price_data 
    
    #updated_price_data.to_excel("price.csv", index=False)
##price update
UpdatePrice = st.session_state.UpdatePrice if "UpdatePrice" in st.session_state else False
PriceSubmission = st.session_state.PriceSubmission if "PriceSubmission" in st.session_state else []
if st.sidebar.button("Update Price Data") or UpdatePrice:
    st.session_state.UpdatePrice=True
    product_id = st.sidebar.number_input("Product_ID:",step=1)
    new_price = st.sidebar.number_input("New Price:", step=0.25)
    if st.sidebar.button("Submit New Price") and PriceSubmission!=[product_id,new_price]:# maybe block duplicates too
        st.session_state.PriceSubmission=[product_id,new_price]
        
        update_price_data(new_price, product_id)
        st.sidebar.success("Price data updated.")
        st.session_state.price_data=load_price()

if st.sidebar.button("Clear Cart"):
    st.session_state.cart= init_cart()

if st.sidebar.button("Backup Data"): # shutil is a convenient and powerful module for working with files and directories in Python, making various file-related tasks easier to perform.
    backup_data()

if st.sidebar.button("Recover Data"):
    backup_folder = "backup_data"
    shutil.copy(f"{backup_folder}/products.csv", "products.csv")
    shutil.copy(f"{backup_folder}/price.csv", "price.csv")
    st.sidebar.success("Data recovered from backup.")

# Show Data
st.sidebar.header("Data Files")

if st.sidebar.button("Show Product Data"):
    st.sidebar.dataframe(st.session_state.product_data)

if st.sidebar.button("Show Price Data"):
    st.sidebar.dataframe(st.session_state.price_data)

#download_data.clear() # clear function so reload raw data
st.session_state.transaction_data=download_data('transactions.csv')#?token=GHSAT0AAAAAACUX2XWM36QGCSK7KFGRMQKQZUQGBCA')#"transactions.csv?token=GHSAT0AAAAAACJ3ULJUSULGHYXPQDJGVUQUZKGM4YQ")
if st.sidebar.button("Show Transaction Data"):
    st.sidebar.dataframe(st.session_state.transaction_data.sort_values(by='Date', ascending=False))
st.sidebar.write('Most recent transaction',np.max(st.session_state.transaction_data['Date']))