import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from ultralytics import YOLO

# โหลดโมเดล YOLO
model = YOLO("yolov8n.pt")

st.title("🎯 ตรวจจับวัตถุจากลิงก์รูปภาพ")

# รับ URL จากผู้ใช้
img_url = st.text_input("ใส่ลิงก์ภาพที่ต้องการตรวจจับวัตถุ", 
                        value="https://www.hrmagazine.co.uk/media/bgofcr0p/young-people.jpeg")

if img_url:
    try:
        response = requests.get(img_url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        st.image(image, caption="ภาพที่โหลดจาก URL", use_column_width=True)

        # ตรวจจับวัตถุ
        results = model(np.array(image))[0]
        annotated_img = results.plot()

        st.image(annotated_img, caption="ภาพพร้อมผลตรวจจับ", use_column_width=True)

        detected_classes = set([results.names[int(cls)] for cls in results.boxes.cls])
        st.write("### วัตถุที่พบในภาพ:")
        for obj in detected_classes:
            st.write(f"- {obj}")
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")
