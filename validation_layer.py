"""
Yatradham SEO Pipeline — Validation Layer
==========================================
Drop-in checks to run on every generated row BEFORE it can be marked
"Approved" or queued for WordPress publish. Designed to replace the
current self-graded "QA Score" (which the LLM assigns to its own output)
with objective, code-based checks.

Wire this in as: generate_content() -> run_validation(row) -> review queue
A row that fails any HARD check should be auto-set to "Rejected" or
"Flagged for Review" — never allowed to reach "Approved" automatically.
"""

import re
from difflib import SequenceMatcher

# ---------------------------------------------------------------------
# 1. DESTINATION VALIDATION
# ---------------------------------------------------------------------
# Problem observed: LLM invented destinations like "Seven Days Ayurveda"
# or "Wellness.Yatradham.Org" when the scraper found no real location.
#
# Fix: destination must match "City, State" against a known list of
# valid Indian states/UTs, and must NOT contain duration/product words.

INDIAN_STATES_UTS = {
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand",
    "karnataka", "kerala", "madhya pradesh", "maharashtra", "manipur",
    "meghalaya", "mizoram", "nagaland", "odisha", "punjab", "rajasthan",
    "sikkim", "tamil nadu", "telangana", "tripura", "uttar pradesh",
    "uttarakhand", "west bengal", "delhi", "jammu and kashmir", "ladakh",
    "puducherry", "chandigarh", "andaman and nicobar islands",
    "dadra and nagar haveli and daman and diu", "lakshadweep",
}

# Words that indicate the LLM substituted a product/duration label
# instead of a real place name.
DESTINATION_BLOCKLIST_WORDS = {
    "day", "days", "night", "nights", "yoga", "ayurveda", "wellness",
    "retreat", "package", "camp", "program", ".org", ".com", "yatradham",
}


def validate_destination(destination: str) -> tuple[bool, str]:
    """
    Returns (is_valid, error_message).
    Hard fail if destination is missing, malformed, or contains a
    blocklisted word (strong signal of an LLM-hallucinated location).
    """
    if not destination or not destination.strip():
        return False, "Destination is empty."

    dest_lower = destination.lower()

    # Must contain a comma separating city from state (our data format)
    if "," not in destination:
        return False, f"Destination '{destination}' is not in 'City, State' format."

    city_part, state_part = [p.strip() for p in destination.split(",", 1)]

    # Reject if any blocklisted word appears anywhere in the string
    for word in DESTINATION_BLOCKLIST_WORDS:
        if word in dest_lower:
            return False, f"Destination '{destination}' contains suspicious term '{word}' — likely hallucinated, not a real place."

    # State part must match a known Indian state/UT (case-insensitive)
    st_low = state_part.lower()
    ct_low = city_part.lower()
    if st_low not in INDIAN_STATES_UTS:
        if st_low in ["india", "bharat"] and ct_low in INDIAN_STATES_UTS:
            return True, "OK"
        return False, f"State '{state_part}' not recognized — verify or add to INDIAN_STATES_UTS list."

    return True, "OK"



# ---------------------------------------------------------------------
# 2. PRICE SANITY CHECK
# ---------------------------------------------------------------------
# Problem observed: row priced at "₹24 Per Person" for a wellness retreat.
#
# Fix: enforce a realistic price floor/ceiling per night. Adjust these
# bounds based on your actual catalog range.

MIN_PRICE_PER_NIGHT_INR = 500      # anything below this is almost certainly a scrape/parse error
MAX_PRICE_PER_NIGHT_INR = 100_000  # sanity ceiling — flag extreme outliers for human check


def extract_price_number(price_string: str) -> int | None:
    """Extract the numeric ₹ amount from a string like 'Starting From ₹ 13,125.00 Per Person'."""
    match = re.search(r"₹\s*([\d,]+(?:\.\d+)?)", price_string)
    if not match:
        return None
    return int(float(match.group(1).replace(",", "")))


