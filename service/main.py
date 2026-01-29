"""
Marketing Agency API Service

HTTP service that exposes marketing skills via REST API.
Designed for deployment on Google Cloud Run.
"""

import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Security, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from service.api.schemas import (
    AssetRequest,
    ErrorResponse,
    HealthResponse,
    SkillName,
    WorkRequest,
    WorkResult,
    BriefCreate,
    BriefResponse,
    BriefList,
    LeadCreate,
    LeadResponse,
    UserProfile
)
from service.core.executor import get_executor, SkillExecutor
from service.core.storage import get_storage
from service.core.db import get_db
from service.core.queue import get_queue
from service.core.assets import get_asset_manager
from service.core.auth import get_current_user
from service.core.limiter import get_limiter
from service.core.models import ImageModels, VideoModels, AudioModels


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

# Include swarm router for sprite management
try:
    from service.api.swarm import router as swarm_router
    app.include_router(swarm_router)
    print("Swarm API enabled")
except ImportError as e:
    print(f"Swarm API not available: {e}")


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
        "video": {
            "remotion-script": "Dynamic video scripts",
            "remotion-layout": "Video component design",
            "manim-composer": "Mathematical animations",
            "manim-best-practices": "Manim optimization",
        }
    }
    return {"skills": skills, "total": len(SkillName)}


from starlette.concurrency import run_in_threadpool

@app.get("/assets")
async def list_assets(prefix: Optional[str] = None):
    """List assets in Cloud Storage."""
    storage = get_storage()
    return {"assets": storage.list_assets(prefix=prefix)}


