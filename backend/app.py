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

# Full path to Potrace executable
POTRACE_PATH = r"C:\Program Files\potrace\potrace.exe"

@app.route("/", methods=["GET"])
def home():
    return "✅ Flask server is running!"

@app.route("/convert", methods=["POST"])
def convert_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = os.path.splitext(file.filename)[0] or "uploaded"
    bmp_path = os.path.join(UPLOAD_FOLDER, filename + ".bmp")

    # Step 1: Convert uploaded image to 1-bit BMP (black-and-white)
    try:
        img = Image.open(file)
        img = img.convert("1")  # 1-bit black and white
        img.save(bmp_path)
    except Exception as e:
        return jsonify({"error": f"Image processing error: {str(e)}"}), 500

    # Step 2: Check if Potrace exists
    if not os.path.exists(POTRACE_PATH):
        return jsonify({"error": f"Potrace executable not found at {POTRACE_PATH}"}), 500

    # Step 3: Run Potrace to generate SVG
    svg_path = os.path.join(VECTOR_FOLDER, filename + ".svg")
    try:
        subprocess.run(
            [POTRACE_PATH, "-s", "-o", svg_path, bmp_path],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Potrace error: {e.stderr}"}), 500

    return jsonify({"vector_file": filename + ".svg"}), 200

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(VECTOR_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
