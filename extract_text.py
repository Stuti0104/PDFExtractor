import pdfplumber
from transformers import BertTokenizer, BertModel
from summarizer import Summarizer

def extract_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
        extracted_text = ' '.join(pages)

    return extracted_text

def summarize_text(text):
    model = Summarizer()  # Load BERT-based summarizer
    summary = model(text, ratio=0.3)  # Extract 30% of key sentences
    return summary
