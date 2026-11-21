# ResumeIQ — AI-Powered Resume Analyzer & Job Matching

**Milestone 2 | Prompt Engineering Mini Project**

**Team:** PromptForge
**Team ID:** PE-B49-36
**Batch:** B49–B64

## Project Overview

ResumeIQ is an AI-powered resume analysis and job-matching application developed using Python, Streamlit, and Google's Gemini API.

The application analyzes a candidate's resume against a job description to identify matching skills, missing qualifications, potential improvements, and learning recommendations.

It also demonstrates the impact of different prompt engineering strategies on AI-generated resume evaluations.

## Key Features

- **Resume PDF Analysis:** Upload a text-based PDF resume for automatic text extraction.
- **Job Description Matching:** Compare resume content with the requirements of a target job.
- **AI Compatibility Score:** Generate an indicative resume-to-job alignment score.
- **Skill Gap Analysis:** Identify matched, partially matched, missing, and unverified skills.
- **Resume Improvement Suggestions:** Receive actionable recommendations for improving resume content.
- **Learning Roadmap:** Identify skills and knowledge areas that could improve job readiness.
- **Prompt Strategy Comparison:** Compare Basic, Structured, and Multi-Step prompting.
- **Interactive Dashboard:** View analysis results through metrics, charts, and structured tables.
- **JSON and CSV Export:** Download analysis results and prompt comparison data.
- **Demo Mode:** Explore illustrative saved results without making live Gemini API requests.

## Application Navigation

ResumeIQ has two primary navigation options.

### 1. Dashboard

The Dashboard provides an overview of ResumeIQ, its capabilities, and the available prompt engineering strategies. Users can navigate directly to the Resume Analyzer.

### 2. Resume Analyzer

The Resume Analyzer provides the main analysis workspace, where users can:

- Upload a resume PDF or use sample data.
- Enter or load a job description.
- Select a prompt engineering strategy.
- Enable comparison across all three prompt strategies.
- Run AI-powered resume analysis.
- View compatibility scores, skill-gap visualizations, and recommendations.
- Download results in JSON or CSV format.

Prompt comparison and analysis results are integrated into the Resume Analyzer workspace rather than appearing as separate sidebar pages.

## Prompt Engineering Strategies

| Strategy             | Description                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| Basic Prompting      | Uses direct instructions to perform resume and job-description analysis.                       |
| Structured Prompting | Uses organized instructions and defined output requirements for consistent analysis.           |
| Multi-Step Prompting | Guides the model through multiple reasoning and evaluation stages within a single API request. |

These strategies allow comparison of AI response structure, skill identification, compatibility scoring, and recommendation quality.

## Technology Stack

| Component            | Technology        |
| -------------------- | ----------------- |
| Programming Language | Python            |
| Frontend             | Streamlit         |
| Generative AI        | Google Gemini API |
| PDF Text Extraction  | PyMuPDF           |
| Data Processing      | Pandas            |
| Visualizations       | Plotly            |
| Configuration        | python-dotenv     |
| Version Control      | Git and GitHub    |

## Project Structure

```text
ResumeIQ/
├── .streamlit/
├── app.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── code/
├── prompts/
├── sample_data/
├── test-data/
├── tests/
└── docs/
    ├── diagrams/
    └── evidence/
```

**Directory descriptions**

- `app.py` — Streamlit interface, PDF processing, Gemini integration, analysis results, and export functionality.
- `prompts/` — Runtime prompt templates, prompt versions, and final prompt documentation.
- `sample_data/` — Sample resume, job description, and illustrative analysis data.
- `test-data/` — Test scenarios, input datasets, available AI outputs, and evaluation records.
- `tests/` — Offline tests for project functionality and prompt integrity.
- `docs/` — Milestone reports, architecture diagrams, testing evidence, and supporting documentation.
- `CHANGELOG.md` — Project development and milestone updates.

## Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/RC0809/ResumeIQ.git
cd ResumeIQ
```

### 2. Create a virtual environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```cmd
python -m pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

Replace the placeholder with your own valid Gemini API key. The configured model must be available to your account.

**Security:** Never commit `.env`, `.env.example`, API keys, or Streamlit secret files to the repository.

### 5. Run the application

```cmd
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

## Testing and Evaluation

ResumeIQ includes **10 documented test scenarios** covering normal inputs, edge cases, and invalid inputs.

Testing focuses on:

- Resume and job-description input validation.
- PDF text extraction.
- Gemini-generated structured responses.
- Skill matching and missing-skill identification.
- Compatibility score generation.
- Prompt strategy comparison.
- Error handling and response consistency.

The project also contains prompt iteration records, available AI output evidence, and supporting documentation.

Some saved outputs and screenshots have documented evidence limitations. Refer to `docs/EVIDENCE_NOTES.md` for details.

Offline tests can be executed using:

```cmd
python -m pytest tests -q
```

Live AI testing requires a valid Gemini API key, network access, and available API quota.

**Note:** Compatibility scores are AI-generated estimates, not verified hiring probabilities. Saved demo results are illustrative and should not be presented as live Gemini outputs.

## Architecture and Workflow

The application follows this general workflow:

**Resume PDF + Job Description → Text Extraction and Validation → Prompt Strategy Selection → Gemini AI Analysis → Structured JSON Processing → Compatibility Dashboard and Recommendations → Results Export**

Supporting architecture, prompt workflow, and data-flow diagrams are available in `docs/diagrams/`.

## Team Members and Contributions

| Team Member     | Enrollment Number | Responsibility                                  |
| --------------- | ----------------- | ----------------------------------------------- |
| Rakshit Chugh   | S24CSEU2485       | AI Integration & Project Development            |
| Nakul Luthra    | S24CSEU1038       | Team Lead, Frontend Development & Prompt Design |
| Ashdeep Panesar | S24CSEU1078       | Prompt Evaluation, Testing & Documentation      |

### Rakshit Chugh

Responsible for application architecture and workflow, Gemini API integration, AI resume analysis, Basic and Multi-Step prompting, prompt comparison and testing coordination, and application integration and debugging.

### Nakul Luthra

Responsible for team coordination, Streamlit UI/UX, resume and job-description input components, Structured prompting, compatibility visualizations, and interface improvements.

### Ashdeep Panesar

Responsible for test case preparation, evaluation of the three prompting strategies, normal/edge/invalid testing, accuracy and consistency analysis, screenshots and evidence collection, and project documentation.

## Project Documentation

Milestone 2 documentation includes:

- Main milestone report: `docs/M2_PE-B49-36_ResumeIQ.pdf`
- Supporting technical report: `docs/PromptForge_TechnicalReport.pdf`
- Architecture and workflow diagrams
- Prompt versions and iteration evidence
- Test cases and evaluation records
- Development changelog

## Project Links

**GitHub Repository:** [https://github.com/RC0809/ResumeIQ](https://github.com/RC0809/ResumeIQ)

**Project Demonstration Video:** Coming soon — 90–150-second demonstration video pending.

## Future Enhancements

- Support for additional resume file formats.
- Improved skill extraction and semantic matching.
- More detailed prompt evaluation and benchmarking.
- Enhanced resume improvement recommendations.
- Improved comparison across different job descriptions.
- Expanded automated testing and evaluation.
- Additional dashboard visualizations.

## Disclaimer

ResumeIQ is an educational AI-assisted resume analysis prototype. Its recommendations and compatibility scores are indicative and should be reviewed by users. The application does not guarantee employment outcomes.

In Live Gemini mode, submitted resume and job-description content is sent to the Gemini API for analysis. Users should avoid uploading confidential information.

---

**Developed by Team PromptForge | ResumeIQ — Milestone 2**
