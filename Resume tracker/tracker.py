import streamlit as st
import fitz  # PyMuPDF
import re
from docx import Document  # Ensure 'python-docx' is installed

# Placeholder for AI integration (Mock Analysis Function)
def analyze_resume(api_key, text):
    """
    Simulates AI-powered resume analysis.
    Replace this with actual API integration for advanced insights.
    """
    return {
        "Extracted Skills": ["Python", "AI", "Streamlit", "Machine Learning", "Data Analysis"],
        "Identified Keywords": ["Resume", "ATS", "Collaboration", "Problem-Solving"],
        "Missing Keywords": ["Leadership", "Teamwork", "Project Management"],
        "Tailored Recommendations": [
            "Add leadership roles or examples.",
            "Include specific achievements in past projects.",
            "Use keywords like 'strategic planning' and 'team collaboration'.",
        ],
    }

# API Key for AI Integration
API_KEY = "api key"

# Preprocess the extracted text
def clean_text(text):
    """
    Cleans and structures the extracted text.
    Groups sentences into paragraphs and ensures proper formatting.
    """
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    paragraphs = []
    current_paragraph = []

    # Group sentences into paragraphs
    for sentence in sentences:
        current_paragraph.append(sentence.strip())
        if len(current_paragraph) >= 3:  # Group sentences into chunks of 3
            paragraphs.append(". ".join(current_paragraph) + ".")
            current_paragraph = []

    # Append any remaining sentences as a paragraph
    if current_paragraph:
        paragraphs.append(". ".join(current_paragraph) + ".")

    return paragraphs

# Set custom CSS
def local_css(file_name):
    """
    Loads local CSS for custom styling of the Streamlit app.
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS (Ensure 'style.css' exists in the same directory)
local_css("style.css")

# Streamlit App Layout
st.markdown("<h1>R - Resume ATS Tracker</h1>", unsafe_allow_html=True)
st.markdown("<h3>Your AI-powered career partner for job applications</h3>", unsafe_allow_html=True)

# File Upload Section
st.markdown('<div class="file-upload">Drag and drop your Resume (PDF, Text, or DOCX) or click to upload</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf", "text", "docx"])

if uploaded_file:
    st.markdown('<div class="results"><h3>Resume Analysis Results</h3>', unsafe_allow_html=True)

    # Extract Text Based on File Type
    file_type = uploaded_file.name.split(".")[-1]  # Get the file extension
    text = ""

    if file_type == "pdf":
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif file_type == "text":
        text = uploaded_file.read().decode("utf-8")  # Read and decode text file
    elif file_type == "docx":
        doc = Document(uploaded_file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

    # Clean and Display Extracted Text as Paragraphs
    st.write("### Extracted Resume Data")
    paragraphs = clean_text(text)
    for idx, paragraph in enumerate(paragraphs, 1):  # Enumerate paragraphs
        st.markdown(f"**Paragraph {idx}:** {paragraph}")

    # Analyze Resume
    st.write("### Processing your resume...")
    insights = analyze_resume(API_KEY, text)

    # Display Insights
    st.markdown("#### Resume Analysis Insights")
    for key, value in insights.items():
        st.markdown(f"**{key}:**")
        if isinstance(value, list):
            for item in value:
                st.markdown(f"- {item}")
        else:
            st.markdown(f"- {value}")

    # Dynamic addition of new insights
    st.markdown("---")
    st.markdown("**💡 Add new data below:**")
    new_data = st.text_input("Enter new data:")
    if st.button("Add Data"):
        st.markdown(f"- {new_data}")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<footer>🔒 We respect your privacy. Your data is not stored.</footer>", unsafe_allow_html=True)
