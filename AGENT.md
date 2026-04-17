# AGENT.md

## Project goal
Build a rigorous evaluation pipeline for paired human vs simulated-human answers in an open-ended interview dataset.

This is an evaluation project, not a generation project.
Do not build a new simulator unless explicitly asked.
Optimize for correctness, clarity, reproducibility, and auditability.

## Working style
Prefer simple, explicit, maintainable code.
Do not optimize prematurely.
Do not create abstractions unless they remove real duplication or improve correctness.

## Non-negotiable coding rules
- No patchy code.
- No placeholder logic in committed files.
- No hidden fallbacks.
- No silent exception swallowing.
- No unnecessary helper functions.
- No giant god functions.
- No marketing language in comments, docs, variable names, or output text.
- No emojis anywhere.
- No "AI-powered", "cutting-edge", "revolutionary", "seamless", or similar filler.
- No unexplained magic numbers.
- No unused imports.
- No dead code.
- No duplicated prompt strings across files.
- No business logic inside notebooks.
- No output schemas defined inline in multiple places.

## Architecture rules
- Keep I/O, schemas, metrics, LLM calls, pipelines, and reporting in separate modules.
- All model names, weights, thresholds, and prompt versions must be config-driven.
- All LLM outputs must use strict structured schemas where possible.
- Every pipeline stage must produce inspectable intermediate outputs.
- Prefer deterministic filenames and stable serialization formats.
- Version prompts explicitly.
- Keep side effects at the edges of the system.

## Prompting rules
- Prompts must be compact, explicit, and testable.
- Each prompt must define:
  - task
  - required inputs
  - output schema
  - scoring criteria
  - failure behavior
- Do not rely on vague instructions.
- Do not ask for prose when a schema is required.
- If a prompt is used for judging, specify the rubric exactly.
- If pairwise order could matter, run order-swapped evaluations.

## Evaluation rules
- Treat the human answer as the reference target.
- Score AI answers on:
  - factual alignment
  - rationale alignment
  - specificity calibration
  - tone/persona match
  - contradiction/hallucination risk
- Record both score and explanation.
- Tag concrete failure modes.
- Separate row-level scoring from person-level consistency scoring.
- Do not claim statistical significance from this small sample unless explicitly supported.

## Reliability rules
- Prefer structured outputs over free-form JSON.
- Validate every model response before downstream use.
- On validation failure, retry with the same prompt and stricter repair instruction.
- Log every retry.
- Flag unstable judge outputs.
- Run order-swapped judging for pairwise comparisons.
- Keep a manual-audit sample in the final outputs.

## Data rules
- Never mutate raw input files.
- Save normalized data to processed files.
- Validate required columns before scoring.
- Fail fast on missing fields or unexpected schema changes.

## Reporting rules
- All output text must be plain, direct, and specific.
- Use consultant-style clarity, not hype.
- Prefer short sentences.
- Every claim in summaries must trace back to a computed result.
- Highlight both strengths and failure modes.
- Do not overclaim.
- Distinguish observed evidence from interpretation.

## Documentation rules
- README must explain:
  - setup
  - data expectations
  - config options
  - how to run the full pipeline
  - where outputs are written
- Each module should have a short docstring stating its responsibility.
- Public functions need concise docstrings only when they add value.

## Anti-slop rules
Do not produce:
- ornamental abstractions
- performative enterprise patterns
- speculative future-proofing
- unnecessary indirection
- verbose comments that restate the code
- vague names like process_data, handle_stuff, do_eval, helper, utils2

Prefer:
- explicit names
- narrow modules
- strong typing
- visible schemas
- testable units
- small prompt surfaces

## Default output standard
When unsure, choose:
- simpler design
- stricter validation
- clearer naming
- fewer layers
- more inspectable outputs
- less prose