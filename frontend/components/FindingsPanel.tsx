'use client';

import React from 'react';
import { usePromptStore } from '../store/usePromptStore';
import { ActionOverride } from '../lib/types';
import { ShieldAlert, Info, RotateCcw, Check, EyeOff, Tag, ShieldCheck } from 'lucide-react';

export const FindingsPanel: React.FC = () => {
  const { findings, actions, setActionOverride, resetAllActions, isAnalyzing } = usePromptStore();

  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'Critical':
        return 'bg-rose-950/80 text-rose-400 border-rose-800';
      case 'High':
        return 'bg-orange-950/80 text-orange-400 border-orange-800';
      case 'Medium':
        return 'bg-amber-950/80 text-amber-400 border-amber-800';
      default:
        return 'bg-blue-950/80 text-blue-400 border-blue-800';
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-xl border border-slate-800 flex flex-col h-full space-y-4">
      
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
          <h2 className="text-base font-semibold text-slate-100">Findings & Controls</h2>
          {findings.length > 0 && (
            <span className="px-2 py-0.5 text-xs font-mono bg-amber-950 text-amber-400 border border-amber-800 rounded-full">
              {findings.length}
            </span>
          )}
        </div>

        {findings.length > 0 && (
          <button
            onClick={() => resetAllActions()}
            className="flex items-center space-x-1 text-xs text-slate-400 hover:text-cyan-400 transition-colors"
            title="Reset all actions to default replacement"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>
        )}
      </div>

      {/* Findings List Area */}
      <div className="flex-1 overflow-y-auto max-h-[500px] pr-1 space-y-3">
        {findings.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center text-slate-500 space-y-2">
            <ShieldCheck className="w-10 h-10 text-emerald-500/50" />
            <p className="text-sm font-medium text-slate-400">No Privacy Risks Detected</p>
            <p className="text-xs max-w-xs text-slate-500">
              Type or paste a prompt in the editor to scan for sensitive PII, passwords, API keys, or financial data.
            </p>
          </div>
        ) : (
          findings.map((f) => {
            const currentAction: ActionOverride = actions[f.id] || 'replace';

            return (
              <div
                key={f.id}
                className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 hover:border-slate-700 transition-all flex flex-col space-y-2.5"
              >
                {/* Header info */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-bold text-cyan-300 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/50">
                      {f.type}
                    </span>
                    <span className="text-[11px] text-slate-400 flex items-center">
                      <Tag className="w-3 h-3 mr-1 text-slate-500" />
                      {f.category}
                    </span>
                  </div>

                  <span className={`px-2 py-0.5 text-[10px] font-semibold rounded border ${getRiskBadge(f.risk_level)}`}>
                    {f.risk_level}
                  </span>
                </div>

                {/* Snippet text */}
                <div className="p-2 rounded bg-slate-900/90 font-mono text-xs text-slate-200 break-all border border-slate-800">
                  <span className="text-slate-500 select-none mr-2">Snippet:</span>
                  <span className="text-amber-300 font-semibold">{f.text}</span>
                </div>

                {/* Reason & Confidence */}
                <div className="text-xs text-slate-400 flex items-start space-x-1.5">
                  <Info className="w-3.5 h-3.5 text-cyan-400 mt-0.5 shrink-0" />
                  <div>
                    <span>{f.reason}</span>
                    <span className="ml-2 text-[10px] font-mono text-slate-500">
                      (Conf: {Math.round(f.confidence * 100)}% via {f.source})
                    </span>
                  </div>
                </div>

                {/* Interactive Action Controls */}
                <div className="pt-2 border-t border-slate-900 flex items-center justify-between text-xs">
                  <span className="text-[11px] font-medium text-slate-400">Action:</span>
                  <div className="flex items-center space-x-1 bg-slate-900 p-1 rounded-lg border border-slate-800">
                    
                    {/* Replace Option */}
                    <button
                      onClick={() => setActionOverride(f.id, 'replace')}
                      className={`px-2 py-1 rounded text-[11px] font-medium transition-all ${
                        currentAction === 'replace'
                          ? 'bg-cyan-600 text-white shadow-sm font-semibold'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                      title={`Replace with ${f.placeholder}`}
                    >
                      Replace ({f.placeholder})
                    </button>

                    {/* Remove Option */}
                    <button
                      onClick={() => setActionOverride(f.id, 'remove')}
                      className={`px-2 py-1 rounded text-[11px] font-medium transition-all ${
                        currentAction === 'remove'
                          ? 'bg-rose-600 text-white shadow-sm font-semibold'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                      title="Remove text completely"
                    >
                      Remove
                    </button>

                    {/* Keep Option */}
                    <button
                      onClick={() => setActionOverride(f.id, 'keep')}
                      className={`px-2 py-1 rounded text-[11px] font-medium transition-all ${
                        currentAction === 'keep'
                          ? 'bg-amber-600 text-white shadow-sm font-semibold'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                      title="Keep original un-sanitized text"
                    >
                      Keep
                    </button>

                  </div>
                </div>

              </div>
            );
          })
        )}
      </div>

    </div>
  );
};
