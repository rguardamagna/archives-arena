import React, { useState } from 'react';
import { PlayerHud } from './PlayerHud';
import { playTurn } from '../api/gameClient';
import { Sword, Zap, RefreshCw, LogOut, Skull, Book, HelpCircle } from 'lucide-react';

export const CombatArena = ({ initialSession, onFlee }) => {
  const [sessionId] = useState(initialSession.session_id);
  const [enemy, setEnemy] = useState(initialSession.enemy);
  const [playerHp, setPlayerHp] = useState(initialSession.player_hp || 100);
  const [currentQuestion, setCurrentQuestion] = useState(initialSession.current_question);
  const [isActive, setIsActive] = useState(initialSession.is_active ?? true);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [consequence, setConsequence] = useState(null);

  const handleAnswer = async (optionId) => {
    if (loading || !isActive) return;
    setLoading(true);
    setFeedback(null);
    setConsequence(null);

    try {
      const result = await playTurn(sessionId, optionId);
      
      setPlayerHp(result.player_hp);
      setEnemy((prev) => ({ ...prev, current_hp: result.enemy_hp }));
      setCurrentQuestion(result.next_question);
      setIsActive(result.is_session_active);
      setFeedback(result.feedback);
      setConsequence(result.consequence);

      if (result.player_hp <= 0) {
        setIsActive(false);
      } else if (result.enemy_hp <= 0) {
        setIsActive(false);
      }

    } catch (error) {
      console.error("Error during turn:", error);
    } finally {
      setLoading(false);
    }
  };

  if (!currentQuestion && isActive) return null;

  return (
    <div className="w-full max-w-6xl mx-auto flex flex-col gap-8 animate-fade-in py-6 px-4">
      
      {/* Top Navigation */}
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center gap-3 text-gold/40">
          <Book size={16} strokeWidth={1.5} />
          <span className="text-[10px] font-mono uppercase tracking-[0.3em]">Lecture SID: {sessionId.substring(0, 8)}</span>
        </div>
        <button 
          onClick={onFlee}
          className="flex items-center gap-2 text-dim hover:text-gold transition-colors font-mono text-[10px] uppercase tracking-widest"
        >
          <LogOut size={14} />
          <span>Abandon Research</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left: Player Status */}
        <div className="lg:col-span-3">
          <PlayerHud 
            currentHp={playerHp} 
            maxHp={100} 
            level={1} 
            xp={enemy ? 100 - (enemy.current_hp || 0) : 0} 
          />
        </div>

        {/* Center: Dialogue & Combat Area */}
        <div className="lg:col-span-6 flex flex-col gap-6">
          
          {isActive ? (
            <div className="glass-panel border-gold/10 relative overflow-hidden bg-white/[0.01] min-h-[450px] flex flex-col">
              <div className="flex justify-between items-start mb-10">
                <span className="text-[10px] text-gold font-mono uppercase tracking-[0.4em]">Inquiry Segment</span>
                <HelpCircle size={20} className="text-gold/20" strokeWidth={1} />
              </div>

              <h2 className="text-2xl font-header font-bold text-white leading-relaxed mb-12 text-center px-4">
                {currentQuestion.question_text}
              </h2>

              <div className="grid grid-cols-1 gap-4 mt-auto">
                {currentQuestion.options.map((option, idx) => (
                  <button
                    key={option.id}
                    onClick={() => handleAnswer(option.id)}
                    disabled={loading}
                    className="group relative flex items-center justify-between p-5 bg-black/40 border border-gold/5 hover:border-gold/40 transition-all text-left rounded-sm overflow-hidden"
                  >
                    <div className="flex items-center gap-4 z-10 transition-transform group-hover:translate-x-1">
                      <span className="text-[10px] font-mono text-gold/40 group-hover:text-gold transition-colors">0{idx + 1}</span>
                      <span className="text-sm text-dim group-hover:text-white transition-colors">{option.text}</span>
                    </div>
                    <Sword size={16} className="text-gold opacity-0 group-hover:opacity-100 transition-opacity z-10" strokeWidth={1.5} />
                    <div className="absolute top-0 left-0 w-0 h-full bg-gold/5 transition-all duration-300 group-hover:w-full" />
                  </button>
                ))}
              </div>

              {loading && (
                <div className="absolute inset-0 bg-space/60 backdrop-blur-sm flex items-center justify-center z-50">
                  <div className="flex flex-col items-center gap-4">
                    <RefreshCw className="animate-spin text-gold" size={32} strokeWidth={1} />
                    <span className="text-[10px] font-mono text-gold uppercase tracking-[0.2em]">Consulting Archives...</span>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="glass-panel border-gold/20 text-center py-16 animate-fade-in bg-white/[0.02]">
               <h2 className="text-4xl font-header font-bold mb-4 tracking-widest uppercase">
                  {playerHp > 0 ? <span className="text-gold">Synthesis Complete</span> : <span className="text-error">Link Collapsed</span>}
               </h2>
               <p className="text-dim mb-10 max-w-sm mx-auto italic">
                  {playerHp > 0 
                    ? "The concepts have been successfully archived in your long-term memory." 
                    : "The complexity of the subject matter has overwhelmed your current neural capacity."}
               </p>
               <button 
                  onClick={onFlee}
                  className="btn-primary max-w-[240px] mx-auto"
               >
                  Return to Lobby
               </button>
            </div>
          )}

          {/* Feedback Section */}
          {(feedback || consequence) && isActive && (
            <div className="animate-fade-in p-6 glass-panel border-gold/10 bg-white/[0.01] flex flex-col gap-3">
              <div className="flex items-center gap-2 text-gold/60">
                <Zap size={14} strokeWidth={1.5} />
                <span className="text-[10px] font-mono uppercase tracking-widest font-bold">Feedback Loop</span>
              </div>
              <p className="text-dim text-sm italic leading-relaxed">"{feedback}"</p>
              {consequence && (
                <div className={`text-[10px] font-mono uppercase tracking-widest mt-2 ${consequence.includes('-') ? 'text-error' : 'text-gold'}`}>
                  {consequence}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right: Enemy Status */}
        <div className="lg:col-span-3">
          {enemy && (
            <div className="glass-panel border-gold/10 p-5 flex flex-col gap-6 bg-white/[0.02]">
              <div className="flex flex-col gap-1 items-center pb-4 border-b border-gold/5">
                <Skull size={32} strokeWidth={1} className={enemy.current_hp < 30 ? 'text-error animate-pulse' : 'text-gold'} />
                <h3 className="font-header text-lg uppercase tracking-widest text-white mt-2">{enemy.name}</h3>
                <span className="text-[10px] text-dim font-mono uppercase tracking-[0.2em]">Adversary Schema</span>
              </div>

              <div className="flex flex-col gap-2 pt-2">
                <div className="flex justify-between text-[10px] font-mono uppercase tracking-widest text-dim">
                  <span>Knowledge Integrity</span>
                  <span className="text-white">{enemy.current_hp}%</span>
                </div>
                <div className="h-1.5 bg-black/40 rounded-full overflow-hidden border border-white/5">
                  <div 
                    className="h-full bg-gold transition-all duration-700 shadow-[0_0_8px_rgba(197,160,89,0.2)]"
                    style={{ width: `${enemy.current_hp}%` }}
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
