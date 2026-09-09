'use client';

import React, { useEffect, useRef, useState } from 'react';
import { usePromptStore } from '../store/usePromptStore';
import { Sparkles, Trash2, Zap, FileText, AlertTriangle, ShieldCheck } from 'lucide-react';

const SAMPLE_PROMPTS = [
  {
    label: '🔴 API Keys & DB Credentials',
    text: `Hi AI, please review this connection string and API key for bugs:\n\nconst db = "postgresql://admin:secretPass123@prod-db.internal:5432/finance_db";\nconst apiKey = "sk-proj-492049182390182309128309128309128309";\nconst awsKey = "AKIAIOSFODNN7EXAMPLE";`
  },
  {
    label: '🟠 PII & Contact Information',
    text: `Hello, I'm writing an email to customer John Doe at john.doe@acme-corp.com or mobile +1 (555) 234-5678. Our meeting is on 2026-09-15.`
  },
  {
    label: '🟣 Financial & Cards',
    text: `Please verify invoice #9401 sent to UPI handle user@paytm. Credit card used: 4532 1123 9081 2234 with PAN ABCDE1234F.`
  },
  {
    label: '🟢 Safe Code Prompt',
    text: `Write a Python function to sort an array of integers using quicksort and calculate its time complexity.`
  }
];

export const PromptEditor: React.FC = () => {
  const { originalPrompt, setOriginalPrompt, runAnalysis, isAnalyzing, findings } = usePromptStore();
  const [localText, setLocalText] = useState(originalPrompt);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const backdropRef = useRef<HTMLDivElement>(null);

  // Sync scroll between textarea and backdrop highlight layer
  const handleScroll = () => {
    if (textareaRef.current && backdropRef.current) {
      backdropRef.current.scrollTop = textareaRef.current.scrollTop;
      backdropRef.current.scrollLeft = textareaRef.current.scrollLeft;
    }
  };

  // Debounced real-time scanning (300ms)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (localText !== originalPrompt) {
        setOriginalPrompt(localText);
        runAnalysis(localText);
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [localText, originalPrompt, setOriginalPrompt, runAnalysis]);

  const handleSampleClick = (sampleText: string) => {
    setLocalText(sampleText);
    setOriginalPrompt(sampleText);
    runAnalysis(sampleText);
  };

  const handleClear = () => {
    setLocalText('');
    setOriginalPrompt('');
    runAnalysis('');
  };

  // Construct highlighted overlay JSX
  const renderHighlights = () => {
    if (!localText) return null;
    if (!findings || findings.length === 0) return localText;

    const elements: React.ReactNode[] = [];
    let lastIndex = 0;

    // Findings are already non-overlapping
    const sorted = [...findings].sort((a, b) => a.start - b.start);

    sorted.forEach((f, i) => {
      // Un-highlighted preceding text
      if (f.start > lastIndex) {
        elements.push(localText.substring(lastIndex, f.start));
      }

      // Highlighted text span
      const matched = localText.substring(f.start, f.end);
      const hlClass =
        f.risk_level === 'Critical'
          ? 'hl-critical'
          : f.risk_level === 'High'
          ? 'hl-high'
          : f.risk_level === 'Medium'
          ? 'hl-medium'
          : 'hl-low';

      elements.push(
        <mark key={`hl_${f.id}_${i}`} className={`${hlClass} font-mono px-0.5 rounded cursor-pointer`}>
          {matched}
        </mark>
      );

      lastIndex = f.end;
    });

    if (lastIndex < localText.length) {
      elements.push(localText.substring(lastIndex));
    }

    return elements;
  };

  const wordCount = localText.trim() ? localText.trim().split(/\s+/).length : 0;
  const charCount = localText.length;

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-xl border border-slate-800 flex flex-col space-y-4">
      
      {/* Header & Quick Preset Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <FileText className="w-5 h-5 text-cyan-400" />
          <h2 className="text-base font-semibold text-slate-100">Original Prompt Input</h2>
          {isAnalyzing && (
            <span className="flex items-center text-xs text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded-full border border-cyan-800">
              <Sparkles className="w-3 h-3 animate-spin mr-1" />
              Scanning...
            </span>
          )}
        </div>

        {/* Clear Button */}
        {localText && (
          <button
            onClick={handleClear}
            className="flex items-center space-x-1 text-xs text-slate-400 hover:text-rose-400 transition-colors self-end sm:self-auto"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear prompt</span>
          </button>
        )}
      </div>

      {/* Preset Samples */}
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-xs text-slate-400 font-medium flex items-center mr-1">
          <Zap className="w-3.5 h-3.5 text-amber-400 mr-1" /> Presets:
        </span>
        {SAMPLE_PROMPTS.map((sample, idx) => (
          <button
            key={idx}
            onClick={() => handleSampleClick(sample.text)}
            className="px-2.5 py-1 text-xs rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition-all font-medium hover:border-slate-700"
          >
            {sample.label}
          </button>
        ))}
      </div>

      {/* Textarea Container with Highlight Overlay */}
      <div className="relative w-full h-56 rounded-xl bg-slate-950/80 border border-slate-800 overflow-hidden group focus-within:border-cyan-500/50 transition-colors">
        
        {/* Backdrop Highlight Layer */}
        <div
          ref={backdropRef}
          aria-hidden="true"
          className="absolute inset-0 p-4 font-mono text-sm leading-relaxed whitespace-pre-wrap break-words overflow-auto pointer-events-none text-transparent select-none"
        >
          {renderHighlights()}
        </div>

        {/* Transparent Interactive Textarea */}
        <textarea
          ref={textareaRef}
          value={localText}
          onChange={(e) => setLocalText(e.target.value)}
          onScroll={handleScroll}
          placeholder="Paste or type your AI prompt here... PromptShield will automatically detect sensitive data, API keys, PII, and credentials in real-time."
          className="relative z-10 w-full h-full p-4 font-mono text-sm leading-relaxed text-slate-100 bg-transparent resize-none outline-none caret-cyan-400 placeholder:text-slate-600"
          spellCheck={false}
        />
      </div>

      {/* Footer Stats & Status Bar */}
      <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
        <div className="flex items-center space-x-4">
          <span>{charCount} characters</span>
          <span>{wordCount} words</span>
        </div>
        <div className="flex items-center space-x-2">
          {findings.length > 0 ? (
            <span className="flex items-center text-amber-400 font-medium">
              <AlertTriangle className="w-3.5 h-3.5 mr-1" />
              {findings.length} sensitive item{findings.length > 1 ? 's' : ''} detected
            </span>
          ) : localText.trim() ? (
            <span className="flex items-center text-emerald-400 font-medium">
              <ShieldCheck className="w-3.5 h-3.5 mr-1" />
              No sensitive items detected
            </span>
          ) : null}
        </div>
      </div>

    </div>
  );
};
