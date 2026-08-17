# main.py

> 30 nodes · cohesion 0.09

## Key Concepts

- **main.py** (45 connections) — `main.py`
- **batch_urls()** (6 connections) — `main.py`
- **get_stats()** (5 connections) — `database.py`
- **get** (5 connections)
- **generate_content()** (5 connections) — `main.py`
- **clear_cache()** (4 connections) — `main.py`
- **export_csv()** (4 connections) — `main.py`
- **get_outputs()** (4 connections) — `main.py`
- **BatchURLRequest** (3 connections) — `main.py`
- **ContentGenerateRequest** (3 connections) — `main.py`
- **delete_single_output()** (3 connections) — `main.py`
- **get_single_output()** (3 connections) — `main.py`
- **BaseModel** (3 connections)
- **stats()** (3 connections) — `main.py`
- **URLRequest** (3 connections) — `main.py`
- **scraper.py** (3 connections) — `scraper.py`
- **FastAPI** (2 connections)
- **lifespan()** (2 connections) — `main.py`
- **root()** (2 connections) — `main.py`
- **BackgroundTasks** (1 connections)
- **Any** (1 connections)
- **delete** (1 connections)
- **e2e_test.py** (1 connections) — `e2e_test.py`
- **FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…** (1 connections) — `main.py`
- **Scrape and process multiple URLs automatically in the background.** (1 connections) — `main.py`
- *... and 5 more nodes in this community*

## Relationships

- [database.py](database.py.md) (18 shared connections)
- [process_package](process_package.md) (15 shared connections)
- [models.py](models.py.md) (4 shared connections)
- [LLMClient](LLMClient.md) (2 shared connections)
- [content_creator_agent.py](content_creator_agent.py.md) (2 shared connections)

## Source Files

- `database.py`
- `e2e_test.py`
- `main.py`
- `scraper.py`

## Audit Trail

- EXTRACTED: 118 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*