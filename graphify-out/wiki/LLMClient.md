# LLMClient

> 26 nodes · cohesion 0.11

## Key Concepts

- **LLMClient** (20 connections) — `llm_client.py`
- **llm_client.py** (10 connections) — `llm_client.py`
- **content_agent.py** (6 connections) — `agents/content_agent.py`
- **run()** (5 connections) — `agents/content_agent.py`
- **keyword_agent.py** (5 connections) — `agents/keyword_agent.py`
- **meta_agent.py** (5 connections) — `agents/meta_agent.py`
- **title_agent.py** (5 connections) — `agents/title_agent.py`
- **run()** (4 connections) — `agents/keyword_agent.py`
- **run()** (4 connections) — `agents/meta_agent.py`
- **run()** (4 connections) — `agents/title_agent.py`
- **_extract_json_from_response()** (3 connections) — `agents/content_agent.py`
- **.chat_completion()** (3 connections) — `llm_client.py`
- **._mock_response()** (3 connections) — `llm_client.py`
- **._wait_for_rate_limit()** (2 connections) — `llm_client.py`
- **Any** (1 connections)
- **Content agent: generates all 19 structured sections from scraped page data.** (1 connections) — `agents/content_agent.py`
- **Robustly extract JSON from LLM response, handling markdown blocks and…** (1 connections) — `agents/content_agent.py`
- **Any** (1 connections)
- **Keyword agent: enforces 2-4 word primary keyword.** (1 connections) — `agents/keyword_agent.py`
- **Any** (1 connections)
- **Meta description agent: 145-155 chars, natural language, no repetition.** (1 connections) — `agents/meta_agent.py`
- **Any** (1 connections)
- **Title tag agent: 50-60 chars, optimized for click-through rate.** (1 connections) — `agents/title_agent.py`
- **.__init__()** (1 connections) — `llm_client.py`
- **OpenRouter LLM client with token-limit retry and rate limiting.** (1 connections) — `llm_client.py`
- *... and 1 more nodes in this community*

## Relationships

- [process_package](process_package.md) (11 shared connections)
- [content_creator_agent.py](content_creator_agent.py.md) (3 shared connections)
- [qa_agent.py](qa_agent.py.md) (3 shared connections)
- [main.py](main.py.md) (2 shared connections)

## Source Files

- `agents/content_agent.py`
- `agents/keyword_agent.py`
- `agents/meta_agent.py`
- `agents/title_agent.py`
- `llm_client.py`

## Audit Trail

- EXTRACTED: 80 (88%)
- INFERRED: 11 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*