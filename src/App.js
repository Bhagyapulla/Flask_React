import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import collegeLogo from "./shrignanambica.jpeg";

function App() {
  const [image, setImage] = useState(null);
  const [convertedFile, setConvertedFile] = useState(null);
  const [format, setFormat] = useState("svg");
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        alert("Please upload a valid image file!");
        return;
      }
      setImage(file);
    }
  };

  const handleConvert = async () => {
    if (!image) {
      alert("Please upload an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("format", format);

    setLoading(true);
    setConvertedFile(null);

    try {
      const response = await axios.post(`${API_URL}/convert`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Conversion Successful! Download your file below.");
      setConvertedFile(response.data.vector_file);
    } catch (error) {
      console.error("Error converting image:", error);
      alert(
        `Conversion failed! ${error.response?.data?.message || "Check console for details."}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container fade-in">
      <div className="header slide-down">
        <img src={collegeLogo} alt="Shrignanabbica college Logo" className="college-logo rotate-in" />
        <h1 className="title scale-in">Image File Conversion</h1>
        <p className="subtitle zoom-in">
          <strong>Convert, optimize, and enhance your images effortlessly!</strong>
        </p>
      </div>

      <div className="content-wrapper slide-up">
        <div className="file-format-wrapper">
          <div className="file-input-container">
            <label htmlFor="file">Choose Image File:</label>
            <input
              type="file"
              id="file"
              accept="image/*"
              onChange={handleImageUpload}
            />
            <p className="file-size-info">Max size: 1GB</p>
          </div>

          <div className="format-select-container">
            <label htmlFor="format">Select Output Format:</label>
            <select
              id="format"
              value={format}
              onChange={(e) => setFormat(e.target.value)}
            >
              <option value="svg">SVG</option>
              <option value="eps">EPS</option>
              <option value="pdf">PDF</option>
            </select>
          </div>
        </div>

        {image && (
          <img
            src={URL.createObjectURL(image)}
            alt="Uploaded Preview"
            className="preview fade-in"
          />
        )}

        <button
          className={`convert-btn ${loading ? "pulse" : "bounce"}`}
          onClick={handleConvert}
          disabled={loading}
        >
          {loading ? "Converting..." : "Convert"}
        </button>

        {convertedFile && (
          <a
            href={`${API_URL}/download/${convertedFile}`}
            download
            className="download-btn shine"
          >
            Download Converted File
          </a>
        )}
      </div>
    </div>
  );
}

export default App;