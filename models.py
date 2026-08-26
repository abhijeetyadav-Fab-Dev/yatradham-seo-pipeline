"""Pydantic models for the SEO pipeline."""
from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class PackageInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    url: Optional[str] = Field(None, description="The source URL of the package")
    name: str = Field(..., min_length=2, description="The name of the package")
    duration: Optional[str] = Field(None, description="The duration of the trip (e.g. 5 Days)")
    destination: Optional[str] = Field(None, description="Primary location")
    category: Optional[str] = Field("auto", description="Category: wellness, tour, stay, puja, or auto")
    center_name: Optional[str] = Field(None, description="Ashram / Center / Hotel name")
    cost: Optional[str] = Field(None, description="Cost per person or per night")
    raw_html: Optional[str] = Field(None, description="Raw HTML for storage")
    raw_text: Optional[str] = Field(None, description="Cleaned raw text for the LLM context")

    @field_validator("name", "destination", "center_name", "cost", "raw_text", mode="before")
    @classmethod
    def sanitize_xss_and_prompt_injection(cls, v: Any) -> Any:
        if isinstance(v, str):
            from security_firewall import sanitize_xss, sanitize_user_prompt
            v = sanitize_xss(v)
            try:
                v = sanitize_user_prompt(v, max_chars=10000)
            except Exception as e:
                raise ValueError(f"Input validation error: {str(e)}")
        return v





class QuickFacts(BaseModel):
    package_name: str = ""
    cost: str = ""
    duration: str = ""
    destination: str = ""
    level: str = ""
    accommodation: str = ""
    food: str = ""
    activities: str = ""
    center_name: str = ""
    yoga_sessions: str = ""



class ProgramSession(BaseModel):
    time: str = ""
    activity: str = ""


class ProgramHighlights(BaseModel):
    heading: str = ""
    morning: List[ProgramSession] = Field(default_factory=list)
    daytime: List[ProgramSession] = Field(default_factory=list)
    evening: List[ProgramSession] = Field(default_factory=list)


class ItineraryDay(BaseModel):
    day_number: int = 1
    sessions: List[ProgramSession] = Field(default_factory=list)


class PricingRow(BaseModel):
    guests: str = ""
    cost_per_person: str = ""


class NearbyLocation(BaseModel):
    name: str = ""
    distance: str = ""
    type: str = ""  # airport, railway, bus, sightseeing


class FAQItem(BaseModel):
    question: str = ""
    answer: str = ""


class SectionedContent(BaseModel):
    package_overview: str = ""
    geo_quick_answer: str = ""  # GEO Answer-First Quick Summary for AI Overviews / Search
    quick_facts: QuickFacts = Field(default_factory=QuickFacts)
    why_choose_heading: str = ""
    why_choose_intro: str = ""
    why_choose_bullets: List[str] = Field(default_factory=list)
    who_can_benefit_heading: str = ""
    who_can_benefit_intro: str = ""
    who_can_benefit_bullets: List[str] = Field(default_factory=list)
    program_highlights: ProgramHighlights = Field(default_factory=ProgramHighlights)
    meal_section_heading: str = ""
    meal_section_bullets: List[str] = Field(default_factory=list)
    accommodation_heading: str = ""
    accommodation_bullets: List[str] = Field(default_factory=list)
    benefits_heading: str = ""
    benefits_items: List[str] = Field(default_factory=list)
    how_to_book_heading: str = ""
    how_to_book_steps: List[str] = Field(default_factory=list)
    prices_photos_reviews: str = ""
    itinerary: List[ItineraryDay] = Field(default_factory=list)
    pricing_table: List[PricingRow] = Field(default_factory=list)
    inclusions: List[str] = Field(default_factory=list)
    exclusions: List[str] = Field(default_factory=list)
    nearby_locations_heading: str = ""
    nearby_locations: List[NearbyLocation] = Field(default_factory=list)
    smart_internal_links: List[Dict[str, Any]] = Field(default_factory=list)
    cancellation_policy: str = ""
    payment_policy_bullets: List[str] = Field(default_factory=list)
    terms_conditions: List[str] = Field(default_factory=list)
    faq: List[FAQItem] = Field(default_factory=list)


class SEOOutput(BaseModel):
    id: Optional[int] = None
    package_input: PackageInput
    primary_keyword: str = ""
    title_tag: str = Field("", max_length=65)
    meta_description: str = Field("", max_length=160)
    sections: SectionedContent = Field(default_factory=SectionedContent)
    qa_score: int = Field(0, ge=0, le=100)
    qa_flags: List[str] = Field(default_factory=list)
    factual_integrity_score: int = Field(100, ge=0, le=100)
    ground_truth_report: Optional[Dict[str, Any]] = None
    json_ld_schema: Optional[Dict[str, Any]] = None
    linter_metrics: Optional[Dict[str, Any]] = None
    language: str = "en"  # en, hi, gu
    status: str = "pending"  # pending, approved, flagged_review, rejected
    created_at: str = ""
    updated_at: str = ""



    @field_validator("title_tag", mode="before")
    @classmethod
    def sanitize_title_tag(cls, v: Any) -> str:
        s = str(v or "").strip()
        if len(s) > 65:
            s = s[:62].rsplit(" ", 1)[0] + "..." if " " in s[:62] else s[:65]
        return s

    @field_validator("meta_description", mode="before")
    @classmethod
    def sanitize_meta_description(cls, v: Any) -> str:
        s = str(v or "").strip()
        if len(s) > 160:
            s = s[:157].rsplit(" ", 1)[0] + "..." if " " in s[:157] else s[:160]
        return s


class BatchRequest(BaseModel):
    urls: List[str]


class BulkActionRequest(BaseModel):
    ids: List[int]
    action: str  # approve, reject
