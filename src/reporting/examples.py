"""Formatting outputs in markdown for report injection."""

from pathlib import Path
from typing import List, Dict, Any
from ..io.save_outputs import save_markdown_snippet

def format_representative_examples(best: List[dict], worst: List[dict]) -> None:
    """Takes aggregated top/bottom examples and writes Markdown."""
    
    md_content = "# Representative Examples of Simulation Fidelity\n\n"
    
    md_content += "## High Fidelity (Strongest Semantic and Tone Alignments)\n"
    for ex in best:
        md_content += f"### ID {ex['id']} - Person: {ex['person_id']} - Category: {ex['category']}\n"
        md_content += f"**Question:** `{ex.get('question_text', 'N/A')}`\n"
        md_content += f"- **Human:** {ex['human_answer']}\n"
        md_content += f"- **AI:** {ex['ai_answer']}\n"
        md_content += f"- **Score:** {ex['overall_score']:.1f}/100\n"
        md_content += f"- **Judge Notes:** {ex.get('judge_explanation', '')}\n\n"
        
    md_content += "## Low Fidelity (Highest Hallucinations and Tone Mismatches)\n"
    for ex in worst:
        md_content += f"### ID {ex['id']} - Person: {ex['person_id']} - Category: {ex['category']}\n"
        md_content += f"**Question:** `{ex.get('question_text', 'N/A')}`\n"
        md_content += f"- **Human:** {ex['human_answer']}\n"
        md_content += f"- **AI:** {ex['ai_answer']}\n"
        md_content += f"- **Score:** {ex['overall_score']:.1f}/100\n"
        md_content += f"- **Error Tags:** {ex.get('error_tags', 'None')}\n"
        md_content += f"- **Judge Notes:** {ex.get('judge_explanation', '')}\n\n"

    Path("deliverables").mkdir(parents=True, exist_ok=True)
    with open("deliverables/representative_examples.md", "w") as f:
        f.write(md_content)
    print("Saved deliverables/representative_examples.md")
