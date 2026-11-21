# ResumeIQ — AI Resume Analysis and Job Matching

**Team:** PromptForge | **Team ID:** PE-B49-36 | **Batch:** B49–B64

**Members:** Rakshit Chugh (S24CSEU2485) — AI Integration & Project Development; Nakul Luthra (S24CSEU1038) — Team Lead, Frontend Development & Prompt Design; Ashdeep Panesar (S24CSEU1078) — Prompt Evaluation, Testing & Documentation.

ResumeIQ compares a resume PDF against a job description using Gemini and Basic, Structured, and Multi-Step prompt strategies. It displays an indicative compatibility score, evidence-based matched/partial/missing/unverified skills, resume improvements and a learning roadmap. The four sidebar pages are clickable: Dashboard, Resume Analyzer, Prompt Comparison and Analysis Results.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python -m streamlit run app.py
```

Set `GEMINI_API_KEY` in your **local** `.env`, or Streamlit Cloud secrets. `GEMINI_MODEL` is configurable; the default is `gemini-3-flash-preview`, subject to model access and quota. Never commit real secrets. On macOS/Linux, use `source .venv/bin/activate` and `cp .env.example .env`.

## Submission links — fill after publishing

- Public prototype: **PENDING — add Streamlit deployment URL**
- GitHub repository: https://github.com/RC0809/ResumeIQ (verify uploaded files and access)
- 90–150 second project reel: **PENDING — video is being prepared**

## Structure

- `app.py`: Streamlit frontend, Gemini integration, PDF validation, result display and export
- `prompts/`: exact runtime prompt templates, v1/v2/v3 staged candidates and final sheets
- `test-data/inputs/`: ten source test scenarios, PDF resumes, JDs and expectations
- `test-data/outputs/`: available original AI JSON outputs and prompt comparison evidence
- `test-data/test_cases.csv`: ten test scenarios with observed results and evidence status
- `docs/diagrams/`: architecture, prompt workflow, task decomposition, input/output flow
- `docs/evidence/`: screenshot evidence, including prior screenshots with uncertain mapping
- `docs/M2_PE-B49-36_ResumeIQ.pdf`: seven-section main report
- `docs/PromptForge_TechnicalReport.pdf`: supporting report
- `docs/EVIDENCE_NOTES.md`: documented mismatches and limitations
- `CHANGELOG.md`: milestone changes

## Testing

The test log documents ten scenarios including edge/invalid cases. T02 screenshot score 70 is genuine but its separately supplied JSON belongs to another JD; do not mislabel it. See `docs/EVIDENCE_NOTES.md`. Prompt comparison 75/80/75 and a separate 72/72/75 run are kept distinct. Some AI resume rewrites add unverified details; candidates must verify suggestions before use.

Offline unit checks: `python -m pytest tests -q` (install pytest separately if needed). Live Gemini requires network, key, and quota. Saved demo results are illustrative, not actual live outputs.
