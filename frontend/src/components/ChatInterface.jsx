// frontend/src/components/ChatInterface.jsx
import React, { useState } from "react";
import axios from "axios";
import "./ChatInterface.css";

export default function ChatInterface() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleSend = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResponse(null);

    try {
      const res = await axios.post("http://localhost:8000/api/chat", { query });
      setResponse(res.data);
    } catch (error) {
      console.error(error);
      setResponse({
        recommendation: "Error fetching response",
        rationale: "Please check backend connection",
        confidence: 0,
        sources: []
      });
    }
    setLoading(false);
  };

  return (
    <div className="chat-container">
      <h1>AgriAgent 🌱</h1>
      <p className="subtitle">Ask anything about your crops, weather, or market</p>

      <div className="chat-box">
        <input
          type="text"
          placeholder="Type your question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {response && (
        <div className="response-box">
          <h2>Recommendation:</h2>
          <p>{response.recommendation}</p>

          <h3>Rationale:</h3>
          <p>{response.rationale}</p>

          <h3>Confidence:</h3>
          <p>{(response.confidence * 100).toFixed(1)}%</p>

          <h3>Sources:</h3>
          <ul>
            {response.sources.map((src, index) => (
              <li key={index}>{src}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
