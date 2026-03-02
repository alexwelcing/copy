# How to Use Agency Studio for Agents

Agency Studio is designed as a "Headless Agency." While humans use the Go frontend, external agents can use the REST API to orchestrate marketing campaigns, generate assets, and audit landing pages using our specialized swarm intelligence.

---

## 1. Authentication

External agents can authenticate in two ways:

### A. Professional (Authenticated)
Use a Firebase ID Token in the `Authorization` header. This is required for paid features and high-volume usage.
```http
Authorization: Bearer <FIREBASE_ID_TOKEN>
```

### B. Anonymous (Identity Stitching)
Use a persistent Anonymous ID to start work that can later be "claimed" by a human user. Use the `ajs_anonymous_id` cookie (recommended) or the `X-Anonymous-ID` header.
```http
Cookie: ajs_anonymous_id=uuid-goes-here
# OR
X-Anonymous-ID: uuid-goes-here
```

---

## 2. Core Endpoints

### Execute a Skill (`POST /api/work`)
Trigger one of our 29+ specialized marketing skills.

**Request:**
```json
{
  "skill": "copywriting",
  "task": "Write a landing page headline for a project management tool",
  "context": {
    "product": "TaskFlow AI",
    "audience": "Engineering Managers",
    "tone": "Direct and Technical"
  }
}
```

### Async Work (`POST /api/work/async`)
For heavy tasks (like video generation or deep strategy), use the async endpoint. It returns a `job_id` you can poll via `/api/briefs/{id}`.

### URL Analysis (`POST /api/analyze-url`)
Send a URL; our agents will capture a screenshot and perform a conversion audit (PAGE_CRO).
```json
{
  "url": "https://example.com",
  "task": "Identify the top 3 friction points in the signup flow."
}
```

### Asset Generation (`POST /api/generate-asset`)
Generate high-fidelity marketing assets via FAL.ai integration.
```json
{
  "type": "image",
  "prompt": "Cinematic shot of a neo-madison avenue office, 1960s aesthetic",
  "model": "flux-pro-1.1"
}
```

---

## 3. Available Agents (The Swarm)

When you call `/api/work`, your task is automatically routed through our internal swarm logic:

| Agent | Domain | Best For... |
| :--- | :--- | :--- |
| **Strategist** | Positioning | Market gaps, reframing, unique value props. |
| **Copywriter** | Persuasion | Ad copy, landing pages, email sequences. |
| **Analyst** | Data | A/B test design, analytics tracking, performance audits. |
| **Director** | Quality | Brand guardianship and cinematic standards. |
| **Optimizer** | Iteration | Incremental gains on existing copy/funnels. |
| **Editor** | Precision | Technical accuracy and tonal consistency. |

---

## 4. The "Stitching" Pattern (For Onboarding Agents)

If you are building an agent that helps users "try" Agency Studio, follow this pattern:

1.  **Generate a UUID** for the session.
2.  **Set the Cookie** `ajs_anonymous_id` in your requests.
3.  **Run a Skill** (e.g., `marketing-ideas`) to show the user immediate value.
4.  **Redirect the User** to `https://agency.studio/login?signup=true&reason=view_results`.
5.  **Claim Work:** After the user signs up, call `POST /api/user/claim` with that same Anonymous ID to move the results to their permanent account.

---

## 5. Developer Best Practices

-   **Context is King:** The more detail you provide in the `context` object, the better the agents perform. Always include `product`, `audience`, and `constraints`.
-   **Structured Outputs:** Most endpoints return a `sections` object in the response. Use this for programmatic integration instead of parsing the raw `output` string.
-   **Rate Limits:** Free tier (anonymous) is limited to 5 runs per day. Authenticated users scale based on their plan (Starter/Growth/Enterprise).
