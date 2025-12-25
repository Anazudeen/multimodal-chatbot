export default function AnswerBox({ answer }) {
  if (!answer) return null;

  return (
    <div style={styles.container}>
      {answer.summary && (
        <>
          <h4>📄 Summary</h4>
          <p>{answer.summary}</p>
        </>
      )}

      {answer.key_points && answer.key_points.length > 0 && (
        <>
          <h4>🔑 Key Points</h4>
          <ul>
            {answer.key_points.map((point, idx) => (
              <li key={idx}>{point}</li>
            ))}
          </ul>
        </>
      )}

      {answer.answer && (
        <>
          <h4>💬 Answer</h4>
          <p>{answer.answer}</p>
        </>
      )}

      <small style={styles.meta}>
        Confidence: <b>{answer.confidence}</b>
      </small>
    </div>
  );
}

const styles = {
  container: {
    marginTop: "20px",
    padding: "20px",
    background: "#f9fafb",
    borderRadius: "14px",
    border: "1px solid #ddd",
  },
  meta: {
    display: "block",
    marginTop: "10px",
    color: "#555",
  },
};
