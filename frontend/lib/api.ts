import axios from 'axios';
import { AnalyzeResponse, Finding, ActionOverride } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function analyzePrompt(prompt: string): Promise<AnalyzeResponse> {
  const response = await axios.post<AnalyzeResponse>(`${API_BASE_URL}/analyze`, { prompt });
  return response.data;
}

export async function sanitizePrompt(
  prompt: string,
  findings: Finding[],
  actions: Record<string, ActionOverride>
): Promise<string> {
  const response = await axios.post<{ sanitized_prompt: string }>(`${API_BASE_URL}/sanitize`, {
    prompt,
    findings,
    actions,
  });
  return response.data.sanitized_prompt;
}

export async function sendToLLM(prompt: string, model?: string) {
  const response = await axios.post<{ response: string; model_used: string; sanitized: boolean }>(
    `${API_BASE_URL}/chat`,
    { prompt, model }
  );
  return response.data;
}
