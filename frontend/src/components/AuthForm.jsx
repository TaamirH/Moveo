import { useState } from "react";

const AuthForm = ({ onLogin, onRegister }) => {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ email: "", name: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      if (mode === "login") {
        await onLogin({ email: form.email, password: form.password });
      } else {
        if (form.password.length < 6) {
          setError("Password must be at least 6 characters.");
          return;
        }
        if (!/[A-Z]/.test(form.password) || !/[a-z]/.test(form.password) || !/[0-9]/.test(form.password)) {
          setError("Password must include uppercase, lowercase, and a number.");
          return;
        }
        await onRegister(form);
      }
    } catch (err) {
      const message = err?.response?.data?.detail;
      setError(message || "Authentication failed. Please try again.");
    }
  };

  return (
    <div className="card auth-card">
      <h2>AI Crypto Advisor</h2>
      <p className="muted">Sign in to personalize your dashboard.</p>
      <form onSubmit={handleSubmit} className="form">
        {mode === "register" && (
          <label>
            Name
            <input name="name" value={form.name} onChange={handleChange} required />
          </label>
        )}
        <label>
          Email
          <input name="email" type="email" value={form.email} onChange={handleChange} required />
        </label>
        <label>
          Password
          <input
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
          />
        </label>
        {mode === "register" && (
          <p className="muted">At least 6 chars, with uppercase, lowercase, and a number.</p>
        )}
        {error && <p className="error">{error}</p>}
        <button type="submit" className="primary">
          {mode === "login" ? "Login" : "Create Account"}
        </button>
      </form>
      <button
        type="button"
        className="link"
        onClick={() => setMode(mode === "login" ? "register" : "login")}
      >
        {mode === "login" ? "Need an account? Register" : "Already have an account? Login"}
      </button>
    </div>
  );
};

export default AuthForm;
