import AuthForm from "./components/AuthForm";
import OnboardingForm from "./components/OnboardingForm";
import Dashboard from "./components/Dashboard";
import { useAuth } from "./hooks/useAuth";

const App = () => {
  const { user, loading, login, register, logout, refresh } = useAuth();

  if (loading) {
    return <div className="page">Loading...</div>;
  }

  if (!user) {
    return (
      <div className="page">
        <AuthForm onLogin={login} onRegister={register} />
      </div>
    );
  }

  if (!user.profile) {
    return (
      <div className="page">
        <OnboardingForm onComplete={refresh} />
      </div>
    );
  }

  return (
    <div className="page">
      <Dashboard onLogout={logout} userName={user?.name} />
    </div>
  );
};

export default App;
