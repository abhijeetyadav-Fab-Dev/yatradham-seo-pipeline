# Graph Report - yatradham-seo-pipeline  (2026-08-22)

## Corpus Check
- 26 files · ~56,235 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 267 nodes · 581 edges · 14 communities (11 shown, 3 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `771fbdac`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- stress_test.py
- LLMClient
- models.py
- WordPressPublisher
- SitemapCrawler
- run_seo_linter
- qa_agent.py
- .sanitize_meta_description
- generate_json_ld

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 34 edges
2. `run_suite()` - 19 edges
3. `SEOOutput` - 17 edges
4. `process_package()` - 17 edges
5. `PackageInput` - 14 edges
6. `SectionedContent` - 13 edges
7. `save_output()` - 12 edges
8. `worker_db_stress()` - 12 edges
9. `get_output()` - 11 edges
10. `run()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `_row_to_output()` --uses--> `PackageInput`  [INFERRED]
  database.py → models.py
- `localize()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py
- `process_batch_background()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py

## Import Cycles
- None detected.

## Communities (14 total, 3 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.06
Nodes (57): BackgroundTasks, clear_all_outputs(), FastAPI, batch_urls(), BatchURLRequest, bulk_action(), check_ai_endpoint(), CheckAIRequest (+49 more)

### Community 2 - "stress_test.py"
Cohesion: 0.10
Nodes (45): bulk_update_status(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats(), init_db() (+37 more)

### Community 3 - "LLMClient"
Cohesion: 0.06
Nodes (45): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections() (+37 more)

### Community 4 - "models.py"
Cohesion: 0.13
Nodes (21): get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…, batch_process(), process_single(), Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (manual input)., BatchRequest (+13 more)

### Community 7 - "run_seo_linter"
Cohesion: 0.33
Nodes (6): calculate_flesch_reading_ease(), Any, Real-Time SEO & GEO (Generative Engine Optimization) Linter for YatraDham., Audit content for SEO and AI Overview (GEO) citation compliance., Calculate Flesch Reading Ease score (0-100)., run_seo_linter()

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 13 - "generate_json_ld"
Cohesion: 0.40
Nodes (4): generate_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results, SGE…

## Knowledge Gaps
- **17 isolated node(s):** `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1`, `Day 2` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `stress_test.py`, `qa_agent.py`, `models.py`?**
  _High betweenness centrality (0.181) - this node is a cross-community bridge._
- **Why does `process_package()` connect `models.py` to `main.py`, `stress_test.py`, `LLMClient`, `run_seo_linter`, `qa_agent.py`, `generate_json_ld`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `run_seo_linter()` connect `run_seo_linter` to `main.py`, `LLMClient`, `models.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._