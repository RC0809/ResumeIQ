# Prompt sheets and iteration plan

Final prompt sheets are the three **currently implemented** strategies in `prompts/final/`. The application uses `prompts/templates.py` as its runtime source of truth.

## Final prompts (3 distinct Gemini calls available)

- P1 Basic: single-call basic resume-to-JD comparison
- P2 Structured: single-call recruiter-oriented comparison
- P3 Multi-Step: **one Gemini call**, sequential internal instructions; NOT a multi-agent pipeline

Each uses Gemini `GEMINI_MODEL` (environment-configured), temperature 0.1, JSON response MIME type, no few-shot examples, and `{resume_text}` and `{job_description}` variables. No separate system prompt is supplied: rules are embedded in the user message. All return the JSON schema in `prompts/templates.py`.

## Iteration experiment (run and document)

`v1`, `v2`, `v3` are intentionally staged candidate prompts for a **planned** comparative experiment, corresponding to Basic, Structured, Multi-Step. They were reconstructed from the supplied project, **not claimed as historical development runs**. Test them on identical inputs and record observed outputs, dates, and findings in `test-data/prompt_iteration_log.csv`. Do not report unperformed runs as completed.

## Real sample run

Run each strategy in Live Gemini AI, export the JSON, and copy one input/output pair per final prompt into `test-data/outputs/`. The bundled demo JSON is illustrative, not evidence of an actual model call.
