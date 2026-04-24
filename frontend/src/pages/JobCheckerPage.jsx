import React, { useState } from "react";
import { predictJob } from "../services/api";

export function JobCheckerPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [companyProfile, setCompanyProfile] = useState("");
  const [requirements, setRequirements] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const data = await predictJob({
        title,
        description,
        company_profile: companyProfile,
        requirements
      });
      setResult(data);
    } catch (err) {
      setError("Failed to analyze job. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  const probabilityPercent = result ? Math.round(result.fraud_probability * 100) : 0;

  return (
    <div className="card">
      <h2>Job Checker</h2>
      <p className="card-subtitle">
        Paste a job posting to check whether it is likely to be real or fraudulent.
      </p>
      <div className="grid-2">
        <form onSubmit={handleSubmit}>
          <div className="field-group">
            <label className="field-label">Job title</label>
            <input
              className="input"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Remote Data Entry Specialist"
            />
          </div>
          <div className="field-group">
            <label className="field-label">Job description</label>
            <textarea
              className="textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Paste the main job description here..."
            />
          </div>
          <div className="field-group">
            <label className="field-label">Company profile (optional)</label>
            <textarea
              className="textarea"
              value={companyProfile}
              onChange={(e) => setCompanyProfile(e.target.value)}
              placeholder="Tell us about the company if available..."
            />
          </div>
          <div className="field-group">
            <label className="field-label">Requirements (optional)</label>
            <textarea
              className="textarea"
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
              placeholder="List the job requirements if available..."
            />
          </div>
          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Check Job Authenticity"}
          </button>
          {error && <p className="text-muted" style={{ marginTop: 8, color: "#f97373" }}>{error}</p>}
        </form>
        <div>
          <h3>Result</h3>
          {!result && (
            <p className="text-muted">
              Prediction details will appear here after you submit a job posting.
            </p>
          )}
          {result && (
            <>
              <div className="metric-row">
                <span className="metric-label">Prediction</span>
                <span className="metric-value">
                  <span
                    className={
                      result.prediction === "Fraud" ? "badge badge-danger" : "badge badge-success"
                    }
                  >
                    {result.prediction === "Fraud" ? "Likely Fraudulent" : "Likely Real"}
                  </span>
                </span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Fraud probability</span>
                <span className="metric-value">{probabilityPercent}%</span>
              </div>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${probabilityPercent}%` }}
                />
              </div>
              <div className="metric-row" style={{ marginTop: 12 }}>
                <span className="metric-label">Rule-based risk score</span>
                <span className="metric-value">{result.rule_score}</span>
              </div>
              <div style={{ marginTop: 12 }}>
                <div className="metric-label">Top contributing signals</div>
                <div className="pill-list">
                  {result.explanation && result.explanation.length > 0 ? (
                    result.explanation.map((word, idx) => (
                      <span key={idx} className="pill">
                        {word}
                      </span>
                    ))
                  ) : (
                    <span className="text-muted">No strong signals detected.</span>
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

