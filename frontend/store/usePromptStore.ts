import { create } from 'zustand';
import { Finding, RiskLevel, StatsSummary, ChatMessage, ActionOverride } from '../lib/types';
import { analyzePrompt, sendToLLM } from '../lib/api';
import { applySanitization } from '../lib/sanitize';

interface PromptState {
  originalPrompt: string;
  analyzedPrompt: string;
  findings: Finding[];
  actions: Record<string, ActionOverride>;
  sanitizedPrompt: string;
  privacyScore: number;
  riskLevel: RiskLevel;
  stats: StatsSummary | null;
  isAnalyzing: boolean;
  analysisError: string | null;

  chatMessages: ChatMessage[];
  isChatLoading: boolean;

  setOriginalPrompt: (text: string) => void;
  runAnalysis: (text: string) => Promise<void>;
  setActionOverride: (findingId: string, action: ActionOverride) => void;
  resetAllActions: () => void;
  sendChat: () => Promise<void>;
  clearChat: () => void;
}

let activeRequestId = 0;

export const usePromptStore = create<PromptState>((set, get) => ({
  originalPrompt: '',
  analyzedPrompt: '',
  findings: [],
  actions: {},
  sanitizedPrompt: '',
  privacyScore: 100,
  riskLevel: 'Safe',
  stats: null,
  isAnalyzing: false,
  analysisError: null,

  chatMessages: [],
  isChatLoading: false,

  setOriginalPrompt: (text: string) => {
    set({ originalPrompt: text });
  },

  runAnalysis: async (text: string) => {
    const currentReqId = ++activeRequestId;

    if (!text.trim()) {
      set({
        originalPrompt: text,
        analyzedPrompt: text,
        findings: [],
        actions: {},
        sanitizedPrompt: '',
        privacyScore: 100,
        riskLevel: 'Safe',
        stats: null,
        isAnalyzing: false,
        analysisError: null,
      });
      return;
    }

    set({ isAnalyzing: true, analysisError: null });

    try {
      const result = await analyzePrompt(text);

      // Discard stale out-of-order response
      if (currentReqId !== activeRequestId) {
        return;
      }

      // Default all findings to 'replace'
      const initialActions: Record<string, ActionOverride> = {};
      result.findings.forEach((f) => {
        initialActions[f.id] = 'replace';
      });

      set({
        findings: result.findings,
        actions: initialActions,
        sanitizedPrompt: result.sanitized_prompt,
        analyzedPrompt: text, // Set ONLY when analysis result for exactly this text is applied
        privacyScore: result.privacy_score,
        riskLevel: result.risk_level,
        stats: result.stats,
        isAnalyzing: false,
        analysisError: null,
      });
    } catch (err: any) {
      if (currentReqId !== activeRequestId) {
        return;
      }
      const errorMsg =
        err?.response?.data?.detail ||
        err?.message ||
        'Analysis failed. Please check backend connection.';
      console.error('Analysis failed', err);
      set({
        isAnalyzing: false,
        analysisError: typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg),
      });
    }
  },

  setActionOverride: (findingId: string, action: ActionOverride) => {
    const { originalPrompt, findings, actions } = get();
    const updatedActions = { ...actions, [findingId]: action };
    const newSanitized = applySanitization(originalPrompt, findings, updatedActions);
    set({
      actions: updatedActions,
      sanitizedPrompt: newSanitized,
    });
  },

  resetAllActions: () => {
    const { originalPrompt, findings } = get();
    const resetActions: Record<string, ActionOverride> = {};
    findings.forEach((f) => {
      resetActions[f.id] = 'replace';
    });
    const newSanitized = applySanitization(originalPrompt, findings, resetActions);
    set({
      actions: resetActions,
      sanitizedPrompt: newSanitized,
    });
  },

  sendChat: async () => {
    const {
      sanitizedPrompt,
      originalPrompt,
      analyzedPrompt,
      isAnalyzing,
      analysisError,
      chatMessages,
      isChatLoading,
    } = get();

    // Prevent sending under blocked conditions
    if (isChatLoading) return;
    if (!originalPrompt.trim()) return;
    if (isAnalyzing || analysisError) return;
    if (analyzedPrompt !== originalPrompt) return;
    if (!sanitizedPrompt.trim()) return;

    // NEVER fallback to originalPrompt
    const targetPrompt = sanitizedPrompt;

    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: targetPrompt,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    set({
      chatMessages: [...chatMessages, userMsg],
      isChatLoading: true,
    });

    try {
      const res = await sendToLLM(targetPrompt);
      const assistantMsg: ChatMessage = {
        id: `assistant_${Date.now()}`,
        role: 'assistant',
        content: res.response,
        modelUsed: res.model_used,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      set({
        chatMessages: [...get().chatMessages, assistantMsg],
        isChatLoading: false,
      });
    } catch (err: any) {
      const errorDetail =
        err?.response?.data?.detail ||
        '⚠️ Error sending prompt to LLM. Please check backend connection.';
      const errorMsg: ChatMessage = {
        id: `assistant_err_${Date.now()}`,
        role: 'assistant',
        content: typeof errorDetail === 'string' ? `⚠️ ${errorDetail}` : JSON.stringify(errorDetail),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      set({
        chatMessages: [...get().chatMessages, errorMsg],
        isChatLoading: false,
      });
    }
  },

  clearChat: () => {
    set({ chatMessages: [] });
  },
}));
