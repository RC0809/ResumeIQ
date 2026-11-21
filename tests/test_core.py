import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from prompts.templates import make_prompt

def test_prompts():
    for version in ("Basic", "Structured", "Multi-Step"):
        prompt=make_prompt(version,"Python experience","Python required")
        assert "Python experience" in prompt
        assert "compatibility_score" in prompt

def test_version_snapshots():
    root=Path(__file__).resolve().parents[1]
    for v in ("v1","v2","v3"):
        assert (root/'prompts'/v/'analysis_prompt.txt').exists()
