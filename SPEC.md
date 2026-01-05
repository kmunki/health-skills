# AI Health Companion: Spec v2

## Purpose

Help people who are comfortable with AI but aren't using it well for health to have a better system for it. Half the benefit is explaining how it works.

The AI already knows medicine. What it doesn't know is the person. These skills fix that.

---

## The Two Skills

### Skill 1: Health Baseline

**What it does:** Conducts a one-time interview to build personal health context—medical history, health psychology, access constraints, communication preferences.

**Mental model it teaches:** "AI should know you as a person, not just your symptoms. Context changes everything."

**Why this is underserved:** Users ask AI health questions in isolation. They don't think to establish ongoing context. They don't realize that telling the AI "I tend to minimize symptoms and delay care" changes how it should respond to them.

**Key elements:**
- Basic health profile (conditions, medications, family history)
- Health psychology calibration (avoider vs. anxious, past negative experiences, what kind of reassurance helps)
- Access and constraints (insurance, geography, time/cost sensitivity)
- Communication preferences (detail level, decision-making style)

**Output:** A summary document the user keeps in their Project/conversation for future reference.

---

### Skill 2: Visit Prep

**What it does:** Helps the user prepare for an upcoming medical appointment—clarifying concerns, anticipating questions, preparing to communicate effectively.

**Mental model it teaches:** "AI can help you prepare for real-world medical interactions, not just answer health questions."

**Why this is underserved:** People with doctors in their social network get informal visit prep ("here's what they'll probably ask, here's what to make sure you mention"). Everyone else walks in cold. This is the "clinical friend" gap.

**Key elements:**
- Clarify the concern (what, how long, what you've tried, what you're hoping to learn)
- Anticipate the visit (likely questions, possible exam/tests)
- Prepare communication (how to describe symptoms clearly, questions to ask, how to advocate if dismissed)
- Output stays in thread—user accesses it from their phone during the appointment

**Closes the loop:** After the visit, the skill prompts the user to report back. What did they learn? What changed? This naturally updates the baseline context over time.

**References baseline if available:** Adapts approach based on health psychology—reminds an avoider not to downplay symptoms, helps an anxious person prioritize concerns.

---

## Web Page Context

The page isn't just hosting skills—it's teaching the approach.

**1. The Problem (brief)**
- The "clinical friend" gap
- AI can fill it, but most people aren't using it well

**2. The Insight**
- AI already knows medicine
- What it doesn't know is you
- Context changes everything

**3. The Skills**
For each skill:
- What it does (one sentence)
- Why it helps (the mental model)
- The full skill text (transparency)
- How to install

**4. Important Limitations**
- This is not for emergencies—if you're in crisis, call 911 or go to the ER
- This doesn't replace doctors—it helps you work with them better
- Clear, upfront, before they install

**5. Getting Started**
- Do Health Baseline once
- Use Visit Prep before appointments
- Report back after visits
- That's the system

---

## Skill Text Structure

Each skill should include:

1. **Purpose statement** (why this exists—the pedagogy)
2. **Instructions** (what to actually do)
3. **Tone/approach guidance** (how to do it)
4. **What not to do** (guardrails—including: if user appears to be in an emergency, stop and direct them to emergency services)

---

## What This Spec Doesn't Cover

- Website technical implementation
- Branding/domain decisions
- Repository structure
