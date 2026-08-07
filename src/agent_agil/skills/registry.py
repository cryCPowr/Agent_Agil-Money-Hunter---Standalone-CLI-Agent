"""Skill System — Modular skills for the agent."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


# =============================================================================
# SKILL DEFINITIONS
# =============================================================================

@dataclass
class Skill:
    """Represents a skill."""
    name: str
    description: str
    category: str
    trigger: str
    steps: List[str] = field(default_factory=list)
    output_format: str = ""
    ponytail: str = ""


# =============================================================================
# BUILT-IN SKILLS
# =============================================================================

BUILTIN_SKILLS = {
    "market-research": Skill(
        name="market-research",
        description="Validate niche viability, competition & demand before pursuing.",
        category="research",
        trigger="need niche validation, market research, check competition, estimate demand",
        steps=[
            "Define niche & research questions",
            "Check competition (browser search)",
            "Validate demand (keyword volume, forums)",
            "Estimate cost vs revenue",
            "Score niche (1-10) with weighted criteria",
            "Decide: proceed / validate_more / skip"
        ],
        output_format='{"niche": "name", "score": 8, "competitors": [], "demand_signals": [], "recommendation": "proceed", "next_steps": []}',
        ponytail="Skipped: deep financial analysis (add when niche decided). Skipped: legal/compliance check (add when niche involves regulation)."
    ),
    "trend-scraping": Skill(
        name="trend-scraping",
        description="Analyze social media trends (read-only) for niche validation.",
        category="research",
        trigger="need social media trend data, analyze viral topics, track niche conversations",
        steps=[
            "Identify platforms (X, Reddit, LinkedIn, TikTok)",
            "Define keywords/hashtags for target niche",
            "Scrape READ-ONLY data",
            "Analyze: volume, sentiment, top accounts, emerging topics",
            "Output trend report"
        ],
        output_format='{"platform": "x", "keywords": [], "volume": 0, "sentiment": "neutral", "top_posts": [], "emerging_topics": []}',
        ponytail="Skipped: write access (requires approval). Skipped: historical analysis beyond 30 days."
    ),
    "content-creation": Skill(
        name="content-creation",
        description="Create content for niche (writing, visual, video scripts).",
        category="execution",
        trigger="need content draft, blog post, social media content, video script",
        steps=[
            "Analyze target audience & platform",
            "Research trending topics in niche",
            "Draft content with hooks & CTAs",
            "Review against platform ToS",
            "Output final content"
        ],
        output_format='{"title": "", "content": "", "platform": "", "hashtags": [], "cta": ""}',
        ponytail="Skipped: publishing (requires approval). Skipped: media generation (needs external tools)."
    ),
    "freelance-proposal": Skill(
        name="freelance-proposal",
        description="Write winning freelance proposals for Upwork/Fiverr/etc.",
        category="execution",
        trigger="need freelance proposal, pitch client, bid on project",
        steps=[
            "Analyze job posting requirements",
            "Match agent skills to requirements",
            "Draft personalized proposal",
            "Include portfolio/relevant experience",
            "Add pricing & timeline"
        ],
        output_format='{"cover_letter": "", "pricing": "", "timeline": "", "questions_for_client": []}',
        ponytail="Skipped: submission (requires approval). Skipped: negotiation (human decision)."
    ),
    "cost-accounting": Skill(
        name="cost-accounting",
        description="Track LLM credits, tool costs, and revenue per project.",
        category="financial",
        trigger="need cost tracking, calculate ROI, generate financial report",
        steps=[
            "Log LLM token usage per task",
            "Track external API costs",
            "Record revenue from completed work",
            "Calculate net profit/loss",
            "Generate per-project & aggregate report"
        ],
        output_format='{"project": "", "llm_cost": 0.0, "tool_cost": 0.0, "revenue": 0.0, "net": 0.0, "period": ""}',
        ponytail="Skipped: tax calculations. Skipped: multi-currency (add when needed)."
    ),
    "risk-assessment": Skill(
        name="risk-assessment",
        description="Evaluate risk before committing time/money to a project.",
        category="financial",
        trigger="need risk evaluation, assess project viability, check ToS compliance",
        steps=[
            "Identify financial risks (spend limits, revenue uncertainty)",
            "Identify platform risks (ToS, account suspension)",
            "Identify technical risks (API changes, dependencies)",
            "Score each risk (1-5 likelihood × 1-5 impact)",
            "Recommend: proceed / mitigate / abort"
        ],
        output_format='{"project": "", "risks": [{"name": "", "likelihood": 1, "impact": 1, "mitigation": ""}], "recommendation": "proceed"}',
        ponytail="Skipped: legal review (human decision). Skipped: insurance analysis."
    ),
}


# =============================================================================
# SKILL REGISTRY
# =============================================================================

class SkillRegistry:
    """Registry for managing skills."""
    
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._load_builtins()
    
    def _load_builtins(self) -> None:
        """Load built-in skills."""
        for skill in BUILTIN_SKILLS.values():
            self._skills[skill.name] = skill
    
    def register(self, skill: Skill) -> None:
        """Register a new skill."""
        self._skills[skill.name] = skill
    
    def get(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self._skills.get(name)
    
    def list_by_category(self, category: str) -> List[Skill]:
        """List skills by category."""
        return [s for s in self._skills.values() if s.category == category]
    
    def list_all(self) -> List[Skill]:
        """List all skills."""
        return list(self._skills.values())
    
    def get_system_prompt(self) -> str:
        """Generate system prompt section for all skills."""
        lines = ["## Available Skills"]
        for skill in self._skills.values():
            lines.append(f"\n### {skill.name} ({skill.category})")
            lines.append(f"Trigger: {skill.trigger}")
            lines.append(f"Description: {skill.description}")
            if skill.steps:
                lines.append("Steps:")
                for i, step in enumerate(skill.steps, 1):
                    lines.append(f"  {i}. {step}")
            if skill.output_format:
                lines.append(f"Output: {skill.output_format}")
            if skill.ponytail:
                lines.append(f"Note: {skill.ponytail}")
        return "\n".join(lines)


# Singleton
_registry: Optional[SkillRegistry] = None


def get_skill_registry() -> SkillRegistry:
    """Get the singleton skill registry."""
    global _registry
    if _registry is None:
        _registry = SkillRegistry()
    return _registry