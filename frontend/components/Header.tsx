'use client';

import React from 'react';
import Link from 'next/link';
import { Shield, Sparkles, Lock, Terminal } from 'lucide-react';

interface HeaderProps {
  activeTab?: 'home' | 'scanner';
}

export const Header: React.FC<HeaderProps> = ({ activeTab = 'scanner' }) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-gray-800 bg-opacity-80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 p-0.5 shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform duration-200">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Shield className="w-5 h-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
                PromptShield
              </span>
              <span className="px-1.5 py-0.5 text-[10px] font-semibold bg-cyan-950 text-cyan-400 border border-cyan-800 rounded">
                MVP
              </span>
            </div>
            <p className="text-[11px] text-gray-400 font-medium tracking-wide">Think before you Prompt</p>
          </div>
        </Link>

        {/* Navigation Items */}
        <nav className="flex items-center space-x-1 sm:space-x-4">
          <Link
            href="/"
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'home'
                ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
                : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
            }`}
          >
            Overview
          </Link>
          <Link
            href="/app"
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center space-x-1.5 ${
              activeTab === 'scanner'
                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-md shadow-cyan-600/20'
                : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>Prompt Scanner</span>
          </Link>
        </nav>

        {/* Live Backend Status */}
        <div className="hidden md:flex items-center space-x-2 text-xs text-gray-400 bg-slate-900/80 px-3 py-1.5 rounded-full border border-gray-800">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <Lock className="w-3.5 h-3.5 text-emerald-400" />
          <span>Local Engine Active</span>
        </div>
      </div>
    </header>
  );
};
