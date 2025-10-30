"""
Conversation orchestrator for LLM-to-LLM dialogue
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from agents.base_agent import BaseAgent
from simulator.customer_simulator import CustomerSimulator
from scenarios.scenario_loader import Scenario
from models.base_model import BaseModel
import time

try:
    import weave
    WEAVE_AVAILABLE = True
except ImportError:
    WEAVE_AVAILABLE = False


@dataclass
class ConversationTurn:
    """Single turn in a conversation"""
    turn_number: int
    customer_message: str
    agent_message: str
    customer_tokens: int = 0
    agent_tokens: int = 0
    turn_latency: float = 0.0


@dataclass
class ConversationResult:
    """Complete conversation result"""
    scenario_id: str
    agent_type: str
    model_name: str
    turns: List[ConversationTurn]
    total_turns: int
    success: bool
    end_reason: str
    total_tokens: int
    total_latency: float
    customer_satisfied: bool = False  # Will be evaluated later
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for export"""
        return {
            "scenario_id": self.scenario_id,
            "agent_type": self.agent_type,
            "model_name": self.model_name,
            "total_turns": self.total_turns,
            "success": self.success,
            "end_reason": self.end_reason,
            "total_tokens": self.total_tokens,
            "total_latency": self.total_latency,
            "turns": [
                {
                    "turn": t.turn_number,
                    "customer": t.customer_message,
                    "agent": t.agent_message,
                    "tokens": t.customer_tokens + t.agent_tokens,
                    "latency": t.turn_latency
                }
                for t in self.turns
            ]
        }


