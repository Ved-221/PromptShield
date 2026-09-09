'use client';

import React, { useState } from 'react';
import { usePromptStore } from '../store/usePromptStore';
import { Lock, Copy, Check, Send, Sparkles, Eye, ShieldCheck } from 'lucide-react';

export const PromptPreview: React.FC = () => {
  const { originalPrompt, sanitizedPrompt, sendChat, isChatLoading } = usePromptStore();
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState<'sanitized' | 'comparison'>('sanitized');

  const activePrompt = sanitizedPrompt || originalPrompt;

  const handleCopy = () => {
    if (!activePrompt) return;
    navigator.clipboard.writeText(activePrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-xl border border-slate-800 flex flex-col space-y-4">
      
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Lock className="w-5 h-5 text-emerald-400" />
          <h2 className="text-base font-semibold text-slate-100">Sanitized Prompt Preview</h2>
        </div>

        {/* View Mode & Actions */}
        <div className="flex items-center space-x-2">
          <div className="bg-slate-900 p-1 rounded-lg border border-slate-800 flex items-center text-xs">
            <button
              onClick={() => setViewMode('sanitized')}
              className={`px-2.5 py-1 rounded font-medium transition-all ${
                viewMode === 'sanitized'
                  ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Sanitized Preview
            </button>
            <button
              onClick={() => setViewMode('comparison')}
              className={`px-2.5 py-1 rounded font-medium transition-all ${
                viewMode === 'comparison'
                  ? 'bg-cyan-600 text-white shadow-sm font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Side-by-Side
            </button>
          </div>

          <button
            onClick={handleCopy}
            disabled={!activePrompt}
            className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition-colors disabled:opacity-50"
            title="Copy sanitized prompt"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Main Preview Area */}
      {viewMode === 'sanitized' ? (
        <div className="relative w-full min-h-[140px] max-h-[220px] p-4 rounded-xl bg-slate-950/80 border border-slate-800 font-mono text-sm leading-relaxed text-emerald-300 overflow-y-auto break-words">
          {activePrompt ? (
            activePrompt
          ) : (
            <span className="text-slate-600 font-sans italic">
              Sanitized prompt preview will appear here in real-time...
            </span>
          )}
        </div>
      ) : (
        /* Side-by-Side Comparison */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 min-h-[140px] max-h-[220px]">
          {/* Original */}
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 overflow-y-auto">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
              Original
            </span>
            <div className="font-mono text-xs text-rose-300/90 whitespace-pre-wrap break-words">
              {originalPrompt || <span className="text-slate-600 font-sans italic">Empty input</span>}
            </div>
          </div>
          {/* Sanitized */}
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-emerald-950/80 overflow-y-auto">
            <span className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider block mb-1">
              Sanitized
            </span>
            <div className="font-mono text-xs text-emerald-300 whitespace-pre-wrap break-words">
              {sanitizedPrompt || originalPrompt || (
                <span className="text-slate-600 font-sans italic">Empty input</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Send to LLM Action Footer */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800">
        <div className="flex items-center space-x-1.5 text-xs text-slate-400">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Prompt is safe to transmit to any external LLM model.</span>
        </div>

        <button
          onClick={sendChat}
          disabled={!activePrompt.trim() || isChatLoading}
          className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-semibold text-sm shadow-lg shadow-emerald-500/20 flex items-center space-x-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isChatLoading ? (
            <>
              <Sparkles className="w-4 h-4 animate-spin" />
              <span>Forwarding...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Send to LLM</span>
            </>
          )}
        </button>
      </div>

    </div>
  );
};
