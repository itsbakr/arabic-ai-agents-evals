#!/usr/bin/env python3
"""
Full Evaluation Pipeline for Arabic Customer Service Agents

Runs all scenarios across all models and generates comprehensive benchmarks.
"""

import os
import time
import json
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# Import core modules
import config
from models.gemini_client import GeminiClient
from models.claude_client import ClaudeClient
from models.weave_client import WeaveClient
from agents.agent_a_ecommerce import AgentA_Ecommerce
from scenarios.scenario_loader import load_scenarios_for_agent
from simulator.customer_simulator import CustomerSimulator
from orchestrator import ConversationOrchestrator
from storage.results_storage import get_storage
from utils.weave_init import initialize_weave, get_weave_status

load_dotenv()


class EvaluationPipeline:
    """Main evaluation pipeline to test all scenarios across all models"""
    
    def __init__(self):
        """Initialize the evaluation pipeline"""
        self.results_dir = config.RESULTS_DIR
        self.models = self._initialize_models()
        self.agent_types = ["agent_a"]  # Can expand to agent_b, agent_c later
        
        # Initialize storage (fallback to JSON if Supabase not configured)
        try:
            self.storage = get_storage(config.STORAGE_MODE)
            print(f"✅ Storage mode: {config.STORAGE_MODE}")
        except Exception as e:
            print(f"⚠️  Supabase not configured, using JSON storage: {e}")
            self.storage = get_storage("json")
        
        self.all_results = []
        
        # Initialize Weave tracing
        if config.ENABLE_WEAVE_TRACING:
            initialize_weave()
            print(f"✅ Weave tracing initialized: {get_weave_status()}")
        else:
            print("⚠️  Weave tracing disabled")
    
    def _initialize_models(self) -> Dict:
        """Initialize all available LLM models"""
        models = {}
        
        # Gemini (with English prompts for safety filter compatibility)
        if config.GOOGLE_API_KEY:
            try:
                models["gemini"] = {
                    "client": GeminiClient(
                        api_key=config.GOOGLE_API_KEY,
                        model_name=config.MODELS_CONFIG["gemini"]["name"]
                    ),
                    "name": config.MODELS_CONFIG["gemini"]["name"],
                    "language_mode": "english"  # Use English prompts
                }
                print(f"✅ Gemini initialized: {models['gemini']['name']}")
            except Exception as e:
                print(f"❌ Gemini init failed: {e}")
        
        # Claude
        if config.ANTHROPIC_API_KEY:
            try:
                models["claude"] = {
                    "client": ClaudeClient(
                        api_key=config.ANTHROPIC_API_KEY,
                        model_name=config.MODELS_CONFIG["claude"]["name"]
                    ),
                    "name": config.MODELS_CONFIG["claude"]["name"],
                    "language_mode": "arabic"  # Use Arabic prompts
                }
                print(f"✅ Claude initialized: {models['claude']['name']}")
            except Exception as e:
                print(f"❌ Claude init failed: {e}")
        
        # Weave/OpenAI GPT OSS
        if config.WANDB_API_KEY:
            try:
                models["openai_gpt"] = {
                    "client": WeaveClient(
                        api_key=config.WANDB_API_KEY,
                        model_name=config.MODELS_CONFIG["qwen"]["name"]
                    ),
                    "name": config.MODELS_CONFIG["qwen"]["name"],
                    "language_mode": "arabic"  # Use Arabic prompts
                }
                print(f"✅ OpenAI GPT OSS initialized: {models['openai_gpt']['name']}")
            except Exception as e:
                print(f"❌ OpenAI GPT OSS init failed: {e}")
        
        return models
    
    def run_evaluation(
        self,
        agent_types: List[str] = None,
        model_names: List[str] = None,
        max_turns: int = 10,
        temperature: float = 0.7
    ) -> Dict:
        """
        Run full evaluation pipeline
        
        Args:
            agent_types: List of agent types to test (default: all)
            model_names: List of models to test (default: all)
            max_turns: Maximum conversation turns
            temperature: LLM temperature
            
        Returns:
            Aggregated results dictionary
        """
        print("="*80)
        print("STARTING FULL EVALUATION PIPELINE")
        print("="*80)
        
        agent_types = agent_types or self.agent_types
        model_names = model_names or list(self.models.keys())
        
        print(f"📊 Agent Types: {agent_types}")
        print(f"🤖 Models: {model_names}")
        print(f"🔄 Max Turns: {max_turns}")
        print(f"🌡️  Temperature: {temperature}")
        print("="*80)
        
        start_time = time.time()
        total_tests = 0
        successful_tests = 0
        failed_tests = 0
        
        for agent_type in agent_types:
            print(f"\n{'='*80}")
            print(f"TESTING AGENT: {agent_type.upper()}")
            print(f"{'='*80}")
            
            # Load scenarios
            scenarios = load_scenarios_for_agent(agent_type)
            print(f"📚 Loaded {len(scenarios)} scenarios")
            
            for model_key in model_names:
                if model_key not in self.models:
                    print(f"⚠️  Skipping unavailable model: {model_key}")
                    continue
                
                model_info = self.models[model_key]
                print(f"\n{'-'*80}")
                print(f"🤖 Testing with: {model_info['name']}")
                print(f"   Language mode: {model_info['language_mode']}")
                print(f"{'-'*80}")
                
                for idx, scenario in enumerate(scenarios):
                    total_tests += 1
                    print(f"\n[{idx+1}/{len(scenarios)}] Scenario: {scenario.title}")
                    
                    try:
                        result = self._run_single_test(
                            agent_type=agent_type,
                            scenario=scenario,
                            model_key=model_key,
                            model_info=model_info,
                            max_turns=max_turns,
                            temperature=temperature
                        )
                        
                        if result["success"]:
                            successful_tests += 1
                            print(f"   ✅ Success: {result['total_turns']} turns, "
                                  f"{result['total_tokens']} tokens, "
                                  f"{result['total_time']:.2f}s")
                        else:
                            failed_tests += 1
                            print(f"   ❌ Failed: {result.get('finish_reason', 'Unknown error')}")
                        
                        self.all_results.append(result)
                        
                    except Exception as e:
                        failed_tests += 1
                        print(f"   ❌ Exception: {e}")
                        self.all_results.append({
                            "agent_type": agent_type,
                            "scenario_id": scenario.scenario_id,
                            "model_key": model_key,
                            "model_name": model_info["name"],
                            "success": False,
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        })
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*80}")
        print("EVALUATION COMPLETE")
        print(f"{'='*80}")
        print(f"⏱️  Total Time: {elapsed_time:.2f}s")
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(successful_tests/total_tests*100):.1f}%")
        print(f"{'='*80}")
        
        # Generate and save benchmark report
        benchmark = self._generate_benchmark()
        self._save_benchmark(benchmark)
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "elapsed_time": elapsed_time,
            "results": self.all_results,
            "benchmark": benchmark
        }
    
    def _run_single_test(
        self,
        agent_type: str,
        scenario,
        model_key: str,
        model_info: Dict,
        max_turns: int,
        temperature: float
    ) -> Dict:
        """Run a single test scenario"""
        
        # Initialize agent with appropriate language mode
        language_mode = model_info["language_mode"]
        agent = AgentA_Ecommerce(language=language_mode)
        
        # Initialize customer simulator
        customer_model = model_info["client"]
        customer_simulator = CustomerSimulator(customer_model)
        
        # Initialize agent model (same as customer for now)
        agent_model = model_info["client"]
        
        # Run conversation
        orchestrator = ConversationOrchestrator(
            agent=agent,
            agent_model=agent_model,
            customer_simulator=customer_simulator
        )
        
        result = orchestrator.run_conversation(
            scenario=scenario,
            max_turns=max_turns
        )
        
        # Add metadata to result
        conversation_id = f"{scenario.scenario_id}_{model_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Convert result to dict and add metadata
        result_dict = result.to_dict() if hasattr(result, 'to_dict') else result
        result_dict["agent_type"] = agent_type
        result_dict["model_key"] = model_key
        result_dict["model_name"] = model_info["name"]
        result_dict["language_mode"] = language_mode
        result_dict["timestamp"] = datetime.now().isoformat()
        result_dict["conversation_id"] = conversation_id
        
        # Save conversation results
        try:
            self.storage.save_conversation(result_dict)
        except Exception as e:
            print(f"   ⚠️  Failed to save conversation: {e}")
        
        return result_dict
    
    def _generate_benchmark(self) -> Dict:
        """Generate benchmark metrics from all results"""
        
        benchmark = {
            "generated_at": datetime.now().isoformat(),
            "total_tests": len(self.all_results),
            "by_model": {},
            "by_agent": {},
            "by_scenario_complexity": {},
            "overall_metrics": {
                "avg_turns": 0,
                "avg_tokens": 0,
                "avg_time": 0,
                "avg_tokens_per_turn": 0,
                "success_rate": 0
            }
        }
        
        # Group results by model
        model_groups = {}
        for result in self.all_results:
            model_name = result.get("model_name", "unknown")
            if model_name not in model_groups:
                model_groups[model_name] = []
            model_groups[model_name].append(result)
        
        # Calculate per-model metrics
        for model_name, results in model_groups.items():
            successful = [r for r in results if r.get("success", False)]
            
            if successful:
                benchmark["by_model"][model_name] = {
                    "total_tests": len(results),
                    "successful_tests": len(successful),
                    "failed_tests": len(results) - len(successful),
                    "success_rate": len(successful) / len(results) * 100,
                    "avg_turns": sum(r.get("total_turns", 0) for r in successful) / len(successful),
                    "avg_tokens": sum(r.get("total_tokens", 0) for r in successful) / len(successful),
                    "avg_time": sum(r.get("total_time", 0) for r in successful) / len(successful),
                    "avg_tokens_per_turn": sum(r.get("avg_tokens_per_turn", 0) for r in successful) / len(successful),
                }
        
        # Calculate overall metrics
        successful_all = [r for r in self.all_results if r.get("success", False)]
        if successful_all:
            benchmark["overall_metrics"] = {
                "avg_turns": sum(r.get("total_turns", 0) for r in successful_all) / len(successful_all),
                "avg_tokens": sum(r.get("total_tokens", 0) for r in successful_all) / len(successful_all),
                "avg_time": sum(r.get("total_time", 0) for r in successful_all) / len(successful_all),
                "avg_tokens_per_turn": sum(r.get("avg_tokens_per_turn", 0) for r in successful_all) / len(successful_all),
                "success_rate": len(successful_all) / len(self.all_results) * 100
            }
        
        return benchmark
    
    def _save_benchmark(self, benchmark: Dict):
        """Save benchmark report to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_report_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(benchmark, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Benchmark saved: {filepath}")
        
        # Print summary table
        self._print_benchmark_table(benchmark)
    
    def _print_benchmark_table(self, benchmark: Dict):
        """Print benchmark results in a nice table format"""
        
        print(f"\n{'='*80}")
        print("BENCHMARK RESULTS")
        print(f"{'='*80}")
        
        print(f"\n{'Model':<30} {'Tests':<8} {'Success':<8} {'Turns':<8} {'Tokens':<10} {'Time (s)':<10}")
        print("-"*80)
        
        for model_name, metrics in benchmark["by_model"].items():
            print(f"{model_name:<30} "
                  f"{metrics['total_tests']:<8} "
                  f"{metrics['success_rate']:<7.1f}% "
                  f"{metrics['avg_turns']:<7.1f} "
                  f"{metrics['avg_tokens']:<9.0f} "
                  f"{metrics['avg_time']:<10.2f}")
        
        print("-"*80)
        overall = benchmark["overall_metrics"]
        print(f"{'OVERALL':<30} "
              f"{benchmark['total_tests']:<8} "
              f"{overall['success_rate']:<7.1f}% "
              f"{overall['avg_turns']:<7.1f} "
              f"{overall['avg_tokens']:<9.0f} "
              f"{overall['avg_time']:<10.2f}")
        
        print(f"{'='*80}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run full evaluation pipeline")
    parser.add_argument(
        "--agents",
        nargs="+",
        default=["agent_a"],
        help="Agent types to test (default: agent_a)"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=["gemini", "claude", "openai_gpt"],
        help="Models to test (default: all available)"
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=10,
        help="Maximum conversation turns (default: 10)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="LLM temperature (default: 0.7)"
    )
    
    args = parser.parse_args()
    
    pipeline = EvaluationPipeline()
    results = pipeline.run_evaluation(
        agent_types=args.agents,
        model_names=args.models,
        max_turns=args.max_turns,
        temperature=args.temperature
    )
    
    print("\n✅ Evaluation complete!")
    print(f"📊 Results saved to: {config.RESULTS_DIR}")
    print(f"🔍 View Weave traces at: https://wandb.ai/{config.WEAVE_PROJECT_NAME}/weave")


if __name__ == "__main__":
    main()

