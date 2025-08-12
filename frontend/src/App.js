import React, { useEffect, useMemo, useState } from "react";
import { api } from "./api";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [status, setStatus] = useState("Connecting…");
  const apiBase = useMemo(
    () => process.env.REACT_APP_API_URL || "https://fxgsyc-5000.csb.app",
    []
  );

  // Initial load
  useEffect(() => {
    (async () => {
      try {
        const health = await api.get("/api/health");
        setStatus(`API: ${health.status} (${apiBase})`);
        const list = await api.get("/api/messages");
        setMessages(list);
      } catch (e) {
        setStatus(`Error: ${e.message}`);
      }
    })();
  }, [apiBase]);

  async function sendMessage(e) {
    e.preventDefault();
    const t = text.trim();
    if (!t) return;
    try {
      const created = await api.post("/api/messages", { text: t });
      setMessages((prev) => [...prev, created]);
      setText("");
    } catch (e) {
      alert(e.message);
    }
  }

  return (
    <div
      style={{
        maxWidth: 640,
        margin: "2rem auto",
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <h1>Messages: React ↔ Flask (GET + POST)</h1>
      <p style={{ opacity: 0.8 }}>{status}</p>

      <form
        onSubmit={sendMessage}
        style={{
          display: "grid",
          gridTemplateColumns: "1fr auto",
          gap: 8,
          margin: "1rem 0",
        }}
      >
        <input
          placeholder="Type a message..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{ padding: 10 }}
        />
        <button type="submit">Send</button>
      </form>

      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: 0,
          display: "grid",
          gap: 8,
        }}
      >
        {messages.map((m) => (
          <li
            key={m.id}
            style={{ border: "1px solid #ddd", borderRadius: 8, padding: 10 }}
          >
            <strong>#{m.id}</strong> — {m.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
