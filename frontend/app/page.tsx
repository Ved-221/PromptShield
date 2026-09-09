'use client';

import React from 'react';
import Link from 'next/link';
import { Header } from '../components/Header';
import { Shield, Sparkles, Lock, ArrowRight, CheckCircle, FileCode, AlertOctagon, Key, CreditCard, Cpu, Activity } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-cyan-500 selection:text-slate-950">
      <Header activeTab="home" />

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto flex flex-col items-center text-center overflow-hidden">
        
        {/* Glow backdrop decorative light */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-cyan-600/20 via-blue-600/20 to-purple-600/10 rounded-full blur-[120px] pointer-events-none" />

        {/* Hero Tagline pill */}
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-cyan-950/80 border border-cyan-800/80 text-cyan-400 text-xs font-medium mb-6 backdrop-blur-md">
          <Lock className="w-3.5 h-3.5 text-cyan-400" />
          <span>PromptShield AI Privacy Guard (MVP)</span>
        </div>

        {/* Vision Title */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight max-w-4xl leading-[1.15]">
          <span className="bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent">
            Think before you
          </span>{' '}
          <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-400 bg-clip-text text-transparent">
            Prompt.
          </span>
        </h1>

        <p className="mt-6 text-lg sm:text-xl text-slate-400 max-w-2xl font-normal leading-relaxed">
          Millions of users paste passwords, API keys, customer PII, and financial records into LLMs.
          PromptShield acts as a real-time privacy checkpoint before any prompt leaves your system.
        </p>

        {/* CTA Buttons */}
        <div className="mt-10 flex flex-col sm:flex-row items-center gap-4">
          <Link
            href="/app"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-base shadow-xl shadow-cyan-500/25 flex items-center justify-center space-x-3 transition-all hover:scale-[1.02]"
          >
            <Sparkles className="w-5 h-5" />
            <span>Launch Prompt Scanner</span>
            <ArrowRight className="w-5 h-5 ml-1" />
          </Link>

          <a
            href="#features"
            className="w-full sm:w-auto px-7 py-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 font-semibold text-base flex items-center justify-center transition-all"
          >
            <span>Learn How It Works</span>
          </a>
        </div>

        {/* Quick Highlights Row */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 w-full max-w-4xl text-left">
          <div className="glass-panel p-4 rounded-xl border border-slate-800">
            <div className="text-cyan-400 font-bold text-lg mb-1">Regex + spaCy</div>
            <div className="text-xs text-slate-400">Multi-layer hybrid engine</div>
          </div>
          <div className="glass-panel p-4 rounded-xl border border-slate-800">
            <div className="text-emerald-400 font-bold text-lg mb-1">MS Presidio</div>
            <div className="text-xs text-slate-400">Enterprise PII detection</div>
          </div>
          <div className="glass-panel p-4 rounded-xl border border-slate-800">
            <div className="text-amber-400 font-bold text-lg mb-1">Real-Time</div>
            <div className="text-xs text-slate-400">&lt;500ms debounced analysis</div>
          </div>
          <div className="glass-panel p-4 rounded-xl border border-slate-800">
            <div className="text-purple-400 font-bold text-lg mb-1">OpenRouter</div>
            <div className="text-xs text-slate-400">Sanitized LLM proxying</div>
          </div>
        </div>

      </section>

      {/* Feature Breakdown */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-t border-slate-800/80 w-full">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-100">Comprehensive Threat Protection</h2>
          <p className="mt-3 text-slate-400 text-base max-w-2xl mx-auto">
            PromptShield automatically inspects, scores, and redacts 7 key categories of sensitive information.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
            <div className="w-12 h-12 rounded-xl bg-cyan-950/80 border border-cyan-800 flex items-center justify-center text-cyan-400">
              <Key className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">Authentication & Secrets</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Detects OpenAI Keys, AWS Access & Secret Keys, GitHub Access Tokens, JWTs, Private RSA Keys, Database Connection URIs, and passwords.
            </p>
          </div>

          {/* Card 2 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
            <div className="w-12 h-12 rounded-xl bg-emerald-950/80 border border-emerald-800 flex items-center justify-center text-emerald-400">
              <Shield className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">PII & Personal Data</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Scans for names, emails, phone numbers, SSNs, Aadhaar, PAN cards, dates of birth, addresses, and location identifiers.
            </p>
          </div>

          {/* Card 3 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
            <div className="w-12 h-12 rounded-xl bg-amber-950/80 border border-amber-800 flex items-center justify-center text-amber-400">
              <CreditCard className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">Financial & Banking</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Catches credit/debit card numbers, UPI handles, IFSC codes, bank account strings, invoices, and salary figures.
            </p>
          </div>

        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto py-8 border-t border-slate-900 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <Shield className="w-4 h-4 text-cyan-400" />
            <span className="font-bold text-slate-300">PromptShield MVP</span>
            <span>— AI Privacy Checkpoint</span>
          </div>
          <div>Built with Next.js, TailwindCSS & FastAPI</div>
        </div>
      </footer>
    </div>
  );
}
