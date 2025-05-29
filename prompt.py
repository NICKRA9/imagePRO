import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดงและปรับขนาดรูปภาพจาก URL")

# URL ของภาพ
image_url = "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg"

# ป้อนขนาดที่ต้องการ (ค่า default เป็น 300x300)
new_width = st.number_input("ความกว้าง (px)", min_value=50, max_value=2000, value=300)
new_height = st.number_input("ความสูง (px)", min_value=50, max_value=2000, value=300)

try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # ปรับขนาดภาพ
    resized_image = image.resize((new_width, new_height))

    st.image(resized_image, caption="ภาพหลังปรับขนาด", use_column_width=False)
except Exception as e:
    st.error(f"ไม่สามารถโหลดภาพได้: {e}")
