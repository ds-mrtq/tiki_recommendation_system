import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from underthesea import word_tokenize, pos_tag, sent_tokenize
import warnings
from gensim import corpora, models, similarities
import jieba
import re
import pickle

from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import glob
import streamlit as st

# Read data
data = pd.read_csv('data/ProductRaw.csv')
data.head()

# Functions
# Define a function to display product details when a product is clicked
def display_product_details(product):
    st.write("## Product Details")
    st.write(f"**Name:** {product['name']}")
    st.write(f"**Description:** {product['description']}")
    st.write(f"**List Price:** {product['list_price']}")
    st.write(f"**Brand:** {product['brand']}")
    st.write(f"**Group:** {product['group']}")
    
# GUI

# st.markdown("Contend Based")
st.sidebar.markdown('# Content Based')

st.subheader("Product Catalog")


# Display a random selection of 6 products in a grid
random_products = data.sample(n=6)
random_products.shape[0]

n_cols = 3
n_rows = 1 + random_products.shape[0] // int(n_cols)
# 'n_rows:'
# n_rows
rows = [st.container() for _ in range(n_rows)]
# 'rows:'
# rows
cols_per_row = [r.columns(n_cols) for r in rows]
# 'cols_per_row'
# cols_per_row
cols = [column for row in cols_per_row for column in row]
# 'cols'
# cols
count = 0
for i, product in random_products.iterrows():
    # i
    # product
    cols[count].image(product['image'], width=150, caption=product['name'], 
                use_column_width=True, output_format="PNG")
    cols[count].write(f"**Giá:** {product['list_price']}")
    count = count + 1


# When a product is clicked, open a new browser tab to display more details
if st.button("Click here to select a product"):
    selected_product = st.selectbox("Select a product", random_products["name"])
    product_info = random_products[random_products["name"] == selected_product].iloc[0]
    url = product_info["url"]
    js = f"window.open('{url}')"  # JavaScript to open a new tab
    html = '<img src="{}" style="max-width: 200px">'.format(product_info["image"])
    html += f"<h2>{product_info['name']}</h2>"
    html += f"<p>{product_info['description']}</p>"
    html += f"<p>List price: {product_info['list_price']}</p>"
    html += f"<p>Brand: {product_info['brand']}</p>"
    html += f"<p>Group: {product_info['group']}</p>"
    st.write("You have selected this product:")
    st.write(html, unsafe_allow_html=True)
    st.write(
        f'<script type="text/javascript">{js}</script>',
        unsafe_allow_html=True,
    )


# ########
render_image = JsCode('''
                      
    function renderImage(params){
    // Create a new image element
        var img = new Image();
        
        img.src = params.value;
        
        img.width = 35;
        img.height = 35;
        
        return img;
        
    }             
                      ''')

# build gridoptions object

# Build GridOptions object
options_builder = GridOptionsBuilder.from_dataframe(random_products)
options_builder.configure_column('image', cellRenderer = render_image)
options_builder.configure_selection(selection_mode="single", use_checkbox=True)
grid_options = options_builder.build()

# Create AgGrid component
grid = AgGrid(random_products, 
                gridOptions = grid_options,
                allow_unsafe_jscode=True,
                height=200, width=500, theme='streamlit')

sel_row = grid["selected_rows"]
if sel_row:
    col1, col2 = st.columns(2)
    st.info(sel_row[0]['description'])
    col1.image(sel_row[0]['image'],caption = sel_row[0]['name'])
    col2.subheader("Rating: " + str(sel_row[0]['rating']))
