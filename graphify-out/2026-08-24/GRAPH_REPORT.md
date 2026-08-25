# Graph Report - yatradham-seo-pipeline  (2026-08-24)

## Corpus Check
- 35 files · ~68,801 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 347 nodes · 717 edges · 25 communities (22 shown, 3 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4848c0e0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- test_e2e_suite.py
- LLMClient
- WordPressPublisher
- SitemapCrawler
- process_package
- qa_agent.py
- .sanitize_meta_description
- validation_layer.py
- extract_package_data
- content_creator_agent.py
- TestArchitecturalDecoupling
- enrich_destination_data
- models.py
- llm_client.py
- content_agent.py
- run_seo_linter
- generate_json_ld
- title_agent.py

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 37 edges
2. `process_package()` - 23 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `PackageInput` - 14 edges
6. `SectionedContent` - 13 edges
7. `save_output()` - 12 edges
8. `extract_package_data()` - 12 edges
9. `worker_db_stress()` - 12 edges
10. `run_validation()` - 12 edges

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

## Communities (25 total, 3 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.06
Nodes (59): BackgroundTasks, delete, FastAPI, batch_process(), batch_urls(), BatchURLRequest, bulk_action(), check_ai_endpoint() (+51 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.12
Nodes (40): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats() (+32 more)

### Community 3 - "LLMClient"
Cohesion: 0.16
Nodes (9): LLMClient, Any, Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., Strip internal thinking/reasoning tags leaked from thinking models., Return a rich, dynamic response when no LLM provider key is available.…, OpenAI (+1 more)

### Community 7 - "process_package"
Cohesion: 0.14
Nodes (14): Any, Keyword agent: enforces 2-4 word primary keyword., run(), Any, Meta description agent: 145-155 chars, natural language, no repetition., run(), get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem. (+6 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.18
Nodes (16): check_duplicate_content(), extract_price_number(), find_duplicated_words(), Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same…, Returns a report dict: { "status": "approved_candidate" | "flagged" |…, Returns (is_valid, error_message). Hard fail if destination is missing,… (+8 more)

### Community 14 - "extract_package_data"
Cohesion: 0.10
Nodes (23): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+15 more)

### Community 15 - "content_creator_agent.py"
Cohesion: 0.22
Nodes (15): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+7 more)

### Community 17 - "TestArchitecturalDecoupling"
Cohesion: 0.14
Nodes (8): Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio…, TestArchitecturalDecoupling

### Community 18 - "enrich_destination_data"
Cohesion: 0.10
Nodes (24): get, enrich_destination_endpoint(), get_outputs(), get_providers_status(), get_single_output(), List all SEO outputs with optional filter and pagination., Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Return status of configured backend AI providers. (+16 more)

### Community 19 - "models.py"
Cohesion: 0.29
Nodes (11): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession (+3 more)

### Community 20 - "llm_client.py"
Cohesion: 0.25
Nodes (6): localize_content(), Any, Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., Translate and culturally localize SEOOutput sections into Hindi or Gujarati., clean_price_string(), Sanitize and format price strings cleanly. Never return hardcoded mock numbers…

### Community 21 - "content_agent.py"
Cohesion: 0.40
Nodes (5): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run()

### Community 22 - "run_seo_linter"
Cohesion: 0.50
Nodes (4): calculate_flesch_reading_ease(), Any, Real-Time Dynamic SEO & GEO Linter for YatraDham. Performs rigorous, non-…, run_seo_linter()

### Community 23 - "generate_json_ld"
Cohesion: 0.40
Nodes (4): generate_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results, SGE…

### Community 24 - "title_agent.py"
Cohesion: 0.50
Nodes (3): Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate…, run()

## Knowledge Gaps
- **17 isolated node(s):** `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1`, `Day 2` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `test_e2e_suite.py`, `process_package`, `qa_agent.py`, `content_creator_agent.py`, `TestArchitecturalDecoupling`, `llm_client.py`, `content_agent.py`, `title_agent.py`?**
  _High betweenness centrality (0.198) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `main.py`, `process_package`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `main.py`, `test_e2e_suite.py`, `LLMClient`, `qa_agent.py`, `validation_layer.py`, `extract_package_data`, `content_agent.py`, `run_seo_linter`, `generate_json_ld`, `title_agent.py`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._