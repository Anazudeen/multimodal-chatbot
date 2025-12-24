import { askLLM } from "../api";
import { useState } from "react";

export default function ChatBox({ uploadedImage, setAnswer }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!query.trim()) return;

    setLoading(true);

    try {
      const res = await askLLM(query, uploadedImage);
      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("⚠️ Error: Could not reach the model.");
    }

    setLoading(false);
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>💬 Ask Something</h3>

      <textarea
        style={styles.textarea}
        placeholder="Type your question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button style={styles.button} onClick={send} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>
    </div>
  );
}

const styles = {
  container: {
    padding: "20px",
    background: "#fff",
    borderRadius: "14px",
    border: "1px solid #ddd",
  },
  title: {
    marginBottom: "10px",
  },
  textarea: {
    width: "100%",
    height: "120px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #ccc",
    resize: "none",
    outline: "none",
    marginBottom: "10px",
    fontSize: "15px",
  },
  button: {
    width: "100%",
    padding: "12px",
    borderRadius: "10px",
    border: "none",
    background: "#4f46e5",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
  },
};
