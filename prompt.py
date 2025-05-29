import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("Select, Resize (Scale), Rotate Image")

# --- Image options ---
image_options = {
    "PPTV Image": "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg",
    "Thairath Image": "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa5K4BG1afANvfhsI0uwEO1wESe3ZeLKGyfPL4Ti6DjFSG9nsKQwF.jpg"
}

# --- Image selection ---
selected_image_name = st.selectbox("Choose an image", list(image_options.keys()))
image_url = image_options[selected_image_name]

# --- Resize and rotate controls ---
st.subheader("Resize (scale image size)")
scale = st.slider("Scale (%)", min_value=10, max_value=300, value=100)

st.subheader("Rotate image")
rotation_angle = st.slider("Rotation angle (counter-clockwise)", min_value=0, max_value=360, value=0)

# --- Load and process image ---
try:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # Calculate new size using scale
    width, height = image.size
    new_width = int(width * scale / 100)
    new_height = int(height * scale / 100)

    # Resize and rotate
    resized_image = image.resize((new_width, new_height))
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    # Display image with axes, no grid
    fig, ax = plt.subplots()
    ax.imshow(rotated_image)
    ax.set_title(f"{selected_image_name} (Rotated {rotation_angle}° | Scaled to {scale}%)")
    ax.set_xlabel("X axis (pixels)")
    ax.set_ylabel("Y axis (pixels)")
    ax.set_xticks([])  # remove tick marks if desired
    ax.set_yticks([])
    ax.tick_params(left=False, bottom=False)  # remove axis ticks
    # Grid removed by not calling ax.grid()

    st.pyplot(fig)

except Exception as e:
    st.error(f"Failed to load image: {e}")
