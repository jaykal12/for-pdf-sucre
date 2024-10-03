import streamlit as st
import time
import fitz  # PyMuPDF
import io
import os


# Function to save uploaded file locally
def save_uploaded_file(uploadedfile):
    with open(os.path.join("saved_pdf", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"File '{uploadedfile.name}' saved successfully!")


# Create a folder to save the uploaded PDFs
if not os.path.exists("saved_pdf"):
    os.makedirs("saved_pdf")

# Set timer for 45 minutes (in seconds)
COUNTDOWN_SECONDS = 45 * 60

# Title of the web app
st.title("Secure PDF Viewer (As Images) with 45 Minute Timer")

# PDF upload functionality
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Check if file is already uploaded and saved in session state
if 'saved_file' not in st.session_state and uploaded_file is not None:
    # Save the uploaded file
    save_uploaded_file(uploaded_file)
    # Store the file path in session state
    st.session_state['saved_file'] = uploaded_file.name
    st.session_state['start_time'] = time.time()

# If session already has a saved file
if 'saved_file' in st.session_state:
    # Load the saved PDF file
    pdf_path = os.path.join("saved_pdf", st.session_state['saved_file'])

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
    if 'saved_file' in st.session_state:
        del st.session_state['saved_file']
    if os.path.exists("saved_pdf"):
        for file in os.listdir("saved_pdf"):
            os.remove(os.path.join("saved_pdf", file))
    st.success("Document cleared successfully!")
