# Graph Report - yatradham-seo-pipeline  (2026-08-20)

## Corpus Check
- 16 files · ~31,637 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 148 nodes · 305 edges · 19 communities (16 shown, 3 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cbebb6bb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- generate_content
- main.py
- database.py
- LLMClient
- models.py
- pipeline.py
- content_creator_agent.py
- process_package
- qa_agent.py
- list_outputs
- ._discover_active_models
- content_agent.py
- get_conn
- run
- run
- run

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 26 edges
2. `process_package()` - 16 edges
3. `SEOOutput` - 11 edges
4. `get_conn()` - 10 edges
5. `PackageInput` - 10 edges
6. `run()` - 9 edges
7. `save_output()` - 9 edges
8. `SectionedContent` - 9 edges
9. `_generate_long_form_blog()` - 8 edges
10. `run()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_agent.py → llm_client.py
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/keyword_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/meta_agent.py → llm_client.py

## Import Cycles
- None detected.

## Communities (19 total, 3 thin omitted)

### Community 0 - "generate_content"
Cohesion: 0.18
Nodes (11): BatchURLRequest, ContentGenerateRequest, generate_content(), ProviderSettingsRequest, BaseModel, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime., Test a provider API key live and return latency & status., Generate net-new SEO content from scratch using AI. (+3 more)

### Community 1 - "main.py"
Cohesion: 0.24
Nodes (9): clear_all_outputs(), get_stats(), Any, FastAPI, clear_cache(), lifespan(), FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…, Wipe all outputs from the database to start fresh. (+1 more)

### Community 2 - "database.py"
Cohesion: 0.28
Nodes (12): _dict_to_sections(), get_output(), SQLite database with JSON storage for sections., _row_to_output(), _sections_to_dict(), update_output(), Any, update_single_output() (+4 more)

### Community 3 - "LLMClient"
Cohesion: 0.33
Nodes (3): LLMClient, Strip internal thinking/reasoning tags leaked from thinking models., Return a useful mock response when no LLM provider is available. For content…

### Community 4 - "models.py"
Cohesion: 0.23
Nodes (13): bulk_action(), Bulk approve or reject outputs., BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow (+5 more)

### Community 5 - "pipeline.py"
Cohesion: 0.31
Nodes (4): Keyword agent: enforces 2-4 word primary keyword., Meta description agent: 145-155 chars, natural language, no repetition., Title tag agent: 50-60 chars, optimized for click-through rate., Orchestrator: runs all 5 agents in sequence.

### Community 6 - "content_creator_agent.py"
Cohesion: 0.24
Nodes (13): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+5 more)

### Community 7 - "process_package"
Cohesion: 0.15
Nodes (19): BackgroundTasks, save_output(), batch_process(), batch_urls(), process_batch_background(), process_single(), Scrape and process multiple URLs automatically in the background., Process a single package through all 5 agents (manual JSON input). (+11 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.43
Nodes (7): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run()

### Community 12 - "list_outputs"
Cohesion: 0.29
Nodes (8): list_outputs(), get, export_csv(), get_outputs(), get_single_output(), List all SEO outputs with optional filter., Export outputs to CSV., root()

### Community 13 - "._discover_active_models"
Cohesion: 0.29
Nodes (5): Any, Allow setting keys dynamically from UI or runtime., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., OpenAI

### Community 14 - "content_agent.py"
Cohesion: 0.40
Nodes (5): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run()

### Community 15 - "get_conn"
Cohesion: 0.33
Nodes (6): bulk_update_status(), delete_output(), get_conn(), init_db(), delete, delete_single_output()

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `pipeline.py`, `content_creator_agent.py`, `process_package`, `qa_agent.py`, `._discover_active_models`, `content_agent.py`, `run`, `run`, `run`?**
  _High betweenness centrality (0.306) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `main.py`, `database.py`, `LLMClient`, `pipeline.py`, `qa_agent.py`, `content_agent.py`, `run`, `run`, `run`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Why does `run()` connect `qa_agent.py` to `LLMClient`, `process_package`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 6 INFERRED edges - model-reasoned connections that need verification._