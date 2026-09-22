"""
Comprehensive Test Suite for 55-Pattern Humanizer Engine & 5 Voice Profiles
Integrates standards from:
- Aboudjem/humanizer-skill (55 patterns, 5 voices, burstiness std-dev, em-dash ban, non-fabrication)
- blader/humanizer (25 core AI tells across 5 categories)
- topics/text-humanizer (statistical burstiness modeling & structure preservation)
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anti_ai_guardrails import (
    HUMANIZER_55_PATTERNS,
    AI_REPLACEMENT_TABLE,
    VOICE_PROFILES,
    detect_55_patterns,
    calculate_copyleaks_metrics,
    de_slop_and_humanize,
    calculate_burstiness_metrics,
)


class TestHumanizer55Patterns:
    """Verify that all 55 patterns are defined, detectable, and actionable."""

    def test_all_55_patterns_registered(self):
        """Ensure all 55 patterns (P01 through P55) are correctly registered."""
        assert len(HUMANIZER_55_PATTERNS) >= 55, f"Expected >= 55 patterns, found {len(HUMANIZER_55_PATTERNS)}"
        ids = [p["id"] for p in HUMANIZER_55_PATTERNS]
        for i in range(1, 56):
            expected_id = f"P{i:02d}"
            assert expected_id in ids, f"Pattern {expected_id} is missing from HUMANIZER_55_PATTERNS"

    def test_pattern_detection_significance_inflation(self):
        """P01: Detects 'stands as a testament to' and 'pivotal role'."""
        text = "This temple stands as a testament to the devotion of pilgrims and plays a pivotal role in Haridwar."
        res = detect_55_patterns(text)
        detected_ids = [p["id"] for p in res["detected_patterns"]]
        assert "P01" in detected_ids
        assert res["total_pattern_count"] >= 1
        assert res["pattern_score"] > 0

    def test_pattern_detection_em_dash_ban(self):
        """P13: Detects em-dash overuse."""
        text = "The Ganga Aarti ceremony—held daily at sunset—draws thousands of devotees."
        res = detect_55_patterns(text)
        detected_ids = [p["id"] for p in res["detected_patterns"]]
        assert "P13" in detected_ids

    def test_pattern_detection_negative_parallelism(self):
        """P09: Detects 'not only X, but also Y'."""
        text = "The temple is not only a spiritual sanctuary, but also an architectural wonder."
        res = detect_55_patterns(text)
        detected_ids = [p["id"] for p in res["detected_patterns"]]
        assert "P09" in detected_ids

    def test_pattern_detection_superficial_ing(self):
        """P03: Detects trailing -ing phrases."""
        text = "The priest offers prayers every morning, highlighting the importance of inner peace."
        res = detect_55_patterns(text)
        detected_ids = [p["id"] for p in res["detected_patterns"]]
        assert "P03" in detected_ids

    def test_pattern_detection_chat_residue(self):
        """P18: Detects chatbot residue like 'Certainly! Here is a guide'."""
        text = "Certainly! Here is a detailed breakdown of your spiritual tour. I hope this helps!"
        res = detect_55_patterns(text)
        detected_ids = [p["id"] for p in res["detected_patterns"]]
        assert "P18" in detected_ids

    def test_pattern_detection_throat_clearing(self):
        """P20: Detects 'In today's fast-paced world' and 'When it comes to'."""
        text = "In today's fast-paced world, finding peace is hard. When it comes to spiritual journeys, Dwarka is best."
        res = detect_55_patterns(text)
        detected_ids = [p["id"] for p in res["detected_patterns"]]
        assert "P20" in detected_ids


class TestDeSlopAndHumanize:
    """Verify deterministic de-slopping, em-dash removal, and replacements."""

    def test_em_dash_eradication(self):
        """Em dashes must be replaced with commas, colons, or clean punctuation."""
        text = "The evening aarti—a sacred ritual—starts at 7:00 PM."
        humanized = de_slop_and_humanize(text)
        assert "—" not in humanized
        assert "--" not in humanized
        assert "7:00 PM" in humanized

    def test_negative_parallelism_transformation(self):
        """'not only X, but also Y' should be transformed to natural 'X and Y'."""
        text = "The package is not only affordable, but also includes full meals."
        humanized = de_slop_and_humanize(text)
        assert "not only" not in humanized.lower()
        assert "affordable" in humanized
        assert "meals" in humanized

    def test_buzzword_replacements(self):
        """Key AI buzzwords must be replaced with clean plain English."""
        text = "We leverage cutting-edge facilities to delve into a transformative journey nestled in Rishikesh."
        humanized = de_slop_and_humanize(text)
        assert "leverage" not in humanized.lower()
        assert "cutting-edge" not in humanized.lower()
        assert "delve into" not in humanized.lower()
        assert "transformative journey" not in humanized.lower()
        assert "nestled" not in humanized.lower()

    def test_preserves_markdown_tables_and_code(self):
        """Markdown tables, URLs, and code blocks must not be corrupted."""
        text = (
            "| Room Type | Price |\n"
            "| --- | --- |\n"
            "| AC Deluxe | ₹1,500 |\n"
            "| Non-AC | ₹800 |\n\n"
            "Visit [Official Portal](https://yatradham.org/packages) for details."
        )
        humanized = de_slop_and_humanize(text)
        assert "| Room Type | Price |" in humanized
        assert "₹1,500" in humanized
        assert "https://yatradham.org/packages" in humanized

    def test_curly_quotes_normalized(self):
        """Smart curly quotes must be normalized to straight ASCII quotes."""
        text = "“Special Darshan” at ‘Badrinath’"
        humanized = de_slop_and_humanize(text)
        assert "“" not in humanized
        assert "”" not in humanized
        assert "‘" not in humanized
        assert "’" not in humanized
        assert '"Special Darshan"' in humanized or "'Special Darshan'" in humanized


