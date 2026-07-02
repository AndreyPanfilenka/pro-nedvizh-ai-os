# PRO Nedvizh AI OS

**Repository:** `pro-nedvizh-ai-os`

An AI-powered operating system for real estate content production. PRO Nedvizh AI OS turns property listing URLs into structured data, marketing copy, and multi-channel publishing drafts — with quality control before anything goes live.

## Mission

Automate the end-to-end workflow from a single property URL to ready-to-publish content across Telegram, Instagram, and Reels — while keeping humans in control at the quality gate.

Reduce manual copy-paste, inconsistent formatting, and channel-specific rework. Give the PRO Nedvizh team a repeatable, auditable pipeline that scales with listing volume without scaling headcount linearly.

## Vision

A unified AI operating layer for real estate marketing where:

- Any listing source (URL) is recognized and parsed reliably
- Property data is normalized into a single structured schema
- Descriptions and channel-specific drafts are generated from that schema
- Quality control is built into the workflow, not bolted on afterward
- Integrations (Google Workspace, Make, OpenRouter) are documented and modular
- Agents, prompts, and workflows are versioned, testable, and improvable over time

PRO Nedvizh AI OS is the foundation — structure, documentation, and conventions first; implementation follows.

## Main Workflow

```
User inserts URL
        ↓
AI identifies source
        ↓
Extracts information
        ↓
Creates structured property
        ↓
Generates description
        ↓
Creates Telegram draft
        ↓
Creates Instagram draft
        ↓
Creates Reels scenario
        ↓
Quality control
        ↓
Ready for publishing
```

### Stage overview

| Stage | Purpose |
|-------|---------|
| **URL input** | User provides a listing or property page URL |
| **Source identification** | AI detects platform, site, and extraction strategy |
| **Information extraction** | Raw facts pulled from the page (price, area, location, features, media) |
| **Structured property** | Normalized record aligned to the internal property schema |
| **Description generation** | Marketing text from structured data |
| **Telegram draft** | Channel-formatted post ready for review |
| **Instagram draft** | Caption, hashtags, and layout notes for IG |
| **Reels scenario** | Script, shots, and timing for short-form video |
| **Quality control** | Human or automated checks before publish |
| **Ready for publishing** | Approved assets handed off to channels |

## Repository layout

| Path | Role |
|------|------|
| [`/docs`](docs/) | Architecture, agents, workflows, and release notes |
| [`/google`](google/) | Google Workspace integration specs (Sheets, Docs, Drive) |
| [`/make`](make/) | Make.com scenario definitions and automation docs |
| [`/openrouter`](openrouter/) | LLM routing, models, and API configuration |
| [`/prompts`](prompts/) | System and agent prompt libraries |
| [`/tests`](tests/) | Test plans and fixtures (future) |
| [`/examples`](examples/) | Sample inputs, outputs, and walkthroughs |
| [`/assets`](assets/) | Static assets (brand, templates, media) |

## Status

**Foundation phase** — directory structure and documentation only. No application code, Make scenarios, or API implementation yet.

See nested `README.md` files in each folder for scope and planned contents.
