import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  }
});

export async function healthCheck() {
  const res = await apiClient.get("/health");
  return res.data;
}

export async function predictJob(payload) {
  const res = await apiClient.post("/predict", payload);
  return res.data;
}

export async function fetchHistory(params = {}) {
  const res = await apiClient.get("/history", { params });
  return res.data;
}

