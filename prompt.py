import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดงและปรับขนาดรูปภาพจาก URL ด้วย Slider")

# URL ของภาพ
image_url = "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg"

# ปรับขนาดด้วย Slider
st.subheader("เลือกขนาดที่ต้องการ")
new_width = st.slider("ความกว้าง (px)", min_value=50, max_value=1000, value=300)
new_height = st.slider("ความสูง (px)", min_value=50, max_value=1000, value=300)

try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # ปรับขนาดภาพ
    resized_image = image.resize((new_width, new_height))

    # แสดงภาพ
    st.image(resized_image, caption=f"ขนาด {new_width}x{new_height} px", use_column_width=False)

except Exception as e:
    st.error(f"ไม่สามารถโหลดภาพได้: {e}")
