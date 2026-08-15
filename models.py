"""Pydantic models for the SEO pipeline."""
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class PackageInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    url: Optional[str] = Field(None, description="The source URL of the package")
    name: str = Field(..., min_length=2, description="The name of the package")
    duration: Optional[str] = Field(None, description="The duration of the trip (e.g. 5 Days)")
    destination: Optional[str] = Field(None, description="Primary location")
    raw_html: Optional[str] = Field(None, description="Raw HTML for storage")
    raw_text: Optional[str] = Field(None, description="Cleaned raw text for the LLM context")


class QuickFacts(BaseModel):
    package_name: str = ""
    cost: str = ""
    duration: str = ""
    destination: str = ""
    level: str = ""
    accommodation: str = ""
    food: str = ""
    activities: str = ""


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
    status: str = "pending"  # pending, approved, rejected
    created_at: str = ""
    updated_at: str = ""


class BatchRequest(BaseModel):
    urls: List[str]


class BulkActionRequest(BaseModel):
    ids: List[int]
    action: str  # approve, reject
