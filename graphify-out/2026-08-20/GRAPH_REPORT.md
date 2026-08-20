# Graph Report - yatradham-seo-pipeline  (2026-08-20)

## Corpus Check
- 17 files · ~35,456 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 160 nodes · 375 edges · 15 communities (14 shown, 1 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a4e3fb20`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- post
- main.py
- test_e2e_suite.py
- LLMClient
- models.py
- delete_single_output
- content_creator_agent.py
- extract_package_data
- qa_agent.py
- get
- ProviderSettingsRequest
- scrape_and_process

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 30 edges
2. `run_suite()` - 19 edges
3. `process_package()` - 17 edges
4. `SEOOutput` - 13 edges
5. `PackageInput` - 12 edges
6. `save_output()` - 11 edges
7. `SectionedContent` - 11 edges
8. `get_conn()` - 10 edges
9. `run()` - 9 edges
10. `get_output()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_row_to_output()` --uses--> `PackageInput`  [INFERRED]
  database.py → models.py
- `process_batch_background()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py

## Import Cycles
- None detected.

## Communities (15 total, 1 thin omitted)

### Community 0 - "post"
Cohesion: 0.22
Nodes (9): batch_process(), bulk_action(), clear_cache(), process_single(), Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (manual input)., Bulk approve or reject outputs., Wipe all outputs from the database to start fresh. (+1 more)

### Community 1 - "main.py"
Cohesion: 0.24
Nodes (11): FastAPI, check_ai_endpoint(), CheckAIRequest, humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk(), HumanizeRequest, lifespan() (+3 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.21
Nodes (24): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), get_conn(), get_output(), get_stats(), init_db() (+16 more)

### Community 3 - "LLMClient"
Cohesion: 0.09
Nodes (25): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+17 more)

### Community 4 - "models.py"
Cohesion: 0.27
Nodes (12): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PackageInput, PricingRow, ProgramHighlights (+4 more)

### Community 6 - "content_creator_agent.py"
Cohesion: 0.24
Nodes (13): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+5 more)

### Community 7 - "extract_package_data"
Cohesion: 0.22
Nodes (8): BackgroundTasks, batch_urls(), process_batch_background(), Scrape and process multiple URLs automatically in the background., extract_package_data(), Any, Extract structured data from Yatradham HTML pages., Extract basic package metadata and raw text for LLM processing.

### Community 11 - "qa_agent.py"
Cohesion: 0.43
Nodes (7): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run()

### Community 12 - "get"
Cohesion: 0.25
Nodes (8): get, export_csv(), get_outputs(), get_single_output(), List all SEO outputs with optional filter., Export outputs to CSV., root(), stats()

### Community 16 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime., Test a provider API key live and return latency & status., test_provider_endpoint(), update_provider_settings()

### Community 19 - "scrape_and_process"
Cohesion: 0.25
Nodes (8): BatchURLRequest, ContentGenerateRequest, generate_content(), BaseModel, Generate net-new SEO content from scratch using AI., Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process(), URLRequest

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `test_e2e_suite.py`, `content_creator_agent.py`, `extract_package_data`, `qa_agent.py`, `scrape_and_process`?**
  _High betweenness centrality (0.274) - this node is a cross-community bridge._
- **Why does `process_package()` connect `LLMClient` to `post`, `main.py`, `test_e2e_suite.py`, `models.py`, `extract_package_data`, `qa_agent.py`, `scrape_and_process`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `run_suite()` connect `test_e2e_suite.py` to `main.py`, `LLMClient`, `models.py`, `content_creator_agent.py`, `extract_package_data`, `get`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 7 INFERRED edges - model-reasoned connections that need verification._