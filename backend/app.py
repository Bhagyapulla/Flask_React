from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import subprocess
from PIL import Image
import shutil

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
VECTOR_FOLDER = "vectors"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTOR_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return "✅ Flask server is running!"

@app.route("/convert", methods=["POST"])
def convert_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = os.path.splitext(file.filename)[0] or "uploaded"
    file_path = os.path.join(UPLOAD_FOLDER, filename + ".bmp")

    # Step 1: Convert image to BMP
    try:
        img = Image.open(file)
        img = img.convert("L")  # grayscale
        img.save(file_path)
    except Exception as e:
        return jsonify({"error": f"Image processing error: {str(e)}"}), 500

    # Step 2: Check Potrace availability
    potrace_path = shutil.which("potrace")
    if not potrace_path:
        return jsonify({"error": "Potrace not found. Please install or add to PATH."}), 500

    # Step 3: Run Potrace
    vector_file = os.path.join(VECTOR_FOLDER, filename + ".svg")
    try:
        result = subprocess.run(
            [potrace_path, "-s", "-o", vector_file, file_path],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Potrace error: {e.stderr}"}), 500
    except FileNotFoundError:
        return jsonify({"error": f"Potrace executable not found at {potrace_path}"}), 500

    return jsonify({"vector_file": filename + ".svg"}), 200

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(VECTOR_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
