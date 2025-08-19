import axios from "axios";

const api = axios.create({
  baseURL:  "https://web-production-f83f0.up.railway.app",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
