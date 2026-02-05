import { useEffect, useState } from "react";
import api, { setAuthToken } from "../api/client";

const TOKEN_KEY = "crypto_token";

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const saveToken = (token) => {
    localStorage.setItem(TOKEN_KEY, token);
    setAuthToken(token);
  };

  const clearToken = () => {
    localStorage.removeItem(TOKEN_KEY);
    setAuthToken(null);
  };

  const fetchMe = async () => {
    try {
      const { data } = await api.get("/auth/me");
      setUser(data);
    } catch (err) {
      clearToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      setAuthToken(token);
      fetchMe();
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (payload) => {
    const { data } = await api.post("/auth/login", payload);
    saveToken(data.access_token);
    await fetchMe();
  };

  const register = async (payload) => {
    const { data } = await api.post("/auth/register", payload);
    saveToken(data.access_token);
    await fetchMe();
  };

  const logout = () => {
    clearToken();
    setUser(null);
  };

  return { user, loading, login, register, logout, refresh: fetchMe };
};
