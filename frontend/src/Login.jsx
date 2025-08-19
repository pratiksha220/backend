import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErr("");
    setLoading(true);
    try {
      // Adjust to match your FastAPI schema/route. Common FastAPI returns: { "access_token": "...", "token_type": "bearer" }
      const res = await api.post("/auth/login", { email, password });
      const token = res.data?.access_token || res.data?.token;
      if (!token) throw new Error("Token not found in response");
      localStorage.setItem("token", token);
      navigate("/dashboard", { replace: true });
    } catch (error) {
      setErr("Invalid credentials or server error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="center">
      <form className="card" onSubmit={handleSubmit}>
        <h1 className="title">Blink Tracker Login</h1>
        {err && <div className="alert">{err}</div>}
        <label className="label" htmlFor="email">Email</label>
        <input
          id="email"
          className="input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
        />

        <label className="label" htmlFor="password">Password</label>
        <input
          id="password"
          className="input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          required
        />

        <button className="button" type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Login"}
        </button>
      </form>
    </div>
  );
}
