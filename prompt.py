import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("Select, Resize (Custom Size) with Size Display, Rotate Image")

# Image options
image_options = {
    "PPTV Image": "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg",
    "Thairath Image": "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa5K4BG1afANvfhsI0uwEO1wESe3ZeLKGyfPL4Ti6DjFSG9nsKQwF.jpg"
}

selected_image_name = st.selectbox("Choose an image", list(image_options.keys()))
image_url = image_options[selected_image_name]

# Slider for resizing (width and height equal)
st.subheader("Resize image")

size_px = st.slider("Image size (Width = Height)", min_value=50, max_value=1500, value=500, step=10)

st.subheader("Rotate image")
rotation_angle = st.slider("Rotation angle (counter-clockwise)", 0, 360, 0)

try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    resized_image = image.resize((size_px, size_px))
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(rotated_image)
    ax.set_title(f"{selected_image_name} | Rotated {rotation_angle}°")
    
    # Remove axis ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.tick_params(left=False, bottom=False)

    # Add text for image size on top center
    ax.text(0.5, 1.05, f"Image size: {size_px} x {size_px} pixels", transform=ax.transAxes,
            ha='center', va='bottom', fontsize=12, color='blue')

    # Add text for image size on bottom center
    ax.text(0.5, -0.1, f"Image size: {size_px} x {size_px} pixels", transform=ax.transAxes,
            ha='center', va='top', fontsize=12, color='blue')

    st.pyplot(fig)

except Exception as e:
    st.error(f"Failed to load image: {e}")
