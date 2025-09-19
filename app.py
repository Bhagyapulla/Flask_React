from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask Backend is Running!"

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))  # Render gives PORT, else fallback 5000
    app.run(host="0.0.0.0", port=port, debug=True)
