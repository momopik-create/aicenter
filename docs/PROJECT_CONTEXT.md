# AICenter — Project Context

## Project

AICenter is an AI-tool affiliate/research platform.

Repository:
`aicenter`

The project includes an automated Research Engine that researches products/tools and prepares structured research packages for later review and publishing.

---

# Research Engine

## Current Version

Research Engine v2

## Core Contract

The main data flow is:

ResearchInput
→ ResearchPipeline
→ ResearchPackage

The research pipeline is:

Search
→ Fetch
→ Validate
→ Evidence
→ Review

---

# Architecture

The intended research architecture is:

Tavily
→ SearchResult
→ SourceValidator
→ WebFetch
→ SourceEvidence
→ ResearchPackage
→ ReviewStore

The system should separate:

1. Discovering sources
2. Fetching source content
3. Validating sources
4. Extracting evidence
5. Building structured research data
6. Human review
7. Publishing

---

# Current Components

Important Research Engine components include:

- `web_fetch.py`
- `tavily_provider.py`
- `pipeline.py`
- `research.py`
- `publish.py`

Research reviews are stored under:

`data/research_reviews`

---

# Review / Publishing

The MVP includes:

- Tavily lazy loading
- ReviewStore
- PublishGate
- Approval workflow
- `research.py`
- `publish.py`

PublishGate is intended to prevent publishing unless the research package satisfies the required conditions, including:

- research is complete
- research is approved
- minimum source requirement is satisfied
- the item has not already been published

---

# Current Runtime Status

A real Vultr research execution was successfully completed.

Observed result:

- `status = completed`
- `sources = 8`
- `review_status = pending`

However:

- `facts = 0`
- `pricing = 0`

This means the current pipeline successfully collects research sources but does NOT yet perform the required structured extraction of facts and pricing.

---

# Current Known Limitation

The current Research Engine is primarily functioning as a source-collection pipeline.

It does not yet reliably transform the collected source material into structured fields such as:

- facts
- pricing
- pros
- cons

The next major implementation step is therefore structured extraction.

---

# Current Decision

Add a Gemini-powered extraction stage after source collection/evidence gathering and before Review/Publish.

Target flow:

Search
→ Fetch
→ Validate
→ Evidence
→ Gemini Extraction
→ ResearchPackage
→ Review
→ PublishGate
→ Publish

Gemini should extract structured research information from the collected evidence.

At minimum, extraction should support:

- facts
- pricing
- pros
- cons

The extraction stage should preserve source attribution so that extracted claims can be traced back to evidence.

---

# Important Engineering Rules

1. Do not bypass the existing Research Engine contracts without a clear reason.

2. Keep source collection and structured extraction as separate stages.

3. Do not treat search-result snippets as sufficient evidence when the source page can be fetched.

4. Extracted claims should retain their source/evidence relationship.

5. Review must happen before publishing.

6. PublishGate must remain the final protection against invalid or unapproved publishing.

7. Do not silently publish research that has not passed the review requirements.

8. Preserve compatibility with the existing `ResearchInput` and `ResearchPackage` contracts unless the architecture explicitly requires a versioned change.

---

# Recent Development History

## September 24, 2026

Research Engine v2 contracts were integrated.

The main synchronization work involved:

- `web_fetch.py`
- `tavily_provider.py`
- `pipeline.py`

The intended architecture was validated around:

Tavily
→ SearchResult
→ SourceValidator
→ WebFetch
→ SourceEvidence
→ ResearchPackage
→ ReviewStore

The MVP was subsequently integrated with:

- Tavily lazy loading
- ReviewStore
- PublishGate
- approval workflow
- research script
- publish script

Python tests were reported as passing.

Local `npm run build` had not yet been verified at that point.

## September 25, 2026

A real Vultr execution completed successfully.

The pipeline returned:

`status=completed`

with:

`sources=8`

and:

`review_status=pending`

But:

`facts=0`

and:

`pricing=0`

This confirmed that the next required step is structured extraction rather than additional source collection.

---

# Current Priority

## Priority 1 — Structured Extraction

Implement and test Gemini extraction of:

- facts
- pricing
- pros
- cons

from the collected evidence.

The extraction output must integrate with the existing `ResearchPackage`.

## Priority 2 — Evidence Traceability

Ensure every important extracted claim can be traced to the source/evidence from which it was derived.

## Priority 3 — Review Integration

Ensure extracted results enter the existing ReviewStore and approval workflow correctly.

## Priority 4 — Publish Integration

Ensure PublishGate continues to block incomplete or unapproved research.

## Priority 5 — End-to-End Test

Run a real research job and verify that:

- sources > 0
- facts > 0
- pricing is populated when pricing information exists
- pros > 0 when evidence supports them
- cons > 0 when evidence supports them
- review status is correct
- publishing remains blocked until approval

---

# Current Task for Codex

Before modifying files:

1. Inspect the repository.
2. Read the current Research Engine implementation.
3. Identify the current `ResearchPackage` structure.
4. Identify where source evidence is stored.
5. Identify the existing Gemini integration, if any.
6. Identify the current tests.
7. Compare the implementation with this project context.

Do not immediately rewrite the architecture.

First report:

- current architecture
- relevant files
- current data structures
- current extraction capabilities
- what is missing for Gemini extraction
- proposed minimal implementation

Do not modify files until the implementation plan is reviewed.