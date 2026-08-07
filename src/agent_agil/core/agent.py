"""Core Agent Brain — The main agent logic."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from dotenv import load_dotenv
import yaml


# =============================================================================
# ENUMS & CONSTANTS
# =============================================================================

class AgentMode(Enum):
    """Agent operating modes."""
    RESEARCH = "research"
    EXECUTION = "execution"
    TESTING = "testing"
    REPORTING = "reporting"


class RiskLevel(Enum):
    """Risk tolerance levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# =============================================================================
# CONFIG LOADERS
# =============================================================================

class ConfigLoader:
    """Load and manage all configuration files."""

    CONFIG_DIR = Path(__file__).parent.parent / "config"

    @classmethod
    def load_soul(cls) -> str:
        """Load SOUL.md — the core identity."""
        return (cls.CONFIG_DIR / "SOUL.md").read_text(encoding="utf-8")

    @classmethod
    def load_agents(cls) -> str:
        """Load AGENTS.md — domain context and tools."""
        return (cls.CONFIG_DIR / "AGENTS.md").read_text(encoding="utf-8")

    @classmethod
    def load_workflow(cls) -> str:
        """Load WORKFLOW.md — execution flow."""
        return (cls.CONFIG_DIR / "WORKFLOW.md").read_text(encoding="utf-8")

    @classmethod
    def load_memory_seed(cls) -> Dict[str, Any]:
        """Load MEMORY_SEED.json — initial memory and preferences."""
        with open(cls.CONFIG_DIR / "MEMORY_SEED.json", "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def load_personalities(cls) -> Dict[str, Any]:
        """Load config.yaml — personality overlays."""
        with open(cls.CONFIG_DIR / "config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @classmethod
    def load_env(cls) -> Dict[str, str]:
        """Load .env file."""
        load_dotenv(cls.CONFIG_DIR / ".env")
        return dict(os.environ)


# =============================================================================
# AGENT STATE
# =============================================================================

@dataclass
class AgentState:
    """Current state of the agent."""
    mode: AgentMode = AgentMode.RESEARCH
    current_niche: Optional[str] = None
    current_project: Optional[str] = None
    personality: str = "money_hunter_base"
    spend_limit_daily: float = 0.0
    spend_limit_per_transaction: float = 0.0
    wallet_balance: float = 0.0
    memory: Dict[str, Any] = field(default_factory=dict)

    def update_from_memory_seed(self, seed: Dict[str, Any]) -> None:
        """Update state from MEMORY_SEED.json."""
        prefs = seed.get("user_preferences", {})
        self.spend_limit_daily = float(prefs.get("daily_spend_limit", "0").replace("$", ""))
        self.spend_limit_per_transaction = float(prefs.get("per_transaction_limit", "0").replace("$", ""))
        self.memory = seed.get("procedural_memory", {})


# =============================================================================
# PERSONALITY SYSTEM
# =============================================================================

class PersonalityManager:
    """Manage personality switching."""

    def __init__(self):
        self.personalities = ConfigLoader.load_personalities()
        self.default = self.personalities.get("default_personality", "money_hunter_base")

    def get_personality(self, name: str) -> Dict[str, Any]:
        """Get personality config by name."""
        return self.personalities.get("personalities", {}).get(name, {})

    def switch(self, name: str) -> str:
        """Switch to a personality. Returns system prompt overlay."""
        personality = self.get_personality(name)
        if not personality:
            raise ValueError(f"Personality '{name}' not found")

        description = personality.get("description", "")
        tone = personality.get("tone", "")
        focus = personality.get("focus", "")

        overlay = f"""[PERSONALITY OVERLAY: {name}]
Description: {description}
Tone: {tone}
Focus: {focus}
"""
        return overlay


# =============================================================================
# WALLET MANAGER (Read-Only)
# =============================================================================

class WalletManager:
    """Manage wallet operations (read-only for safety)."""

    def __init__(self):
        self.env = ConfigLoader.load_env()
        self.private_key = self.env.get("PK_WALLET", "")

    def get_balance(self) -> float:
        """
        Get wallet balance.
        NOTE: This is a placeholder. In production, integrate with:
        - Solana RPC (for pump.fun monitoring)
        - Ethereum RPC
        - Or other blockchain providers

        For now, returns 0.0 as we're starting from $0.
        """
        # TODO: Implement actual RPC call
        # For now, return 0 since we start from $0
        return 0.0

    def is_configured(self) -> bool:
        """Check if wallet is configured."""
        return bool(self.private_key)


# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class AgentAgil:
    """
    Main Agent_Agil class.

    This is the core agent that:
    1. Loads all configuration files
    2. Manages personality switching
    3. Executes skills
    4. Tracks spending and revenue
    5. Generates reports
    """

    def __init__(self):
        """Initialize the agent."""
        # Load configurations
        self.soul = ConfigLoader.load_soul()
        self.agents_config = ConfigLoader.load_agents()
        self.workflow = ConfigLoader.load_workflow()
        self.memory_seed = ConfigLoader.load_memory_seed()
        self.env = ConfigLoader.load_env()

        # Initialize systems
        self.personality_manager = PersonalityManager()
        self.wallet = WalletManager()
        self.state = AgentState()
        self.state.update_from_memory_seed(self.memory_seed)

        # Load personality overlay
        self.personality_overlay = self.personality_manager.switch(
            self.state.personality
        )

    def get_system_prompt(self) -> str:
        """
        Build the complete system prompt.

        Structure:
        1. SOUL.md (core identity) — slot #1
        2. Personality overlay (from config.yaml)
        3. AGENTS.md (context & tools)
        4. WORKFLOW.md (execution flow)
        5. Current state (limits, niche, project)
        """
        parts = [
            "# SYSTEM PROMPT — Agent_Agil (Money-Hunter)",
            "",
            "## 1. SOUL (Core Identity)",
            self.soul,
            "",
            "## 2. Personality Overlay",
            self.personality_overlay,
            "",
            "## 3. Domain Context & Tools",
            self.agents_config,
            "",
            "## 4. Workflow",
            self.workflow,
            "",
            "## 5. Current State",
            f"- Mode: {self.state.mode.value}",
            f"- Current Niche: {self.state.current_niche or 'None'}",
            f"- Current Project: {self.state.current_project or 'None'}",
            f"- Daily Spend Limit: ${self.state.spend_limit_daily}",
            f"- Per-Transaction Limit: ${self.state.spend_limit_per_transaction}",
            f"- Wallet Balance: ${self.wallet.get_balance()}",
        ]
        return "\n".join(parts)

    def switch_personality(self, name: str) -> str:
        """Switch to a different personality."""
        self.state.personality = name
        self.personality_overlay = self.personality_manager.switch(name)
        return f"Switched to personality: {name}"

    def set_niche(self, niche: str) -> str:
        """Set the current niche to focus on."""
        self.state.current_niche = niche
        return f"Current niche set to: {niche}"

    def set_project(self, project: str) -> str:
        """Set the current project."""
        self.state.current_project = project
        return f"Current project set to: {project}"

    def get_wallet_balance(self) -> float:
        """Get current wallet balance."""
        return self.wallet.get_balance()

    def check_spend_limit(self, amount: float) -> bool:
        """Check if spending is within limits."""
        if amount > self.state.spend_limit_per_transaction:
            return False
        # TODO: Track daily spending
        return True


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_agent_instance: Optional[AgentAgil] = None


def get_agent() -> AgentAgil:
    """Get the singleton agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = AgentAgil()
    return _agent_instance


def reset_agent() -> None:
    """Reset the agent instance (for testing)."""
    global _agent_instance
    _agent_instance = None