class ConversationOrchestrator:
    """
    Orchestrates conversations between customer simulator and agent
    """
    
    def __init__(
        self,
        agent: BaseAgent,
        agent_model: BaseModel,
        customer_simulator: CustomerSimulator,
        verbose: bool = True
    ):
        """
        Initialize orchestrator
        
        Args:
            agent: Customer service agent
            agent_model: Model to use for agent responses
            customer_simulator: Customer simulator
            verbose: Print conversation in real-time
        """
        self.agent = agent
        self.agent_model = agent_model
        self.customer_simulator = customer_simulator
        self.verbose = verbose
        
    @weave.op() if WEAVE_AVAILABLE else lambda f: f
    def run_conversation(
        self,
        scenario: Scenario,
        max_turns: int = None
    ) -> ConversationResult:
        """
        Run a complete conversation for a scenario
        
        Args:
            scenario: Test scenario
            max_turns: Maximum conversation turns (overrides scenario)
            
        Returns:
            ConversationResult with full conversation
        """
        max_turns = max_turns or scenario.max_turns
        
        # Reset both agent and customer
        self.agent.reset_conversation()
        self.customer_simulator.reset()
        
        turns: List[ConversationTurn] = []
        total_tokens = 0
        total_latency = 0.0
        
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"🎬 بدء المحادثة: {scenario.title}")
            print(f"📋 السيناريو: {scenario.description}")
            print(f"👤 العميل: {scenario.customer_persona.name} ({scenario.customer_persona.personality})")
            print(f"🤖 الوكيل: {self.agent.agent_name} ({self.agent_model.model_name})")
            print(f"{'='*80}\n")
        
        # Generate initial customer message
        if self.verbose:
            print("🔄 توليد الرسالة الأولية للعميل...")
        
        customer_message = self.customer_simulator.generate_initial_message(
            persona=scenario.customer_persona,
            goal=scenario.customer_goal,
            context=scenario.initial_context
        )
        
        if not customer_message:
            return ConversationResult(
                scenario_id=scenario.scenario_id,
                agent_type=scenario.agent_type,
                model_name=self.agent_model.model_name,
                turns=[],
                total_turns=0,
                success=False,
                end_reason="Failed to generate initial customer message",
                total_tokens=0,
                total_latency=0.0
            )
        
        # Start conversation loop
        for turn_num in range(1, max_turns + 1):
            turn_start = time.time()
            
            if self.verbose:
                print(f"\n--- الدورة {turn_num} ---")
                print(f"👤 العميل: {customer_message}")
            
            # Get agent response
            agent_result = self.agent_model.generate_response(
                system_prompt=self.agent.get_system_prompt(),
                conversation_history=self.agent.get_conversation_history(),
                user_message=customer_message,
                temperature=0.7,
                max_tokens=800
            )
            
            if agent_result["error"]:
                if self.verbose:
                    print(f"❌ خطأ في الوكيل: {agent_result['error']}")
                return ConversationResult(
                    scenario_id=scenario.scenario_id,
                    agent_type=scenario.agent_type,
                    model_name=self.agent_model.model_name,
                    turns=turns,
                    total_turns=turn_num - 1,
                    success=False,
                    end_reason=f"Agent error: {agent_result['error']}",
                    total_tokens=total_tokens,
                    total_latency=total_latency
                )
            
            agent_message = agent_result["response"]
            agent_tokens = agent_result["tokens_used"]
            
            if self.verbose:
                print(f"🤖 {self.agent.agent_name}: {agent_message}")
            
            # Add to agent's history
            self.agent.add_to_history("user", customer_message)
            self.agent.add_to_history("assistant", agent_message)
            
            # Get customer response
            customer_result = self.customer_simulator.generate_response(
                persona=scenario.customer_persona,
                goal=scenario.customer_goal,
                context=scenario.initial_context,
                agent_message=agent_message,
                turn_number=turn_num,
                max_turns=max_turns
            )
            
            if customer_result["error"]:
                if self.verbose:
                    print(f"❌ خطأ في العميل: {customer_result['error']}")
                return ConversationResult(
                    scenario_id=scenario.scenario_id,
                    agent_type=scenario.agent_type,
                    model_name=self.agent_model.model_name,
                    turns=turns,
                    total_turns=turn_num,
                    success=False,
                    end_reason=f"Customer error: {customer_result['error']}",
                    total_tokens=total_tokens,
                    total_latency=total_latency
                )
            
            customer_tokens = customer_result["tokens_used"]
            turn_latency = time.time() - turn_start
            
            # Record turn
            turns.append(ConversationTurn(
                turn_number=turn_num,
                customer_message=customer_message,
                agent_message=agent_message,
                customer_tokens=customer_tokens,
                agent_tokens=agent_tokens,
                turn_latency=turn_latency
            ))
            
            total_tokens += agent_tokens + customer_tokens
            total_latency += turn_latency
            
            # Check if conversation should end
            if customer_result["should_end"]:
                if self.verbose:
                    print(f"\n✅ انتهت المحادثة: العميل راضي/أنهى المحادثة")
                return ConversationResult(
                    scenario_id=scenario.scenario_id,
                    agent_type=scenario.agent_type,
                    model_name=self.agent_model.model_name,
                    turns=turns,
                    total_turns=turn_num,
                    success=True,
                    end_reason="Customer ended conversation naturally",
                    total_tokens=total_tokens,
                    total_latency=total_latency
                )
            
            # Update customer message for next turn
            customer_message = customer_result["response"]
            
            if not customer_message:
                if self.verbose:
                    print(f"\n⚠️ انتهت المحادثة: لم يتم توليد رسالة عميل")
                return ConversationResult(
                    scenario_id=scenario.scenario_id,
                    agent_type=scenario.agent_type,
                    model_name=self.agent_model.model_name,
                    turns=turns,
                    total_turns=turn_num,
                    success=False,
                    end_reason="Customer stopped responding",
                    total_tokens=total_tokens,
                    total_latency=total_latency
                )
        
        # Max turns reached
        if self.verbose:
            print(f"\n⏱️ انتهت المحادثة: وصلت للحد الأقصى من الدورات ({max_turns})")
        
        return ConversationResult(
            scenario_id=scenario.scenario_id,
            agent_type=scenario.agent_type,
            model_name=self.agent_model.model_name,
            turns=turns,
            total_turns=max_turns,
            success=True,
            end_reason="Max turns reached",
            total_tokens=total_tokens,
            total_latency=total_latency
        )
    
    def print_summary(self, result: ConversationResult):
        """Print conversation summary"""
        print(f"\n{'='*80}")
        print(f"📊 ملخص المحادثة")
        print(f"{'='*80}")
        print(f"السيناريو: {result.scenario_id}")
        print(f"النموذج: {result.model_name}")
        print(f"عدد الدورات: {result.total_turns}")
        print(f"النجاح: {'✅' if result.success else '❌'}")
        print(f"سبب الانتهاء: {result.end_reason}")
        print(f"إجمالي Tokens: {result.total_tokens:,}")
        print(f"إجمالي الوقت: {result.total_latency:.2f} ثانية")
        if result.total_turns > 0:
            print(f"متوسط الوقت/دورة: {result.total_latency/result.total_turns:.2f} ثانية")
        print(f"{'='*80}\n")

