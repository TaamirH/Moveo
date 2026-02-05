import { useEffect } from "react";
import { useDashboard } from "../hooks/useDashboard";

const FeedbackButtons = ({ onVote }) => (
  <div className="feedback">
    <button type="button" onClick={() => onVote(true)}>
      👍
    </button>
    <button type="button" onClick={() => onVote(false)}>
      👎
    </button>
  </div>
);

const Dashboard = ({ onLogout, userName }) => {
  const { dashboard, loading, loadDashboard, sendFeedback } = useDashboard();

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading || !dashboard) {
    return <div className="card">Loading your dashboard...</div>;
  }

  const { news, prices, ai_insight, ai_source, meme } = dashboard;

  return (
    <div className="dashboard">
      <header className="topbar">
        <div>
          <h1>Daily Crypto Brief</h1>
          {userName && <p className="muted">Welcome back, {userName}.</p>}
        </div>
        <button className="link" type="button" onClick={onLogout}>
          Logout
        </button>
      </header>
      <div className="grid">
        <section className="card">
          <h3>Market News</h3>
          <ul className="list">
            {news.map((item) => (
              <li key={item.url}>
                <a href={item.url} target="_blank" rel="noreferrer">
                  {item.title}
                </a>
                <span className="muted">{item.source}</span>
              </li>
            ))}
          </ul>
          <FeedbackButtons
            onVote={(vote) =>
              sendFeedback({
                content_type: "news",
                content_id: news[0]?.url || "news",
                vote
              })
            }
          />
        </section>
        <section className="card">
          <h3>Coin Prices</h3>
          <ul className="list">
            {Object.entries(prices).map(([coin, data]) => (
              <li key={coin}>
                <strong>{coin.toUpperCase()}</strong>
                <span>${data.usd ?? "N/A"}</span>
              </li>
            ))}
          </ul>
          <FeedbackButtons
            onVote={(vote) =>
              sendFeedback({ content_type: "prices", content_id: "prices", vote })
            }
          />
        </section>
        <section className="card">
          <h3>AI Insight</h3>
          <p>{ai_insight}</p>
          <p className="muted">Source: {ai_source}</p>
          <FeedbackButtons
            onVote={(vote) =>
              sendFeedback({ content_type: "ai", content_id: ai_insight.slice(0, 50), vote })
            }
          />
        </section>
        <section className="card">
          <h3>Crypto Meme</h3>
          <div className="meme">
            <img src={meme.url} alt={meme.title} />
            <p className="muted">{meme.title}</p>
            <p className="muted">Source: {meme.source}</p>
          </div>
          <FeedbackButtons
            onVote={(vote) =>
              sendFeedback({ content_type: "meme", content_id: meme.url, vote })
            }
          />
        </section>
      </div>
      <button className="secondary" type="button" onClick={loadDashboard}>
        Refresh Dashboard
      </button>
    </div>
  );
};

export default Dashboard;
