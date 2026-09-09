## NLP project PRD 

# **Product Requirements Document (PRD)** 

# **PromptShield — AI Privacy Layer (MVP)** 

# **1. Vision** 

PromptShield is a privacy-first interface that sits between users and Large Language Models (LLMs), helping users identify and control sensitive information before it is sent. 

Instead of blindly sending prompts containing personal, financial, or confidential information, PromptShield scans the prompt in real time, highlights risky content, explains why it is sensitive, and allows users to redact or replace it before forwarding the sanitized prompt to any LLM. 

##### **Tagline** 

##### **Think before you Prompt.** 

# **2. Problem Statement** 

Millions of users unknowingly paste: 

- passwords 

- API keys 

- company documents 

- customer information 

- phone numbers 

- addresses 

- medical records 

into AI systems. 

Most users have no visibility into: 

- what information they’re exposing 

- whether it’s personally identifiable 

- whether it’s confidential 

- whether they should remove it 

PromptShield solves this by becoming a **privacy checkpoint** before every AI interaction. 

# **3. Goals** 

#### **Primary Goals** 

- Detect sensitive information 

- Explain why it is risky 

- Let user control every detected item 

- Send only sanitized prompts to LLM 

#### **Non Goals (MVP)** 

- Browser extension 

- Enterprise policies 

- Custom organization dictionaries 

- Local desktop monitoring 

- LLM semantic reasoning 

- Authentication 

- User accounts 

# **4. Target Users** 

- Students 

- Developers 

- Researchers 

- Business Professionals 

- HR 

- Healthcare Workers 

- Lawyers 

- Anyone using ChatGPT, Claude or Gemini 

# **5. User Flow** 

Landing Page 

↓ 

Prompt Editor 

##### ↓ 

Real-Time Analysis 

##### ↓ 

Highlight Sensitive Information 

##### ↓ 

Risk Score Generated 

##### ↓ 

User Reviews Findings 

##### ↓ 

Choose Action 

Keep 

Replace 

Remove 

↓ 

Preview Sanitized Prompt 

↓ 

Send to LLM 

↓ 

Receive Response 

# **6. Functional Requirements** 

### **Prompt Editor** 

Rich textarea 

Supports: 

- Paste 

- Typing 

- Editing 

### **Real-Time Scanner** 

Runs automatically 

Delay: 

300–500 ms after typing stops 

Pipeline 

Regex 

↓ 

spaCy NER 

↓ 

Microsoft Presidio 

↓ 

Merge Results 

### **Highlighting** 

Sensitive text 

Highlight colors 

Red 

High Risk 

Orange 

Medium 

Yellow 

Low 

Hover 

Shows 

Type 

Confidence 

Reason 

Recommendation 

### **Findings Panel** 

Shows every detected item. 

Example 

Email 

Confidence 99% 

Risk High 

Replace 

Ignore 

Remove 

------------------- 

Phone Number 

Confidence 100% 

Replace 

Ignore 

Remove 

### **Risk Score** 

Example 

Privacy Score 

82 / 100 

Risk 

Medium 

Detected 

2 Emails 

- 1 Phone 

- 1 Address 

### **Actions** 

Each finding supports 

Keep 

Replace with placeholder 

Example 

[email] 

[phone] 

[address] 

[company_name] 

Remove 

### **Sanitized Prompt Preview** 

Split view 

Original 

-------------------- 

Hi 

My email is 

ved@gmail.com 

-------------------- 

Sanitized 

Hi 

My email is 

[EMAIL] 

### **Send to LLM** 

User clicks 

Send 

Backend forwards sanitized prompt 

Returns response 

# **7. Detection Categories Personally Identifiable Information** 

Name 

Phone 

Email 

DOB 

Age 

Gender 

Address Zip Code 

Passport Driving License PAN 

Aadhaar 

Student ID 

Employee ID 

### **Financial** 

Credit Card Debit Card Bank Account 

IFSC 

UPI 

Salary Invoice Numbers 

### **Authentication** 

Passwords 

OTP 

JWT 

Bearer Token API Keys GitHub Token AWS Secret Azure Secret OpenAI Key SSH Keys Private Keys Database URLs .env contents 

### **Organization** 

Company Name 

Employee List 

Internal Roadmap 

Revenue 

Meeting Notes 

Project Names 

Customer List 

Confidential Files 

### **Healthcare** 

Medical Reports 

Diagnosis 

Prescription 

Insurance 

Blood Group 

### **Legal** 

Agreement 

NDA 

Contracts 

Court Files 

Police Documents 

### **Technical** 

IP Address 

MAC Address 

Server URL 

Internal Hostnames 

SSH Config 

Database Connection String 

# **8. Detection Engine** 

### **Layer 1** 

Regex 

Detect 

Emails 

Phone 

Cards 

URLs 

JWT 

API Keys 

### **Layer 2** 

spaCy 

NER 

PERSON 

ORG 

LOCATION 

DATE 

### **Layer 3** 

Microsoft Presidio 

PII detection 

### **Merge Engine** 

Merge duplicate findings 

Resolve overlaps 

Generate confidence 

Assign severity 

# **9. Backend APIs** 

### **POST** 

/analyze 

Input 

{ prompt } 

Returns 

risk score 

findings 

highlight positions 

### **POST** 

/chat 

Input 

sanitized prompt 

Returns 

LLM response 

# **10. Frontend Pages** 

Landing 

Prompt Scanner 

Results 

Chat 

Settings (future) 

# **11. Tech Stack** 

### **Frontend** 

Next.js 

TypeScript 

TailwindCSS 

shadcn/ui 

Framer Motion 

React Hook Form 

Zustand 

### **Backend** 

FastAPI 

Python 

### **NLP** 

spaCy 

Microsoft Presidio 

Regex phonenumbers 

### **AI** 

OpenRouter Free Model 

### **Database** 

None 

(Optional later) 

Supabase 

# **12. Folder Structure** 

frontend/ 

app/ 

components/ 

PromptEditor 

HighlightLayer 

RiskPanel 

ChatWindow 

Preview 

lib/ 

hooks/ 

store/ 

----------------------------------- 

backend/ 

main.py 

routers/ 

chat.py 

analyze.py 

services/ 

regex.py 

presidio.py 

spacy.py 

merge.py 

risk.py 

schemas.py 

# **13. UI Components** 

Landing Hero 

Prompt Editor 

Risk Meter 

Highlighted Text 

Findings Sidebar 

Sanitized Preview 

Chat Response Window 

Loading Animation 

# **14. Success Metrics** 

Detection Accuracy 

95% for regex-detectable PII 

Analysis Latency 

<500 ms for common prompts 

Prompt-to-Response Time 

<3 s (excluding model latency) 

##### False Positives 

<10% on common prompts 

# **15. Future Enhancements (Out of Scope for MVP)** 

- LLM-based semantic confidentiality detection 

- Browser extension 

- Desktop application 

- Enterprise policy management 

- Team dashboards 

- Custom organization dictionaries 

- Local-only inference 

- Prompt history 

- User accounts and sync 

