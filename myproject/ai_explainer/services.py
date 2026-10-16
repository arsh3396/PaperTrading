"""
AI Financial Term Explainer service layer (DC-01, F6).

DC-01 cites `ai/services.py`; the app name in DC-09 is `ai_explainer`,
so this file is `ai_explainer/services.py`.

Intended responsibilities (not implemented yet):
    - Gemini wrapper behind an abstract provider (A-8, DC-04, SI-02)
    - Fixed two-sentence beginner prompt (FR-AI-04)
    - Input sanitization and prompt-injection isolation (FR-AI-06)
    - Post-process, cache, rate limits (FR-AI-05, FR-AI-07, FR-AI-09)
"""
