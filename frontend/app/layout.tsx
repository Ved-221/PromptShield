import React from 'react';
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'PromptShield — AI Privacy Layer',
  description: 'Real-time AI prompt scanner, PII & credential anonymizer, and LLM privacy guard.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-slate-950 text-slate-100">{children}</body>
    </html>
  );
}
