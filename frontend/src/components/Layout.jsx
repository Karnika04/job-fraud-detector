import React from "react";
import { NavLink } from "react-router-dom";

export function Layout({ children }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Job Fraud Detection</h1>
        <nav className="nav-links">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `nav-link ${isActive ? "nav-link-active" : ""}`
            }
          >
            Home
          </NavLink>
          <NavLink
            to="/checker"
            className={({ isActive }) =>
              `nav-link ${isActive ? "nav-link-active" : ""}`
            }
          >
            Job Checker
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) =>
              `nav-link ${isActive ? "nav-link-active" : ""}`
            }
          >
            History
          </NavLink>
        </nav>
      </header>
      <main className="app-main">{children}</main>
    </div>
  );
}

