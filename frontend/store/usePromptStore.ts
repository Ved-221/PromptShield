import { create } from 'zustand';
import { Finding, RiskLevel, StatsSummary, ChatMessage, ActionOverride } from '../lib/types';
import { analyzePrompt, sanitizePrompt, sendToLLM } from '../lib/api';

interface PromptState {
  originalPrompt: string;
  findings: Finding[];
  actions: Record<string, ActionOverride>;
  sanitizedPrompt: string;
  privacyScore: number;
  riskLevel: RiskLevel;
  stats: StatsSummary | null;
  isAnalyzing: boolean;
  
  chatMessages: ChatMessage[];
  isChatLoading: boolean;

  setOriginalPrompt: (text: string) => void;
  runAnalysis: (text: string) => Promise<void>;
  setActionOverride: (findingId: string, action: ActionOverride) => Promise<void>;
  resetAllActions: () => Promise<void>;
  sendChat: () => Promise<void>;
  clearChat: () => void;
}

export const usePromptStore = create<PromptState>((set, get) => ({
  originalPrompt: '',
  findings: [],
  actions: {},
  sanitizedPrompt: '',
  privacyScore: 100,
  riskLevel: 'Safe',
  stats: null,
  isAnalyzing: false,

  chatMessages: [],
  isChatLoading: false,

  setOriginalPrompt: (text: string) => {
    set({ originalPrompt: text });
  },

  runAnalysis: async (text: string) => {
    if (!text.trim()) {
      set({
        findings: [],
        actions: {},
        sanitizedPrompt: '',
        privacyScore: 100,
        riskLevel: 'Safe',
        stats: null,
        isAnalyzing: false
      });
      return;
    }

    set({ isAnalyzing: true });
    try {
      const result = await analyzePrompt(text);
      
      // Default all findings to 'replace'
      const initialActions: Record<string, ActionOverride> = {};
      result.findings.forEach(f => {
        initialActions[f.id] = 'replace';
      });

      set({
        findings: result.findings,
        actions: initialActions,
        sanitizedPrompt: result.sanitized_prompt,
        privacyScore: result.privacy_score,
        riskLevel: result.risk_level,
        stats: result.stats,
        isAnalyzing: false
      });
    } catch (err) {
      console.error("Analysis failed", err);
      set({ isAnalyzing: false });
    }
  },

  setActionOverride: async (findingId: string, action: ActionOverride) => {
    const { originalPrompt, findings, actions } = get();
    const updatedActions = { ...actions, [findingId]: action };
    set({ actions: updatedActions });

    try {
      const newSanitized = await sanitizePrompt(originalPrompt, findings, updatedActions);
      set({ sanitizedPrompt: newSanitized });
    } catch (err) {
      console.error("Sanitization update failed", err);
    }
  },

  resetAllActions: async () => {
    const { originalPrompt, findings } = get();
    const resetActions: Record<string, ActionOverride> = {};
    findings.forEach(f => {
      resetActions[f.id] = 'replace';
    });
    set({ actions: resetActions });

    try {
      const newSanitized = await sanitizePrompt(originalPrompt, findings, resetActions);
      set({ sanitizedPrompt: newSanitized });
    } catch (err) {
      console.error("Reset sanitization failed", err);
    }
  },

  sendChat: async () => {
    const { sanitizedPrompt, originalPrompt, chatMessages } = get();
    const targetPrompt = sanitizedPrompt || originalPrompt;
    if (!targetPrompt.trim()) return;

    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: targetPrompt,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    set({
      chatMessages: [...chatMessages, userMsg],
      isChatLoading: true
    });

    try {
      const res = await sendToLLM(targetPrompt);
      const assistantMsg: ChatMessage = {
        id: `assistant_${Date.now()}`,
        role: 'assistant',
        content: res.response,
        modelUsed: res.model_used,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      set({
        chatMessages: [...get().chatMessages, assistantMsg],
        isChatLoading: false
      });
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: `assistant_err_${Date.now()}`,
        role: 'assistant',
        content: "⚠️ Error sending prompt to LLM. Please check backend connection.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      set({
        chatMessages: [...get().chatMessages, errorMsg],
        isChatLoading: false
      });
    }
  },

  clearChat: () => set({ chatMessages: [] })
}));
