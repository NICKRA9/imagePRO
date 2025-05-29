import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("Select, Resize, Rotate Image and Show Axes")

# --- Image options ---
image_options = {
    "PPTV Image": "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg",
    "Thairath Image": "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa5K4BG1afANvfhsI0uwEO1wESe3ZeLKGyfPL4Ti6DjFSG9nsKQwF.jpg"
}

# --- Image selection ---
selected_image_name = st.selectbox("Choose an image", list(image_options.keys()))
image_url = image_options[selected_image_name]

# --- Resize and rotate controls ---
st.subheader("Resize image")
new_width = st.slider("Width (X axis, pixels)", min_value=50, max_value=1000, value=300)
new_height = st.slider("Height (Y axis, pixels)", min_value=50, max_value=1000, value=300)

st.subheader("Rotate image")
rotation_angle = st.slider("Rotation angle (counter-clockwise)", min_value=0, max_value=360, value=0)

# --- Load and process image ---
try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # Resize and rotate
    resized_image = image.resize((new_width, new_height))
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    # Display image with axes
    fig, ax = plt.subplots()
    ax.imshow(rotated_image)
    ax.set_title(f"{selected_image_name} (Rotated {rotation_angle}°)")
    ax.set_xlabel("X axis (pixels)")
    ax.set_ylabel("Y axis (pixels)")
    ax.grid(True)

    st.pyplot(fig)

except Exception as e:
    st.error(f"Failed to load image: {e}")
