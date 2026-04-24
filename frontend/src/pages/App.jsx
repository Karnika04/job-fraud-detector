import React from "react";
import { Routes, Route } from "react-router-dom";
import { Layout } from "../components/Layout";
import { HomePage } from "./HomePage";
import { JobCheckerPage } from "./JobCheckerPage";
import { HistoryPage } from "./HistoryPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/checker" element={<JobCheckerPage />} />
        <Route path="/history" element={<HistoryPage />} />
      </Routes>
    </Layout>
  );
}

