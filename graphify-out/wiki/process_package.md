# process_package

> 17 nodes · cohesion 0.19

## Key Concepts

- **process_package()** (16 connections) — `pipeline.py`
- **pipeline.py** (14 connections) — `pipeline.py`
- **PackageInput** (10 connections) — `models.py`
- **save_output()** (9 connections) — `database.py`
- **scrape_and_process()** (8 connections) — `main.py`
- **post** (7 connections)
- **batch_process()** (6 connections) — `main.py`
- **process_batch_background()** (6 connections) — `main.py`
- **process_single()** (6 connections) — `main.py`
- **extract_package_data()** (6 connections) — `scraper.py`
- **Process a single package through all 5 agents (manual JSON input).** (1 connections) — `main.py`
- **Process multiple packages from JSON (manual input).** (1 connections) — `main.py`
- **Scrape a Yatradham URL and auto-process through all 5 agents.** (1 connections) — `main.py`
- **Orchestrator: runs all 5 agents in sequence.** (1 connections) — `pipeline.py`
- **Run the full pipeline on a single package.** (1 connections) — `pipeline.py`
- **Any** (1 connections)
- **Extract basic package metadata and raw text for LLM processing.** (1 connections) — `scraper.py`

## Relationships

- [main.py](main.py.md) (15 shared connections)
- [LLMClient](LLMClient.md) (11 shared connections)
- [database.py](database.py.md) (10 shared connections)
- [models.py](models.py.md) (5 shared connections)
- [qa_agent.py](qa_agent.py.md) (2 shared connections)

## Source Files

- `database.py`
- `main.py`
- `models.py`
- `pipeline.py`
- `scraper.py`

## Audit Trail

- EXTRACTED: 80 (84%)
- INFERRED: 15 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*