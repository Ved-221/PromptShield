'use client';

import React from 'react';
import { Header } from '../../components/Header';
import { PromptEditor } from '../../components/PromptEditor';
import { RiskMeter } from '../../components/RiskMeter';
import { FindingsPanel } from '../../components/FindingsPanel';
import { PromptPreview } from '../../components/PromptPreview';
import { ChatWindow } from '../../components/ChatWindow';

export default function ScannerAppPage() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-cyan-500 selection:text-slate-950">
      <Header activeTab="scanner" />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        
        {/* Top Grid: Editor + Risk Meter */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
          <div className="lg:col-span-2 flex flex-col">
            <PromptEditor />
          </div>
          <div className="flex flex-col">
            <RiskMeter />
          </div>
        </div>

        {/* Middle Grid: Findings Panel + Sanitized Preview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
          <div className="lg:col-span-1 flex flex-col">
            <FindingsPanel />
          </div>
          <div className="lg:col-span-2 flex flex-col space-y-6">
            <PromptPreview />
            <ChatWindow />
          </div>
        </div>

      </main>
    </div>
  );
}
