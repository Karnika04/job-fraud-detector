import React from "react";
import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <div className="card">
      <div className="hero-banner">
        <div>
          <div className="badge badge-success">Production-ready ML pipeline</div>
          <h2 className="hero-title">Online Job Fraud Detection Platform</h2>
          <p className="hero-subtitle">
            Detect fraudulent job postings in real time using machine learning, NLP,
            explainable AI, and rule-based checks.
          </p>
          <div style={{ display: "flex", gap: 12 }}>
            <Link to="/checker" className="btn-primary">
              Check Job Authenticity
            </Link>
            <Link to="/history" className="nav-link nav-link-active">
              View History
            </Link>
          </div>
        </div>
        <div className="hero-metrics">
          <div className="hero-metric-card">
            <div className="hero-metric-label">Explainability</div>
            <div className="hero-metric-value">SHAP</div>
            <div className="hero-metric-caption">
              Top contributing words for each prediction.
            </div>
          </div>
          <div className="hero-metric-card">
            <div className="hero-metric-label">Rule engine</div>
            <div className="hero-metric-value">Hybrid</div>
            <div className="hero-metric-caption">
              Keyword rules combined with ML outputs.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

