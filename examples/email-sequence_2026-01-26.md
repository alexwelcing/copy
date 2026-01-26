# Example: Email-Sequence
**Date:** 2026-01-26
**Status:** ⚠️ Needs Polish
**Score:** 0/10

## The Brief
**Task:** Write a 3-email welcome sequence for new users who just signed up for the 'Studio' tier.
**Context:** {
  "product": "High Era Terminal",
  "goal": "Activation (create first brief)"
}

---

## The Output
# Welcome Sequence for High Era Terminal (Studio Tier)

## Sequence Overview

**Purpose**: Drive activation by guiding new Studio users to create their first brief, while establishing High Era's value and building confidence in the platform.

**Length**: 3 emails over 5 days

**Entry Trigger**: User completes Studio tier signup

**Success Goal**: User creates and publishes their first brief within 7 days

**Exit Conditions**: 
- User creates first brief (moves to onboarding sequence)
- User upgrades/downgrades tier
- User unsubscribes

---

## Email Schedule

- **Email 1**: Immediate (within 5 minutes of signup)
- **Email 2**: Day 2 (48 hours after signup)
- **Email 3**: Day 5 (120 hours after signup)

**Automation Note**: If user creates brief after Email 1 or 2, exit sequence and enter "Active User Onboarding" sequence.

---

## Email 1: Welcome + First Step

### Subject Lines
**Primary**: "Welcome to Studio, [First Name] 🎯 Your first brief awaits"

**Alternative A**: "[First Name], you're 5 minutes away from your first brief"

**Alternative B**: "Your Studio workspace is ready—here's what to do first"

### Preview Text
"Let's get you from blank canvas to brilliant brief in minutes (no pressure—we'll guide you)"

### Email Body

**From**: [Founder Name] at High Era Terminal  
**Tone**: Encouraging, confident, action-oriented

---

Hi [First Name],

Welcome to High Era Terminal Studio! 🎉

You just unlocked a workspace where great creative work starts—with clarity, not chaos.

I know staring at a blank brief can feel daunting. But here's the thing: you don't need everything figured out. You just need to start.

**Your first mission (5 minutes, tops):**

Create your first brief using our Studio Brief Builder. Even if it's just a rough sketch. Even if you change everything tomorrow.

[CTA Button: Create My First Brief]

**Here's why this matters:**

Most creative projects fail before they begin—not from lack of talent, but from lack of clarity. Studio briefs force the important questions upfront: What's the goal? Who's it for? What defines success?

Once you've created your first brief, you'll:
- ✓ See how Studio organizes your creative thinking
- ✓ Have a living document you can refine (not a static PDF gathering dust)
- ✓ Unlock collaboration features to bring your team in

**Need a starting point?**

Try one of our Studio templates:
- Brand Campaign Brief
- Product Launch Brief  
- Content Series Brief
- Rebrand Strategy Brief

Pick the closest match, customize it, and you're off.

I'm rooting for you,  
[Founder Signature]

**P.S.** Stuck? Hit reply. I read every single one, and I love helping new Studio users find their groove. No question is too basic.

---

### Automation Notes
- **Tag**: "Studio_Welcome_Sent"
- **Wait condition**: 48 hours OR "First Brief Created" event
- **Branch logic**: If brief created → Exit to onboarding sequence; If not → Send Email 2

---

## Email 2: Quick Win + Social Proof

### Subject Lines
**Primary**: "How Sarah went from chaos to clarity (in one brief)"

**Alternative A**: "The 3-minute brief that changed everything"

**Alternative B**: "[First Name], here's the Studio feature everyone uses first"

### Preview Text
"Plus: A simple framework to structure any creative brief—even when you don't have all the answers yet"

### Email Body

**From**: [Founder Name] at High Era Terminal  
**Tone**: Story-driven, empathetic, practical

---

Hey [First Name],

Quick question: Have you created your first brief yet?

No judgment if you haven't—I get it. Starting is the hardest part.

Let me share how Sarah, a brand strategist at a Series B startup, approached her first Studio brief:

**She didn't have all the answers.**

Her CMO asked her to "figure out Q2 messaging," but the strategy was still fuzzy. Budget? TBD. Channels? Under discussion. Timeline? Flexible.

Most people would've waited for clarity. Sarah did the opposite.

**She created a Studio brief with what she knew:**

- Goal: "Increase product awareness in mid-market segment"
- Open questions: "Budget depends on last month's performance—updating by March 15"
- Success metrics: "TBD with sales team—meeting scheduled"

