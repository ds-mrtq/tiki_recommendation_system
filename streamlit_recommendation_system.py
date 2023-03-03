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
st.set_page_config(page_title="Tiki.vn", page_icon=":moneybag:")
st.title("Tiki Recommendation System")
menu = ["Business Objective", "Content-Based", "Collaborative Filtering"]
choice = st.sidebar.selectbox('Menu', menu)
if choice == 'Business Objective':    
    st.subheader("Tổng quát về Recommender system")
    st.write("""
    * Recommender system là các thuật toán nhằm đề xuất các item có liên quan cho người dùng (Item có thể là phim để xem, văn bản để đọc, sản phẩm cần mua hoặc bất kỳ thứ gì khác tùy thuộc vào ngành dịch vụ). 
    """)  
    st.write("""* Recommender system thực sự quan trọng trong một số lĩnh vực vì chúng có thể tạo ra một khoản thu nhập khổng lồ hoặc cũng là một cách để nổi bật đáng kể so với các đối thủ cạnh tranh.""")
    st.write("""* Có hai recommender system phổ biến nhất là
Collaborative Filtering (CF) và Content-Based
    """)
    st.image("images/reco-sys-diagram_orig.png")
    st.subheader("Mục tiêu dự án")
    st.image("images/tikis-scaled-1536x949.jpg")
    st.write("""* Tiki là một hệ sinh thái thương mại “all in one”, trong
đó có tiki.vn, là một website thương mại điện tử đứng
top 2 của Việt Nam, top 6 khu vực Đông Nam Á.
             """)
    st.write("""* Trên trang này đã triển khai nhiều tiện ích hỗ trợ nâng
cao trải nghiệm người dùng và họ muốn xây dựng
nhiều tiện ích hơn nữa.
             """)
    st.write("""* Giả sử công ty này chưa triển khai Recommender
System và chúng ta hãy cùng nhau xem demo về hệ thống này.
             """)

elif choice == 'Content-Based':
    # st.subheader("Content-Based")
    # st.write("##### 1. Some data")
    # st.dataframe(data[['name', 'list_price']].head(3))
    # st.dataframe(data[['name', 'list_price']].tail(3))  
    

    # Define the layout of the web app
    
    st.subheader("Product Catalog")

    # Display a random selection of 6 products in a grid
    random_products = data.sample(n=6)
    # # Define the columns to display in the grid
    # columns = ["name", "list_price", "image"]

    # # Define the width of the columns
    # column_widths = [0.6, 0.3, 0.1]

    # # Create the grid
    # for i, product in random_products.iterrows():
    #     col1, col2, col3 = st.columns(column_widths)
    #     with col1:
    #         st.image(product["image"], width=150, caption=product['name'])
    #     with col2:
    #         st.radio(label=product["name"][:20], options=[i], key=i)
    #     with col3:
    #         st.write(f"${product['list_price']}")

    # # Create a section to display the details of the selected product
    # selected_product = st.radio("You choose this product:", options=random_products.iterrows(), format_func=lambda x: x[1]["name"][:20])
    # st.write(selected_product[1]["name"])
    # st.write(selected_product[1]["description"])
    # st.write(f"List Price: ${selected_product[1]['list_price']}")
    # st.write(f"Brand: {selected_product[1]['brand']}")
    # st.write(f"Group: {selected_product[1]['group']}")
    
    col1, col2, col3 = st.columns(3)
    for i, product in random_products.iterrows():
        with eval(f"col{i%3+1}"):
            # st.write(f"## {product['name']}")
            # st.write(f"## {product['name'][:20]}...")
            # st.write(f"**List Price:** {product['list_price']}")
            # st.image(product['image'], width=150)
            
            st.image(product['image'], width=150, caption=product['name'][:20], 
                    use_column_width=True, output_format="PNG")
            
            st.write(f"**List Price:** {product['list_price']}")
        
            if st.button(f"View Product {product['item_id']} Details"):
                display_product_details(product)
            
    
    # st.write("##### 2. Visualize Ham and Spam")
    # fig1 = sns.countplot(data=data[['v1']], x='v1')    
    # st.pyplot(fig1.figure)

    # st.write("##### 3. Build model...")
    # st.write("##### 4. Evaluation")
    # st.code("Score train:"+ str(round(score_train,2)) + " vs Score test:" + str(round(score_test,2)))
    # st.code("Accuracy:"+str(round(acc,2)))
    # st.write("###### Confusion matrix:")
    # st.code(cm)
    # st.write("###### Classification report:")
    # st.code(cr)
    # st.code("Roc AUC score:" + str(round(roc,2)))

    # # calculate roc curve
    # st.write("###### ROC curve")
    # fpr, tpr, thresholds = roc_curve(y_test, y_prob[:, 1])
    # fig, ax = plt.subplots()       
    # ax.plot([0, 1], [0, 1], linestyle='--')
    # ax.plot(fpr, tpr, marker='.')
    # st.pyplot(fig)

    # st.write("##### 5. Summary: This model is good enough for Ham vs Spam classification.")

elif choice == 'Collaborative Filtering':
    st.subheader("Collaborative Filtering")
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
    

