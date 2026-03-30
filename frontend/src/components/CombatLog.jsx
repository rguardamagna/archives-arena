import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export const CombatLog = ({ logs }) => {
  const scrollRef = useRef(null);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="glass-panel w-full sm:w-1/3 flex flex-col h-48 sm:h-auto">
      <h4 className="text-dim text-xs uppercase mb-2 border-b border-white/10 pb-1">Combat Log</h4>
      
      <div className="flex-1 overflow-y-auto pr-2 space-y-2 font-mono text-sm" ref={scrollRef}>
        <AnimatePresence>
          {logs.map((log, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className={`p-2 rounded bg-black/40 border-l-2 ${
                log.includes('Correct') ? 'border-cyan text-cyan' : 
                log.includes('damage') ? 'border-magenta text-magenta' : 
                'border-white/20 text-dim'
              }`}
            >
              {log}
            </motion.div>
          ))}
        </AnimatePresence>
        {logs.length === 0 && (
          <p className="text-dim/50 italic text-center mt-4">Awaiting engagement...</p>
        )}
      </div>
    </div>
  );
};
