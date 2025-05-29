import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("Select, Resize (Small/Medium/Large) with Size Display, Rotate Image")

# Image options
image_options = {
    "PPTV Image": "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg",
    "Thairath Image": "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa5K4BG1afANvfhsI0uwEO1wESe3ZeLKGyfPL4Ti6DjFSG9nsKQwF.jpg"
}

selected_image_name = st.selectbox("Choose an image", list(image_options.keys()))
image_url = image_options[selected_image_name]

# Mapping size labels to pixel values
size_mapping = {
    "Small": 100,
    "Medium": 500,
    "Large": 1000
}

# Resize selection with size display
st.subheader("Resize image")

col1, col2 = st.columns([3, 2])

with col1:
    width_label = st.select_slider(
        "Width",
        options=["Small", "Medium", "Large"],
        value="Medium"
    )
with col2:
    st.write(f"{size_mapping[width_label]} px")

col3, col4 = st.columns([3, 2])
with col3:
    height_label = st.select_slider(
        "Height",
        options=["Small", "Medium", "Large"],
        value="Medium"
    )
with col4:
    st.write(f"{size_mapping[height_label]} px")

new_width = size_mapping[width_label]
new_height = size_mapping[height_label]

# Rotate slider
st.subheader("Rotate image")
rotation_angle = st.slider("Rotation angle (counter-clockwise)", 0, 360, 0)

try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # Resize and rotate
    resized_image = image.resize((new_width, new_height))
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    # Display image without grid
    fig, ax = plt.subplots()
    ax.imshow(rotated_image)
    ax.set_title(f"{selected_image_name} | {width_label} x {height_label} | Rotated {rotation_angle}°")
    ax.set_xlabel("X axis (pixels)")
    ax.set_ylabel("Y axis (pixels)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.tick_params(left=False, bottom=False)

    st.pyplot(fig)

except Exception as e:
    st.error(f"Failed to load image: {e}")
