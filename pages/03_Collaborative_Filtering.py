import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
import datetime


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
data = pd.read_csv('data/Review.csv')
# st.write(data.head())

recommend_dict = pd.read_parquet('data/collaborative_filtering_all_users_recs.parqet')
# recommend_dict

products = pd.read_csv('data/ProductRaw.csv')

# st.markdown("Collaborative Filtering")
st.sidebar.markdown('# Collaborative Filtering')

# Define a search input where the user can type in their query
search_input = st.text_input('Search for an customer id')

# Filter the items based on the user's query
filtered_items = [item for item in recommend_dict['customer_id'] if str(search_input).lower() in str(item).lower()]

# Show the filtered items in a list
if filtered_items:
    selected_item = st.selectbox('Select a customer', filtered_items[:5])
    # selected_customer_id = recommend_dict[recommend_dict['customer_id'] == selected_item]['customer_id'].head(1)
    st.write(f"You selected: {selected_item}")
else:
    st.write('No customer found.')

st.markdown("""### Your recommendation products:""")
# recommend_items = recommend_dict[recommend_dict['customer_id'] == selected_item]['recommendations']
# recommend_items.iloc[0]

# # Initialize an empty dataframe with columns name
# recommend_items_df = pd.DataFrame(columns=['customer_id', 'product_id', 'rating'])
# # st.write(len(recommend_items.iloc[0]))

# # Add values using for loop 
# i = 0
# for item in recommend_items.iloc[0]:
#     # st.write(i)
#     # st.write(item['product_id'])
#     recommend_items_df.loc[i] = [selected_item, item['product_id'], item['rating']]
#     i = i + 1
# recommend_items_df

recommend_items = recommend_dict.loc[recommend_dict['customer_id'] == selected_item, 'recommendations']
recommend_items_lst = recommend_items.iloc[0]
# recommend_items_lst

# Create a list of tuples with required data 
rcm_item_tuples_list = [(selected_item, item.get('product_id'), item.get('rating')) for item in recommend_items_lst]
# rcm_item_tuples_list

# Create dataframe directly from the list of tuples
recommend_items_df = pd.DataFrame(rcm_item_tuples_list, columns=['customer_id', 'product_id', 'rating'])
# recommend_items_df

# get products list
products_df = pd.read_csv('data/ProductRaw.csv')

recommend_result = pd.merge(recommend_items_df, products_df, left_on='product_id', right_on='item_id', how='left')
recommend_result.sort_values(by=['rating_x'], ascending=False, inplace=True)
# recomend_result


def show_items(recommend_result):
    n_cols = 3
    n_rows = 1 + recommend_result.shape[0] // int(n_cols)
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

    for i, product in recommend_result.iterrows():
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
        cols[count].write(f"***Rating:*** {product['rating_x']}")
        cols[count].write(f"**Giá:** {price}")
    

        count = count + 1

show_items(recommend_result)

