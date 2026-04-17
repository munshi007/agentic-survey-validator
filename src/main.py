"""Main entrypoint for the GenAI evaluation pipeline."""

import os
from .io.load_dataset import load_and_validate_dataset, save_processed
from .pipelines.run_extraction import run_extraction_pass
from .pipelines.run_pair_scoring import run_judging_pass
from .pipelines.run_consistency import run_consistency_layer
from .pipelines.aggregate_results import run_aggregations
from .reporting.examples import format_representative_examples
from .utils.logging import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Initializing Roland Berger GenAI Evaluation Pipeline...")
    
    # 1. Load and validate strict data schema
    records = load_and_validate_dataset()
    save_processed(records)
    
    # 2. Extract structured attributes per string
    # Warning: this makes 2 API calls per row (Human + AI)
    logger.info("--- Phase 2: Attribute Extraction ---")
    extracted_data = run_extraction_pass(records)
    
    # 3. Pairwise Judging & Lexical Metrics
    # Warning: this makes 1 API call per row (2 if swapped)
    logger.info("--- Phase 3: Pairwise Scoring & Debias ---")
    scored_pairs = run_judging_pass(extracted_data)
    
    # 4. Profile Consistency (Person Level)
    logger.info("--- Phase 4: Persona Consistency Analysis ---")
    # passing flattened dicts for consistency
    records_dict = [r.model_dump() for r in records]
    consistency_scores = run_consistency_layer(records_dict)
    
    # 5. Aggregation and formatting
    logger.info("--- Phase 5: Aggregation and Synthesis ---")
    agg_run = run_aggregations(scored_pairs)
    
    # Format and save exactly the top/bottom models
    format_representative_examples(agg_run['best'], agg_run['worst'])
    
    logger.info("Pipeline Complete. Delivery artifacts written to `./deliverables`, raw outputs to `./outputs`.")
    logger.info(f"Overall Final Score: {agg_run['report_json']['overall_score']}")

if __name__ == "__main__":
    main()
