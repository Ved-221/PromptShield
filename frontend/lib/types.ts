export type RiskLevel = 'Safe' | 'Low' | 'Medium' | 'High' | 'Critical';

export interface Finding {
  id: string;
  text: string;
  type: string;
  category: string;
  start: number;
  end: number;
  confidence: number;
  risk_level: RiskLevel;
  reason: string;
  recommendation: string;
  placeholder: string;
  source: string;
}

export interface StatsSummary {
  total_findings: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  by_category: Record<string, number>;
}

export interface AnalyzeResponse {
  prompt: string;
  findings: Finding[];
  sanitized_prompt: string;
  privacy_score: number;
  risk_level: RiskLevel;
  stats: StatsSummary;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  modelUsed?: string;
  timestamp: string;
}

export type ActionOverride = 'replace' | 'remove' | 'keep';
