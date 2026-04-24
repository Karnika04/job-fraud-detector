import React, { useEffect, useState } from "react";
import { fetchHistory } from "../services/api";

export function HistoryPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError("");
      try {
        const data = await fetchHistory({ limit: 100 });
        setItems(data.items || []);
      } catch (err) {
        setError("Unable to load history. Please ensure the backend and database are running.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="card">
      <h2>Analysis History</h2>
      <p className="card-subtitle">
        Recent jobs that have been analyzed by the fraud detection engine.
      </p>
      {loading && <p className="text-muted">Loading...</p>}
      {error && <p className="text-muted" style={{ color: "#f97373" }}>{error}</p>}
      {!loading && !error && items.length === 0 && (
        <p className="text-muted">No history yet. Analyze a job to see it here.</p>
      )}
      {!loading && items.length > 0 && (
        <div style={{ overflowX: "auto" }}>
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Prediction</th>
                <th>Fraud probability</th>
                <th>Rule score</th>
                <th>Checked at</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.title || <span className="text-muted">Untitled</span>}</td>
                  <td>
                    <span
                      className={
                        item.prediction === "Fraud" ? "chip badge-danger" : "chip badge-success"
                      }
                    >
                      {item.prediction}
                    </span>
                  </td>
                  <td>{(item.fraud_probability * 100).toFixed(0)}%</td>
                  <td>{item.rule_score}</td>
                  <td>{new Date(item.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

