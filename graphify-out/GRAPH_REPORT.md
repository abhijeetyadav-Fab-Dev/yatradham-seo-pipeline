# Graph Report - yatradham-seo-pipeline  (2026-08-18)

## Corpus Check
- 16 files · ~28,956 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 142 nodes · 290 edges · 17 communities (16 shown, 1 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fce400f6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- keyword_agent.py
- database.py
- get_output
- models.py
- qa_agent.py
- content_creator_agent.py
- process_package
- list_outputs
- ._discover_active_models
- LLMClient
- content_agent.py
- llm_client.py
- title_agent.py

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 24 edges
2. `process_package()` - 16 edges
3. `SEOOutput` - 11 edges
4. `get_conn()` - 10 edges
5. `PackageInput` - 10 edges
6. `save_output()` - 9 edges
7. `SectionedContent` - 9 edges
8. `run()` - 8 edges
9. `scrape_and_process()` - 8 edges
10. `run()` - 7 edges

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

## Communities (17 total, 1 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.24
Nodes (9): delete_output(), get_stats(), Any, delete, FastAPI, delete_single_output(), lifespan(), FastAPI server with .env auto-loading, URL auto-scraping, batch processing,… (+1 more)

### Community 1 - "keyword_agent.py"
Cohesion: 0.50
Nodes (3): Any, Keyword agent: enforces 2-4 word primary keyword., run()

### Community 2 - "database.py"
Cohesion: 0.40
Nodes (9): bulk_update_status(), clear_all_outputs(), get_conn(), init_db(), SQLite database with JSON storage for sections., save_output(), _sections_to_dict(), update_output() (+1 more)

### Community 3 - "get_output"
Cohesion: 0.25
Nodes (8): _dict_to_sections(), get_output(), _row_to_output(), get_single_output(), Any, update_single_output(), put, Row

### Community 4 - "models.py"
Cohesion: 0.23
Nodes (14): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PackageInput, PricingRow, ProgramHighlights (+6 more)

### Community 5 - "qa_agent.py"
Cohesion: 0.43
Nodes (7): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run()

### Community 6 - "content_creator_agent.py"
Cohesion: 0.28
Nodes (8): _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings., Strip LLM repetition loops (repeated single characters, phrases, or unicode…, Generate net-new content based on user requirements using robust markdown…, run(), _sanitize_repetition()

### Community 7 - "process_package"
Cohesion: 0.08
Nodes (32): BackgroundTasks, batch_process(), batch_urls(), BatchURLRequest, bulk_action(), clear_cache(), ContentGenerateRequest, generate_content() (+24 more)

### Community 11 - "list_outputs"
Cohesion: 0.33
Nodes (7): list_outputs(), get, export_csv(), get_outputs(), List all SEO outputs with optional filter., Export outputs to CSV., root()

### Community 12 - "._discover_active_models"
Cohesion: 0.29
Nodes (5): Any, Allow setting keys dynamically from UI or runtime., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., OpenAI

### Community 14 - "content_agent.py"
Cohesion: 0.40
Nodes (5): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run()

### Community 15 - "llm_client.py"
Cohesion: 0.33
Nodes (4): Any, Meta description agent: 145-155 chars, natural language, no repetition., run(), OpenRouter LLM client with token-limit retry and rate limiting.

### Community 16 - "title_agent.py"
Cohesion: 0.50
Nodes (3): Any, Title tag agent: 50-60 chars, optimized for click-through rate., run()

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `keyword_agent.py`, `models.py`, `qa_agent.py`, `content_creator_agent.py`, `process_package`, `._discover_active_models`, `content_agent.py`, `llm_client.py`, `title_agent.py`?**
  _High betweenness centrality (0.277) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `main.py`, `keyword_agent.py`, `database.py`, `models.py`, `qa_agent.py`, `LLMClient`, `content_agent.py`, `llm_client.py`, `title_agent.py`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `run()` connect `content_creator_agent.py` to `LLMClient`, `process_package`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `LLMClient` (e.g. with `run()` and `run()`) actually correct?**
  _`LLMClient` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `process_package` be split into smaller, more focused modules?**
  _Cohesion score 0.07575757575757576 - nodes in this community are weakly interconnected._