import streamlit as st

st.set_page_config(page_title="Tiki.vn", page_icon=":moneybag:")
st.title("Tiki Recommendation System")

# st.markdown("# Main page")
st.sidebar.markdown("# Business Objective")

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