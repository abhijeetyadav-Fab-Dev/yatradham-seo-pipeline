# Graph Report - yatradham-seo-pipeline  (2026-08-17)

## Corpus Check
- 16 files · ~26,742 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 132 nodes · 271 edges · 10 communities
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ceb375bb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- LLMClient
- database.py
- post
- models.py
- qa_agent.py
- content_creator_agent.py

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 22 edges
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
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_row_to_output()` --uses--> `PackageInput`  [INFERRED]
  database.py → models.py
- `scrape_and_process()` --uses--> `PackageInput`  [INFERRED]
  main.py → models.py
- `process_batch_background()` --uses--> `PackageInput`  [INFERRED]
  main.py → models.py

## Import Cycles
- None detected.

## Communities (10 total, 0 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.09
Nodes (29): BackgroundTasks, get_stats(), Any, delete, FastAPI, get, batch_urls(), BatchURLRequest (+21 more)

### Community 1 - "LLMClient"
Cohesion: 0.10
Nodes (21): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+13 more)

### Community 2 - "database.py"
Cohesion: 0.22
Nodes (19): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), get_conn(), get_output(), init_db(), list_outputs() (+11 more)

### Community 3 - "post"
Cohesion: 0.18
Nodes (11): batch_process(), bulk_action(), clear_cache(), process_single(), Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (manual input)., Bulk approve or reject outputs., Wipe all outputs from the database to start fresh. (+3 more)

### Community 4 - "models.py"
Cohesion: 0.27
Nodes (12): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PackageInput, PricingRow, ProgramHighlights (+4 more)

### Community 5 - "qa_agent.py"
Cohesion: 0.43
Nodes (7): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run()

### Community 6 - "content_creator_agent.py"
Cohesion: 0.22
Nodes (9): _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings., Generate net-new content based on user requirements using robust markdown…, run(), ContentGenerateRequest, generate_content() (+1 more)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `qa_agent.py`, `content_creator_agent.py`?**
  _High betweenness centrality (0.234) - this node is a cross-community bridge._
- **Why does `process_package()` connect `LLMClient` to `main.py`, `database.py`, `post`, `models.py`, `qa_agent.py`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `run()` connect `qa_agent.py` to `LLMClient`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `LLMClient` (e.g. with `run()` and `run()`) actually correct?**
  _`LLMClient` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0907258064516129 - nodes in this community are weakly interconnected._