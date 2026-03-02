"""
Marketing Agency API Service

HTTP service that exposes marketing skills via REST API.
Designed for deployment on Google Cloud Run.
"""

import logging
import os
import signal
import sys
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Security, Depends, Request, status

logger = logging.getLogger(__name__)
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
from service.billing.stripe_client import get_stripe_client, PLANS
from service.billing.enforcement import get_enforcement, PLAN_LIMITS


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


def _validate_env():
    """Validate critical environment variables at startup. Fail fast, not on first request."""
    required = {
        "ANTHROPIC_API_KEY": "Required for LLM skill execution",
    }
    warned = {
        "GCP_PROJECT_ID": "Needed for Firestore/GCS in Cloud Run (ok if using service.json locally)",
        "CORS_ORIGINS": "Defaults to '*' which is insecure in production",
    }
    missing = []
    for var, desc in required.items():
        if not os.getenv(var):
            missing.append(f"  {var} — {desc}")
    if missing:
        logger.error("Missing required environment variables:\n%s", "\n".join(missing))
        sys.exit(1)
    for var, desc in warned.items():
        if not os.getenv(var):
            logger.warning("Environment variable %s not set: %s", var, desc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Validate environment before anything else
    _validate_env()

    # Startup: warm up the executor and validate skills
    executor = get_executor()
    logger.info("Marketing Agency API v%s starting...", VERSION)
    logger.info("Skills path: %s", executor.skills_path)
    logger.info("Default Model: %s", executor.default_model)

    # Validate all skills are loadable
    for skill in SkillName:
        try:
            executor.load_skill(skill)
        except FileNotFoundError:
            logger.warning("Skill not found: %s", skill.value)

    logger.info("Loaded %d skills", len(executor._skill_cache))

    # Validate Firestore connectivity
    try:
        db = get_db()
        if db.check_connectivity():
            logger.info("Firestore connectivity: OK")
        else:
            logger.warning("Firestore connectivity: FAILED — database queries will error")
    except Exception as e:
        logger.warning("Firestore init failed: %s", e)

    yield

    # Graceful shutdown — Cloud Run sends SIGTERM with 10s grace period
    logger.info("Shutting down gracefully...")


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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request with its status code and duration."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Get identity if possible
    auth_header = request.headers.get("Authorization")
    anon_id = request.cookies.get("ajs_anonymous_id") or request.headers.get("X-Anonymous-ID")
    identity = "authenticated" if auth_header else (f"anon:{anon_id}" if anon_id else "guest")
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.3f}s Identity: {identity}"
    )
    return response

# Include swarm router for sprite management
try:
    from service.api.swarm import router as swarm_router
    app.include_router(swarm_router)
    print("Swarm API enabled")
except ImportError as e:
    print(f"Swarm API not available: {e}")


