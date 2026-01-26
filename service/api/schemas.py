"""
Request and response schemas for the Marketing Agency API.
"""

from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class SkillName(str, Enum):
    """Available marketing skills."""
    # Writing
    COPYWRITING = "copywriting"
    COPY_EDITING = "copy-editing"
    EMAIL_SEQUENCE = "email-sequence"
    SOCIAL_CONTENT = "social-content"

    # CRO
    PAGE_CRO = "page-cro"
    FORM_CRO = "form-cro"
    SIGNUP_FLOW_CRO = "signup-flow-cro"
    ONBOARDING_CRO = "onboarding-cro"
    POPUP_CRO = "popup-cro"
    PAYWALL_UPGRADE_CRO = "paywall-upgrade-cro"

    # SEO
    SEO_AUDIT = "seo-audit"
    PROGRAMMATIC_SEO = "programmatic-seo"
    SCHEMA_MARKUP = "schema-markup"

    # Strategy
    MARKETING_IDEAS = "marketing-ideas"
    MARKETING_PSYCHOLOGY = "marketing-psychology"
    PRICING_STRATEGY = "pricing-strategy"
    LAUNCH_STRATEGY = "launch-strategy"
    COMPETITOR_ALTERNATIVES = "competitor-alternatives"
    REFERRAL_PROGRAM = "referral-program"
    FREE_TOOL_STRATEGY = "free-tool-strategy"

    # Measurement
    AB_TEST_SETUP = "ab-test-setup"
    ANALYTICS_TRACKING = "analytics-tracking"
    PAID_ADS = "paid-ads"

    # Remotion
    REMOTION_SCRIPT = "remotion-script"
    REMOTION_LAYOUT = "remotion-layout"

    # Manim
    MANIM_COMPOSER = "manim-composer"
    MANIM_BEST_PRACTICES = "manim-best-practices"


class WorkRequest(BaseModel):
    """Request to execute a marketing skill."""

    skill: SkillName = Field(
        ...,
        description="The marketing skill to use"
    )

    task: str = Field(
        ...,
        description="What you want the skill to do",
        min_length=10,
        examples=[
            "Write a landing page headline for a project management tool targeting engineering managers",
            "Audit this landing page for conversion issues: [page content]",
            "Create a 5-email onboarding sequence for a SaaS product"
        ]
    )

    model: Optional[str] = Field(
        default=None,
        description="Optional model to use (e.g. MiniMax-M2.1-lightning)"
    )

    context: Optional[dict] = Field(
        default=None,
        description="Additional context for the skill",
        examples=[{
            "product": "TaskFlow - AI project management",
            "audience": "Engineering managers at mid-size tech companies",
            "tone": "Professional but approachable",
            "constraints": ["No emojis", "Keep it under 10 words"]
        }]
    )

    content: Optional[str] = Field(
        default=None,
        description="Content to analyze or improve (for CRO audits, copy editing, etc.)",
        examples=["<html>Your landing page HTML here</html>"]
    )


class WorkResult(BaseModel):
    """Result from executing a marketing skill."""

    skill: SkillName = Field(
        description="The skill that was executed"
    )

    output: str = Field(
        description="The generated output from the skill"
    )

    sections: Optional[dict] = Field(
        default=None,
        description="Structured sections if the output has multiple parts"
    )

    alternatives: Optional[list[str]] = Field(
        default=None,
        description="Alternative options if generated (headlines, CTAs, etc.)"
    )

    recommendations: Optional[list[str]] = Field(
        default=None,
        description="Actionable recommendations if applicable"
    )

    metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata about the execution"
    )


class WorkflowName(str, Enum):
    """Available pre-built workflows."""
    FULL_SERVICE = "full-service"
    QUICK_COPY = "quick-copy"
    CRO_AUDIT = "cro-audit"
    SEO_CAMPAIGN = "seo-campaign"


class WorkflowRequest(BaseModel):
    """Request to execute a multi-skill workflow."""

    workflow: WorkflowName = Field(
        ...,
        description="The workflow to execute"
    )

    brief: str = Field(
        ...,
        description="Project brief describing what you need",
        min_length=50
    )

    context: Optional[dict] = Field(
        default=None,
        description="Additional context for the workflow"
    )


class WorkflowResult(BaseModel):
    """Result from executing a workflow."""

    workflow: WorkflowName
    phases: list[dict] = Field(
        description="Results from each phase of the workflow"
    )
    deliverables: dict = Field(
        description="Final deliverables organized by type"
    )


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    skills_available: int


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    skill: Optional[str] = None

class AssetRequest(BaseModel):
    """Request to generate an AI asset."""
    type: str = Field(..., description="'image', 'video', or 'audio'")
    prompt: str = Field(..., description="The prompt for generation")
    model: Optional[str] = Field(None, description="Specific model to use")

class AssetEvaluation(BaseModel):
    """Evaluation of a generated asset."""
    status: str = Field(..., description="'approved' or 'rejected'")
    critique: str = Field(..., description="Detailed feedback on why it was approved or rejected")
    refined_prompt: Optional[str] = Field(None, description="Improved prompt if rejected")

class BriefCreate(BaseModel):
    """Request to create or update a brief."""
    id: Optional[str] = Field(None, description="Optional ID to update existing brief")
    title: str = Field(..., description="Project title")
    product: str = Field(..., description="Product or service name")
    audience: str = Field(..., description="Target audience")
    value: str = Field(..., description="Core value proposition")
    context: Optional[dict] = Field(default={}, description="Additional key-value context")
    description: Optional[str] = Field(None, description="Long form description")

class BriefResponse(BriefCreate):
    """Full brief object."""
    id: str
    created_at: Any = Field(None, description="Creation timestamp")
    updated_at: Any = Field(None, description="Last update timestamp")

class BriefList(BaseModel):
    """List of briefs."""
    briefs: list[BriefResponse]
    total: int

class LeadCreate(BaseModel):
    """Request to capture a new lead."""
    email: str = Field(..., description="Lead email address")
    role: Optional[str] = Field(None, description="User role or job title")
    company: Optional[str] = Field(None, description="Company name")
    source: Optional[str] = Field(None, description="Source campaign or slug")
    intent: Optional[str] = Field(None, description="User intent or project type")

class LeadResponse(LeadCreate):
    """Lead capture response."""
    id: str
    created_at: Any
