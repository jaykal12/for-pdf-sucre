import streamlit as st
import os
from PIL import Image

# Set the directory to store uploaded images
UPLOAD_FOLDER = 'uploaded_images'

# Create the folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Function to display images with delete option
def display_images():
    images = os.listdir(UPLOAD_FOLDER)
    if images:
        st.subheader("Binod ka message hai ")
        for image in images:
            img = Image.open(os.path.join(UPLOAD_FOLDER, image))
            st.image(img, caption=image, use_column_width=True)

            # Add a button to delete each image
            if st.button(f"Delete {image}", key=image):
                os.remove(os.path.join(UPLOAD_FOLDER, image))
                st.success(f"Image {image} deleted successfully!")
                st.experimental_rerun()  # Refresh the app to update the display
    else:
        st.write("No images uploaded yet.")


# Streamlit application UI
st.title("नैतिक्ता नियतिश्चैव भ्रम एव हि केवलम्। शून्यं सत्यं परं तत्त्वं तत्र नास्ति शुभाशुभम्|| Binod ka message niche hai koi or button par click na kare")

# Uploading the image
uploaded_file = st.file_uploader("yha na click karo", type=["png", "jpg", "jpeg", "gif"])

if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Image {uploaded_file.name} uploaded successfully!")

# Display the uploaded images with delete options
display_images()