@app.get("/user/profile", response_model=Optional[UserProfile])
async def get_user_profile(
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """Get the current user's profile."""
    user_id, _ = user_info
    db = get_db()
    profile = db.get_user_profile(user_id)
    if not profile:
        return None
    return profile


@app.post("/user/profile", response_model=UserProfile)
async def save_user_profile(
    profile: UserProfile,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """Save or update the current user's profile."""
    user_id, _ = user_info
    db = get_db()
    
    data = profile.model_dump(exclude_unset=True)
    db.save_user_profile(user_id, data)
    
    updated = db.get_user_profile(user_id)
    return updated


@app.post("/briefs", response_model=BriefResponse)
async def save_brief(
    brief: BriefCreate,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """Save or update a strategic brief."""
    user_id, _ = user_info
    db = get_db()
    
    # Check ownership if updating
    if brief.id:
        existing = db.get_brief(brief.id)
        if existing and existing.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this brief")
    
    # Convert Pydantic model to dict
    data = brief.model_dump()
    data["user_id"] = user_id # Attach owner
    
    doc_id = db.save_brief(data)
    
    # Fetch the full object back to get timestamps
    saved_data = db.get_brief(doc_id)
    if not saved_data:
        raise HTTPException(status_code=500, detail="Failed to save brief")
        
    return saved_data


@app.get("/briefs", response_model=BriefList)
async def list_briefs(
    limit: int = 20,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """List recent strategic briefs for the current user."""
    user_id, _ = user_info
    db = get_db()
    
    # We need to update db.py to support filtering by user_id
    # For now, let's assume list_briefs can take a user_id filter
    # If not, we'll filter in memory (inefficient but works for Phase 2 prototype)
    
    all_briefs = db.list_briefs(limit=100) # Fetch more, filter here
    user_briefs = [b for b in all_briefs if b.get("user_id") == user_id]
    
    return {"briefs": user_briefs[:limit], "total": len(user_briefs)}


@app.get("/briefs/{brief_id}", response_model=BriefResponse)
async def get_brief(
    brief_id: str,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """Get a specific brief by ID."""
    user_id, _ = user_info
    db = get_db()
    brief = db.get_brief(brief_id)
    
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
        
    if brief.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this brief")
        
    return brief


@app.post("/leads", response_model=LeadResponse)
async def create_lead(lead: LeadCreate):
    """Capture a new lead."""
    db = get_db()
    data = lead.model_dump()
    doc_id = db.save_lead(data)
    
    return {**data, "id": doc_id, "created_at": None} # Timestamp handled by DB, just return dummy or fetch


@app.post("/generate-asset")
async def generate_asset(request: AssetRequest):
    """Generate an AI asset via FAL and store in GCS."""
    manager = get_asset_manager()
    
    if request.type == "image":
        if not request.model:
            # Smart default based on prompt content
            text_keywords = ["text", "sign", "label", "headline", "words", "typography", "logo"]
            if any(k in request.prompt.lower() for k in text_keywords):
                model = ImageModels.QWEN_IMAGE_2512  # Better for text
            else:
                model = ImageModels.FLUX_PRO_1_1  # Best for general photorealism
        else:
            model = request.model
        
        result = await manager.generate_image(request.prompt, model=model)
    elif request.type == "video":
        result = await manager.generate_video(request.prompt, model=request.model or VideoModels.KLING_V1_STANDARD)
    elif request.type == "audio":
        result = await manager.generate_audio(request.prompt, model=request.model or AudioModels.STABLE_AUDIO)
    else:
        raise HTTPException(status_code=400, detail="Invalid asset type. Use 'image', 'video', or 'audio'.")
    
    return result


from service.core.browser import capture_screenshot

@app.post("/analyze-url", response_model=WorkResult)
async def analyze_url(
    url: str,
    task: Optional[str] = "Audit this page for conversion optimization opportunities.",
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """
    Capture a screenshot of a URL and analyze it using AI vision.
    """
    user_id, _ = user_info
    
    # 1. Capture Screenshot
    try:
        image_base64 = await capture_screenshot(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to capture screenshot: {str(e)}")
    
    # 2. Execute Work
    request = WorkRequest(
        skill=SkillName.PAGE_CRO, # Reuse CRO skill logic
        task=task,
        image_data=image_base64,
        context={"url": url}
    )
    
    return await execute_work(request, user_info)


@app.post("/work", response_model=WorkResult)
async def execute_work(
    request: WorkRequest,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """
    Execute a marketing skill synchronously.
    """
    user_id, is_anon = user_info
    
    # Rate Limit Check
    limiter = get_limiter()
    if not limiter.check_limit(user_id, is_anon):
        limit = limiter.daily_limit_anon if is_anon else limiter.daily_limit_user
        raise HTTPException(
            status_code=429, 
            detail=f"Daily limit exceeded ({limit} requests/day). {'Sign in for more.' if is_anon else 'Upgrade plan for more.'}"
        )

    try:
        executor = get_executor()
        result = executor.execute(request)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.post("/work/async")
async def execute_work_async(
    request: WorkRequest,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """
    Queue a marketing skill for background execution.
    Returns a Job ID that can be tracked via GET /briefs/{id}.
    """
    user_id, is_anon = user_info
    
    # Rate Limit Check
    limiter = get_limiter()
    if not limiter.check_limit(user_id, is_anon):
        limit = limiter.daily_limit_anon if is_anon else limiter.daily_limit_user
        raise HTTPException(
            status_code=429, 
            detail=f"Daily limit exceeded ({limit} requests/day). {'Sign in for more.' if is_anon else 'Upgrade plan for more.'}"
        )

    try:
        db = get_db()
        queue = get_queue()
        
        # Create initial Job/Brief record
        brief_data = {
            "title": f"Async {request.skill.value.title()}",
            "product": request.context.get("product", "Unknown") if request.context else "Unknown",
            "audience": request.context.get("audience", "Unknown") if request.context else "Unknown",
            "value": "N/A", # Placeholder
            "description": request.task,
            "status": "pending",
            "type": "async_job",
            "user_id": user_id # Track ownership
        }
        job_id = db.save_brief(brief_data)
        
        # Publish to queue
        queue.publish_task(request, job_id)
        
        return {"job_id": job_id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to queue job: {str(e)}")


@app.post("/copywriting", response_model=WorkResult)
async def copywriting(
    task: str, 
    context: dict = None, 
    content: str = None,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
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
    return await execute_work(request, user_info)


@app.post("/page-cro", response_model=WorkResult)
async def page_cro(
    task: str, 
    content: str, 
    context: dict = None,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
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
    return await execute_work(request, user_info)


@app.post("/email-sequence", response_model=WorkResult)
async def email_sequence(
    task: str, 
    context: dict = None,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """
    Shortcut endpoint for email-sequence skill.

    Design complete email sequences with strategic frameworks.
    """
    request = WorkRequest(
        skill=SkillName.EMAIL_SEQUENCE,
        task=task,
        context=context,
    )
    return await execute_work(request, user_info)


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