def validate_price(price_string: str) -> tuple[bool, str]:
    if not price_string or not price_string.strip():
        return False, "Price field is empty."
    if any(q in price_string.lower() for q in ["contact for pricing", "on request", "inquire", "custom quote"]):
        return True, "Price on request / custom quote mode."
    amount = extract_price_number(price_string)
    if amount is None:
        return False, f"Could not parse a numeric price from '{price_string}'."
    if amount < MIN_PRICE_PER_NIGHT_INR:
        return False, f"Price ₹{amount} is below realistic floor (₹{MIN_PRICE_PER_NIGHT_INR}) — likely a scrape/currency parsing error."
    if amount > MAX_PRICE_PER_NIGHT_INR:
        return False, f"Price ₹{amount} exceeds sanity ceiling (₹{MAX_PRICE_PER_NIGHT_INR}) — flag for manual check."
    return True, "OK"



# ---------------------------------------------------------------------
# 3. DUPLICATED-WORD / GRAMMAR CHECK
# ---------------------------------------------------------------------
# Problem observed: "Guided Guided morning nature walk..." appearing
# across 21 of 25 rows — same word repeated back-to-back.

def find_duplicated_words(text: str) -> list[str]:
    """Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'."""
    return re.findall(r"\b(\w+)\s+\1\b", text, flags=re.IGNORECASE)


def validate_no_duplicated_words(full_row_text: str) -> tuple[bool, str]:
    dupes = find_duplicated_words(full_row_text)
    if dupes:
        return False, f"Duplicated word(s) found: {sorted(set(dupes))}. Likely a prompt template bug — check master prompt."
    return True, "OK"


# ---------------------------------------------------------------------
# 4. DUPLICATE-CONTENT / TEMPLATING SIMILARITY CHECK
# ---------------------------------------------------------------------
# Problem observed: all 25 rows share near-identical "Why Choose" /
# "Who Can Join" / "Benefits" sections — a duplicate-content SEO risk.
#
# Fix: compare each new row's key sections against all previously
# approved rows. Flag (don't hard-block — some similarity is expected
# for a template) if similarity exceeds a threshold, so a human decides
# whether more rewriting is needed before publishing.

SIMILARITY_WARN_THRESHOLD = 0.85  # 85%+ textual similarity triggers a flag


def text_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def check_duplicate_content(new_section_text: str, existing_rows_section_texts: list[str]) -> tuple[bool, str]:
    """
    Compare one section (e.g. 'why_choose_bullets') of the new row against
    the same section across all existing approved rows.
    Returns (is_ok, message). is_ok=False means "flag for human review",
    not necessarily reject — duplication across a templated field set is
    expected to some degree.
    """
    for i, existing_text in enumerate(existing_rows_section_texts):
        score = text_similarity(new_section_text, existing_text)
        if score >= SIMILARITY_WARN_THRESHOLD:
            return False, f"{score:.0%} similar to existing approved row #{i} — consider rewriting for uniqueness."
    return True, "OK"


# ---------------------------------------------------------------------
# 5. REQUIRED FIELD COMPLETENESS
# ---------------------------------------------------------------------
REQUIRED_FIELDS = [
    "package_name", "primary_keyword", "title_tag", "meta_description",
    "quick_facts_destination", "quick_facts_cost", "itinerary",
    "pricing_table", "inclusions", "exclusions", "faq",
]


def validate_required_fields(row: dict) -> tuple[bool, str]:
    missing = [f for f in REQUIRED_FIELDS if not row.get(f, "").strip()]
    if missing:
        return False, f"Missing required fields: {missing}"
    return True, "OK"


# ---------------------------------------------------------------------
# 6. TITLE / PRODUCT NAME CONSISTENCY CHECK
# ---------------------------------------------------------------------
# Problem observed: title_tag said "Tour Package" while package_name
# said "Corporate Excellence Program" — mismatched product framing.

