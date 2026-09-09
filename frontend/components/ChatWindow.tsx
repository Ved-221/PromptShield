'use client';

import React, { useRef, useEffect } from 'react';
import { usePromptStore } from '../store/usePromptStore';
import { Bot, User, Sparkles, Trash2, ShieldCheck, Copy, Check } from 'lucide-react';

export const ChatWindow: React.FC = () => {
  const { chatMessages, isChatLoading, clearChat } = usePromptStore();
  const chatEndRef = useRef<HTMLDivElement>(null);
  const [copiedId, setCopiedId] = React.useState<string | null>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages, isChatLoading]);

  const handleCopyText = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-xl border border-slate-800 flex flex-col h-full space-y-4">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Bot className="w-5 h-5 text-cyan-400" />
          <h2 className="text-base font-semibold text-slate-100">LLM Response Window</h2>
        </div>

        {chatMessages.length > 0 && (
          <button
            onClick={clearChat}
            className="flex items-center space-x-1 text-xs text-slate-400 hover:text-rose-400 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear Chat</span>
          </button>
        )}
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto max-h-[350px] min-h-[180px] space-y-4 pr-1">
        {chatMessages.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-10 text-center text-slate-500 space-y-2">
            <Bot className="w-10 h-10 text-cyan-500/40" />
            <p className="text-sm font-medium text-slate-400">No active AI conversation</p>
            <p className="text-xs max-w-xs text-slate-500">
              Sanitize your prompt above and click &quot;Send to LLM&quot; to test receiving AI responses safely.
            </p>
          </div>
        ) : (
          chatMessages.map((msg) => {
            const isUser = msg.role === 'user';

            return (
              <div
                key={msg.id}
                className={`flex items-start space-x-3 ${
                  isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row'
                }`}
              >
                {/* Avatar */}
                <div
                  className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${
                    isUser
                      ? 'bg-gradient-to-tr from-cyan-600 to-blue-600 text-white'
                      : 'bg-gradient-to-tr from-emerald-600 to-teal-600 text-white'
                  }`}
                >
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                {/* Message Content Bubble */}
                <div
                  className={`max-w-[85%] p-4 rounded-2xl text-xs leading-relaxed space-y-2 ${
                    isUser
                      ? 'bg-cyan-950/70 border border-cyan-800 text-cyan-100 rounded-tr-none'
                      : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-none'
                  }`}
                >
                  <div className="flex items-center justify-between text-[10px] text-slate-400 pb-1 border-b border-slate-800/60">
                    <span className="font-semibold flex items-center">
                      {isUser ? 'Sanitized Prompt Sent' : 'AI Assistant'}
                      {!isUser && msg.modelUsed && (
                        <span className="ml-2 font-mono text-[9px] bg-slate-800 px-1.5 py-0.2 rounded text-cyan-400">
                          {msg.modelUsed}
                        </span>
                      )}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span>{msg.timestamp}</span>
                      <button
                        onClick={() => handleCopyText(msg.id, msg.content)}
                        className="hover:text-cyan-400 transition-colors"
                        title="Copy message"
                      >
                        {copiedId === msg.id ? (
                          <Check className="w-3 h-3 text-emerald-400" />
                        ) : (
                          <Copy className="w-3 h-3" />
                        )}
                      </button>
                    </div>
                  </div>

                  <div className="whitespace-pre-wrap font-sans text-slate-200">{msg.content}</div>

                  {!isUser && (
                    <div className="pt-1 flex items-center space-x-1 text-[10px] text-emerald-400">
                      <ShieldCheck className="w-3 h-3" />
                      <span>Protected by PromptShield Privacy Layer</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}

        {isChatLoading && (
          <div className="flex items-center space-x-2 text-xs text-cyan-400 py-2">
            <Sparkles className="w-4 h-4 animate-spin" />
            <span>AI is processing your sanitized prompt...</span>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

    </div>
  );
};
