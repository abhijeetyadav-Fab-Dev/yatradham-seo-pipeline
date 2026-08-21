# Graph Report - yatradham-seo-pipeline  (2026-08-21)

## Corpus Check
- 18 files · ~36,671 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 174 nodes · 420 edges · 10 communities
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a6a497d7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- stress_test.py
- LLMClient
- models.py
- test_e2e_suite.py
- qa_agent.py
- export_csv

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 31 edges
2. `run_suite()` - 19 edges
3. `SEOOutput` - 15 edges
4. `PackageInput` - 14 edges
5. `process_package()` - 14 edges
6. `SectionedContent` - 13 edges
7. `save_output()` - 12 edges
8. `worker_db_stress()` - 12 edges
9. `get_output()` - 11 edges
10. `list_outputs()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `_dict_to_sections()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py

## Import Cycles
- None detected.

## Communities (10 total, 0 thin omitted)

### Community 1 - "main.py"
Cohesion: 0.09
Nodes (40): BackgroundTasks, save_output(), FastAPI, batch_process(), batch_urls(), BatchURLRequest, bulk_action(), check_ai_endpoint() (+32 more)

### Community 2 - "stress_test.py"
Cohesion: 0.13
Nodes (31): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats() (+23 more)

### Community 3 - "LLMClient"
Cohesion: 0.09
Nodes (23): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+15 more)

### Community 4 - "models.py"
Cohesion: 0.18
Nodes (16): _sections_to_dict(), Any, update_single_output(), BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation (+8 more)

### Community 6 - "test_e2e_suite.py"
Cohesion: 0.16
Nodes (20): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+12 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.43
Nodes (7): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run()

### Community 12 - "export_csv"
Cohesion: 0.25
Nodes (8): get, export_csv(), get_outputs(), get_single_output(), List all SEO outputs with optional filter and pagination., Export outputs to CSV., root(), stats()

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `stress_test.py`, `qa_agent.py`, `test_e2e_suite.py`?**
  _High betweenness centrality (0.289) - this node is a cross-community bridge._
- **Why does `process_package()` connect `main.py` to `stress_test.py`, `LLMClient`, `models.py`, `test_e2e_suite.py`, `qa_agent.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `run_suite()` connect `test_e2e_suite.py` to `main.py`, `stress_test.py`, `LLMClient`, `models.py`, `export_csv`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PackageInput` (e.g. with `_row_to_output()` and `process_batch_background()`) actually correct?**
  _`PackageInput` has 7 INFERRED edges - model-reasoned connections that need verification._