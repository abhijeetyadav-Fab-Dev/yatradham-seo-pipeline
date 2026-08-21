# Graph Report - yatradham-seo-pipeline  (2026-08-21)

## Corpus Check
- 20 files · ~44,151 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 204 nodes · 468 edges · 10 communities
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d88a248b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- stress_test.py
- test_e2e_suite.py
- models.py
- content_creator_agent.py
- qa_agent.py

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
10. `run()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `save_output()` --uses--> `SEOOutput`  [INFERRED]
  database.py → models.py

## Import Cycles
- None detected.

## Communities (10 total, 0 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.07
Nodes (47): BackgroundTasks, clear_all_outputs(), save_output(), delete, FastAPI, batch_process(), batch_urls(), BatchURLRequest (+39 more)

### Community 2 - "stress_test.py"
Cohesion: 0.10
Nodes (43): bulk_update_status(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats(), init_db() (+35 more)

### Community 3 - "test_e2e_suite.py"
Cohesion: 0.09
Nodes (24): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+16 more)

### Community 4 - "models.py"
Cohesion: 0.29
Nodes (11): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession (+3 more)

### Community 6 - "content_creator_agent.py"
Cohesion: 0.22
Nodes (15): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+7 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.24
Nodes (13): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+5 more)

## Knowledge Gaps
- **17 isolated node(s):** `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1`, `Day 2` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `test_e2e_suite.py` to `main.py`, `stress_test.py`, `qa_agent.py`, `content_creator_agent.py`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **Why does `process_package()` connect `main.py` to `qa_agent.py`, `stress_test.py`, `test_e2e_suite.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `run_suite()` connect `stress_test.py` to `main.py`, `test_e2e_suite.py`, `content_creator_agent.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PackageInput` (e.g. with `_row_to_output()` and `process_batch_background()`) actually correct?**
  _`PackageInput` has 7 INFERRED edges - model-reasoned connections that need verification._