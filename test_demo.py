"""
Demo test script for Agent A scenarios
Run this to test the LLM-to-LLM conversation system
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.agent_a_ecommerce import AgentA_Ecommerce
from models.gemini_client import GeminiClient
from models.claude_client import ClaudeClient
from models.weave_client import WeaveClient
from simulator.customer_simulator import CustomerSimulator
from scenarios.agent_a_scenarios import get_agent_a_scenarios
from orchestrator import ConversationOrchestrator
from storage.results_storage import get_storage
from utils.weave_init import initialize_weave, get_weave_status
import config


def test_scenario(scenario_index: int = 0, agent_model: str = "gemini"):
    """
    Test a specific scenario
    
    Args:
        scenario_index: Index of scenario to test (0-9)
        agent_model: Model to use for agent ('gemini', 'claude', or 'qwen')
    """
    
    print(f"\n{'#'*80}")
    print(f"# اختبار نظام المحادثة LLM-to-LLM")
    print(f"{'#'*80}\n")
    
    # Initialize Weave tracing
    print("📊 تهيئة Weave Tracing...")
    initialize_weave()
    weave_status = get_weave_status()
    if weave_status["initialized"]:
        print(f"   ✅ Weave متصل: {weave_status['project']}")
    else:
        print(f"   ⚠️ Weave غير متاح (الاختبار سيستمر بدون tracing)")
    print()
    
    # Check API keys
    if not config.GOOGLE_API_KEY:
        print("❌ خطأ: يرجى إضافة GOOGLE_API_KEY في ملف .env")
        print("مثال: GOOGLE_API_KEY=your_key_here")
        return
    
    # Load scenarios
    print("📚 تحميل السيناريوهات...")
    scenarios = get_agent_a_scenarios()
    print(f"✅ تم تحميل {len(scenarios)} سيناريو\n")
    
    # Select scenario
    if scenario_index >= len(scenarios):
        print(f"❌ خطأ: رقم السيناريو {scenario_index} غير موجود (0-{len(scenarios)-1})")
        return
    
    scenario = scenarios[scenario_index]
    
    print(f"🎯 السيناريو المختار:")
    print(f"   ID: {scenario.scenario_id}")
    print(f"   العنوان: {scenario.title}")
    print(f"   الوصف: {scenario.description}")
    print(f"   التعقيد: {scenario.complexity}")
    print(f"   الشخصية: {scenario.customer_persona.name} - {scenario.customer_persona.personality}")
    print(f"   الهدف: {scenario.customer_goal}\n")
    
    # Initialize models
    print(f"🤖 تهيئة النماذج...")
    
    # Customer simulator - use same model as agent for consistency
    if agent_model == "gemini":
        customer_model = GeminiClient(
            api_key=config.GOOGLE_API_KEY,
            model_name=config.MODELS_CONFIG["gemini"]["name"]
        )
        print(f"   ✅ نموذج العميل: {config.MODELS_CONFIG['gemini']['name']}")
    elif agent_model == "claude":
        customer_model = ClaudeClient(
            api_key=config.ANTHROPIC_API_KEY,
            model_name=config.MODELS_CONFIG["claude"]["name"]
        )
        print(f"   ✅ نموذج العميل: {config.MODELS_CONFIG['claude']['name']}")
    elif agent_model == "qwen":
        customer_model = WeaveClient(
            api_key=config.WEAVE_API_KEY,
            model_name=config.MODELS_CONFIG["qwen"]["name"]
        )
        print(f"   ✅ نموذج العميل: {config.MODELS_CONFIG['qwen']['name']}")
    else:
        print(f"   ❌ خطأ: نموذج غير مدعوم: {agent_model}")
        return
    
    # Agent model
    if agent_model == "gemini":
        agent_llm = GeminiClient(
            api_key=config.GOOGLE_API_KEY,
            model_name=config.MODELS_CONFIG["gemini"]["name"]
        )
        print(f"   ✅ نموذج الوكيل: {config.MODELS_CONFIG['gemini']['name']}")
    elif agent_model == "claude":
        if not config.ANTHROPIC_API_KEY:
            print("   ❌ خطأ: Claude يحتاج ANTHROPIC_API_KEY")
            return
        agent_llm = ClaudeClient(
            api_key=config.ANTHROPIC_API_KEY,
            model_name=config.MODELS_CONFIG["claude"]["name"]
        )
        print(f"   ✅ نموذج الوكيل: {config.MODELS_CONFIG['claude']['name']}")
    elif agent_model == "qwen":
        agent_llm = WeaveClient(
            api_key=config.WEAVE_API_KEY,
            model_name=config.MODELS_CONFIG["qwen"]["name"]
        )
        print(f"   ✅ نموذج الوكيل: {config.MODELS_CONFIG['qwen']['name']}")
    else:
        print(f"   ❌ خطأ: نموذج غير مدعوم: {agent_model}")
        return
    
    # Initialize agent
    agent = AgentA_Ecommerce(language="arabic")
    print(f"   ✅ الوكيل: {agent.agent_name}\n")
    
    # Initialize customer simulator
    customer_sim = CustomerSimulator(model=customer_model, language="arabic")
    
    # Create orchestrator
    orchestrator = ConversationOrchestrator(
        agent=agent,
        agent_model=agent_llm,
        customer_simulator=customer_sim,
        verbose=True
    )
    
    # Initialize storage
    print("💾 تهيئة نظام التخزين...")
    try:
        storage = get_storage(
            storage_mode=config.STORAGE_MODE,
            output_dir="results",
            supabase_url=config.SUPABASE_URL,
            supabase_key=config.SUPABASE_KEY
        )
        print(f"   ✅ وضع التخزين: {config.STORAGE_MODE}\n")
    except Exception as e:
        print(f"   ⚠️ تحذير: {e}")
        print("   📝 سيتم الحفظ في CSV فقط\n")
        storage = get_storage(storage_mode="csv", output_dir="results")
    
    # Run conversation
    print("🚀 بدء المحادثة...\n")
    result = orchestrator.run_conversation(scenario)
    
    # Print summary
    orchestrator.print_summary(result)
    
    # Save results
    print("💾 حفظ النتائج...")
    conversation_data = result.to_dict()
    conversation_data['customer_persona'] = scenario.customer_persona.name
    conversation_data['customer_goal'] = scenario.customer_goal
    storage.save_conversation(conversation_data)
    print()
    
    # Print evaluation criteria
    print("📋 معايير التقييم المتوقعة:")
    for criterion, description in scenario.evaluation_dimensions.items():
        print(f"   • {criterion}: {description}")
    
    print("\n✅ معايير النجاح:")
    for criterion in scenario.success_criteria:
        print(f"   ✓ {criterion}")
    
    print("\n🚫 ممنوع:")
    for dont in scenario.must_not_do:
        print(f"   ✗ {dont}")
    
    print(f"\n{'#'*80}")
    print("# انتهى الاختبار")
    print(f"{'#'*80}\n")
    
    return result


def list_scenarios():
    """List all available scenarios"""
    scenarios = get_agent_a_scenarios()
    
    print(f"\n{'='*80}")
    print("📚 السيناريوهات المتاحة (Agent A - E-commerce)")
    print(f"{'='*80}\n")
    
    for i, scenario in enumerate(scenarios):
        print(f"{i}. {scenario.title}")
        print(f"   ID: {scenario.scenario_id}")
        print(f"   التعقيد: {scenario.complexity}")
        print(f"   الشخصية: {scenario.customer_persona.name} - {scenario.customer_persona.personality}")
        print()
    
    print(f"{'='*80}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="اختبار نظام المحادثة LLM-to-LLM")
    parser.add_argument(
        "--list",
        action="store_true",
        help="عرض قائمة السيناريوهات المتاحة"
    )
    parser.add_argument(
        "--scenario",
        type=int,
        default=0,
        help="رقم السيناريو للاختبار (0-9)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini",
        choices=["gemini", "claude", "qwen"],
        help="النموذج المستخدم للوكيل"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_scenarios()
    else:
        test_scenario(args.scenario, args.model)