Here's what happened next:

✓ She shared the brief with stakeholders  
✓ The blank spaces became conversation starters  
✓ Within 3 days, all the "TBDs" were filled in  
✓ The project kicked off a week earlier than planned

**The brief didn't need to be perfect. It needed to exist.**

[CTA Button: Start My Brief Like Sarah Did]

**Sarah's framework (steal this):**

When creating your first brief, answer just these three:
1. **What's the objective?** (Even if it's vague, write it down)
2. **Who's it for?** (Audience, stakeholders, team)
3. **What does success look like?** (Metrics, outcomes, feelings)

Everything else? You can add it as you go. Studio briefs are living documents.

Ready to give it a shot?

[CTA Button: Create My First Brief]

Looking forward to seeing what you build,  
[Founder Signature]

**P.S.** Prefer to see how it works first? Here's a [2-minute video walkthrough](#) of someone creating their first Studio brief in real-time. No fluff, just the basics.

---

### Automation Notes
- **Tag**: "Studio_Day2_Sent"
- **Wait condition**: 72 hours OR "First Brief Created" event
- **Branch logic**: If brief created → Exit to onboarding sequence; If not → Send Email 3
- **A/B Test**: Test story-driven vs. feature-benefit focused email

---

## Email 3: Objection Handling + Incentive

### Subject Lines
**Primary**: "Last nudge: Your Studio brief is waiting (+ I removed one excuse)"

**Alternative A**: "What's holding you back from creating your first brief?"

**Alternative B**: "[First Name], let's get that brief done together"

### Preview Text
"Book 15 minutes with our team and we'll build your first brief with you—completely free, zero pressure"

### Email Body

**From**: [Founder Name] at High Era Terminal  
**Tone**: Direct, helpful, offering support

---

Hi [First Name],

I'll be direct: Most new Studio users who create their first brief in the first week become power users. Those who don't... often never do.

I don't want you to fall into that second group.

So I'm reaching out personally to ask: **What's in the way?**

**Common blockers I hear:**

❌ "I don't have a project right now"  
→ Your best brief is the one you *will* have. Future-you will thank present-you.

❌ "I want to explore Studio more first"  
→ Exploring is fine, but creating is where it clicks. You'll learn more in 5 minutes of building than 50 minutes of browsing.

❌ "I'm not sure if I'm using it right"  
→ There's no wrong way. And if you get stuck, we're here.

**Here's what I'm offering:**

Book a 15-minute "Build Your First Brief" session with our team. We'll:
- Hop on a quick call (video optional)
- Ask you a few questions about your project
- Build the brief structure together in real-time
- Show you Studio features as they come up naturally

No sales pitch. No upsell. Just hands-on help getting you unstuck.

[CTA Button: Book My Brief Building Session]

**Or, if you prefer to fly solo:**

Use our Studio Quick-Start Brief template—it's pre-filled with examples and prompts. Just swap in your details.

[CTA Button: Use Quick-Start Template]

**Why this matters to me:**

I built High Era Terminal because I was tired of watching brilliant creative projects derail from poor planning. Studio is my answer to that—but only if you use it.

Give it one real shot. Create one brief. If it doesn't click, you'll know. But if it does? You'll wonder how you worked without it.

Let's make this happen,  
[Founder Signature]

**P.S.** If Studio isn't the right fit, that's totally okay. Hit reply and let me know why—your feedback genuinely shapes what we build next. And if you'd like to pause or cancel your subscription, I respect that. [Manage subscription](#)

---

### Automation Notes
- **Tag**: "Studio_Day5_Sent"
- **Wait condition**: 48 hours OR "First Brief Created" event OR "Session Booked" event
- **Branch logic**: 
  - If brief created → Exit to onboarding sequence
  - If session booked → Exit to "Concierge Onboarding" sequence
  - If no action after 48 hours → Tag "Studio_Inactive" and enter re-engagement sequence (Day 14)
- **Send time optimization**: Send during work hours in user's timezone (9am-11am performs best)

---

## Segmentation Recommendations

### Priority Segments for This Sequence

1. **By signup source** (customize Email 1 reference):
   - Product Hunt users: Mention "You found us on PH—welcome to the community!"
   - Direct signup: Standard version
   - Referral: "Thanks to [referrer] for sending you our way"

2. **By industry** (if collected at signup):
   - Agencies: Emphasize client collaboration features
   - In-house teams: Emphasize stakeholder alignment
   - Freelancers: Emphasize solo workflow and client sharing

