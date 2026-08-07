"""Basic tests for Agent_Agil."""

from agent_agil.core.agent import get_agent, reset_agent
from agent_agil.skills.registry import get_skill_registry


def test_agent_loads():
    reset_agent()
    agent = get_agent()
    assert agent is not None
    assert agent.state.personality == "money_hunter_base"


def test_skills_load():
    registry = get_skill_registry()
    assert registry.get("market-research") is not None
    assert registry.get("trend-scraping") is not None


def test_system_prompt_contains_soul():
    reset_agent()
    agent = get_agent()
    prompt = agent.get_system_prompt()
    assert "SOUL" in prompt
    assert "AGENTS" in prompt