@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint — validates core dependencies."""
    executor = get_executor()
    checks = {"skills": len(executor._skill_cache) > 0}

    # Firestore check (cached singleton, cheap)
    try:
        db = get_db()
        checks["firestore"] = db.check_connectivity()
    except Exception:
        checks["firestore"] = False

    all_healthy = all(checks.values())
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
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


@app.post("/user/claim")
async def claim_work(
    request: Request,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """Claim work done anonymously using Cookie or X-Anonymous-ID header."""
    user_id, is_anon = user_info
    if is_anon:
        raise HTTPException(401, "Only signed-in users can claim work")

    anon_id = request.cookies.get("ajs_anonymous_id") or request.headers.get("X-Anonymous-ID")
    if not anon_id:
        logger.info(f"User {user_id} tried to claim work but no anonymous ID found in cookies or headers.")
        return {"status": "no_anon_id"}

    # Normalize anon_id (strip quotes from cookie)
    anon_id = str(anon_id).strip('"')
    
    db = get_db()
    logger.info(f"Claiming work: Transferring from anon_{anon_id} to {user_id}")
    db.claim_anonymous_work(f"anon_{anon_id}", user_id)
    return {"status": "claimed", "user_id": user_id}


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
    user_id, is_anon = user_info
    db = get_db()
    
    # Check ownership if updating
    if brief.id:
        existing = db.get_brief(brief.id)
        if existing:
            if is_anon and existing.get("anonymous_id") != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to edit this brief")
            elif not is_anon and existing.get("user_id") != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to edit this brief")
    
    # Convert Pydantic model to dict
    data = brief.model_dump()
    if is_anon:
        data["anonymous_id"] = user_id # Track by anonymous ID
    else:
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
    user_id, is_anon = user_info
    db = get_db()
    
    # We fetch briefs for the specific identity
    all_briefs = db.list_briefs(limit=100)
    if is_anon:
        user_briefs = [b for b in all_briefs if b.get("anonymous_id") == user_id]
    else:
        user_briefs = [b for b in all_briefs if b.get("user_id") == user_id]
    
    return {"briefs": user_briefs[:limit], "total": len(user_briefs)}


@app.get("/briefs/{brief_id}", response_model=BriefResponse)
async def get_brief(
    brief_id: str,
    user_info: tuple[str, bool] = Depends(get_current_user)
):
    """Get a specific brief by ID."""
    user_id, is_anon = user_info
    db = get_db()
    brief = db.get_brief(brief_id)
    
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
        
    # Check ownership (either anonymous_id or user_id)
    if is_anon:
        if brief.get("anonymous_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this brief")
    else:
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
    is_allowed, count = limiter.check_limit(user_id, is_anon)
    
    if not is_allowed:
        # Trigger the "extraordinary feedback loop"
        # Instead of a 429 error, we return a structured Paywall object
        return WorkResult(
            paywall=Paywall(
                message="You've experienced the speed of the swarm. To unlock your next campaign, choose a plan.",
                upgrade_url="https://agency.studio/pricing",
                plan_options={
                    "Starter": "$49/mo - 1M tokens, 3 Agents",
                    "Growth": "$199/mo - 10M tokens, All Agents",
                    "Enterprise": "Custom - Unlimited Scale"
                },
                runs_remaining=0
            )
        )

    # Billing enforcement for paid users
    if not is_anon:
        try:
            db = get_db()
            tenant = db.get_tenant_by_user(user_id)
            if tenant and tenant.get("plan", "free") != "free":
                enforcement = get_enforcement()
                status = await enforcement.check_billing_status(tenant["id"])
                if status not in ("active", "past_due"):
                    raise HTTPException(402, f"Billing status: {status}. Please update your payment method.")
                await enforcement.check_can_spawn_sprite(tenant["id"], request.skill.value)
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"Billing enforcement check failed (allowing): {e}")

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
    is_allowed, count = limiter.check_limit(user_id, is_anon)
    
    if not is_allowed:
        raise HTTPException(
            status_code=402,
            detail="Limit reached. To unlock your next campaign, choose a plan: https://agency.studio/pricing"
        )

    # Billing enforcement for paid users
    if not is_anon:
        try:
            db_check = get_db()
            tenant = db_check.get_tenant_by_user(user_id)
            if tenant and tenant.get("plan", "free") != "free":
                enforcement = get_enforcement()
                status = await enforcement.check_billing_status(tenant["id"])
                if status not in ("active", "past_due"):
                    raise HTTPException(402, f"Billing status: {status}. Please update your payment method.")
                await enforcement.check_can_spawn_sprite(tenant["id"], request.skill.value)
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"Billing enforcement check failed (allowing): {e}")

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
        }
        if is_anon:
            brief_data["anonymous_id"] = user_id
        else:
            brief_data["user_id"] = user_id # Track ownership
        
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


# =============================================================================
# Billing & Checkout Endpoints
# =============================================================================

from pydantic import BaseModel

class CheckoutRequest(BaseModel):
    plan: str

@app.post("/checkout")
async def create_checkout(
    req: CheckoutRequest,
    user_info: tuple[str, bool] = Depends(get_current_user),
    request: Request = None,
):
    """Create a Stripe Checkout Session for a plan."""
    user_id, is_anon = user_info
    if is_anon:
        raise HTTPException(401, "Sign in to subscribe to a plan")

    if req.plan not in PLANS:
        raise HTTPException(400, f"Invalid plan: {req.plan}. Choose from: {list(PLANS.keys())}")

    db = get_db()
    tenant = db.get_or_create_tenant(user_id)
    stripe_client = get_stripe_client()

    # Get or create Stripe customer
    customer_id = tenant.get("billing", {}).get("stripe_customer_id")
    if not customer_id:
        customer = stripe_client.create_customer(
            tenant_id=tenant["id"],
            email=tenant.get("email", ""),
            name=tenant.get("email", ""),
        )
        customer_id = customer.id
        db.update_tenant(tenant["id"], {"billing.stripe_customer_id": customer_id})

    plan_config = PLANS[req.plan]
    base_url = str(request.base_url).rstrip("/") if request else ""

    url = stripe_client.create_checkout_session(
        customer_id=customer_id,
        price_id=plan_config["stripe_price_id"],
        success_url=f"{base_url}/welcome?checkout=success",
        cancel_url=f"{base_url}/pricing",
        tenant_id=tenant["id"],
        plan=req.plan,
    )

    return {"url": url}


@app.post("/billing/portal")
async def billing_portal(
    user_info: tuple[str, bool] = Depends(get_current_user),
    request: Request = None,
):
    """Create a Stripe Customer Portal session."""
    user_id, is_anon = user_info
    if is_anon:
        raise HTTPException(401, "Sign in to manage billing")

    db = get_db()
    tenant = db.get_tenant_by_user(user_id)
    if not tenant:
        raise HTTPException(404, "No billing account found")

    customer_id = tenant.get("billing", {}).get("stripe_customer_id")
    if not customer_id:
        raise HTTPException(404, "No Stripe customer found. Subscribe to a plan first.")

    stripe_client = get_stripe_client()
    base_url = str(request.base_url).rstrip("/") if request else ""

    url = stripe_client.create_portal_session(
        customer_id=customer_id,
        return_url=f"{base_url}/account",
    )

    return {"url": url}


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    import stripe as _stripe

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        try:
            from google.cloud import secretmanager
            sm = secretmanager.SecretManagerServiceClient()
            project_id = os.getenv("GCP_PROJECT_ID")
            name = f"projects/{project_id}/secrets/stripe-webhook-secret/versions/latest"
            resp = sm.access_secret_version(request={"name": name})
            webhook_secret = resp.payload.data.decode("UTF-8")
        except Exception:
            logger.warning("Stripe webhook secret not available")

    try:
        event = _stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, _stripe.error.SignatureVerificationError) as e:
        logger.error(f"Webhook verification failed: {e}")
        raise HTTPException(400, "Invalid webhook payload or signature")

    event_type = event["type"]
    data = event["data"]["object"]
    db = get_db()

    logger.info(f"Stripe webhook: {event_type}")

    if event_type == "customer.subscription.created":
        tenant_id = data["metadata"].get("tenant_id")
        if tenant_id:
            plan = data["metadata"].get("plan", "starter")
            db.update_tenant(tenant_id, {
                "billing.status": "active",
                "billing.stripe_subscription_id": data["id"],
                "billing.stripe_customer_id": data["customer"],
                "billing.current_period_start": datetime.fromtimestamp(data["current_period_start"]),
                "billing.current_period_end": datetime.fromtimestamp(data["current_period_end"]),
                "plan": plan,
            })

    elif event_type == "customer.subscription.updated":
        tenant_id = data["metadata"].get("tenant_id")
        if tenant_id:
            updates = {
                "billing.status": "active" if data["status"] == "active" else data["status"],
                "billing.current_period_start": datetime.fromtimestamp(data["current_period_start"]),
                "billing.current_period_end": datetime.fromtimestamp(data["current_period_end"]),
            }
            plan = data["metadata"].get("plan")
            if plan:
                updates["plan"] = plan
            if data.get("cancel_at_period_end"):
                updates["billing.canceling"] = True
            db.update_tenant(tenant_id, updates)

    elif event_type == "customer.subscription.deleted":
        tenant_id = data["metadata"].get("tenant_id")
        if tenant_id:
            db.update_tenant(tenant_id, {
                "billing.status": "cancelled",
                "plan": "free",
            })

    elif event_type == "invoice.paid":
        customer_id = data["customer"]
        tenant = db.get_tenant_by_stripe_customer(customer_id)
        if tenant:
            db.update_tenant(tenant["id"], {"billing.status": "active"})

    elif event_type == "invoice.payment_failed":
        customer_id = data["customer"]
        tenant = db.get_tenant_by_stripe_customer(customer_id)
        if tenant:
            attempt_count = data.get("attempt_count", 1)
            new_status = "suspended" if attempt_count >= 3 else "past_due"
            db.update_tenant(tenant["id"], {"billing.status": new_status})

    return {"status": "ok"}


# =============================================================================
# Usage & Billing Status Endpoints
# =============================================================================

from datetime import datetime

@app.get("/usage")
async def get_usage(
    user_info: tuple[str, bool] = Depends(get_current_user),
):
    """Get current billing period usage summary."""
    user_id, is_anon = user_info
    if is_anon:
        raise HTTPException(401, "Sign in to view usage")

    db = get_db()
    tenant = db.get_tenant_by_user(user_id)
    if not tenant:
        return {
            "plan": "free",
            "tokens": {"used": 0, "limit": 50000, "percentage": 0},
            "sprites": {"spawned_this_period": 0, "period_limit": 5, "active": 0, "concurrent_limit": 1},
            "enabled_agents": ["director", "copywriter", "editor"],
        }

    plan = tenant.get("plan", "free")
    usage = tenant.get("usage", {})

    if plan == "free":
        limits = {"tokens_per_period": 50000, "sprites_per_period": 5, "max_concurrent_sprites": 1,
                  "enabled_agents": ["director", "copywriter", "editor"]}
    else:
        limits = PLAN_LIMITS.get(plan, PLAN_LIMITS.get("starter", {}))

    tokens_used = usage.get("tokens_this_period", 0)
    token_limit = limits.get("tokens_per_period", 50000)

    return {
        "plan": plan,
        "tokens": {
            "used": tokens_used,
            "limit": token_limit,
            "percentage": round(tokens_used / token_limit * 100, 1) if token_limit > 0 else 0,
        },
        "sprites": {
            "spawned_this_period": usage.get("sprites_spawned_this_period", 0),
            "period_limit": limits.get("sprites_per_period", 5),
            "active": 0,
            "concurrent_limit": limits.get("max_concurrent_sprites", 1),
        },
        "enabled_agents": limits.get("enabled_agents", ["director", "copywriter", "editor"]),
    }


@app.get("/billing/status")
async def billing_status(
    user_info: tuple[str, bool] = Depends(get_current_user),
):
    """Get plan and subscription info."""
    user_id, is_anon = user_info
    if is_anon:
        raise HTTPException(401, "Sign in to view billing")

    db = get_db()
    tenant = db.get_tenant_by_user(user_id)

    if not tenant:
        return {
            "plan": "free",
            "status": "active",
            "current_period_end": None,
            "limits": {"tokens_per_period": 50000, "sprites_per_period": 5, "max_concurrent_sprites": 1},
        }

    plan = tenant.get("plan", "free")
    billing = tenant.get("billing", {})

    if plan == "free":
        plan_limits = {"tokens_per_period": 50000, "sprites_per_period": 5, "max_concurrent_sprites": 1}
    else:
        plan_limits = PLAN_LIMITS.get(plan, {})

    return {
        "plan": plan,
        "status": billing.get("status", "active"),
        "current_period_end": billing.get("current_period_end"),
        "limits": plan_limits,
    }


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Handle unexpected errors. Never leak stack traces to clients."""
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=None,
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
