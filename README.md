# Health Skills

AI skills that close the "clinical friend" gap.

## The Problem

People with doctors in their social network get informal health guidance—"here's what they'll probably ask," "make sure you mention X," "that sounds like it could be Y." Everyone else navigates healthcare alone.

AI can fill this gap, but most people aren't using it well. They ask questions in isolation, as if talking to a stranger every time. They don't realize that context changes everything.

## The Insight

AI already knows medicine. What it doesn't know is *you*.

This skill fixes that.

## How It Works

**One skill, always current.**

Install `health-assistant` once. It fetches the latest guidance from this repo whenever you ask health questions. No reinstalls needed when we improve things.

The skill handles three modes:
- **Health Baseline** — Build your health context (one-time setup)
- **Symptom Exploration** — Think through concerns like a clinician would
- **Visit Prep** — Prepare for medical appointments

## Transparency

Everything the AI sees is public in [`/guidance`](./guidance/). You can read exactly what instructions it's getting.

## Installation

1. Download [`skills/health-assistant`](./skills/health-assistant/) as a zip
2. In Claude Desktop, go to Settings → Skills → Add Skill
3. Upload the zip

## Important Limitations

- **Not for emergencies.** If you're in crisis, call 911 or go to the ER.
- **Doesn't replace doctors.** This helps you work with them better, not avoid them.
- **Not medical advice.** AI can help you think, but decisions are yours.

## Status

Early development. Testing with friends before wider release.
