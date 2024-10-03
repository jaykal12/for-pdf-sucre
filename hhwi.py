import streamlit as st
import time
import fitz  # PyMuPDF
import io
import os

# Directory to save uploaded files permanently
PDF_DIR = "permanent_saved_pdf"

# Create a folder to save the uploaded PDFs if it doesn't exist
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)


# Function to save uploaded file permanently and return its path
def save_uploaded_file(uploadedfile):
    file_path = os.path.join(PDF_DIR, uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return file_path, uploadedfile.getvalue(), f"File '{uploadedfile.name}' saved successfully!"


# Set timer for 45 minutes (in seconds)
COUNTDOWN_SECONDS = 45 * 60

# Title of the web app
st.title("Secure PDF Viewer with 45 Minute Timer (Persistent Storage)")

# PDF upload functionality
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Check if file is already uploaded and saved in session state
if 'saved_file_path' not in st.session_state and uploaded_file is not None:
    # Save the uploaded file permanently and store it in a variable
    saved_file_path, pdf_file_content, message = save_uploaded_file(uploaded_file)

    # Store the file path and the PDF content in session state
    st.session_state['saved_file_path'] = saved_file_path
    st.session_state['pdf_file_content'] = pdf_file_content  # Store PDF content in variable
    st.session_state['start_time'] = time.time()

    # Display success message
    st.success(message)

# If session already has a saved file
if 'saved_file_path' in st.session_state:
    # Load the saved PDF file from the permanent directory
    pdf_path = st.session_state['saved_file_path']
    pdf_file_content = st.session_state['pdf_file_content']  # Get the stored PDF content

    # Display timer
    time_elapsed = time.time() - st.session_state['start_time']
    time_remaining = COUNTDOWN_SECONDS - time_elapsed

    if time_remaining > 0:
        mins, secs = divmod(time_remaining, 60)
        st.subheader(f"Time Remaining: {int(mins):02d}:{int(secs):02d}")

        # Open and display the saved PDF as images using PyMuPDF
        doc = fitz.open(pdf_path)

        for page in doc:
            pix = page.get_pixmap()  # Convert page to image
            img = io.BytesIO(pix.tobytes())  # Convert image to BytesIO
            st.image(img, use_column_width=True)  # Show image in full width

        st.warning("Note: You cannot copy or download this document.")

    else:
        # When time exceeds 45 minutes, stop access
        st.error("Time's up! Access to this document has expired.")
        st.stop()

# Option to clear session state and remove the saved PDF
if st.button("Clear Document"):
    if 'saved_file_path' in st.session_state:
        del st.session_state['saved_file_path']
    if 'pdf_file_content' in st.session_state:
        del st.session_state['pdf_file_content']
    if os.path.exists(PDF_DIR):
        for file in os.listdir(PDF_DIR):
            os.remove(os.path.join(PDF_DIR, file))
    st.success("Document cleared successfully!")
