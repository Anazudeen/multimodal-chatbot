import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";
import { useState } from "react";

export default function App() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadedPDF, setUploadedPDF] = useState(null);
  const [answer, setAnswer] = useState("");

  return (
    <div style={styles.main}>
      {/* LEFT SIDE */}
      <div style={styles.left}>
        <FileUpload 
          setUploadedImage={setUploadedImage} 
          setUploadedPDF={setUploadedPDF}
        />

        <ChatBox 
          uploadedImage={uploadedImage} 
          uploadedPDF={uploadedPDF}
          setAnswer={setAnswer}
        />
      </div>

      {/* RIGHT SIDE */}
      <div style={styles.right}>
        <h2 style={styles.answerTitle}>🤖 AI Response</h2>
        <div style={styles.answerBox}>{answer || "Ask something..."}</div>
      </div>
    </div>
  );
}

const styles = {
  main: {
    display: "flex",
    height: "100vh",
    background: "#f5f6ff",
    fontFamily: "Inter, sans-serif",
  },
  left: {
    width: "40%",
    padding: "20px",
    borderRight: "1px solid #ddd",
  },
  right: {
    width: "60%",
    padding: "20px",
  },
  answerTitle: {
    marginBottom: "10px",
  },
  answerBox: {
    background: "#fff",
    borderRadius: "12px",
    padding: "20px",
    height: "90%",
    overflowY: "auto",
    border: "1px solid #ddd",
  },
};
