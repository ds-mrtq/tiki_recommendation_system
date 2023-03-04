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

# selected_item
# selected_customer_id['customer_id']
st.markdown("""### Your recommendation products:""")
recommend_items = recommend_dict[recommend_dict['customer_id'] == selected_item]['recommendations']
recommend_items.iloc[0]
# recommend_items = recommend_dict[recommend_dict['customer_id'] == selected_item]['recommendations'][0]
# recommend_items
# recommend_items[0]
i = 0

for item in recommend_items.iloc[0]:
    st.write(i)
    st.write(item['product_id'])
    i = i + 1
# recomend_items = recomend_dict[recomend_dict['product_id'].isin(selected_item)][['product_id', 'rcmd_product_id', 'score']]

# st.write(recomend_items)


# # print (pd.merge(df1, df2, left_on='id', right_on='id1', how='left').drop('id1', axis=1))
# recomend_result = pd.merge(recomend_items, data, left_on='rcmd_product_id', right_on='item_id', how='left').head(6)
# # recomend_result = data[data['item_id'].isin(recomend_items['rcmd_product_id'])]
# # st.write(recomend_result)