import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Loader2 } from 'lucide-react';

export const ProtectedRoute = () => {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen w-full flex flex-col items-center justify-center gap-4 bg-space">
        <div className="w-16 h-16 rounded-full border-t-2 border-cyan animate-spin neon-border" />
        <p className="text-cyan font-mono animate-pulse uppercase tracking-widest text-sm">
          Verifying Neural Identity...
        </p>
      </div>
    );
  }

  // If not authenticated, redirect to login but save the current location
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If user is authenticated but doesn't have a profile in Firestore, redirect to onboarding
  if (user.needsOnboarding && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />;
  }

  return <Outlet />;
};
