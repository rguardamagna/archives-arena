import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Play, LogOut, Youtube, Scroll, Sparkles, BookOpen, Quote } from 'lucide-react';
import { startGame } from '../api/gameClient';

export const Lobby = ({ onStartGame }) => {
  const { user, logout } = useAuth();
  const [videoId, setVideoId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const extractVideoId = (input) => {
    const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    const match = input.match(regExp);
    return (match && match[7].length === 11) ? match[7] : input;
  };

  const handleStart = async (e) => {
    e.preventDefault();
    const cleanId = extractVideoId(videoId);
    if (!cleanId) return;

    setLoading(true);
    setError(null);
    try {
      const session = await startGame(user.user_id || user.uid, user.email, cleanId);
      onStartGame(session);
    } catch (err) {
      setError(err.message || 'The archives failed to retrieve this lecture. Check the ID.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col gap-10 animate-fade-in p-6">
      
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-baseline gap-4 border-b border-gold/10 pb-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2 tracking-widest uppercase">
            Greeting, <span className="text-gold font-header">{user.username}</span>
          </h1>
          <p className="text-dim font-mono text-xs uppercase tracking-[0.3em]">
            Archivist Level {user.level} • {user.xp || 0} XP Inherited
          </p>
        </div>
        <button 
          onClick={logout}
          className="flex items-center gap-2 text-dim hover:text-gold transition-all font-mono text-[10px] uppercase tracking-widest"
        >
          <LogOut size={14} />
          <span>Sever Link</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Main Action Card */}
        <div className="md:col-span-2 glass-panel border-gold/10 flex flex-col gap-8 bg-white/[0.02]">
          <div className="flex items-center gap-4 text-gold/80">
            <Scroll size={28} strokeWidth={1} />
            <h2 className="text-2xl font-header tracking-widest uppercase">Initiate Inquiry</h2>
          </div>

          <form onSubmit={handleStart} className="flex flex-col gap-6">
            <div className="flex flex-col gap-3">
              <label className="text-[10px] text-dim uppercase tracking-[0.2em] font-mono ml-1">YouTube Source Identifier</label>
              <div className="relative">
                <Youtube className="absolute left-3 top-1/2 -translate-y-1/2 text-dim" size={18} strokeWidth={1.5} />
                <input
                  type="text"
                  placeholder="Insert lecture ID or YouTube link"
                  className="neon-input !pl-12 h-14"
                  value={videoId}
                  onChange={(e) => setVideoId(extractVideoId(e.target.value.trim()))}
                  disabled={loading}
                />
              </div>
            </div>

            {error && <p className="text-error text-center font-mono text-[10px] uppercase tracking-tighter">{error}</p>}

            <button
              type="submit"
              disabled={loading || !videoId}
              className="btn-primary h-14"
            >
              {loading ? (
                <>
                  <Sparkles className="animate-pulse" size={20} strokeWidth={1.5} />
                  <span>Deciphering Transcript...</span>
                </>
              ) : (
                <>
                  <Play size={18} fill="currentColor" />
                  <span>Enter the Arena</span>
                </>
              )}
            </button>
          </form>
          
          <div className="p-4 border-l-2 border-gold/20 bg-gold/5 italic text-sm text-dim flex gap-3">
            <Quote size={16} className="text-gold/40 shrink-0" />
            <p>"Knowledge is the only weapon that grows sharper with use."</p>
          </div>
        </div>

        {/* Stats / Status Card */}
        <div className="flex flex-col gap-6">
          <div className="glass-panel border-gold/5 py-8 flex flex-col items-center text-center gap-4">
            <div className="w-16 h-16 rounded-full border border-gold/20 flex items-center justify-center text-gold">
               <BookOpen size={24} strokeWidth={1} />
            </div>
            <div>
              <h3 className="font-header text-sm tracking-widest mb-1">Recent Insight</h3>
              <p className="text-dim text-xs leading-relaxed">
                Your last session on GPT-4 increased your "Neural Connectivity" by 15%.
              </p>
            </div>
          </div>

          <div className="glass-panel border-gold/5 flex flex-col gap-5 bg-white/[0.01]">
              <div className="flex justify-between text-[10px] text-dim font-mono uppercase tracking-widest">
                <span>Link Stability</span>
                <span className="text-gold">Optimum</span>
              </div>
              <div className="w-full h-px bg-white/10 relative">
                <div className="absolute top-0 left-0 h-full bg-gold/40 w-[95%]" />
              </div>
              <div className="flex justify-between text-[10px] text-dim font-mono uppercase tracking-widest">
                <span>Archives Sync</span>
                <span className="text-green-800/80">Active</span>
              </div>
          </div>
        </div>

      </div>

    </div>
  );
};

