import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, Sparkles, Sword, Check } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';

const CLASSES = [
  { id: 'warrior', name: 'Warrior', icon: Sword, desc: 'High physical strength and defense. Born for the frontline.', color: '#ef4444' },
  { id: 'mage', name: 'Mage', icon: Sparkles, desc: 'Master of arcane arts. Low defense but immense cosmic knowledge.', color: '#3b82f6' },
  { id: 'rogue', name: 'Rogue', icon: Shield, desc: 'Agile and mysterious. Expert in shadows and critical strikes.', color: '#10b981' }
];

export const OnboardingPage = () => {
  const { user, logout } = useAuth();
  const [username, setUsername] = useState('');
  const [selectedClass, setSelectedClass] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedClass || !username) return;

    setIsSubmitting(true);
    setError(null);

    try {
      await axios.post('/api/v1/auth/onboarding', {
        username,
        character_class: selectedClass
      }, {
        headers: { Authorization: `Bearer ${user.token}` }
      });
      
      // Force reload user state if necessary or just navigate
      // Since AuthContext listens to onAuthStateChanged, we might need a manual refresh call if we don't handle it there.
      // For now, let's navigate to lobby and let the session check handle it.
      window.location.href = '/lobby';
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl w-full">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel p-8 rounded-3xl border border-white/5 relative overflow-hidden"
      >
        <div className="relative z-10">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent mb-2">
            Initialize Your Persona
          </h1>
          <p className="text-main/60 mb-8 font-mono text-sm uppercase tracking-widest">
            Welcome, {user?.email}. Every legend needs a name and a path.
          </p>

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Username Input */}
            <div className="space-y-2">
              <label className="text-xs uppercase tracking-[0.2em] text-cyan/70 font-bold ml-1">Unique Alias</label>
              <input 
                type="text"
                placeholder="Ex: Nexus_Walker_99"
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan/50 transition-all font-mono"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            {/* Class Selection */}
            <div className="space-y-4">
              <label className="text-xs uppercase tracking-[0.2em] text-cyan/70 font-bold ml-1">Select Your Path</label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {CLASSES.map((cls) => (
                  <button
                    key={cls.id}
                    type="button"
                    onClick={() => setSelectedClass(cls.id)}
                    className={`relative p-6 rounded-2xl border transition-all duration-500 group text-left ${
                      selectedClass === cls.id 
                        ? 'bg-white/10 border-white/30 scale-[1.02]' 
                        : 'bg-white/5 border-white/5 hover:bg-white/8'
                    }`}
                  >
                    <div 
                      className="absolute inset-0 opacity-10 rounded-2xl" 
                      style={{ background: `radial-gradient(circle at center, ${cls.color}, transparent)` }}
                    />
                    <cls.icon className={`h-8 w-8 mb-4 transition-transform duration-500 ${selectedClass === cls.id ? 'scale-110' : 'group-hover:scale-110'}`} style={{ color: cls.color }} />
                    <h3 className="font-bold text-lg mb-1">{cls.name}</h3>
                    <p className="text-xs text-main/50 leading-relaxed">{cls.desc}</p>
                    {selectedClass === cls.id && (
                      <div className="absolute top-4 right-4 text-cyan">
                        <Check size={16} />
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {error && <p className="text-red-400 text-sm font-mono text-center">{error}</p>}

            <div className="flex items-center justify-between pt-4 border-t border-white/10">
              <button 
                type="button" 
                onClick={logout}
                className="text-xs text-white/40 hover:text-white/60 uppercase tracking-widest transition-colors"
              >
                Cancel Initialization
              </button>
              <button
                type="submit"
                disabled={isSubmitting || !username || !selectedClass}
                className="btn-primary px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed group relative"
              >
                <span className="relative z-10 flex items-center gap-2">
                  {isSubmitting ? 'Syncing...' : 'Begin Journey'}
                  <Sword className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </span>
              </button>
            </div>
          </form>
        </div>
      </motion.div>
    </div>
  );
};
