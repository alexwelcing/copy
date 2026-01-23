#!/bin/bash
# Example API requests for Marketing Agency API

# Set your service URL
API_URL="${API_URL:-http://localhost:8080}"

echo "Marketing Agency API Examples"
echo "=============================="
echo "API URL: $API_URL"
echo ""

# Health check
echo "1. Health Check"
echo "---------------"
curl -s "$API_URL/health" | jq .
echo ""

# List skills
echo "2. List Available Skills"
echo "------------------------"
curl -s "$API_URL/skills" | jq .
echo ""

# Copywriting example
echo "3. Copywriting - Generate Headlines"
echo "-----------------------------------"
curl -s -X POST "$API_URL/work" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "copywriting",
    "task": "Write 3 headline options for a landing page",
    "context": {
      "product": "TaskFlow - AI-powered project management",
      "audience": "Engineering managers at tech companies",
      "main_benefit": "Reduce meeting time by 50%",
      "tone": "Professional but approachable"
    }
  }' | jq .
echo ""

# Page CRO example
echo "4. Page CRO - Audit Landing Page"
echo "---------------------------------"
curl -s -X POST "$API_URL/work" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "page-cro",
    "task": "Audit this landing page for conversion optimization opportunities. Focus on the headline, CTA, and trust signals.",
    "content": "<html><head><title>TaskFlow</title></head><body><h1>Welcome to TaskFlow</h1><p>The best project management tool for teams.</p><button>Learn More</button></body></html>",
    "context": {
      "conversion_goal": "Free trial signup",
      "traffic_source": "Google Ads"
    }
  }' | jq .
echo ""

# Email sequence example
echo "5. Email Sequence - Onboarding"
echo "------------------------------"
curl -s -X POST "$API_URL/work" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "email-sequence",
    "task": "Create a 5-email onboarding sequence to get users to their first project",
    "context": {
      "product": "TaskFlow project management",
      "activation_event": "Create first project",
      "audience": "New signups, mostly engineering managers",
      "tone": "Helpful, not pushy"
    }
  }' | jq .
echo ""

# Marketing psychology example
echo "6. Marketing Psychology - Identify Triggers"
echo "--------------------------------------------"
curl -s -X POST "$API_URL/work" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "marketing-psychology",
    "task": "Identify the top 5 psychological triggers we should use on our pricing page and explain how to apply each one",
    "context": {
      "product": "SaaS project management tool",
      "pricing_tiers": "Free, Pro ($15/mo), Team ($30/user/mo)",
      "goal": "Increase Pro tier conversions"
    }
  }' | jq .
echo ""

# Launch strategy example
echo "7. Launch Strategy - Product Hunt"
echo "----------------------------------"
curl -s -X POST "$API_URL/work" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "launch-strategy",
    "task": "Create a Product Hunt launch plan including pre-launch preparation, launch day timeline, and post-launch follow-up",
    "context": {
      "product": "TaskFlow - AI project management",
      "launch_date": "Next Tuesday",
      "existing_audience": "500 beta users, 2000 Twitter followers",
      "goal": "Top 5 Product of the Day"
    }
  }' | jq .
echo ""

echo "Done! All examples executed."
