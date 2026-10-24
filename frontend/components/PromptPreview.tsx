'use client';

import React, { useState } from 'react';
import { usePromptStore } from '../store/usePromptStore';
import { Lock, Copy, Check, Send, Sparkles, ShieldCheck, AlertCircle } from 'lucide-react';

export const PromptPreview: React.FC = () => {
  const {
    originalPrompt,
    sanitizedPrompt,
    analyzedPrompt,
    isAnalyzing,
    analysisError,
    sendChat,
    isChatLoading,
  } = usePromptStore();

  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState<'sanitized' | 'comparison'>('sanitized');

  // Strict check on send blocking criteria
  let sendBlockedReason = '';
  if (!originalPrompt.trim()) {
    sendBlockedReason = 'Enter a prompt to analyze';
  } else if (isAnalyzing) {
    sendBlockedReason = 'Analysis in progress...';
  } else if (analysisError) {
    sendBlockedReason = `Analysis error: ${analysisError}`;
  } else if (analyzedPrompt !== originalPrompt) {
    sendBlockedReason = 'Prompt modified - waiting for analysis...';
  } else if (!sanitizedPrompt.trim()) {
    sendBlockedReason = 'Nothing left to send after sanitization';
  } else if (isChatLoading) {
    sendBlockedReason = 'Waiting for LLM response...';
  }

  const isSendBlocked = Boolean(sendBlockedReason);

  const handleCopy = () => {
    if (!sanitizedPrompt) return;
    navigator.clipboard.writeText(sanitizedPrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isAnalysisFresh = analyzedPrompt === originalPrompt && !isAnalyzing;
  const isCompletelyRemoved =
    originalPrompt.trim().length > 0 && isAnalysisFresh && !sanitizedPrompt.trim();

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
            disabled={!sanitizedPrompt}
            className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition-colors disabled:opacity-50"
            title={sanitizedPrompt ? 'Copy sanitized prompt' : 'Nothing to copy'}
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Main Preview Area */}
      {viewMode === 'sanitized' ? (
        <div className="relative w-full min-h-[140px] max-h-[220px] p-4 rounded-xl bg-slate-950/80 border border-slate-800 font-mono text-sm leading-relaxed text-emerald-300 overflow-y-auto break-words">
          {sanitizedPrompt ? (
            sanitizedPrompt
          ) : isCompletelyRemoved ? (
            <span className="text-amber-400 font-sans italic flex items-center">
              <AlertCircle className="w-4 h-4 mr-1.5 shrink-0" />
              Nothing left to send after sanitization
            </span>
          ) : isAnalyzing ? (
            <span className="text-cyan-400/80 font-sans italic flex items-center">
              <Sparkles className="w-4 h-4 animate-spin mr-1.5 shrink-0" />
              Analyzing prompt...
            </span>
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
          {/* Sanitized (NEVER fallback to originalPrompt) */}
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-emerald-950/80 overflow-y-auto">
            <span className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider block mb-1">
              Sanitized
            </span>
            <div className="font-mono text-xs text-emerald-300 whitespace-pre-wrap break-words">
              {sanitizedPrompt ? (
                sanitizedPrompt
              ) : isCompletelyRemoved ? (
                <span className="text-amber-400 font-sans italic">
                  Nothing left to send after sanitization
                </span>
              ) : (
                <span className="text-slate-600 font-sans italic">Empty output</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Send to LLM Action Footer */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 border-t border-slate-800">
        <div className="flex items-center space-x-1.5 text-xs text-slate-400">
          <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>Only verified sanitized prompt is transmitted to LLM.</span>
        </div>

        <div className="flex items-center space-x-3 self-end sm:self-auto">
          {isSendBlocked && originalPrompt.trim().length > 0 && (
            <span className="text-xs text-amber-400/90 font-medium">{sendBlockedReason}</span>
          )}

          <button
            onClick={sendChat}
            disabled={isSendBlocked}
            title={sendBlockedReason || 'Send sanitized prompt to LLM'}
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
    </div>
  );
};