3. **By user behavior** (dynamic):
   - Logged in but didn't start brief → Send Email 2 earlier (Day 1)
   - Opened brief builder but didn't publish → Add email 2.5 addressing abandonment
   - Zero logins → Add friction indicator; consider phone outreach

### Exclusion Rules
- Users who create brief before next email → Exit immediately
- Users who downgrade from Studio → Exit and enter cancellation feedback sequence
- Users who mark emails as spam → Suppress all marketing emails

---

## A/B Test Suggestions

### Test Priority 1: Email 1 Subject Line
- **Control**: "Welcome to Studio, [First Name] 🎯 Your first brief awaits"
- **Variant**: "[First Name], you're 5 minutes away from your first brief"
- **Hypothesis**: Time-based urgency drives faster action than welcome message
- **Measure**: Email 1 → Brief creation rate (48hr window)

### Test Priority 2: Email 2 Format
- **Control**: Story-driven (Sarah's case study)
- **Variant**: Framework-driven (3-step brief method with bullet points)
- **Hypothesis**: Some users want proof (story), others want process (framework)
- **Measure**: Click-through rate + brief creation rate

### Test Priority 3: Email 3 Incentive
- **Control**: Free brief-building session
- **Variant**: Extended trial period (add 7 days if they create brief)
- **Hypothesis**: Low-touch incentive may outperform high-touch for self-serve users
- **Measure**: Conversion to brief creation + cost per activation

### Test Priority 4: Send Timing
- **Control**: Email 2 at Day 2, Email 3 at Day 5
- **Variant**: Email 2 at Day 1, Email 3 at Day 3 (compressed sequence)
- **Hypothesis**: Faster sequence maintains momentum during high-intent window
- **Measure**: Sequence completion rate + 7-day activation rate

---

## Success Metrics & Benchmarks

### Email Performance Targets

| Email | Open Rate | Click Rate | Brief Creation Rate |
|-------|-----------|------------|---------------------|
| Email 1 | 65-75% | 25-35% | 15-20% |
| Email 2 | 35-45% | 15-20% | 10-15% |
| Email 3 | 25-35% | 12-18% | 5-8% |

**Overall Sequence Goal**: 35-40% of recipients create first brief within 7 days

### Leading Indicators
- Email 1 send-to-login rate: >40%
- Email 2 send-to-brief-builder-open: >20%
- Email 3 session booking rate: >5%

### Warning Signs
- Open rate drop >10% between emails → Review deliverability
- Click rate high but no brief creation → Product friction issue
- High unsubscribe on Email 1 (>2%) → Expectation mismatch at signup

---

## Implementation Checklist

**Before Launch:**
- [ ] Set up "First Brief Created" event tracking
- [ ] Create brief templates mentioned in emails
- [ ] Record 2-minute walkthrough video (Email 2)
- [ ] Set up booking calendar for brief-building sessions (Email 3)
- [ ] Configure timezone-based send time optimization
- [ ] Test all CTA links and tracking parameters
- [ ] Set up exit conditions and sequence branches
- [ ] Create "Studio_Welcome" tag taxonomy

**Week 1 Monitoring:**
- [ ] Review deliverability metrics daily
- [ ] Monitor brief creation correlation with email opens
- [ ] Track session booking fulfillment and outcomes
- [ ] Collect qualitative feedback from session attendees
- [ ] Identify high-performing subject lines for future use

**Week 2 Optimization:**
- [ ] Implement winning A/B test variants
- [ ] Adjust send timing based on open rate patterns
- [ ] Refine segmentation based on conversion data
- [ ] Update copy based on common objections from sessions

---

## Cross-Functional Notes

**For Product Team:**
- Monitor brief abandonment rate (started but not published)
- Consider in-app prompts aligned with email timing
- Track whether email-driven users have better retention than organic activators

**For Customer Success:**
- Users booking sessions may need white-glove onboarding
- Tag session attendees for proactive check-ins at Day 30
- Use session feedback to improve self-serve documentation

**For Content Team:**
- High-performing email stories (like Sarah's) can become blog content
- Track which templates are most popular from email clicks
- Consider video series based on brief-building sessions

---

This sequence is designed to be empathetic but action-oriented, removing friction while maintaining urgency. The key is making that first brief feel achievable, not intimidating—then proving value through the act of creation itself.

---

## Quality Assurance
**Critique:** Failed to parse evaluation.
