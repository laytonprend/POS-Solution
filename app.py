# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:25:49 2023

@author: layto
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import shutil
import numpy as np
import os
import requests
import io
# Load the product and price data from Excel files
@st.cache_data
def load_data(file):
    #data = pd.read_excel(file)
    #return data.copy()
    # Define your authentication or access control headers
    headers = {
        'Authorization': 'Bearer SHA256:22Uyl/hyLTJNhNaGTRuqqdQq3G+22qsLa7Yw0a0cFTw=',
        # Other headers if required
    }
    url = 'https://raw.githubusercontent.com/laytonprend/POS-Solution/main/'+file#'https://github.com/laytonprend/POS-Solution/blob/main/'+file
    
    #if True:# temp 
    #try:
        # Send a request with the appropriate headers
    response = requests.get(url, headers=headers)    
        #if response.status_code == 200:
            # Save the content to a temporary file
            #with open('temp_file.csv', 'wb') as f:
             #   f.write(response.content)    
            #print(f)
            # Load the temporary file into a DataFrame
    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))#'openpyxl')    
            # Now you have your data in the 'df' variable
    print(df)    
     #   else:
      #      print(f"Failed to download the file. Status code: {response.status_code}")    
    #except Exception as e:
     #   print(f"An error occurred: {str(e)}")
    return df.copy()
def load_price():
    price_data = load_data("price.csv")
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
#backup_data() # auto backs up at the start of the code # if backed up then any faults cant be recovered

#product_data=product_data.merge(price_data,by='Product_ID',how='left')


# Streamlit app
st.title("Restaurant POS System")

# Shopping cart
st.header("Shopping Cart")

cart = st.session_state.cart if "cart" in st.session_state else {
    "product_id": [],
    "product_name": [],
    "price": [],
    "quantity": []
}

# Number of buttons to display per row
buttons_per_row = 5
button_columns = st.columns(buttons_per_row)
#def callback():#buttonw as clicked
 #   st.session_state.button_clicked=True
    #cart
# Loop through the Product_IDs to create buttons
for product_id, product_name in zip(product_data['Product_ID'], product_data['Product_Name']):
    product_id = int(product_id)  # Convert product_id to an integer
    if button_columns[(product_id-1) % buttons_per_row].button(f"Add to Cart Product {product_id}, {product_name}", key=f"button_add_{product_id}, {product_name}"):
        product_index = cart["product_id"].index(product_id) if product_id in cart["product_id"] else -1

        if product_index != -1:
            # Update quantity and price for existing product
            cart["quantity"][product_index] += 1
        else:
            # Add new product to cart
            
            try:
                cart["price"].append(price_data.loc[price_data['Product_ID'] == product_id, 'Price'].values[-1]) # price first as may not be in
                cart["product_id"].append(product_id)
                cart["product_name"].append(product_data.loc[product_data['Product_ID'] == product_id, 'Product_Name'].values[-1])
                cart["quantity"].append(1)
            except IndexError:
                st.title(f'Please add price data for {product_name}, unable to add to cart')
            
            
        st.session_state.cart=cart # key to write back to session state

'''# Category selection
categories = product_data["Category"].unique()
selected_category = st.sidebar.selectbox("Select a category", categories)

# Filter products by selected category
filtered_products = product_data[product_data["Category"] == selected_category]

# Number of buttons to display per row
buttons_per_row = 5
button_columns = st.columns(buttons_per_row)

# Loop through the products to create buttons
for index, row in filtered_products.iterrows():
    product_id = int(row["Product_ID"])
    product_name = row["Product_Name"]
    
    if button_columns[(product_id - 1) % buttons_per_row].button(
        f"Add to Cart Product {product_id}, {product_name}",
        key=f"button_add_{product_id}_{product_name}",
    ):
        product_index = cart["product_id"].index(product_id) if product_id in cart["product_id"] else -1

        if product_index != -1:
            # Update quantity and price for existing product
            cart["quantity"][product_index] += 1
        else:
            # Add new product to cart
            try:
                cart["price"].append(price_data.loc[price_data['Product_ID'] == product_id, 'Price'].values[-1])
                cart["product_id"].append(product_id)
                cart["product_name"].append(product_name)
                cart["quantity"].append(1)
            except IndexError:
                st.title(f'Please add price data for {product_name}, unable to add to cart')

        st.session_state.cart = cart'''

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
    transactions_prev = load_data("transactions.csv")
    transaction_id=np.max(transactions_prev['Transaction_ID'])+1#new transaction ID
    transactions = []
    for product_id, product_name, product_price, product_quantity in zip(cart["product_id"], cart["product_name"], cart["price"], cart["quantity"]):# in cart.items():
        #item_price=product_data.loc[]
        transactions.append({"Transaction_ID":transaction_id, "Date": datetime.now(), "Total_Price":product_price*product_quantity, 'Unit_Price':product_price ,"Quantity":product_quantity ,
                             "Product_ID": product_id, "Product_Name": product_name})

        
        #for i in range(product_info["quantity"]):
         #   transactions.append({"Product_ID": product_id, "Price": product_info["price"], "Date": datetime.now()})
    #transactions = load_data("transactions.csv")
    transactions_df = pd.concat([transactions_prev, pd.DataFrame(transactions)])
    transactions_df.to_excel("transactions.csv", index=False)
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
    product_data = load_data("products.csv")
    
    
    
    #issue when adding new products
    new_product_id = np.max(product_data['Product_ID'])+1 # +1 doesnt work but it should#st.sidebar.number_input("Product_ID:",step=1)
    new_product_name = st.sidebar.text_input("New Product Name:")
    if st.sidebar.button("Submit New Product") and ProductSubmission!=[new_product_id,new_product_name]:# maybe block duplicates too
        st.session_state.ProductSubmission=[new_product_id,new_product_name]
        
        update_product_data(product_data,new_product_id,new_product_name)
        st.sidebar.success("Product data updated.")
        product_data = load_data("products.csv")
        
# Function to update price data
def update_price_data(new_price, product_id):
    backup_data() # can recover if faulty
    new_price_entry = {"Product_ID": [product_id], "Price": [new_price], "Date": [datetime.now()]}
    new_price_df = pd.DataFrame(new_price_entry)
    # Load the existing price data
    price_data = load_data("price.csv")
    # Append the new data to the existing data
    updated_price_data = pd.concat([price_data, new_price_df], ignore_index=True)
    # Save the updated price data to the Excel file
    updated_price_data.to_excel("price.csv", index=False)
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
        price_data=load_price()

if st.sidebar.button("Clear Cart"):
    cart = {
        "products": [],
        "price": [],
        "quantity": []
    }

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
    st.sidebar.dataframe(product_data)

if st.sidebar.button("Show Price Data"):
    st.sidebar.dataframe(price_data)
