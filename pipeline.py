"""Orchestrator: runs all 5 agents with parallel acceleration."""
import json
import concurrent.futures
from typing import Dict, Any
from datetime import datetime
from models import SEOOutput, PackageInput, SectionedContent
from llm_client import LLMClient
from agents import keyword_agent, title_agent, meta_agent, content_agent, qa_agent


def process_package(package_input: PackageInput, client: LLMClient) -> SEOOutput:
    """Run the full pipeline on a single package with parallel agent execution."""
    pkg_data = package_input.model_dump()

    # Agent 1: Keywords (needed by downstream agents)
    kw_result = keyword_agent.run(pkg_data, client)
    primary_keyword = kw_result.get("primary_keyword", pkg_data.get("name", ""))

    # Run Agent 2 (Title), Agent 3 (Meta), and Agent 4 (Content) in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        f_title = pool.submit(title_agent.run, pkg_data, primary_keyword, client)
        f_content = pool.submit(content_agent.run, pkg_data, primary_keyword, client)
        title_result = f_title.result()
        title_tag = title_result.get("title_tag", primary_keyword)
        
        # Meta agent can run with the resolved title
        f_meta = pool.submit(meta_agent.run, pkg_data, title_tag, primary_keyword, client)
        meta_result = f_meta.result()
        content_result = f_content.result()

    meta_description = meta_result.get("meta_description", "")

    # Agent 5: QA Review
    qa_result = qa_agent.run(content_result, title_tag, meta_description, client)

    # Build output
    sections = SectionedContent(**content_result)
    now = datetime.now().isoformat()

    return SEOOutput(
        package_input=package_input,
        primary_keyword=primary_keyword,
        title_tag=title_tag,
        meta_description=meta_description,
        sections=sections,
        qa_score=qa_result.get("score", 0),
        qa_flags=qa_result.get("flags", []),
        status="pending",
        created_at=now,
        updated_at=now,
    )
