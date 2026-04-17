# GenAI Evaluation Pipeline

This is an execution-ready, strict, auditable evaluation framework for the Roland Berger GenAI Assignment.
It evaluates paired human vs simulated-human answers in an open-ended interview dataset using a hybrid approach of semantic tools, extraction models, and an LLM-as-a-judge paradigm. 

## Requirements
- Python >= 3.9
- OpenAI API Key

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create an `.env` file from the example:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY
   ```

## Data Expectations
Place the spreadsheet exactly in `data/raw/RB_GenAI_Datatest.xlsx`.
The loader auto-normalizes column names, so either of these schemas will work:
- Capitalized: `Question Category`, `Question Text`, `Person ID`, `Human Answer`, `AI Answer`
- Snake case: `question_category`, `question`, `person_id`, `human_answers`, `ai_answers`

## Config Options
- **`configs/rubric.yaml`:** Defines the 5 judging dimensions, exact scoring weights, and allowable error tags. The overall score is computed deterministically from these weights in Python, not by the LLM.
- **`configs/model_config.yaml`:** Defines primary LLM models (`gpt-4o`) and debiasing parameters (e.g. `order_swapped: true`).

## Running the Pipeline
Execute the main entry point:
```bash
python -m src.main
```

## Where Outputs Are Written

### `./outputs/` — Raw evaluation data (not committed to git)
- `pair_scores.csv`: Row-level accuracy per pair, including forward/swapped scores and instability flags.
- `person_scores.csv`: Group-level metric aggregations and profiles.
- `person_consistency_scores.csv`: Per-person persona drift analysis (separate diagnostic, not included in headline score).
- `category_scores.csv`: Grouped averages over topic.
- `error_analysis.csv`: Distribution of common hallucination types.

### `./deliverables/` — Submission-ready artifacts (committed to git)
- `summary_report.json`: Overall system metrics and headline score.
- `representative_examples.md`: Examples of top performance and drift failures.
- `technical_report.md`: 2-page evaluation methodology and findings.
- `pitch_deck.md`: 3-slide executive presentation.

### `./data/processed/` — Sanitized input (not committed to git)
- `dataset.json`: Validated, normalized copy of the raw spreadsheet.

## Scoring Methodology
The headline fidelity score is a **weighted average** of five LLM-judged rubric dimensions (each scored 1–5), scaled to 0–100:
- Factual Alignment (30%)
- Rationale Alignment (25%)
- Tone & Persona Match (20%)
- Specificity Calibration (15%)
- Contradiction / Hallucination (10%)

Person-level **persona consistency** is computed and reported as a separate diagnostic. It is **not** included in the headline score.
