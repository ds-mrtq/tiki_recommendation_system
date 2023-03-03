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

import streamlit as st


# st.markdown("Collaborative Filtering")
st.sidebar.markdown('# Collaborative Filtering')
# flag = False
# lines = None
# type = st.radio("Upload data or Input data?", options=("Upload", "Input"))
# if type=="Upload":
#     # Upload file
#     uploaded_file_1 = st.file_uploader("Choose a file", type=['txt', 'csv'])
#     if uploaded_file_1 is not None:
#         lines = pd.read_csv(uploaded_file_1, header=None)
#         st.dataframe(lines)
#         # st.write(lines.columns)
#         lines = lines[0]     
#         flag = True       
# if type=="Input":        
#     email = st.text_area(label="Input your content:")
#     if email!="":
#         lines = np.array([email])
#         flag = True

# if flag:
#     st.write("Content:")
#     if len(lines)>0:
#         st.code(lines)        
#         x_new = count_model.transform(lines)        
#         y_pred_new = ham_spam_model.predict(x_new)       
#         st.code("New predictions (0: Ham, 1: Spam): " + str(y_pred_new))
