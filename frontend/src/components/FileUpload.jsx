import { uploadPDF, uploadImage } from "../api";
import { useState } from "react";

export default function FileUpload({ setUploadedImage, setUploadedPDF }) {
  const [imagePreview, setImagePreview] = useState(null);
  const [pdfName, setPdfName] = useState(null);

  async function handlePDF(e) {
    const file = e.target.files[0];
    if (!file) return;

    await uploadPDF(file);
    setUploadedPDF(file.name);
    setPdfName(file.name);
  }

  async function handleImage(e) {
    const file = e.target.files[0];
    if (!file) return;

    await uploadImage(file);
    const previewURL = URL.createObjectURL(file);
    setImagePreview(previewURL);
    setUploadedImage(file.name);
  }

  return (
    <div style={styles.wrapper}>
      <h3 style={styles.title}>📤 Upload Files</h3>

      <label style={styles.button}>
        Upload PDF
        <input type="file" accept="application/pdf" hidden onChange={handlePDF} />
      </label>

      <label style={styles.button}>
        Upload Image
        <input type="file" accept="image/*" hidden onChange={handleImage} />
      </label>

      {/* PREVIEW AREA */}
      <div style={styles.preview}>
        <h4 style={{ marginBottom: "8px" }}>Uploaded Files</h4>

        {pdfName && (
          <p style={{ marginBottom: "10px" }}>
            📄 <strong>{pdfName}</strong>
          </p>
        )}

        {imagePreview && (
          <img
            src={imagePreview}
            alt="Preview"
            style={styles.imagePreview}
          />
        )}
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    padding: "20px",
    background: "#fff",
    borderRadius: "14px",
    border: "1px solid #ddd",
    marginBottom: "20px",
  },
  title: {
    marginBottom: "12px",
    fontSize: "18px",
    fontWeight: "600",
  },
  button: {
    display: "block",
    background: "#4f46e5",
    color: "white",
    padding: "12px",
    borderRadius: "10px",
    textAlign: "center",
    marginBottom: "10px",
    cursor: "pointer",
    fontWeight: "500",
  },
  preview: {
    marginTop: "15px",
  },
  imagePreview: {
    width: "150px",
    height: "150px",
    objectFit: "cover",
    borderRadius: "12px",
    border: "1px solid #ccc",
  },
};
