import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# หัวข้อของแอป
st.title("แสดงรูปภาพจาก URL")

# URL ของรูปภาพ
image_url = "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg"

# โหลดภาพจาก URL
response = requests.get(image_url)
if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="ภาพจาก PPTV", use_column_width=True)
else:
    st.error("ไม่สามารถโหลดภาพได้")
