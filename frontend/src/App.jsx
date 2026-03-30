import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginForm } from './components/LoginForm';
import { Lobby } from './pages/Lobby';
import { OnboardingPage } from './pages/OnboardingPage';
import { CombatArena } from './components/CombatArena';
import { Library } from 'lucide-react';

const AppContent = () => {
  const { login, register, isLoading, error } = useAuth();
  const [currentSession, setCurrentSession] = useState(null);
  const navigate = useNavigate();

  const handleAuth = async (email, password, isRegistering) => {
    try {
      if (isRegistering) {
        await register(email, password);
      } else {
        await login(email, password);
      }
      navigate('/lobby');
    } catch (err) {
      console.error("Auth failed:", err);
    }
  };

  const handleStartGame = (session) => {
    setCurrentSession(session);
    navigate('/arena');
  };

  const handleFlee = () => {
    setCurrentSession(null);
    navigate('/lobby');
  };

  return (
    <main className="min-h-screen bg-space text-main selection:bg-gold/20 flex flex-col items-center justify-center p-4">
      
      {/* Global Background Header Overlay */}
      <div className="fixed top-4 right-8 flex items-center gap-2 text-gold/30 z-50 font-mono">
        <Library size={14} strokeWidth={1.5} />
        <span className="text-[9px] uppercase tracking-[0.3em]">Nexus Archives • v0.1.2</span>
      </div>


      <Routes>
        <Route 
          path="/login" 
          element={<LoginForm onSubmit={handleAuth} isLoading={isLoading} errorMessage={error} />} 
        />
        
        <Route element={<ProtectedRoute />}>
          <Route 
            path="/lobby" 
            element={<Lobby onStartGame={handleStartGame} />} 
          />
          <Route 
            path="/arena" 
            element={currentSession ? (
              <CombatArena initialSession={currentSession} onFlee={handleFlee} />
            ) : (
              <Navigate to="/lobby" replace />
            )} 
          />
        </Route>

        {/* Root redirect */}
        <Route path="*" element={<Navigate to="/lobby" replace />} />
      </Routes>
    </main>
  );
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
