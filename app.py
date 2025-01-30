from flask import Flask, request, render_template, jsonify
import os
from extract_text import extract_text, summarize_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text
    extracted_text = extract_text(file_path)
    summary = summarize_text(extracted_text)

    return jsonify({"extracted_text": extracted_text, "summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
