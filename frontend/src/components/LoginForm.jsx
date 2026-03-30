import React, { useState } from 'react';
import { Fingerprint, Mail, Lock, Loader2 } from 'lucide-react';

export const LoginForm = ({ onSubmit, isLoading, errorMessage }) => {
   const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!email) newErrors.email = 'Neural ID Required';
    else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = 'Invalid ID format';
    
    if (!password) newErrors.password = 'Secure Key Required';
    else if (password.length < 6) newErrors.password = 'Min 6 characters';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

   const handleSubmit = (e) => {
    e.preventDefault();
    if (validate() && !isLoading) {
      onSubmit(email, password, isRegistering);
    }
  };

  return (
    <div className="glass-panel w-full max-w-md mx-auto animate-fade-in">
      <div className="flex flex-col items-center mb-10">
        <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mb-6 gold-border-active">
          <Fingerprint className="text-gold" size={36} strokeWidth={1.5} />
        </div>
         <h2 className="text-3xl font-bold text-white tracking-widest text-center">
          {isRegistering ? 'New Identity' : 'Identity Nexus'}
        </h2>
        <div className="w-12 h-px bg-gold/30 mt-4 mb-2" />
        <p className="text-dim text-xs uppercase tracking-[0.2em] font-mono">
          {isRegistering ? 'Initialize Neural Link' : 'Authenticate Neural Link'}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-6">
        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono uppercase text-gold/60 tracking-widest ml-1">Universal ID</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-dim" size={17} strokeWidth={1.5} />
            <input
              type="email"
              placeholder="archivist@nexus.org"
              className={`neon-input !pl-12 ${errors.email ? 'error' : ''}`}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
            />
          </div>
          {errors.email && <span className="text-error ml-1">{errors.email}</span>}
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono uppercase text-gold/60 tracking-widest ml-1">Access Key</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-dim" size={17} strokeWidth={1.5} />
            <input
              type="password"
              placeholder="••••••••"
              className={`neon-input !pl-12 ${errors.password ? 'error' : ''}`}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
            />
          </div>
          {errors.password && <span className="text-error ml-1">{errors.password}</span>}
        </div>

        {errorMessage && (
          <div className="p-4 bg-red-950/20 border border-red-900/30 rounded text-red-100 text-xs text-center font-mono uppercase tracking-tight">
            Authentication Error: {errorMessage}
          </div>
        )}

         <button
          type="submit"
          disabled={isLoading}
          className="btn-primary mt-6"
        >
          {isLoading ? (
            <>
              <Loader2 className="animate-spin" size={18} />
              <span>{isRegistering ? 'Initializing...' : 'Linking...'}</span>
            </>
          ) : (
            <span>{isRegistering ? 'Register Entity' : 'Initiate Connection'}</span>
          )}
        </button>
      </form>

      <div className="mt-8 text-center">
        <button
          type="button"
          onClick={() => setIsRegistering(!isRegistering)}
          className="text-[10px] uppercase tracking-widest text-gold/40 hover:text-gold transition-colors font-mono"
        >
          {isRegistering 
            ? 'Already have an ID? Switch to Authenticate' 
            : "Don't have an ID? Initialize New Soul"}
        </button>
      </div>

      <div className="mt-10 pt-6 border-t border-white/5 text-center">
        <p className="text-dim text-[10px] uppercase tracking-widest">
          Secured by <span className="text-gold/60">Arcane protocols</span>
        </p>
      </div>
    </div>
  );
};

