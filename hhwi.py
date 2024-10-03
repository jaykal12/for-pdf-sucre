import streamlit as st
from PIL import Image
import os

# Create a directory to save uploaded images
if not os.path.exists('uploaded_images'):
    os.makedirs('uploaded_images')

# Function to save uploaded image
def save_uploaded_file(uploaded_file):
    with open(os.path.join('uploaded_images', uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())

# Initialize session state for uploaded images
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []

# Title of the app
st.title("Image Upload and Display")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded image
    save_uploaded_file(uploaded_file)
    st.session_state.uploaded_images.append(uploaded_file.name)  # Store image name in session state
    st.success("Image uploaded successfully!")

# Display all uploaded images
st.subheader("Uploaded Images")
for img_file in st.session_state.uploaded_images:
    img_path = os.path.join('uploaded_images', img_file)
    image = Image.open(img_path)
    st.image(image, caption=img_file, use_column_width=True)