class TestVoiceProfiles:
    """Verify that the 5 distinct voice profiles apply their characteristics."""

    def test_casual_voice(self):
        """Casual voice introduces natural contractions and conversational tone."""
        text = "Do not forget that you cannot bring cameras inside the temple. It is strictly prohibited."
        humanized = de_slop_and_humanize(text, voice="casual")
        assert "don't" in humanized.lower() or "can't" in humanized.lower() or "it's" in humanized.lower()

    def test_blunt_voice(self):
        """Blunt voice strips hedging and fluff."""
        text = "It seems that perhaps you might want to consider booking early, as it is somewhat busy."
        humanized = de_slop_and_humanize(text, voice="blunt")
        assert "perhaps" not in humanized.lower()
        assert "somewhat" not in humanized.lower()

    def test_technical_voice(self):
        """Technical voice preserves facts and strips flowery praise."""
        text = "Experience the truly breathtaking and magnificent temple situated 12 km from station with ₹500 fee."
        humanized = de_slop_and_humanize(text, voice="technical")
        assert "12 km" in humanized
        assert "₹500" in humanized
        assert "breathtaking" not in humanized.lower()

    def test_warm_voice(self):
        """Warm voice maintains compassionate, pilgrim-friendly atmosphere."""
        text = "The dharamshala provides clean drinking water and a welcoming environment for elderly pilgrims."
        humanized = de_slop_and_humanize(text, voice="warm")
        assert "pilgrim" in humanized.lower()
        assert "clean" in humanized.lower()

    def test_professional_voice(self):
        """Professional voice ensures clear, authoritative prose without corporate jargon."""
        text = "We will optimize bandwidth and leverage synergies in order to coordinate the Aarti."
        humanized = de_slop_and_humanize(text, voice="professional")
        assert "synergies" not in humanized.lower()
        assert "bandwidth" not in humanized.lower()
        assert "in order to" not in humanized.lower()


class TestBurstinessMetrics:
    """Verify statistical burstiness calculation."""

    def test_high_burstiness_for_varied_sentences(self):
        """Human text with short and long sentences should yield high burstiness."""
        text = "Stop now. The morning Ganga Aarti at Har Ki Pauri begins precisely at dawn with holy chimes and thousands of gathered devotees. It is quiet. Later, priests chant Vedic hymns."
        metrics = calculate_burstiness_metrics(text)
        assert metrics["burstiness_score"] >= 60.0
        assert metrics["std_dev"] > 4.0

    def test_low_burstiness_for_uniform_sentences(self):
        """Monotonous text with uniform sentence lengths yields lower burstiness."""
        text = (
            "The temple opens early in the morning for all devotees to pray. "
            "The priests chant sacred hymns while lighting brass lamps at dawn. "
            "Visitors walk along the stone pathways to receive blessed food items. "
            "The river flows past the ancient ghats where pilgrims gather today."
        )
        metrics = calculate_burstiness_metrics(text)
        # Sentence lengths are all around 12-14 words, std_dev should be low
        assert metrics["std_dev"] < 4.0


class TestFastAPIHumanizerEndpoints:
    """Verify the FastAPI HTTP endpoints for check-ai, humanize, and patterns."""

    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)

    def test_get_patterns_endpoint(self, client):
        """GET /api/humanizer/patterns returns 55 patterns and voice profiles."""
        res = client.get("/api/humanizer/patterns")
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["total_patterns"] >= 55
        assert "voices" in data
        assert "casual" in data["voices"]
        assert "professional" in data["voices"]

    def test_check_ai_endpoint(self, client):
        """POST /api/check-ai returns 55-pattern detection and burstiness."""
        payload = {
            "text": "This temple stands as a testament to ancient architecture—a pivotal moment in history. Moreover, it is crucial to delve into it."
        }
        res = client.post("/api/check-ai", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert "patterns_detected" in data
        assert data["pattern_count"] >= 1
        assert "burstiness_score" in data
        assert "eeat_score" in data

    def test_humanize_endpoint(self, client):
        """POST /api/humanize transforms text using selected voice profile and strips em-dashes."""
        payload = {
            "text": "We will leverage cutting-edge facilities—a true testament to quality—to delve into your sacred stay in Rishikesh.",
            "voice": "casual"
        }
        res = client.post("/api/humanize", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert "humanized_text" in data
        assert "—" not in data["humanized_text"]
        assert "leverage" not in data["humanized_text"].lower()
        assert data["voice_used"] == "casual"

