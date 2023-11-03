# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:25:49 2023

@author: layto
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import shutil

# Load the product and price data from Excel files
@st.cache_data
def load_data(file_path):
    data = pd.read_excel(file_path)
    return data

product_data = load_data("products.xlsx").copy()
price_data = load_data("price.xlsx").copy()

# Filter price data
date_format = "%d/%m/%Y"
price_data['Date'] = pd.to_datetime(price_data['Date'], format=date_format, errors='coerce')
price_data = price_data.sort_values(by=['Product ID', 'Date'], ascending=[True, False])

# Keep only the most recent entry for each product
price_data = price_data.drop_duplicates(subset='Product ID', keep='first')

# Function to update price data
def update_price_data(new_price, product_id):
    new_price_entry = {"Product ID": product_id, "Price": new_price, "Date": datetime.now()}
    price_data = load_data("price.xlsx")
    price_data = price_data.append(new_price_entry, ignore_index=True)
    price_data.to_excel("price.xlsx", index=False)

# Streamlit app
st.title("Restaurant POS System")

# Shopping cart
st.header("Shopping Cart")

cart = st.session_state.cart if "cart" in st.session_state else {
    "products": [],
    "price": [],
    "quantity": []
}

# Number of buttons to display per row
buttons_per_row = 5
button_columns = st.columns(buttons_per_row)
#def callback():#buttonw as clicked
 #   st.session_state.button_clicked=True
    #cart
# Loop through the product IDs to create buttons
for product_id in product_data['Product ID']:
    if button_columns[product_id % buttons_per_row].button(f"Add to Cart (Product ID {product_id})", key=f"button_add_{product_id}"):
        product_index = cart["products"].index(product_id) if product_id in cart["products"] else -1

        if product_index != -1:
            # Update quantity and price for existing product
            cart["quantity"][product_index] += 1
        else:
            # Add new product to cart
            cart["products"].append(product_id)
            cart["price"].append(price_data.loc[price_data['Product ID'] == product_id, 'Price'].values[0])
            cart["quantity"].append(1)
            
        st.session_state.cart=cart # key to write back to session state

# Display items in the cart
remove_indices = []
for i, product_id in enumerate(cart["products"]):
    if st.button(f"Remove from Cart (Product ID {product_id})", key=f"button_remove_{product_id}"):
        if cart["quantity"][i] > 1:
            cart["quantity"][i] -= 1
        else:
            remove_indices.append(i)

# Remove items marked for removal
for i in reversed(remove_indices):
    del cart["products"][i]
    del cart["price"][i]
    del cart["quantity"][i]

# Calculate total price
total_price = sum([price * quantity for price, quantity in zip(cart["price"], cart["quantity"])])

# Display the cart contents
st.write("Cart Items:")
for product_id, price, quantity in zip(cart["products"], cart["price"], cart["quantity"]):
    st.write(f"Product ID: {product_id}, Price: ${price:.2f}, Quantity: {quantity}")
st.write(f"Total Price: ${total_price:.2f}")

# Developer Options
st.sidebar.header("Developer Options")

if st.sidebar.button("Update Price Data"):
    new_price = st.sidebar.number_input("New Price:", step=0.01)
    product_id = st.sidebar.number_input("Product ID:")
    update_price_data(new_price, product_id)
    st.sidebar.success("Price data updated.")

if st.sidebar.button("Clear Cart"):
    cart = {
        "products": [],
        "price": [],
        "quantity": []
    }

if st.sidebar.button("Backup Data"):
    backup_folder = "backup_data"
    shutil.rmtree(backup_folder, ignore_errors=True)
    shutil.copy("products.xlsx", backup_folder)
    shutil.copy("price.xlsx", backup_folder)
    st.sidebar.success("Data backed up.")

if st.sidebar.button("Recover Data"):
    backup_folder = "backup_data"
    shutil.copy(f"{backup_folder}/products.xlsx", "products.xlsx")
    shutil.copy(f"{backup_folder}/price.xlsx", "price.xlsx")
    st.sidebar.success("Data recovered from backup.")

# Show Data
st.sidebar.header("Data Files")

if st.sidebar.button("Show Product Data"):
    st.sidebar.dataframe(product_data)

if st.sidebar.button("Show Price Data"):
    st.sidebar.dataframe(price_data)

# Show Cart in Sidebar
st.sidebar.header("Shopping Cart")
for product_id, price, quantity in zip(cart["products"], cart["price"], cart["quantity"]):
    st.sidebar.write(f"Product ID: {product_id}, Price: ${price:.2f}, Quantity: {quantity}")

