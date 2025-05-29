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

# Slider for width and height, range 50 to 1500 px
size_px = st.slider("Image size (Width = Height)", min_value=50, max_value=1500, value=500, step=10)

# Show size above the image
st.write(f"Current image size: {size_px} x {size_px} pixels")

# Rotate slider
st.subheader("Rotate image")
rotation_angle = st.slider("Rotation angle (counter-clockwise)", 0, 360, 0)

try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # Resize and rotate
    resized_image = image.resize((size_px, size_px))
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    # Display image without grid
    fig, ax = plt.subplots()
    ax.imshow(rotated_image)
    ax.set_title(f"{selected_image_name} | Size: {size_px}x{size_px} | Rotated {rotation_angle}°")
    ax.set_xlabel("X axis (pixels)")
    ax.set_ylabel("Y axis (pixels)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.tick_params(left=False, bottom=False)

    st.pyplot(fig)

    # Show size below the image as well
    st.write(f"Current image size: {size_px} x {size_px} pixels")

except Exception as e:
    st.error(f"Failed to load image: {e}")
