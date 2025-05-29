import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("Image Blending from URLs")

# URLs ของรูปภาพ 2 รูป
url1 = "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg"
url2 = "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa5K4BG1afANvfhsI0uwEO1wESe3ZeLKGyfPL4Ti6DjFSG9nsKQwF.jpg"

# โหลดรูปภาพจาก URL
def load_image(url):
    response = requests.get(url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    return img

try:
    img1 = load_image(url1)
    img2 = load_image(url2)

    # ปรับขนาดให้เท่ากัน (ใช้ขนาดของ img1)
    img2 = img2.resize(img1.size)

    # สร้าง canvas ใหม่เพื่อรวมภาพ
    blended = Image.new("RGBA", img1.size)

    # ใส่ภาพแรกเต็มที่ (alpha=1)
    blended = Image.alpha_composite(blended, img1)

    # ใส่ภาพที่สองแบบโปร่งใส (alpha=0.5)
    img2 = img2.copy()
    alpha = 128  # 0-255 (128 ~ 0.5)
    img2.putalpha(alpha)
    blended = Image.alpha_composite(blended, img2)

    # แสดงภาพด้วย matplotlib
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(blended)
    ax.axis('off')
    ax.set_title("Blended Image (50% overlay)")

    st.pyplot(fig)

except Exception as e:
    st.error(f"Error loading or blending images: {e}")
