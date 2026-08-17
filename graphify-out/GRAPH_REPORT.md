# Graph Report - yatradham-seo-pipeline  (2026-08-17)

## Corpus Check
- 16 files · ~28,751 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 137 nodes · 278 edges · 19 communities (18 shown, 1 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `22a0d5b1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- get_stats
- pipeline.py
- database.py
- post
- models.py
- qa_agent.py
- content_creator_agent.py
- main.py
- batch_urls
- LLMClient
- content_agent.py
- process_package
- scrape_and_process
- ProviderSettingsRequest
- title_agent.py
- .test_provider

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 23 edges
2. `process_package()` - 16 edges
3. `SEOOutput` - 11 edges
4. `get_conn()` - 10 edges
5. `PackageInput` - 10 edges
6. `save_output()` - 9 edges
7. `SectionedContent` - 9 edges
8. `run()` - 8 edges
9. `scrape_and_process()` - 8 edges
10. `get_output()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/keyword_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/meta_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py

## Import Cycles
- None detected.

## Communities (19 total, 1 thin omitted)

### Community 0 - "get_stats"
Cohesion: 0.20
Nodes (10): get_stats(), Any, get, export_csv(), get_outputs(), get_single_output(), List all SEO outputs with optional filter., Export outputs to CSV. (+2 more)

### Community 1 - "pipeline.py"
Cohesion: 0.32
Nodes (4): Keyword agent: enforces 2-4 word primary keyword., Meta description agent: 145-155 chars, natural language, no repetition., OpenRouter LLM client with token-limit retry and rate limiting., Orchestrator: runs all 5 agents in sequence.

### Community 2 - "database.py"
Cohesion: 0.23
Nodes (18): bulk_update_status(), delete_output(), _dict_to_sections(), get_conn(), get_output(), init_db(), list_outputs(), SQLite database with JSON storage for sections. (+10 more)

### Community 3 - "post"
Cohesion: 0.20
Nodes (10): clear_all_outputs(), batch_process(), bulk_action(), clear_cache(), process_single(), Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (manual input)., Bulk approve or reject outputs. (+2 more)

### Community 4 - "models.py"
Cohesion: 0.27
Nodes (12): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PackageInput, PricingRow, ProgramHighlights (+4 more)

### Community 5 - "qa_agent.py"
Cohesion: 0.43
Nodes (7): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run()

### Community 6 - "content_creator_agent.py"
Cohesion: 0.33
Nodes (6): _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings., Generate net-new content based on user requirements using robust markdown…, run()

### Community 7 - "main.py"
Cohesion: 0.24
Nodes (8): delete, FastAPI, ContentGenerateRequest, delete_single_output(), generate_content(), lifespan(), FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…, Generate net-new SEO content from scratch using AI.

### Community 11 - "batch_urls"
Cohesion: 0.22
Nodes (8): BackgroundTasks, batch_urls(), process_batch_background(), Scrape and process multiple URLs automatically in the background., extract_package_data(), Any, Extract structured data from Yatradham HTML pages., Extract basic package metadata and raw text for LLM processing.

### Community 12 - "LLMClient"
Cohesion: 0.31
Nodes (3): LLMClient, Return a useful mock response when no LLM provider is available. For content…, Allow setting keys dynamically from UI or runtime.

### Community 13 - "content_agent.py"
Cohesion: 0.40
Nodes (5): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run()

### Community 14 - "process_package"
Cohesion: 0.33
Nodes (6): Any, run(), Any, run(), process_package(), Run the full pipeline on a single package.

### Community 15 - "scrape_and_process"
Cohesion: 0.40
Nodes (5): BatchURLRequest, BaseModel, Scrape a Yatradham URL and auto-process through all 5 agents., scrape_and_process(), URLRequest

### Community 16 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime., Test a provider API key live and return latency & status., test_provider_endpoint(), update_provider_settings()

### Community 17 - "title_agent.py"
Cohesion: 0.50
Nodes (3): Any, Title tag agent: 50-60 chars, optimized for click-through rate., run()

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `pipeline.py`, `qa_agent.py`, `content_creator_agent.py`, `main.py`, `content_agent.py`, `process_package`, `title_agent.py`, `.test_provider`?**
  _High betweenness centrality (0.263) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `pipeline.py`, `database.py`, `post`, `models.py`, `qa_agent.py`, `main.py`, `batch_urls`, `LLMClient`, `content_agent.py`, `scrape_and_process`, `title_agent.py`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `run()` connect `qa_agent.py` to `LLMClient`, `process_package`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `LLMClient` (e.g. with `run()` and `run()`) actually correct?**
  _`LLMClient` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 6 INFERRED edges - model-reasoned connections that need verification._