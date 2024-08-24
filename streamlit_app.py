import streamlit as st
import PyPDF2
import logging
from dotenv import load_dotenv
import os

def main():
    load_dotenv()  # Load environment variables from .env file

    st.set_page_config(page_title="Chatting is fun when you get to chat with your favorite books!", page_icon=":books:")

    st.header("Chat with multiple PDFs! :books:")
    query = st.text_input("Ask about the current document:")

    api_key = os.getenv("API_KEY")  # Access your environment variable
    st.sidebar.write(f"Using API Key: {api_key}")  # Optional: Display the key (for testing purposes)

    with st.sidebar:
        st.subheader("Your Docs")
        uploaded_files = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True, type=['pdf'])
        if st.button("Process"):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    try:
                        process_pdf(uploaded_file)
                    except Exception as e:
                        logging.error(f"Error processing file {uploaded_file.name}: {e}")
                        st.error(f"An error occurred while processing the file: {e}")
            else:
                st.write("No files uploaded.")

def process_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
        all_text = ""
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            all_text += page.extract_text()

        st.write(f"Text from {uploaded_file.name}:")
        st.text_area("", all_text, height=300)
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        logging.error(f"Failed to process PDF: {e}")

if __name__ == '__main__':
    main()
