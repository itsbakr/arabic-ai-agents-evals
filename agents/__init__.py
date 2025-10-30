"""
Agent definitions for Egyptian customer service evaluation
"""

from .base_agent import BaseAgent
from .agent_a_ecommerce import AgentA_Ecommerce
from .agent_b_telecom import AgentB_Telecom
from .agent_c_banking import AgentC_Banking

__all__ = [
    'BaseAgent',
    'AgentA_Ecommerce',
    'AgentB_Telecom',
    'AgentC_Banking',
]

