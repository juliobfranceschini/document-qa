import streamlit as st
from openai import OpenAI
import PyPDF2

# Função para extrair texto de arquivos PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
    return text

# Show title and description
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via st.text_input
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via st.file_uploader
    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .md, or .pdf)", type=("txt", "md", "pdf")
    )

    # Ask the user for a question via st.text_area
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question
        if uploaded_file.type == "application/pdf":
            document = extract_text_from_pdf(uploaded_file)
        else:
            document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using st.write_stream
        st.write_stream(stream)
