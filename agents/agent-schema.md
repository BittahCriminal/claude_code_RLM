# Agent Schema Documentation

This document defines the schema for RLM sub-agents that process domain-specific knowledge.

## Agent File Structure

Each agent is defined in a markdown file with YAML frontmatter:

```yaml
---
name: agent-name
domain: domain-identifier
description: Brief description of the agent's expertise
version: 1.0.0
tags:
  - primary-tag
  - secondary-tag
knowledge_sources:
  - source-id-1
  - source-id-2
models:
  preferred: claude-sonnet-4.5
  fallback: gpt-5-mini
capabilities:
  - capability-1
  - capability-2
---
```

## Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique agent identifier |
| `domain` | string | Yes | Knowledge domain (matches AgentDomain enum) |
| `description` | string | Yes | What this agent specializes in |
| `version` | string | Yes | Semantic version for the agent definition |
| `tags` | list | Yes | Tags that route queries to this agent |
| `knowledge_sources` | list | No | IDs of imported knowledge bases |
| `models.preferred` | string | No | Preferred model for this agent |
| `models.fallback` | string | No | Fallback model if preferred unavailable |
| `capabilities` | list | No | Specific capabilities this agent provides |

## Content Sections

After the frontmatter, agents can include these sections:

### ## System Prompt
Custom system prompt for this agent's subcalls.

### ## Context Template
Template for formatting context passed to the agent.

### ## Output Format
Expected output format/schema for responses.

### ## Examples
Example queries and expected responses.

## Knowledge Source Mapping

Knowledge sources are imported via `knowledge/importer.py` and tagged with:
- Agent domain (required)
- Custom tags (optional, for finer routing)

Agents automatically have access to all knowledge in their domain.
Use tags for routing queries to specific knowledge subsets.

## Agent Invocation

Agents are invoked by the RLM orchestrator when:
1. A query matches the agent's tags
2. Knowledge in the agent's domain is relevant
3. Explicitly requested via `rlm_subcall(provider="copilot", agent="agent-name")`
