"""
Scenario loader and data structures for LLM-to-LLM evaluation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from simulator.customer_simulator import CustomerPersona


@dataclass
class Scenario:
    """
    Test scenario with customer persona and goal
    """
    scenario_id: str
    agent_type: str  # agent_a, agent_b, or agent_c
    title: str
    description: str
    complexity: str  # simple, medium, high, critical
    
    # Customer simulation
    customer_persona: CustomerPersona
    customer_goal: str  # What the customer wants to achieve
    initial_context: Dict[str, any]  # Information customer has (order #, account #, etc.)
    
    # Evaluation criteria
    success_criteria: List[str]  # List of success conditions
    evaluation_dimensions: Dict[str, str]  # Dimension name -> description
    
    # Expected agent behaviors
    expected_actions: List[str]  # Actions agent should take
    must_not_do: List[str] = field(default_factory=list)  # Things agent must avoid
    
    # Scenario metadata
    max_turns: int = 10  # Maximum conversation turns
    min_turns: int = 3   # Minimum expected turns for resolution
    
    def __post_init__(self):
        """Validate scenario data"""
        if self.max_turns < self.min_turns:
            raise ValueError(f"max_turns must be >= min_turns in scenario {self.scenario_id}")


class ScenarioLoader:
    """Loads and manages test scenarios"""
    
    def __init__(self):
        self.scenarios: Dict[str, List[Scenario]] = {
            "agent_a": [],
            "agent_b": [],
            "agent_c": []
        }
    
    def add_scenario(self, scenario: Scenario):
        """Add a scenario to the loader"""
        agent_type = scenario.agent_type.lower().replace("_ecommerce", "").replace("_telecom", "").replace("_banking", "")
        if agent_type not in self.scenarios:
            raise ValueError(f"Invalid agent type: {agent_type}")
        self.scenarios[agent_type].append(scenario)
    
    def get_scenarios(self, agent_type: str) -> List[Scenario]:
        """Get all scenarios for an agent type"""
        agent_type = agent_type.lower().replace("_ecommerce", "").replace("_telecom", "").replace("_banking", "")
        return self.scenarios.get(agent_type, [])
    
    def get_scenario_by_id(self, scenario_id: str) -> Optional[Scenario]:
        """Get a specific scenario by ID"""
        for scenarios in self.scenarios.values():
            for scenario in scenarios:
                if scenario.scenario_id == scenario_id:
                    return scenario
        return None
    
    def get_all_scenarios(self) -> List[Scenario]:
        """Get all scenarios across all agents"""
        all_scenarios = []
        for scenarios in self.scenarios.values():
            all_scenarios.extend(scenarios)
        return all_scenarios
    
    def count_scenarios(self) -> Dict[str, int]:
        """Count scenarios per agent"""
        return {
            agent_type: len(scenarios)
            for agent_type, scenarios in self.scenarios.items()
        }


# Helper function for loading scenarios
def load_scenarios_for_agent(agent_type: str) -> List[Scenario]:
    """
    Load scenarios for a specific agent type
    
    Args:
        agent_type: Agent type (agent_a, agent_b, or agent_c)
        
    Returns:
        List of scenarios for that agent
    """
    # Import scenario modules dynamically
    if agent_type == "agent_a":
        from scenarios.agent_a_scenarios import get_agent_a_scenarios
        return get_agent_a_scenarios()
    elif agent_type == "agent_b":
        from scenarios.agent_b_scenarios import get_agent_b_scenarios
        return get_agent_b_scenarios()
    elif agent_type == "agent_c":
        from scenarios.agent_c_scenarios import get_agent_c_scenarios
        return get_agent_c_scenarios()
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")
