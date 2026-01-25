"""
Marketing Agency API Service

HTTP service that exposes marketing skills via REST API.
Designed for deployment on Google Cloud Run.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Security, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from service.api.schemas import (
    ErrorResponse,
    HealthResponse,
    SkillName,
    WorkRequest,
    WorkResult,
)
from service.core.executor import get_executor, SkillExecutor


VERSION = "1.0.0"

# Security
api_key_header = HTTPBearer(auto_error=False)

async def verify_api_secret(token: HTTPAuthorizationCredentials = Security(api_key_header)):
    """Verify the API secret if configured."""
    secret = os.getenv("API_SECRET")
    if not secret:
        return
    
    if not token or token.credentials != secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API secret"
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: warm up the executor and validate skills
    executor = get_executor()
    print(f"Marketing Agency API v{VERSION} starting...")
    print(f"Skills path: {executor.skills_path}")
    print(f"Default Model: {executor.default_model}")

    # Validate all skills are loadable
    for skill in SkillName:
        try:
            executor.load_skill(skill)
        except FileNotFoundError:
            print(f"Warning: Skill not found: {skill.value}")

    print(f"Loaded {len(executor._skill_cache)} skills")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="Marketing Agency API",
    description="""
Execute marketing skills via HTTP API.

## Overview

This API provides access to 23 specialized marketing skills, each containing
proven frameworks for specific marketing tasks.

## Skills vs Prompts

Unlike raw LLM prompting, each skill contains:
- Context-gathering frameworks
- Proven structures and formulas
- Psychological principles
- Quality checklists
- Strategic rationale

The skill guides the thinking, not just the output.

## Available Skills

**Writing**: copywriting, copy-editing, email-sequence, social-content

**CRO**: page-cro, form-cro, signup-flow-cro, onboarding-cro, popup-cro, paywall-upgrade-cro

**SEO**: seo-audit, programmatic-seo, schema-markup

**Strategy**: marketing-ideas, marketing-psychology, pricing-strategy, launch-strategy,
competitor-alternatives, referral-program, free-tool-strategy

**Measurement**: ab-test-setup, analytics-tracking, paid-ads
    """,
    version=VERSION,
    lifespan=lifespan,
    dependencies=[Depends(verify_api_secret)],
)

# CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    executor = get_executor()
    return HealthResponse(
        status="healthy",
        version=VERSION,
        skills_available=len(SkillName),
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint (alias)."""
    return await health_check()


@app.get("/skills")
async def list_skills():
    """List all available skills with descriptions."""
    skills = {
        "writing": {
            "copywriting": "Conversion-focused copy with strategic frameworks",
            "copy-editing": "Three-pass editing: clarity, concision, power",
            "email-sequence": "Complete email sequences: welcome, nurture, sales",
            "social-content": "Platform-native content that converts",
        },
        "cro": {
            "page-cro": "Landing page audits with prioritized recommendations",
            "form-cro": "Form field optimization and friction reduction",
            "signup-flow-cro": "Registration flow optimization",
            "onboarding-cro": "User activation and aha-moment optimization",
            "popup-cro": "Exit intent, timing, and trigger optimization",
            "paywall-upgrade-cro": "Free-to-paid conversion paths",
        },
        "seo": {
            "seo-audit": "Technical + content + competitive SEO analysis",
            "programmatic-seo": "Template-based pages at scale",
            "schema-markup": "JSON-LD structured data implementation",
        },
        "strategy": {
            "marketing-ideas": "Structured brainstorming with prioritization",
            "marketing-psychology": "Cialdini, cognitive biases, applied persuasion",
            "pricing-strategy": "Models, anchoring, packaging",
            "launch-strategy": "Product Hunt, soft launches, hard launches",
            "competitor-alternatives": "Positioning that creates space",
            "referral-program": "Viral loops that actually loop",
            "free-tool-strategy": "Lead-gen tools worth building",
        },
        "measurement": {
            "ab-test-setup": "Statistical validity and test design",
            "analytics-tracking": "Events, funnels, attribution",
            "paid-ads": "Google, Meta, LinkedIn structure and optimization",
        },
    }
    return {"skills": skills, "total": len(SkillName)}


@app.post("/work", response_model=WorkResult)
async def execute_work(request: WorkRequest):
    """
    Execute a marketing skill.

    Send a task to be processed using a specific marketing skill framework.
    The skill's methodology, structures, and quality checks will be applied.
    """
    try:
        executor = get_executor()
        result = executor.execute(request)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.post("/copywriting", response_model=WorkResult)
async def copywriting(task: str, context: dict = None, content: str = None):
    """
    Shortcut endpoint for copywriting skill.

    Generate conversion-focused copy using strategic frameworks.
    """
    request = WorkRequest(
        skill=SkillName.COPYWRITING,
        task=task,
        context=context,
        content=content,
    )
    return await execute_work(request)


@app.post("/page-cro", response_model=WorkResult)
async def page_cro(task: str, content: str, context: dict = None):
    """
    Shortcut endpoint for page-cro skill.

    Audit a landing page for conversion optimization opportunities.
    """
    request = WorkRequest(
        skill=SkillName.PAGE_CRO,
        task=task,
        content=content,
        context=context,
    )
    return await execute_work(request)


@app.post("/email-sequence", response_model=WorkResult)
async def email_sequence(task: str, context: dict = None):
    """
    Shortcut endpoint for email-sequence skill.

    Design complete email sequences with strategic frameworks.
    """
    request = WorkRequest(
        skill=SkillName.EMAIL_SEQUENCE,
        task=task,
        context=context,
    )
    return await execute_work(request)


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if os.getenv("DEBUG") else None,
        ).model_dump(),
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        "service.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("DEBUG", "").lower() == "true",
    )
