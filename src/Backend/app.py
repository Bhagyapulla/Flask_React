from flask import Flask, request, jsonify
import os
import subprocess  # Import subprocess to call Potrace
from PIL import Image  # To convert PNG to BMP

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "✅ Backend is running!"

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "✅ File uploaded successfully!", "file_path": file_path})

@app.route("/convert", methods=["POST"])
def convert_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Convert PNG to BMP (Potrace only works with BMP)
    bmp_file_path = file_path.replace(".png", ".bmp")
    img = Image.open(file_path)
    img.convert("L").save(bmp_file_path)  # Convert to grayscale BMP

    # Use Potrace to convert BMP to SVG
    svg_file_path = file_path.replace(".png", ".svg")
    command = f"potrace -b svg -o {svg_file_path} {bmp_file_path}"
    subprocess.run(command, shell=True, check=True)

    return jsonify({"message": "✅ Conversion successful!", "vector_file": svg_file_path})

if __name__ == "__main__":
    app.run(debug=True)

