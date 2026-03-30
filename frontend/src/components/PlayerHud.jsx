import React from 'react';
import { Shield, Zap, Award } from 'lucide-react';

export const PlayerHud = ({ currentHp = 100, maxHp = 100, level = 1, xp = 0 }) => {
  const hpPercentage = (currentHp / maxHp) * 100;
  
  return (
    <div className="glass-panel border-gold/10 p-5 flex flex-col gap-4 bg-white/[0.02] min-w-[280px]">
      <div className="flex justify-between items-center border-b border-gold/5 pb-3">
        <div className="flex flex-col">
          <span className="text-[10px] text-dim font-mono uppercase tracking-[0.2em]">Neural Entity</span>
          <h3 className="text-xl font-header text-white font-bold tracking-widest">ARCHIVIST</h3>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-[10px] text-gold font-mono uppercase tracking-widest">Level</span>
          <span className="text-2xl font-header font-bold text-gold">{level}</span>
        </div>
      </div>

      {/* HP Bar */}
      <div className="flex flex-col gap-2">
        <div className="flex justify-between text-[10px] font-mono uppercase tracking-widest">
          <div className="flex items-center gap-1.5 text-gold/80">
            <Shield size={12} strokeWidth={1.5} />
            <span>Vitality</span>
          </div>
          <span className={currentHp < 20 ? 'text-error animate-pulse' : 'text-dim'}>
            {currentHp} / {maxHp}
          </span>
        </div>
        <div className="h-2 bg-black/40 border border-white/5 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gold transition-all duration-500 shadow-[0_0_10px_rgba(197,160,89,0.3)]"
            style={{ width: `${hpPercentage}%` }}
          />
        </div>
      </div>

      {/* XP Bar */}
      <div className="flex flex-col gap-2">
        <div className="flex justify-between text-[10px] font-mono uppercase tracking-widest text-dim">
          <div className="flex items-center gap-1.5">
            <Award size={12} strokeWidth={1.5} />
            <span>Knowledge Inherited</span>
          </div>
          <span>{xp} XP</span>
        </div>
        <div className="h-1 bg-black/40 rounded-full overflow-hidden">
          <div 
            className="h-full bg-white/20 transition-all duration-500"
            style={{ width: `${(xp % 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
};
