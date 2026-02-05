import { useState } from "react";
import api from "../api/client";

export const useDashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/dashboard");
      setDashboard(data);
    } finally {
      setLoading(false);
    }
  };

  const sendFeedback = async ({ content_type, content_id, vote }) => {
    await api.post("/feedback", { content_type, content_id, vote });
  };

  return { dashboard, loading, loadDashboard, sendFeedback };
};
