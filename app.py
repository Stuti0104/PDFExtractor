from flask import Flask, request, jsonify, render_template
from extract_text import extract_text_by_page, summarize_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    """Handles PDF upload, extracts text from a specific page, and summarizes it."""
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400
    
    pdf_file = request.files['pdf']
    page_number = int(request.form.get('page', 0))  # Get page number, default to 0

    text = extract_text_by_page(pdf_file, page_number)
    summary = summarize_text(text)

    return jsonify({"page": page_number, "summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
