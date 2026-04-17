"""Standardized logic for exporting scores and analysis."""

import pandas as pd
from typing import List, Dict, Any
from ..config import OUTPUTS_DIR

def save_csv_output(data: List[Dict[str, Any]], filename: str) -> None:
    """Helper to save a list of flattened dicts to CSV."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(OUTPUTS_DIR / filename, index=False)
    print(f"Saved {OUTPUTS_DIR / filename}")

def save_markdown_snippet(content: str, filename: str) -> None:
    """Helper to save generated markdown sections (like examples_summary)."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUTS_DIR / filename, 'w') as f:
        f.write(content)
    print(f"Saved {OUTPUTS_DIR / filename}")
