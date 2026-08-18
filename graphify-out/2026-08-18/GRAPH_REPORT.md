# Graph Report - yatradham-seo-pipeline  (2026-08-18)

## Corpus Check
- 16 files · ~29,747 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 145 nodes · 300 edges · 10 communities
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `154391bf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- database.py
- models.py
- pipeline.py
- LLMClient
- process_package
- content_agent.py

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 25 edges
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
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/keyword_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/meta_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/title_agent.py → llm_client.py

## Import Cycles
- None detected.

## Communities (10 total, 0 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.10
Nodes (26): get_stats(), Any, delete, FastAPI, get, BatchURLRequest, ContentGenerateRequest, delete_single_output() (+18 more)

### Community 2 - "database.py"
Cohesion: 0.22
Nodes (18): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), get_conn(), get_output(), init_db(), list_outputs() (+10 more)

### Community 4 - "models.py"
Cohesion: 0.23
Nodes (13): bulk_action(), Bulk approve or reject outputs., BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow (+5 more)

### Community 5 - "pipeline.py"
Cohesion: 0.12
Nodes (18): Any, Keyword agent: enforces 2-4 word primary keyword., run(), Any, Meta description agent: 145-155 chars, natural language, no repetition., run(), _check_banned(), _check_sections() (+10 more)

### Community 6 - "LLMClient"
Cohesion: 0.13
Nodes (18): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings., Strip LLM repetition loops (repeated single characters, phrases, or unicode…, 2-Stage chained generation for 2,500 - 3,500 word comprehensive master guides… (+10 more)

### Community 7 - "process_package"
Cohesion: 0.13
Nodes (21): BackgroundTasks, save_output(), batch_process(), batch_urls(), clear_cache(), process_batch_background(), process_single(), Scrape and process multiple URLs automatically in the background. (+13 more)

### Community 14 - "content_agent.py"
Cohesion: 0.40
Nodes (5): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run()

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `pipeline.py`, `content_agent.py`, `process_package`?**
  _High betweenness centrality (0.288) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `main.py`, `database.py`, `pipeline.py`, `LLMClient`, `content_agent.py`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `run()` connect `pipeline.py` to `LLMClient`, `process_package`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10317460317460317 - nodes in this community are weakly interconnected._