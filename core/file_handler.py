import tempfile
import os

def save_uploaded_file(uploaded_file):
    """Saves the uploaded Streamlit file to a temp path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name

def remove_file(file_path):
    """Cleans up the file after processing."""
    if os.path.exists(file_path):
        os.unlink(file_path)