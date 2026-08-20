# Graph Report - yatradham-seo-pipeline  (2026-08-20)

## Corpus Check
- 16 files · ~34,142 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 156 nodes · 323 edges · 20 communities
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `15053f59`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- post
- main.py
- database.py
- LLMClient
- models.py
- pipeline.py
- content_creator_agent.py
- batch_urls
- qa_agent.py
- get
- ._discover_active_models
- process_package
- scrape_and_process
- humanize_endpoint
- meta_agent.py
- title_agent.py
- check_ai_endpoint

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

## Communities (20 total, 0 thin omitted)

### Community 0 - "post"
Cohesion: 0.18
Nodes (12): bulk_action(), clear_cache(), process_single(), ProviderSettingsRequest, Process a single package through all 5 agents (manual JSON input)., Bulk approve or reject outputs., Wipe all outputs from the database to start fresh., Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime. (+4 more)

### Community 1 - "main.py"
Cohesion: 0.32
Nodes (6): FastAPI, ContentGenerateRequest, generate_content(), lifespan(), FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…, Generate net-new SEO content from scratch using AI.

### Community 2 - "database.py"
Cohesion: 0.17
Nodes (23): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), get_conn(), get_output(), get_stats(), init_db() (+15 more)

### Community 3 - "LLMClient"
Cohesion: 0.33
Nodes (3): LLMClient, Strip internal thinking/reasoning tags leaked from thinking models., Return a useful mock response when no LLM provider is available. For content…

### Community 4 - "models.py"
Cohesion: 0.22
Nodes (14): batch_process(), Process multiple packages from JSON (manual input)., BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PackageInput (+6 more)

### Community 5 - "pipeline.py"
Cohesion: 0.38
Nodes (3): Content agent: generates all 19 structured sections from scraped page data., Keyword agent: enforces 2-4 word primary keyword., Orchestrator: runs all 5 agents in sequence.

### Community 6 - "content_creator_agent.py"
Cohesion: 0.24
Nodes (13): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+5 more)

### Community 7 - "batch_urls"
Cohesion: 0.22
Nodes (8): BackgroundTasks, batch_urls(), process_batch_background(), Scrape and process multiple URLs automatically in the background., extract_package_data(), Any, Extract structured data from Yatradham HTML pages., Extract basic package metadata and raw text for LLM processing.

### Community 11 - "qa_agent.py"
Cohesion: 0.43
Nodes (7): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run()

### Community 12 - "get"
Cohesion: 0.25
Nodes (8): get, export_csv(), get_outputs(), get_single_output(), List all SEO outputs with optional filter., Export outputs to CSV., root(), stats()

### Community 13 - "._discover_active_models"
Cohesion: 0.29
Nodes (5): Any, Allow setting keys dynamically from UI or runtime., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., OpenAI

### Community 14 - "process_package"
Cohesion: 0.25
Nodes (8): _extract_json_from_response(), Any, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, run(), process_package(), Run the full pipeline on a single package.

### Community 15 - "scrape_and_process"
Cohesion: 0.40
Nodes (5): BatchURLRequest, BaseModel, Scrape a Yatradham URL and auto-process through all 5 agents., scrape_and_process(), URLRequest

### Community 16 - "humanize_endpoint"
Cohesion: 0.40
Nodes (5): humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk(), HumanizeRequest, Humanize multi-section markdown text concurrently while preserving headings and…

### Community 17 - "meta_agent.py"
Cohesion: 0.50
Nodes (3): Any, Meta description agent: 145-155 chars, natural language, no repetition., run()

### Community 18 - "title_agent.py"
Cohesion: 0.50
Nodes (3): Any, Title tag agent: 50-60 chars, optimized for click-through rate., run()

### Community 19 - "check_ai_endpoint"
Cohesion: 0.67
Nodes (3): check_ai_endpoint(), CheckAIRequest, query_undetectable_detector()

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `pipeline.py`, `content_creator_agent.py`, `qa_agent.py`, `._discover_active_models`, `process_package`, `meta_agent.py`, `title_agent.py`?**
  _High betweenness centrality (0.294) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `post`, `main.py`, `database.py`, `LLMClient`, `models.py`, `pipeline.py`, `batch_urls`, `qa_agent.py`, `scrape_and_process`, `meta_agent.py`, `title_agent.py`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `run()` connect `qa_agent.py` to `LLMClient`, `process_package`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 6 INFERRED edges - model-reasoned connections that need verification._