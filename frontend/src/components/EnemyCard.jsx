import React from 'react';
import { motion } from 'framer-motion';
import { Skull, Swords } from 'lucide-react';

export const EnemyCard = ({ enemy }) => {
  if (!enemy) return null;

  const hpPercentage = Math.max(0, (enemy.current_hp / enemy.max_hp) * 100);

  return (
    <div className="glass-panel w-full sm:w-1/3 flex flex-col items-center gap-3 relative overflow-hidden border-magenta/30">
      {/* Glow effect */}
      <div className="absolute top-[-20%] right-[-20%] w-[150%] h-[150%] bg-magenta/5 blur-3xl rounded-full pointer-events-none" />
      
      <div className="z-10 bg-black/50 p-4 rounded-full border border-magenta/50 mb-2 relative">
        <Skull className="text-magenta" size={48} />
        {/* Simple pulse animation for the enemy avatar */}
        <motion.div 
          className="absolute inset-0 rounded-full border-2 border-magenta"
          animate={{ scale: [1, 1.1, 1], opacity: [0.5, 0, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </div>

      <div className="text-center z-10 w-full">
        <h3 className="font-bold text-xl text-magenta tracking-wider">{enemy.name}</h3>
        <p className="text-dim text-xs uppercase flex items-center justify-center gap-1 mt-1">
          <Swords size={12}/> {enemy.topic}
        </p>
      </div>
      
      {/* Enemy HP Bar */}
      <div className="w-full mt-2 z-10">
        <div className="flex justify-between mb-1 text-xs">
          <span className="text-dim">HP</span>
          <span className="text-magenta font-mono">{enemy.current_hp} / {enemy.max_hp}</span>
        </div>
        <div className="w-full h-2 bg-black/60 rounded-full overflow-hidden border border-magenta/30">
          <motion.div 
            className="h-full bg-magenta"
            initial={{ width: '100%' }}
            animate={{ width: `${hpPercentage}%` }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
            style={{ boxShadow: '0 0 10px rgba(255, 0, 255, 0.8)' }}
          />
        </div>
      </div>
    </div>
  );
};
