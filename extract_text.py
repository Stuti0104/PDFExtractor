import pdfplumber
from transformers import pipeline

# Load Hugging Face's BERT-based summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_by_page(pdf_file, page_number):
    """Extract text from a specific page of a PDF."""
    with pdfplumber.open(pdf_file) as pdf:
        if page_number < len(pdf.pages):
            text = pdf.pages[page_number].extract_text()
            if text:
                return text
    return "No text found on this page."

def summarize_text(text, max_length=500, min_length=100):
    """Summarize the extracted text using BERT-based summarization."""
    if len(text) < min_length:
        return text  # If text is too short, return as is

    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
