import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดง ปรับขนาด และหมุนรูปภาพจาก URL")

# URL ของภาพ
image_url = "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg"

# Slider สำหรับปรับขนาด
st.subheader("เลือกขนาดของภาพ")
new_width = st.slider("ความกว้าง (px)", min_value=50, max_value=1000, value=300)
new_height = st.slider("ความสูง (px)", min_value=50, max_value=1000, value=300)

# Slider สำหรับหมุนภาพ
st.subheader("หมุนภาพ")
rotation_angle = st.slider("องศาที่จะหมุน (ทวนเข็มนาฬิกา)", min_value=0, max_value=360, value=0)

try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # ปรับขนาด
    resized_image = image.resize((new_width, new_height))

    # หมุนภาพ (หมุนทวนเข็มนาฬิกา, expand=True เพื่อให้ภาพไม่ถูกตัด)
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    # แสดงภาพ
    st.image(rotated_image, caption=f"ขนาด {new_width}x{new_height} หมุน {rotation_angle}°", use_column_width=False)

except Exception as e:
    st.error(f"ไม่สามารถโหลดภาพได้: {e}")
