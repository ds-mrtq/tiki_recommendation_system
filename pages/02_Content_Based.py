import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from underthesea import word_tokenize, pos_tag, sent_tokenize
import warnings
from gensim import corpora, models, similarities
import jieba
import re
import pickle
from distutils import errors
from distutils.log import error
import altair as alt
from itertools import cycle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, JsCode
from st_clickable_images import clickable_images

import streamlit as st


# Read data
data = pd.read_csv('data/ProductRaw.csv')
# st.write(data.head())

recomend_dict = pd.read_csv('data/CB_new.csv')
# st.write(recomend_dict.head())
# Functions

    
# GUI

# st.markdown("Contend Based")
st.sidebar.markdown('# Content Based')

# st.subheader("Product Catalog")


# Define a search input where the user can type in their query
search_input = st.text_input('Search for an product')

# Filter the items based on the user's query
filtered_items = [item for item in data['name'] if search_input.lower() in item.lower()]

# Show the filtered items in a list
if filtered_items:
    selected_item = st.selectbox('Select an item', filtered_items[:5])
    selected_product_id = data[data['name'] == selected_item]['item_id'].values
    st.write(f"You selected: {selected_product_id} {selected_item}")
else:
    st.write('No product found.')


# st.write(type(selected_product_id))

st.markdown("""### Your recommendation products:""")

recomend_items = recomend_dict[recomend_dict['product_id'].isin(selected_product_id)][['product_id', 'rcmd_product_id', 'score']].head(6)
# st.write(recomend_items)
recomend_items.sort_values(by=['score'], ascending=False, inplace=True)

# print (pd.merge(df1, df2, left_on='id', right_on='id1', how='left').drop('id1', axis=1))
recomend_result = pd.merge(recomend_items, data, left_on='rcmd_product_id', right_on='item_id', how='left')
recomend_result.sort_values(by=['rating', 'score'], ascending=False, inplace=True)
# recomend_result = data[data['item_id'].isin(recomend_items['rcmd_product_id'])]
# st.write(recomend_result)


n_cols = 3
n_rows = 1 + recomend_result.shape[0] // int(n_cols)
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

for i, product in recomend_result.iterrows():
    # i
    # product
    image_url = product['image']
    target_url = product['url']
    product_name = product['name']
    price = "{:,.0f}".format(product['list_price'])
    
    cols[count].image(product['image']
                      , width=150
                    #   , caption=f'[{product_name}]({target_url})'
                    , caption=product['name']
                      , use_column_width=True
                      , output_format="PNG")
    cols[count].write(f"***Rating:*** {product['rating']}")
    cols[count].write(f"**Giá:** {price}")
    

    count = count + 1

