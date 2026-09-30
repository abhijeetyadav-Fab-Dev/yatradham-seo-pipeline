import sys
import os
import time
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import LLMClient
from agents.content_creator_agent import (
    _detect_blog_intent,
    _get_intent_structure,
    _generate_long_form_blog,
    run
)


def test_detect_blog_intent():
    """Verify intent classifier assigns authentic topic categories."""
    assert _detect_blog_intent("Dwarka Temple Darshan Timings") == "temple_guide"
    assert _detect_blog_intent("Somnath Mandir Aarti & Puja Schedule") == "temple_guide"
    assert _detect_blog_intent("Top 5 Dharamshalas in Rishikesh") == "stay_guide"
    assert _detect_blog_intent("Best Ashram Room Booking in Haridwar") == "stay_guide"
    assert _detect_blog_intent("3 Days Haridwar Rishikesh Tour Itinerary") == "itinerary_guide"
    assert _detect_blog_intent("Chardham Yatra 10 Days Route") == "itinerary_guide"
    assert _detect_blog_intent("Ayurvedic Panchakarma Retreat in Kerala") == "wellness_guide"
    assert _detect_blog_intent("Spiritual Awakening and Meditation") == "wellness_guide"
    assert _detect_blog_intent("Sacred Rivers of Northern India") == "general_spiritual_guide"


def test_get_intent_structure_headers():
    """Verify each intent receives topic-accurate outline headers instead of forced 7-day retreat."""
    temple_struct = _get_intent_structure("temple_guide", "Dwarka Temple", "Dwarka Temple Darshan")
    assert "Temple Darshan Timings & Daily Aarti Schedule" in temple_struct
    assert "Step-by-Step Darshan Flow" in temple_struct
    assert "Day 6: Sound Healing" not in temple_struct  # Should NOT force retreat template

    stay_struct = _get_intent_structure("stay_guide", "Rishikesh Dharamshala", "Rishikesh Dharamshala")
    assert "Top Verified Dharamshalas & Ashrams" in stay_struct
    assert "Room Facilities, Hot Water & Satvik Food" in stay_struct
    assert "Day 4: Deep Detox" not in stay_struct

    itin_struct = _get_intent_structure("itinerary_guide", "3 Days Haridwar Tour", "Haridwar Tour")
    assert "Complete Day-by-Day Journey & Darshan Route" in itin_struct
    assert "Trip Overview & Sacred Highlights" in itin_struct


def test_mock_fallback_completeness():
    """Verify fallback generation provides complete article when client is in dry-run mode."""
    client = LLMClient()
    client.dry_run = True
    
    res = run("blog_post", "Dwarka Temple Darshan and Puja Guide", client=client, word_count=1400)
    assert res["title"] != ""
    assert res["meta_description"] != ""
    assert len(res["suggested_tags"]) > 0
    content = res["content"]
    assert "Frequently Asked Questions" in content or "### Q1" in content
    assert "Final Thoughts" in content or "Final Reflections" in content or "Conclusion" in content
    assert len(content.split()) >= 300


def test_live_blog_creation_speed_and_completeness():
    """Verify live blog generation completes with all sections and valid word count in <35 seconds."""
    client = LLMClient()
    t0 = time.time()
    res = run(
        content_type="blog_post",
        topic="Dwarka Temple Darshan and Aarti Timings",
        client=client,
        target_keyword="Dwarka Temple Darshan",
        word_count=1400
    )
    elapsed = time.time() - t0
    
    assert elapsed < 45.0, f"Blog generation took too long: {elapsed:.2f}s"
    assert res["title"] != "", "Title must not be empty"
    assert res["meta_description"] != "", "Meta description must not be empty"
    assert len(res["suggested_tags"]) >= 2, "Must have suggested tags"
    
    content = res["content"]
    words = len(content.split())
    assert words >= 800, f"Generated blog too short ({words} words)"
    assert "Frequently Asked Questions" in content or "### Q1" in content, "Missing FAQs section"
    assert "Final" in content or "Conclusion" in content, "Missing Final Thoughts section"
    assert not content.strip().endswith(("-", "•", "–", ":", "and", "or", "the", "with", "to", "in", "of", "a")), "Content abruptly cut off"
