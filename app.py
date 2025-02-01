import os
import logging
from flask import Flask, request, jsonify
import pdfplumber
from transformers import pipeline

import os

port = int(os.getenv("PORT", 5000))  # Use PORT from environment, default to 5000
app.run(host="0.0.0.0", port=port)

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", trust_remote_code=True)

print("Model loaded successfully!")

app = Flask(__name__)

# Set the path for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Log file uploads and summarization process
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    """Render the homepage with a form to upload PDFs."""
    return '''
        <html>
            <head><title>PDF Summarizer</title></head>
            <body>
                <h1>Upload a PDF to Summarize</h1>
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <input type="file" name="pdf" required><br><br>
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handles PDF uploads and returns a compressed summary."""
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded PDF
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)
    logging.debug(f"Saved PDF: {pdf_path}")
    
    # Extract text from PDF
    extracted_text = extract_text(pdf_path)
    logging.debug("Text extracted from PDF.")

    # Split the extracted text into smaller chunks
    chunk_size = 1000  # Adjust based on content size
    chunks = [extracted_text[i:i + chunk_size] for i in range(0, len(extracted_text), chunk_size)]
    
    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    
    # Paginate summaries and return as a JSON response
    return jsonify({'summaries': summaries, 'total_pages': len(summaries)})


def extract_text(pdf_path):
    """Extract text from the uploaded PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
        extracted_text = ' '.join(pages)
    return extracted_text

if __name__ == "__main__":
    app.run(debug=True)
