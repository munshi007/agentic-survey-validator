# RB GenAI Evaluation Pipeline

This is an execution-ready, strict, auditable evaluation framework for the Roland Berger GenAI Assignment.
It evaluates paired human vs simulated-human answers in an open-ended interview dataset using a hybrid approach of semantic tools, extraction models, and an LLM-as-a-judge paradigm. 

## Requirements
- Python >= 3.9
- OpenAI API Key

## Setup
1. Define the virtual environment and install components:
   ```bash
   pip install -e .
   ```
2. Create an `.env` file from the example:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY
   ```

## Data Expectations
Place the spreadsheet exactly in `data/raw/RB_GenAI_Datatest.xlsx`.
The schema must exactly match:
- `Question Category`
- `Question Text`
- `Person ID`
- `Human Answer`
- `AI Answer`

## Config Options
- **`configs/rubric.yaml`:** Defines the 5 judging dimensions, exact scoring weights, and allowable error tags.
- **`configs/model_config.yaml`:** Defines primary LLM models (`gpt-4o`) and debiasing parameters (e.g. `order_swapped: true`).

## Running the Pipeline
Execute the main entry point:
```bash
python -m src.main
```

## Where Outputs Are Written
All resulting matrices are dumped to `./outputs`:
- `dataset.json` (inside `data/processed`): Sanitized raw input.
- `pair_scores.csv`: Row-level accuracy per pair.
- `person_scores.csv`: Group level metric aggregations and profiles.
- `category_scores.csv`: Grouped averages over topic.
- `error_analysis.csv`: Distribution of common hallucination types.
- `summary_report.json`: Overall system metrics.
- `representative_examples.md`: Examples of top performance and drift failures.
