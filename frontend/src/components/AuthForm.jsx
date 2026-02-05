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
        await onRegister(form);
      }
    } catch (err) {
      setError("Authentication failed. Please try again.");
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
