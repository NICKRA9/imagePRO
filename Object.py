import streamlit as st
from PIL import Image
from ultralytics import YOLO
import numpy as np
import cv2

# โหลดโมเดล YOLOv8
model = YOLO("yolov8n.pt")

st.title("🔍 ตรวจจับวัตถุในภาพด้วย YOLOv8")

uploaded_file = st.file_uploader("อัปโหลดภาพ", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="ภาพต้นฉบับ", use_column_width=True)

    # แปลงภาพเป็น numpy array
    img_array = np.array(image)

    # ตรวจจับวัตถุ
    results = model(img_array)[0]

    # วาดกรอบผลลัพธ์
    annotated_img = results.plot()  # คืนค่าภาพพร้อมกล่องตรวจจับ

    st.image(annotated_img, caption="ภาพพร้อมผลตรวจจับ", use_column_width=True)

    # แสดงชื่อวัตถุ
    detected_classes = set([results.names[int(cls)] for cls in results.boxes.cls])
    st.write("### วัตถุที่พบในภาพ:")
    for obj in detected_classes:
        st.write(f"- {obj}")
