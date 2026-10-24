# PromptShield

AI prompt sanitization and privacy checkpoint layer.

## Setup & Requirements

### Backend
1. Python 3.12+ virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. spaCy model:
   The `en_core_web_sm` model (v3.8.0) is pinned directly in `backend/requirements.txt`.
   Alternatively install manually via:
   ```bash
   python -m spacy download en_core_web_sm
   ```
   Backend startup will fail with an error if this model is missing.

### Frontend
1. Node.js 18+.
2. Install dependencies & build:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
