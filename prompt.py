import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

st.title("Blending & Editing Two Images from URL")

# Image URLs
image_options = {
    "PPTV Image": "https://img.pptvhd36.com/thumbor/2022/01/26/771eebf1b8.jpg",
    "Thairath Image": "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa5K4BG1afANvfhsI0uwEO1wESe3ZeLKGyfPL4Ti6DjFSG9nsKQwF.jpg"
}

# Image selection
st.subheader("Select base image and overlay image")
col1, col2 = st.columns(2)
with col1:
    base_name = st.selectbox("Base image", list(image_options.keys()), key="base")
with col2:
    overlay_name = st.selectbox("Overlay image", list(image_options.keys()), key="overlay")

base_url = image_options[base_name]
overlay_url = image_options[overlay_name]

# Resize and rotation controls
st.subheader("Resize and Rotate")
size_px = st.slider("Image size (Width = Height)", 50, 1500, 500, 10)
rotation_angle = st.slider("Rotation angle (counter-clockwise)", 0, 360, 0)

# Blending control
st.subheader("Blending")
blend_alpha = st.slider("Overlay opacity (0 = transparent, 1 = full)", 0.0, 1.0, 0.5, 0.01)

# Load image from URL
def load_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGBA")

try:
    # Load and prepare images
    base_img = load_image(base_url).resize((size_px, size_px)).rotate(rotation_angle, expand=True)
    overlay_img = load_image(overlay_url).resize((size_px, size_px)).rotate(rotation_angle, expand=True)

    # Set overlay transparency
    overlay_copy = overlay_img.copy()
    overlay_copy.putalpha(int(blend_alpha * 255))

    # Alpha composite images
    blended_img = Image.new("RGBA", base_img.size)
    blended_img = Image.alpha_composite(blended_img, base_img)
    blended_img = Image.alpha_composite(blended_img, overlay_copy)

    # Prepare to display with matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(blended_img)
    ax.set_title(f"Blended: {base_name} + {overlay_name} | Size: {size_px}px | Rotate {rotation_angle}°")

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

    # Add blended size text on top and bottom (with stroke)
    path_fx = [path_effects.Stroke(linewidth=2, foreground='black', alpha=0.4), path_effects.Normal()]
    size_text = f"Image size: {size_px} x {size_px} px | Alpha: {blend_alpha:.2f}"
    ax.text(0.5, 1.05, size_text, transform=ax.transAxes, ha='center', va='bottom',
            fontsize=14, color='white', alpha=0.6, path_effects=path_fx)
    ax.text(0.5, -0.1, size_text, transform=ax.transAxes, ha='center', va='top',
            fontsize=14, color='white', alpha=0.6, path_effects=path_fx)

    st.pyplot(fig)

except Exception as e:
    st.error(f"Error loading or processing images: {e}")
