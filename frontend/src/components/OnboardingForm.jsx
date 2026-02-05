import { useState } from "react";
import api from "../api/client";

const INVESTOR_TYPES = ["HODLer", "Day Trader", "NFT Collector", "DeFi Farmer", "Casual"];
const CONTENT_TYPES = ["Market News", "Charts", "Social", "Fun", "Tech"];

const OnboardingForm = ({ onComplete }) => {
  const [investorType, setInvestorType] = useState(INVESTOR_TYPES[0]);
  const [assets, setAssets] = useState("");
  const [content, setContent] = useState(["Market News"]);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const toggleContent = (item) => {
    setContent((prev) =>
      prev.includes(item) ? prev.filter((c) => c !== item) : [...prev, item]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      const payload = {
        investor_type: investorType,
        interested_assets: assets.split(",").map((a) => a.trim()).filter(Boolean),
        content_preferences: content
      };
      await api.post("/onboarding", payload);
      onComplete();
    } catch (err) {
      setError("Could not save preferences. Try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="card">
      <h2>Tell us about you</h2>
      <p className="muted">This helps tailor your daily dashboard.</p>
      <form className="form" onSubmit={handleSubmit}>
        <label>
          Favorite assets (comma-separated)
          <input
            value={assets}
            onChange={(e) => setAssets(e.target.value)}
            placeholder="BTC, ETH, SOL"
          />
          <span className="muted">Use popular tickers like BTC, ETH, SOL, ADA.</span>
        </label>
        <label>
          Investor type
          <select value={investorType} onChange={(e) => setInvestorType(e.target.value)}>
            {INVESTOR_TYPES.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>
        <fieldset>
          <legend>Content preferences</legend>
          <div className="chip-grid">
            {CONTENT_TYPES.map((item) => (
              <button
                key={item}
                type="button"
                className={content.includes(item) ? "chip active" : "chip"}
                onClick={() => toggleContent(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </fieldset>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="primary" disabled={saving}>
          {saving ? "Saving..." : "Save Preferences"}
        </button>
      </form>
    </div>
  );
};

export default OnboardingForm;
