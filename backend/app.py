from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import subprocess
from PIL import Image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
VECTOR_FOLDER = "vectors"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTOR_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!"

@app.route("/convert", methods=["POST"])
def convert_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = os.path.splitext(file.filename)[0]
    file_path = os.path.join(UPLOAD_FOLDER, filename + ".bmp")

    # Convert image to BMP
    try:
        img = Image.open(file)
        img = img.convert("L")  # Convert to grayscale
        img.save(file_path)
    except Exception as e:
        return jsonify({"error": f"Image processing error: {str(e)}"}), 500

    # Convert BMP to SVG using Potrace
    vector_file = os.path.join(VECTOR_FOLDER, filename + ".svg")
    command = f"potrace -s -o {vector_file} {file_path}"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        return jsonify({"error": f"Potrace error: {result.stderr}"}), 500

    return jsonify({"vector_file": filename + ".svg"}), 200

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(VECTOR_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
