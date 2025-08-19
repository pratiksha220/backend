import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

function formatDateTime(ts) {
  const d = new Date(ts);
  if (isNaN(d)) return String(ts);
  return d.toLocaleString();
}

export default function Dashboard() {
  const [data, setData] = useState([]); // expects [{ timestamp: "...", count: 12 }, ...]
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBlinks = async () => {
      try {
        const res = await api.get("/blinks");
        const rows = Array.isArray(res.data) ? res.data : res.data?.items || [];
        setData(rows);
      } catch (e) {
        setErr("Session expired or API error.");
        localStorage.removeItem("token");
        navigate("/login", { replace: true });
      } finally {
        setLoading(false);
      }
    };
    fetchBlinks();
  }, [navigate]);

  const chartData = useMemo(
    () =>
      data.map((d) => ({
        time: formatDateTime(d.timestamp),
        count: Number(d.count ?? d.blink_count ?? 0),
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
                    <th>Date & Time</th>
                    <th>Blink Count</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, idx) => (
                    <tr key={idx}>
                      <td>{formatDateTime(row.timestamp)}</td>
                      <td>{row.count ?? row.blink_count ?? "-"}</td>
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
