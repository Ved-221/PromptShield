import { Finding, ActionOverride } from './types';

export const DEFAULT_PLACEHOLDERS: Record<string, string> = {
  EMAIL: '[EMAIL]',
  PHONE: '[PHONE_NUMBER]',
  CREDIT_CARD: '[CREDIT_CARD]',
  OPENAI_KEY: '[OPENAI_API_KEY]',
  AWS_KEY: '[AWS_ACCESS_KEY]',
  GITHUB_TOKEN: '[GITHUB_TOKEN]',
  BEARER_TOKEN: '[BEARER_TOKEN]',
  JWT_TOKEN: '[JWT_TOKEN]',
  PRIVATE_KEY: '[PRIVATE_KEY]',
  DATABASE_URL: '[DATABASE_URL]',
  PASSWORD_IN_TEXT: '[PASSWORD]',
  PASSWORD: '[PASSWORD]',
  SECRET: '[SECRET]',
  SSN: '[SSN]',
  AADHAAR: '[AADHAAR_NUMBER]',
  PAN: '[PAN_NUMBER]',
  UPI_ID: '[UPI_ID]',
  IP_ADDRESS: '[IP_ADDRESS]',
  PERSON: '[PERSON]',
  ORG: '[ORGANIZATION]',
  GPE: '[LOCATION]',
  LOC: '[LOCATION]',
  LOCATION: '[LOCATION]',
  DATE: '[DATE]',
  MONEY: '[FINANCIAL_AMOUNT]',
  NORP: '[GROUP]',
  CRYPTO_ADDRESS: '[CRYPTO_ADDRESS]',
  IBAN: '[IBAN]',
};

export function getPlaceholder(type: string): string {
  if (!type) return '[REDACTED]';
  const clean = type.trim();
  if (DEFAULT_PLACEHOLDERS[clean]) {
    return DEFAULT_PLACEHOLDERS[clean];
  }
  const upper = clean.toUpperCase();
  if (DEFAULT_PLACEHOLDERS[upper]) {
    return DEFAULT_PLACEHOLDERS[upper];
  }
  return `[${upper}]`;
}

export function applySanitization(
  prompt: string,
  findings: Finding[],
  actions: Record<string, ActionOverride> = {}
): string {
  if (!findings || findings.length === 0) return prompt;

  // Filter valid bounds and sort ascending by start position
  const valid = findings
    .filter((f) => 0 <= f.start && f.start < f.end && f.end <= prompt.length)
    .sort((a, b) => a.start - b.start);

  const pieces: string[] = [];
  let lastIdx = 0;

  for (const f of valid) {
    if (f.start < lastIdx) {
      // Skip overlapping spans in client fallback
      continue;
    }

    const action = actions[f.id] || 'replace';
    const prefix = prompt.substring(lastIdx, f.start);

    if (action === 'keep') {
      pieces.push(prefix);
      pieces.push(prompt.substring(f.start, f.end));
      lastIdx = f.end;
    } else if (action === 'replace') {
      pieces.push(prefix);
      pieces.push(getPlaceholder(f.type));
      lastIdx = f.end;
    } else if (action === 'remove') {
      const afterIsSpace = f.end < prompt.length && /\s/.test(prompt[f.end]);
      const beforeIsSpace = prefix.length > 0 && /\s/.test(prefix[prefix.length - 1]);

      if (beforeIsSpace && afterIsSpace) {
        pieces.push(prefix.replace(/ +$/, ''));
        lastIdx = f.end;
      } else if (beforeIsSpace && f.end === prompt.length) {
        pieces.push(prefix.replace(/ +$/, ''));
        lastIdx = f.end;
      } else if (f.start === 0 && afterIsSpace) {
        pieces.push(prefix);
        let idx = f.end;
        while (idx < prompt.length && prompt[idx] === ' ') {
          idx++;
        }
        lastIdx = idx;
      } else {
        pieces.push(prefix);
        lastIdx = f.end;
      }
    }
  }

  if (lastIdx < prompt.length) {
    pieces.push(prompt.substring(lastIdx));
  }

  let output = pieces.join('');
  output = output.replace(/ {2,}/g, ' ');
  if (!prompt.startsWith(' ')) {
    output = output.replace(/^ +/, '');
  }
  if (!prompt.endsWith(' ')) {
    output = output.replace(/ +$/, '');
  }
  return output;
}
