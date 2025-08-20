import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

export default function Dashboard() {
  const [data, setData] = useState([]); // expects [{ date: "...", blink_count: 12 }, ...]
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");
  const navigate = useNavigate();

  // Fetch blink data
  const fetchBlinks = async () => {
    setLoading(true);
    try {
      const res = await api.get("/blink_data", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setData(res.data?.data || []);
    } catch (e) {
      setErr("Session expired or API error.");
      localStorage.removeItem("token");
      navigate("/login", { replace: true });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBlinks();
  }, [navigate]);

  // Handle blink increment
  const handleBlink = async () => {
    try {
      await api.post("/blink", {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      fetchBlinks(); // refresh data
    } catch (e) {
      console.error("Error adding blink", e);
    }
  };

  const chartData = useMemo(
    () =>
      data.map((d) => ({
        time: d.date,
        count: Number(d.blink_count ?? 0),
      })),
    [data]
  );

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">Blink Tracker</div>
        <button
          className="secondary"
          onClick={() => {
            localStorage.removeItem("token");
            navigate("/login", { replace: true });
          }}
        >
          Logout
        </button>
      </header>

      <main className="content">
        <section className="card">
          <div className="section-head">
            <h2 className="section-title">Blink Counts Over Time</h2>
            <button onClick={handleBlink} className="primary">Add Blink</button>
          </div>
          {loading ? (
            <div className="muted">Loading chart…</div>
          ) : chartData.length === 0 ? (
            <div className="muted">No data found.</div>
          ) : (
            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={chartData} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" minTickGap={28} />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="count" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </section>

        <section className="card">
          <div className="section-head">
            <h2 className="section-title">Blink Data Table</h2>
          </div>
          {loading ? (
            <div className="muted">Loading table…</div>
          ) : (
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Blink Count</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, idx) => (
                    <tr key={idx}>
                      <td>{row.date}</td>
                      <td>{row.blink_count ?? "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
