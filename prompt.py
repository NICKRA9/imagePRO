import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("เลือกภาพ ปรับขนาด และหมุนภาพ")

# --- รายการรูปภาพให้เลือก ---
image_options = {
    "ภาพจาก PPTV": "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg",
    "ภาพจาก Thairath": "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa5K4BG1afANvfhsI0uwEO1wESe3ZeLKGyfPL4Ti6DjFSG9nsKQwF.jpg"
}

# --- ตัวเลือกให้ผู้ใช้เลือกภาพ ---
selected_image_name = st.selectbox("เลือกรูปภาพ", list(image_options.keys()))
image_url = image_options[selected_image_name]

# --- ปรับขนาดและหมุนด้วย Slider ---
st.subheader("ขนาดภาพ (พิกเซล)")
new_width = st.slider("ความกว้าง", 50, 1000, 300)
new_height = st.slider("ความสูง", 50, 1000, 300)

st.subheader("หมุนภาพ (ทวนเข็มนาฬิกา)")
rotation_angle = st.slider("องศา", 0, 360, 0)

# --- โหลดและประมวลผลภาพ ---
try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # ปรับขนาด
    resized_image = image.resize((new_width, new_height))

    # หมุนภาพ
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    # แสดงภาพ
    st.image(rotated_image, caption=f"{selected_image_name} | {new_width}x{new_height}px | หมุน {rotation_angle}°", use_column_width=False)

except Exception as e:
    st.error(f"ไม่สามารถโหลดภาพได้: {e}")
