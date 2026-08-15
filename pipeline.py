"""Orchestrator: runs all 5 agents in sequence."""
import json
from typing import Dict, Any
from datetime import datetime
from models import SEOOutput, PackageInput, SectionedContent
from llm_client import LLMClient
from agents import keyword_agent, title_agent, meta_agent, content_agent, qa_agent


def process_package(package_input: PackageInput, client: LLMClient) -> SEOOutput:
    """Run the full pipeline on a single package."""
    pkg_data = package_input.model_dump()

    # Agent 1: Keywords
    kw_result = keyword_agent.run(pkg_data, client)
    primary_keyword = kw_result.get("primary_keyword", pkg_data.get("name", ""))

    # Agent 2: Title
    title_result = title_agent.run(pkg_data, primary_keyword, client)
    title_tag = title_result.get("title_tag", primary_keyword)

    # Agent 3: Meta
    meta_result = meta_agent.run(pkg_data, title_tag, primary_keyword, client)
    meta_description = meta_result.get("meta_description", "")

    # Agent 4: Content (all 19 sections)
    content_result = content_agent.run(pkg_data, primary_keyword, client)

    # Agent 5: QA
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