def validate_title_matches_product(package_name: str, title_tag: str) -> tuple[bool, str]:
    # crude but effective: check that a meaningful chunk of package_name
    # words appear in title_tag
    name_words = {w.lower() for w in re.findall(r"[a-zA-Z]{4,}", package_name)}
    title_words = {w.lower() for w in re.findall(r"[a-zA-Z]{4,}", title_tag)}
    overlap = name_words & title_words
    if len(overlap) < max(1, len(name_words) // 3):
        return False, f"title_tag ('{title_tag}') shares little vocabulary with package_name ('{package_name}') — likely mismatched category/product."
    return True, "OK"


# ---------------------------------------------------------------------
# ORCHESTRATOR — run all checks on one row
# ---------------------------------------------------------------------

def run_validation(row: dict, existing_approved_rows: list[dict] | None = None) -> dict:
    """
    Returns a report dict:
    {
        "status": "approved_candidate" | "flagged" | "rejected",
        "hard_failures": [...],   # block approval outright
        "soft_flags": [...],      # needs human judgment call
    }
    """
    existing_approved_rows = existing_approved_rows or []
    hard_failures = []
    soft_flags = []

    ok, msg = validate_required_fields(row)
    if not ok:
        hard_failures.append(msg)

    ok, msg = validate_destination(row.get("quick_facts_destination", ""))
    if not ok:
        hard_failures.append(msg)

    ok, msg = validate_price(row.get("quick_facts_cost", ""))
    if not ok:
        hard_failures.append(msg)

    full_text_blob = " ".join(str(v) for v in row.values())
    ok, msg = validate_no_duplicated_words(full_text_blob)
    if not ok:
        soft_flags.append(msg)  # grammar issue — annoying but not catastrophic

    ok, msg = validate_title_matches_product(
        row.get("package_name", ""), row.get("title_tag", "")
    )
    if not ok:
        soft_flags.append(msg)

    # duplicate-content check against previously approved rows
    existing_why_choose = [r.get("why_choose_bullets", "") for r in existing_approved_rows]
    if existing_why_choose:
        ok, msg = check_duplicate_content(row.get("why_choose_bullets", ""), existing_why_choose)
        if not ok:
            soft_flags.append(msg)

    if hard_failures:
        status = "rejected"
    elif soft_flags:
        status = "flagged"
    else:
        status = "approved_candidate"  # still needs a human click, per review-gate policy

    # Compute 100% deterministic code-based score
    base_score = 100
    base_score -= len(hard_failures) * 35
    base_score -= len(soft_flags) * 8
    objective_score = max(15, min(100, base_score))

    return {
        "status": status,
        "hard_failures": hard_failures,
        "soft_flags": soft_flags,
        "objective_score": objective_score,
    }


def compute_objective_qa_score(val_report: dict, all_flags: list, factual_score: int = 100, linter_metrics: dict = None) -> int:
    """
    100% deterministic, code-based QA scoring.
    Replaces artificial LLM self-grading with objective rule deductions:
    - Hard failures (bad destination, broken price, missing fields): -35 pts each
    - Soft flags (repeated words, banned phrases, AI-isms, long sentences): -5 to -10 pts each
    - Factual discrepancy: -15 pts
    - Linter / formatting issues: -5 to -10 pts
    """
    score = 100
    hard_fails = val_report.get("hard_failures", [])
    soft_flags = val_report.get("soft_flags", [])

    # 1. Hard Failures (each drops 35 pts immediately)
    score -= len(hard_fails) * 35

    # 2. Soft Flags (each drops 8 pts)
    score -= len(soft_flags) * 8

    # 3. Critical Flags (banned phrases, AI-isms)
    banned_count = sum(1 for f in all_flags if f.startswith("BANNED_PHRASES"))
    score -= banned_count * 10

    ai_ism_count = sum(1 for f in all_flags if f.startswith("AI_ISMS_FOUND"))
    score -= ai_ism_count * 5

    # 4. Factual Integrity
    if factual_score < 80:
        score -= int((80 - factual_score) * 0.5)

    # 5. Linter Score
    if linter_metrics:
        lint_score = linter_metrics.get("overall_score", 100)
        if lint_score < 90:
            score -= int((90 - lint_score) * 0.4)

    return max(15, min(100, score))



# ---------------------------------------------------------------------
# EXAMPLE USAGE
# ---------------------------------------------------------------------
if __name__ == "__main__":
    example_row = {
        "package_name": "Begin Your Wellness Journey With Us",
        "primary_keyword": "Begin Your Wellness",
        "title_tag": "Begin Your Wellness Journey With Us | YatraDham.Org",
        "meta_description": "Discover verified accommodation...",
        "quick_facts_destination": "Wellness.Yatradham.Org",
        "quick_facts_cost": "Starting From ₹ 24",
        "itinerary": "[...]",
        "pricing_table": "[...]",
        "inclusions": "[...]",
        "exclusions": "[...]",
        "faq": "[...]",
        "why_choose_bullets": "Guided Guided morning nature walk...",
    }

    report = run_validation(example_row)
    print(report)
    # Expected: status="rejected", with destination + price hard failures
