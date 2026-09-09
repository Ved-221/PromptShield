'use client';

import React from 'react';
import { usePromptStore } from '../store/usePromptStore';
import { ShieldCheck, AlertCircle, ShieldAlert, Activity, CheckCircle2 } from 'lucide-react';

export const RiskMeter: React.FC = () => {
  const { privacyScore, riskLevel, stats, isAnalyzing, originalPrompt } = usePromptStore();

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-emerald-400 stroke-emerald-500';
    if (score >= 75) return 'text-cyan-400 stroke-cyan-500';
    if (score >= 50) return 'text-amber-400 stroke-amber-500';
    return 'text-rose-500 stroke-rose-500';
  };

  const getBadgeStyle = (level: string) => {
    switch (level) {
      case 'Safe':
        return 'bg-emerald-950/80 text-emerald-400 border-emerald-800';
      case 'Low':
        return 'bg-cyan-950/80 text-cyan-400 border-cyan-800';
      case 'Medium':
        return 'bg-amber-950/80 text-amber-400 border-amber-800';
      case 'High':
        return 'bg-orange-950/80 text-orange-400 border-orange-800';
      case 'Critical':
        return 'bg-rose-950/80 text-rose-400 border-rose-800';
      default:
        return 'bg-slate-900 text-slate-400 border-slate-800';
    }
  };

  // SVG Gauge Calculations
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (privacyScore / 100) * circumference;

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-xl border border-slate-800 flex flex-col justify-between space-y-4">
      
      {/* Title */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-cyan-400" />
          <h2 className="text-base font-semibold text-slate-100">Privacy Risk Gauge</h2>
        </div>
        <span
          className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getBadgeStyle(
            riskLevel
          )} flex items-center space-x-1`}
        >
          {riskLevel === 'Safe' ? (
            <ShieldCheck className="w-3.5 h-3.5 inline mr-1" />
          ) : (
            <ShieldAlert className="w-3.5 h-3.5 inline mr-1" />
          )}
          <span>{riskLevel} Risk</span>
        </span>
      </div>

      {/* Main Score Radial Display */}
      <div className="flex items-center justify-center space-x-6 my-2">
        <div className="relative w-28 h-28 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            {/* Background ring */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              className="stroke-slate-900"
              strokeWidth="8"
              fill="transparent"
            />
            {/* Progress ring */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              className={`transition-all duration-700 ease-out ${getScoreColor(privacyScore)}`}
              strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className={`text-2xl font-bold font-mono tracking-tighter ${getScoreColor(privacyScore).split(' ')[0]}`}>
              {privacyScore}
            </span>
            <span className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider">Score</span>
          </div>
        </div>

        {/* Breakdown Counts */}
        <div className="flex flex-col space-y-1.5 text-xs text-slate-300">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
            <span className="text-slate-400">Critical:</span>
            <span className="font-semibold text-slate-200">{stats?.critical_count || 0}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-orange-500"></span>
            <span className="text-slate-400">High:</span>
            <span className="font-semibold text-slate-200">{stats?.high_count || 0}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
            <span className="text-slate-400">Medium:</span>
            <span className="font-semibold text-slate-200">{stats?.medium_count || 0}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
            <span className="text-slate-400">Low:</span>
            <span className="font-semibold text-slate-200">{stats?.low_count || 0}</span>
          </div>
        </div>
      </div>

      {/* Category Distribution */}
      {stats && Object.keys(stats.by_category).length > 0 && (
        <div className="pt-2 border-t border-slate-800">
          <span className="text-xs font-semibold text-slate-400 block mb-2">Detected Categories</span>
          <div className="flex flex-wrap gap-1.5">
            {Object.entries(stats.by_category).map(([cat, count]) => (
              <span
                key={cat}
                className="px-2 py-0.5 text-[11px] rounded bg-slate-900 text-slate-300 border border-slate-800 flex items-center space-x-1"
              >
                <span>{cat}</span>
                <span className="bg-slate-800 px-1 py-0.2 rounded text-[10px] font-mono text-cyan-400">{count}</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {!originalPrompt.trim() && (
        <div className="text-center py-2 text-xs text-slate-500 flex items-center justify-center space-x-1">
          <CheckCircle2 className="w-3.5 h-3.5 text-slate-600" />
          <span>Ready to analyze your prompt</span>
        </div>
      )}
    </div>
  );
};
