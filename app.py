import json
import os
from pathlib import Path

import fitz
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts.templates import make_prompt

load_dotenv()
BASE = Path(__file__).resolve().parent
VERSIONS = ["Basic", "Structured", "Multi-Step"]


def setting(name, default=""):
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except (FileNotFoundError, KeyError):
        return os.getenv(name, default)


st.set_page_config(page_title="ResumeIQ | AI Career Intelligence", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
:root {color-scheme:dark}
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {background:#0b1020;color:#eaf0ff}
[data-testid="stHeader"] {background:transparent;height:2.2rem}
[data-testid="stMain"] .block-container {
    max-width:1600px !important;width:calc(100% - 48px) !important;
    padding:1.25rem 0 3rem !important;margin:0 auto !important;
}
[data-testid="stSidebar"] {background:#11192d !important;border-right:1px solid #26314c}
[data-testid="stSidebar"] .block-container {padding-top:1.2rem}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color:#c7d2eb}
[data-testid="stSidebar"] label {color:#c7d2eb !important}
h1,h2,h3,h4 {color:#f4f7ff !important;letter-spacing:-.02em}
h1 {font-size:2.0rem !important}
h2 {font-size:1.35rem !important}
h3 {font-size:1.05rem !important}
p,li,span {line-height:1.45}
[data-testid="stCaptionContainer"] {color:#98a9c9 !important}
.hero {padding:24px 28px;border:1px solid #33499b;border-radius:16px;background:linear-gradient(110deg,#192a68,#234bd0);margin-bottom:18px}
.hero h1 {margin:0;color:white !important;font-size:2rem !important}
.hero p {color:#d7e4ff;margin:7px 0 0}
.kicker {color:#9cb3ee;font-size:.74rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.section-note {color:#9aadd2;font-size:.78rem;margin:-.3rem 0 .8rem}
[data-testid="stVerticalBlockBorderWrapper"] > div {border-color:#2a3755 !important}
[data-testid="stMetric"] {background:#18243c !important;border:1px solid #33435f !important;padding:17px !important;border-radius:12px !important;min-height:112px}
[data-testid="stMetricLabel"] *, [data-testid="stMetricLabel"] {color:#b8c8e4 !important}
[data-testid="stMetricValue"] *, [data-testid="stMetricValue"] {color:#f7faff !important;font-weight:750 !important}
[data-testid="stAlert"] {background:#1b3150 !important;border:1px solid #36567d !important;border-radius:10px}
[data-testid="stAlert"] p,[data-testid="stAlert"] strong {color:#edf4ff !important}
[data-testid="stTextArea"] textarea,[data-testid="stTextInput"] input,[data-testid="stSelectbox"] > div > div {background:#19253d !important;color:#f0f5ff !important;border-color:#354563 !important}
[data-testid="stFileUploader"] section {background:#15213a !important;border:1px dashed #6174ab !important;border-radius:12px !important}
[data-testid="stFileUploader"] section * {color:#dbe6ff !important}
[data-testid="stTabs"] button {color:#c6d3ef !important}
[data-testid="stTabs"] button[aria-selected="true"] {color:#a6b8ff !important;border-bottom-color:#697cff !important}
[data-testid="stDataFrame"] {border:1px solid #293956;border-radius:10px;overflow:hidden}
.stButton button[kind="primary"] {background:#5534e8 !important;border:1px solid #7059f5 !important;color:#fff !important;font-weight:700;border-radius:9px;min-height:46px}
.stButton button[kind="primary"]:hover {background:#674bf2 !important}
.stDownloadButton button {background:#213c76 !important;color:#eaf2ff !important;border:1px solid #3b5790 !important;border-radius:8px}
.stDownloadButton button:hover {border-color:#7e9aff !important;color:#fff !important}
div[data-testid="stHorizontalBlock"] {align-items:stretch}
hr {border-color:#2b3956 !important}
@media(max-width:900px) {
 [data-testid="stMain"] .block-container {width:calc(100% - 24px) !important;padding-top:.75rem !important}
 .hero {padding:18px 17px}
 .hero h1 {font-size:1.6rem !important}
}
</style>
""", unsafe_allow_html=True)


def pdf_text(upload):
    data = upload.getvalue()
    if len(data) > 8 * 1024 * 1024:
        raise ValueError("PDF exceeds 8 MB.")
    try:
        with fitz.open(stream=data, filetype="pdf") as doc:
            if len(doc) > 20:
                raise ValueError("Maximum 20 PDF pages supported.")
            content = "\n".join(page.get_text(sort=True) for page in doc)
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Could not read PDF. Upload an unlocked, text-based PDF.") from exc
    if len(content.strip()) < 80:
        raise ValueError("PDF contains too little selectable text; scanned PDFs require OCR.")
    return content[:30000]


def clean_result(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    result = json.loads(raw)
    if not isinstance(result, dict):
        raise ValueError("AI response must be a JSON object.")
    score = result.get("compatibility_score")
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100:
        raise ValueError("Invalid compatibility score returned by AI.")
    for key in ["matched_skills", "partial_skills", "missing_skills", "unverified_skills", "resume_improvements", "strengths", "learning_recommendations", "warnings"]:
        if not isinstance(result.get(key), list):
            raise ValueError(f"AI response is missing list: {key}")
    return result


def analyze(api_key, model, version, resume, jd):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=make_prompt(version, resume, jd),
        config=types.GenerateContentConfig(temperature=0.1, response_mime_type="application/json"),
    )
    if not response.text:
        raise ValueError("Gemini returned an empty response.")
    return clean_result(response.text)


def show_table(items, fields):
    records = [{field.replace("_", " ").title(): str(item.get(field, "")) for field in fields}
               for item in items if isinstance(item, dict)]
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
    else:
        st.caption("No entries found in this category.")


def render_result(result):
    st.markdown("### ◈ Analysis Results Dashboard")
    score = result["compatibility_score"]
    m1, m2, m3, m4 = st.columns(4, gap="small")
    m1.metric("Compatibility Score", f"{score:.0f}/100")
    m2.metric("Matched Skills", len(result["matched_skills"]))
    m3.metric("Partially Matched", len(result["partial_skills"]))
    m4.metric("Missing Skills", len(result["missing_skills"]))
    st.progress(int(score) / 100, text="Resume–job alignment (indicative)")
    st.info("**Score rationale:** " + str(result.get("score_explanation", "Not provided")))

    st.markdown("### ◈ Skill Gap & Alignment Matrix")
    left, right = st.columns([1, 1.25], gap="medium")
    with left:
        counts = [len(result[key]) for key in ("matched_skills", "partial_skills", "missing_skills", "unverified_skills")]
        if sum(counts):
            fig = go.Figure(go.Pie(
                labels=["Matched", "Partial", "Missing", "Unverified"], values=counts,
                hole=.68, marker=dict(colors=["#22c55e", "#a78bfa", "#fb7185", "#64748b"]),
                textinfo="percent", textfont=dict(color="#ffffff", size=12)))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#dbe7ff"), height=320, margin=dict(l=5,r=5,t=20,b=5),
                              legend=dict(orientation="h", y=-.08, x=.03))
            fig.add_annotation(text=f"<b>{sum(counts)}</b><br>skills", showarrow=False,
                               font=dict(size=21, color="#ffffff"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("No skills to chart.")
    with right:
        with st.container(border=True):
            st.markdown("#### Candidate Summary")
            st.write(result.get("candidate_summary", "Not provided"))
        with st.container(border=True):
            st.markdown("#### Job Requirements Summary")
            st.write(result.get("job_summary", "Not provided"))
    st.caption("Compatibility score is an LLM-generated estimate, not a hiring probability.")

    tabs = st.tabs(["Matched Skills", "Partially Matched", "Missing Skills", "Unverified", "Resume Improvements", "Learning Roadmap"])
    with tabs[0]: show_table(result["matched_skills"], ["skill", "evidence"])
    with tabs[1]: show_table(result["partial_skills"], ["skill", "evidence", "gap"])
    with tabs[2]: show_table(result["missing_skills"], ["skill", "importance", "reason"])
    with tabs[3]: show_table(result["unverified_skills"], ["skill", "reason"])
    with tabs[4]: show_table(result["resume_improvements"], ["original", "suggested", "reason"])
    with tabs[5]:
        for item in result["learning_recommendations"]:
            st.write("•", item)
    if result["strengths"]:
        with st.expander("Candidate strengths"):
            for item in result["strengths"]: st.write("•", item)
    if result["warnings"]:
        with st.expander("Assessment limitations"):
            for item in result["warnings"]: st.write("•", item)


# API key is intentionally NOT shown in the sidebar.
api_key = setting("GEMINI_API_KEY", "")
model = setting("GEMINI_MODEL", "gemini-3-flash-preview")

with st.sidebar:
    st.markdown("## ✦ ResumeIQ")
    st.caption("AI CAREER INTELLIGENCE")
    st.divider()
    page = st.radio("Navigation", ["Dashboard", "Resume Analyzer", "Prompt Comparison", "Analysis Results"],
                    index=1, key="nav_page", label_visibility="collapsed")
    st.divider()
    st.markdown("<span class='kicker'>Analysis Settings</span>", unsafe_allow_html=True)
    version = st.selectbox("Prompt Strategy", VERSIONS, index=1)
    compare = st.toggle("Compare All Prompts", value=False)
    mode = st.radio("Analysis Mode", ["Live Gemini AI", "Saved demo results"])
    if mode == "Saved demo results":
        st.caption("Demo mode: illustrative saved data, not a live Gemini response.")
    st.divider()
    sample_resume = st.checkbox("Use sample resume", value=True)
    sample_jd = st.checkbox("Use sample job description", value=True)
    if mode == "Live Gemini AI":
        if api_key:
            st.success("AI engine configured")
        else:
            st.warning("AI key missing in .env; use Saved demo results or configure GEMINI_API_KEY.")
    st.caption("Privacy: In Live mode, resume and job description are sent to Gemini. Avoid confidential data.")

st.markdown('<div class="hero"><div class="kicker">Workspace / Resume Analysis</div><h1>ResumeIQ Analysis Canvas</h1><p>AI-Powered Resume Analyzer & Intelligent Job Matching · Prompt Engineering</p></div>', unsafe_allow_html=True)

if page == "Dashboard":
    st.markdown("### ◈ Project Overview")
    st.write("Analyze resume-to-job alignment using Gemini AI, evidence-based skill matching and three prompt strategies.")
    a,b,c = st.columns(3)
    a.metric("Prompt strategies", "3")
    b.metric("Documented test scenarios", "10")
    c.metric("Analysis outputs", "JSON / CSV")
    st.info("Select **Resume Analyzer** to upload a PDF, **Prompt Comparison** to benchmark strategies, or **Analysis Results** to view the most recent result.")
    if st.button("Open Resume Analyzer", type="primary"):
        st.session_state.nav_page = "Resume Analyzer"
        st.rerun()

if page in ("Resume Analyzer", "Prompt Comparison"):
    st.markdown("### ◈ Resume Analysis Workspace")
    if page == "Prompt Comparison":
        st.info("Enable Compare All Prompts in the sidebar to run Basic, Structured and Multi-Step on the same input. Live mode makes three API requests.")
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("#### ▤ Upload Resume")
            upload = st.file_uploader("Drag and drop your PDF or click Browse", type=["pdf"], disabled=sample_resume)
            if sample_resume:
                resume = (BASE / "sample_data" / "sample_resume.txt").read_text(encoding="utf-8")
                st.success("Sample resume loaded")
                st.text_area("Extracted Resume Preview", resume, height=170, disabled=True)
            elif upload:
                try:
                    resume = pdf_text(upload)
                    st.success(f"Extracted {len(resume):,} characters from {upload.name}")
                    with st.expander("Extracted Resume Preview"):
                        st.text_area("Resume content", resume, height=180, disabled=True)
                except ValueError as exc:
                    st.error(str(exc))
                    resume = ""
            else:
                resume = ""
                st.caption("Upload a text-based PDF, or select the sample resume.")
    with right:
        with st.container(border=True):
            st.markdown("#### ▧ Target Job Description")
            default_jd = (BASE / "sample_data" / "job_description.txt").read_text(encoding="utf-8") if sample_jd else ""
            jd = st.text_area("Paste the job requirements", value=default_jd, height=265,
                              placeholder="Enter required skills, experience, responsibilities, and qualifications...")
            st.caption(f"{len(jd):,} characters · Job requirement input")

    run = st.button("✦ Run AI Resume Analysis", type="primary", use_container_width=True)
    if run:
        if len(resume.strip()) < 80:
            st.error("Please upload a readable resume or enable the sample resume.")
        elif len(jd.strip()) < 60:
            st.error("Enter a meaningful job description (at least 60 characters).")
        elif mode == "Live Gemini AI" and not api_key:
            st.error("GEMINI_API_KEY is missing. Set it in the .env file, or use Saved demo results.")
        else:
            results, errors = {}, {}
            to_run = VERSIONS if compare else [version]
            if mode == "Saved demo results":
                sample = json.loads((BASE / "sample_data" / "demo_analysis.json").read_text(encoding="utf-8"))
                results = {v: json.loads(json.dumps(sample)) for v in to_run}
            else:
                with st.spinner("Analyzing resume with Gemini..."):
                    for v in to_run:
                        try:
                            results[v] = analyze(api_key, model, v, resume, jd[:20000])
                        except Exception as exc:
                            message = str(exc)
                            if "429" in message or "RESOURCE_EXHAUSTED" in message:
                                errors[v] = "Gemini quota exceeded (429). Retry after reset or use Saved demo results."
                                break
                            if "404" in message or "NOT_FOUND" in message:
                                errors[v] = f"Model '{model}' unavailable (404). Update GEMINI_MODEL in .env."
                                break
                            errors[v] = message[:400]
            st.session_state.update(results=results, errors=errors, demo_mode=(mode == "Saved demo results"), selected_version=version)
results = st.session_state.get("results", {})
if page in ("Dashboard",):
    results = {}

for version_name, message in st.session_state.get("errors", {}).items():
    st.error(f"{version_name} prompt failed: {message}")

if results:
    if st.session_state.get("demo_mode", False):
        st.warning("SAVED DEMO RESULTS — illustrative sample output, not live Gemini analysis. Results may not match your uploaded inputs.")
    names = list(results)
    selected = st.session_state.get("selected_version", names[0])
    active = st.selectbox("View result from", names, index=names.index(selected) if selected in names else 0)
    render_result(results[active])
    st.markdown("### ◈ Export Diagnostics")
    st.download_button("⬇ Download Analysis JSON", json.dumps(results[active], indent=2, ensure_ascii=False),
                       file_name="resumeiq_analysis.json", mime="application/json")
    if len(results) > 1:
        st.markdown("### ◈ Prompt Strategy Benchmarking")
        st.caption("Scores below compare outputs for the same input; they do not establish accuracy without human-labelled evaluation.")
        columns = st.columns(len(results), gap="small")
        for column, (name, res) in zip(columns, results.items()):
            with column:
                with st.container(border=True):
                    st.markdown(f"#### {name} Prompt")
                    st.metric("Compatibility", f"{res['compatibility_score']:.0f}/100")
                    st.caption(f"Matched {len(res['matched_skills'])} · Partial {len(res['partial_skills'])} · Missing {len(res['missing_skills'])}")
        comparison = pd.DataFrame([{
            "Prompt": name, "Score": res["compatibility_score"],
            "Matched": len(res["matched_skills"]), "Partial": len(res["partial_skills"]),
            "Missing": len(res["missing_skills"]), "Unverified": len(res["unverified_skills"]),
        } for name, res in results.items()])
        st.dataframe(comparison, hide_index=True, use_container_width=True)
        st.bar_chart(comparison.set_index("Prompt")["Score"])
        if st.session_state.get("demo_mode", False):
            st.caption("Demo comparison repeats one saved result for all strategies; it is NOT a measured prompt benchmark.")
        st.download_button("⬇ Download Comparison CSV", comparison.to_csv(index=False),
                           file_name="resumeiq_prompt_comparison.csv", mime="text/csv")
elif page == "Analysis Results":
    st.info("No analysis available yet. Open Resume Analyzer to run an analysis.")
elif page in ("Resume Analyzer", "Prompt Comparison"):
    st.caption("Choose a resume and job description, then click Run AI Resume Analysis to view the dashboard.")
