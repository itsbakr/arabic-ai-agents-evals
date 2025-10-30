#!/usr/bin/env python3
"""
Run LLM-based evaluation on conversation results

This script loads conversation results and evaluates them using an LLM judge.
"""

import os
import json
import glob
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

import config
from models.claude_client import ClaudeClient
from models.gemini_client import GeminiClient
from evaluator.llm_judge import LLMJudge
from scenarios.scenario_loader import load_scenarios_for_agent
from storage.results_storage import get_storage
from utils.weave_init import initialize_weave

load_dotenv()


def load_conversations_from_json(results_dir: str) -> List[Dict]:
    """Load conversations from JSON files"""
    
    conversations = []
    
    # Load from conversations.json
    conversations_file = os.path.join(results_dir, "conversations.json")
    if os.path.exists(conversations_file):
        try:
            with open(conversations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    conversations.extend(data)
                elif isinstance(data, dict) and 'conversations' in data:
                    conversations.extend(data['conversations'])
        except Exception as e:
            print(f"⚠️  Failed to load {conversations_file}: {e}")
    
    # Load from individual JSON files
    json_files = glob.glob(os.path.join(results_dir, "*_20*.json"))
    for json_file in json_files:
        if "benchmark" in json_file or "conversations.json" in json_file:
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                conversations.append(data)
        except Exception as e:
            print(f"⚠️  Failed to load {json_file}: {e}")
    
    return conversations


def load_scenarios() -> Dict[str, any]:
    """Load all scenarios and index by ID"""
    
    scenarios_map = {}
    
    for agent_type in ["agent_a", "agent_b", "agent_c"]:
        try:
            scenarios = load_scenarios_for_agent(agent_type)
            for scenario in scenarios:
                scenarios_map[scenario.scenario_id] = scenario
        except Exception as e:
            print(f"⚠️  Failed to load scenarios for {agent_type}: {e}")
    
    return scenarios_map


def save_evaluation_results(results: List, output_dir: str):
    """Save evaluation results to JSON"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"evaluation_results_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Convert results to dictionaries
    results_data = [r.to_dict() for r in results]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Evaluation results saved: {filepath}")
    
    return filepath


def print_evaluation_summary(results: List):
    """Print summary of evaluation results"""
    
    if not results:
        print("\n⚠️  No evaluation results to summarize")
        return
    
    print("\n" + "="*80)
    print("EVALUATION SUMMARY")
    print("="*80)
    
    # Overall statistics
    total = len(results)
    avg_overall = sum(r.overall_score for r in results) / total
    avg_task = sum(r.task_completion for r in results) / total
    avg_empathy = sum(r.empathy for r in results) / total
    avg_clarity = sum(r.clarity for r in results) / total
    avg_cultural = sum(r.cultural_fit for r in results) / total
    avg_problem = sum(r.problem_solving for r in results) / total
    
    print(f"\nTotal Conversations Evaluated: {total}")
    print(f"\nAverage Scores (0-10):")
    print(f"  Overall Score:     {avg_overall:.2f}")
    print(f"  Task Completion:   {avg_task:.2f}")
    print(f"  Empathy:           {avg_empathy:.2f}")
    print(f"  Clarity:           {avg_clarity:.2f}")
    print(f"  Cultural Fit:      {avg_cultural:.2f}")
    print(f"  Problem Solving:   {avg_problem:.2f}")
    
    # By model
    print(f"\n{'-'*80}")
    print("SCORES BY MODEL")
    print(f"{'-'*80}")
    
    models = {}
    for r in results:
        if r.model_name not in models:
            models[r.model_name] = []
        models[r.model_name].append(r)
    
    print(f"\n{'Model':<30} {'Count':<8} {'Overall':<10} {'Task':<8} {'Empathy':<10} {'Clarity':<8}")
    print("-"*80)
    
    for model_name, model_results in sorted(models.items()):
        count = len(model_results)
        avg_ov = sum(r.overall_score for r in model_results) / count
        avg_tk = sum(r.task_completion for r in model_results) / count
        avg_em = sum(r.empathy for r in model_results) / count
        avg_cl = sum(r.clarity for r in model_results) / count
        
        print(f"{model_name:<30} {count:<8} {avg_ov:<10.2f} {avg_tk:<8.2f} {avg_em:<10.2f} {avg_cl:<8.2f}")
    
    # Top performers
    print(f"\n{'-'*80}")
    print("TOP 5 CONVERSATIONS")
    print(f"{'-'*80}")
    
    top_5 = sorted(results, key=lambda r: r.overall_score, reverse=True)[:5]
    for i, r in enumerate(top_5, 1):
        print(f"\n{i}. {r.conversation_id}")
        print(f"   Model: {r.model_name}")
        print(f"   Scenario: {r.scenario_id}")
        print(f"   Overall Score: {r.overall_score:.2f}/10")
        print(f"   Top Strength: {r.strengths[0] if r.strengths else 'N/A'}")
    
    # Bottom performers
    print(f"\n{'-'*80}")
    print("BOTTOM 5 CONVERSATIONS (Need Improvement)")
    print(f"{'-'*80}")
    
    bottom_5 = sorted(results, key=lambda r: r.overall_score)[:5]
    for i, r in enumerate(bottom_5, 1):
        print(f"\n{i}. {r.conversation_id}")
        print(f"   Model: {r.model_name}")
        print(f"   Scenario: {r.scenario_id}")
        print(f"   Overall Score: {r.overall_score:.2f}/10")
        print(f"   Key Weakness: {r.weaknesses[0] if r.weaknesses else 'N/A'}")
    
    print("\n" + "="*80)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate conversations using LLM judge")
    parser.add_argument(
        "--results-dir",
        type=str,
        default=config.RESULTS_DIR,
        help="Directory containing conversation results"
    )
    parser.add_argument(
        "--judge-model",
        type=str,
        choices=["claude", "gemini"],
        default="claude",
        help="LLM to use as judge (default: claude)"
    )
    parser.add_argument(
        "--language",
        type=str,
        choices=["arabic", "english"],
        default="english",
        help="Language for evaluation prompts (default: english)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of conversations to evaluate"
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("LLM-AS-JUDGE EVALUATION")
    print("="*80)
    print(f"Results directory: {args.results_dir}")
    print(f"Judge model: {args.judge_model}")
    print(f"Evaluation language: {args.language}")
    print("="*80)
    
    # Initialize Weave tracing
    if config.ENABLE_WEAVE_TRACING:
        initialize_weave()
        print(f"✅ Weave tracing initialized")
    
    # Initialize judge model
    print(f"\n🤖 Initializing {args.judge_model} as judge...")
    
    if args.judge_model == "claude":
        if not config.ANTHROPIC_API_KEY:
            print("❌ Error: ANTHROPIC_API_KEY not found in environment")
            return
        judge_model = ClaudeClient(
            api_key=config.ANTHROPIC_API_KEY,
            model_name=config.MODELS_CONFIG["claude"]["name"]
        )
    elif args.judge_model == "gemini":
        if not config.GOOGLE_API_KEY:
            print("❌ Error: GOOGLE_API_KEY not found in environment")
            return
        judge_model = GeminiClient(
            api_key=config.GOOGLE_API_KEY,
            model_name=config.MODELS_CONFIG["gemini"]["name"]
        )
    else:
        print(f"❌ Error: Unknown judge model: {args.judge_model}")
        return
    
    print(f"✅ Judge model initialized")
    
    # Load conversations
    print(f"\n📚 Loading conversations from {args.results_dir}...")
    conversations = load_conversations_from_json(args.results_dir)
    
    if not conversations:
        print("❌ No conversations found to evaluate")
        return
    
    if args.limit:
        conversations = conversations[:args.limit]
    
    print(f"✅ Loaded {len(conversations)} conversations")
    
    # Load scenarios
    print(f"\n📋 Loading scenarios...")
    scenarios = load_scenarios()
    print(f"✅ Loaded {len(scenarios)} scenarios")
    
    # Initialize judge
    judge = LLMJudge(judge_model, language=args.language)
    
    # Run evaluation
    print(f"\n⚖️  Running evaluations...")
    print("="*80)
    
    results = judge.batch_evaluate(conversations, scenarios)
    
    print("="*80)
    print(f"✅ Evaluation complete! Evaluated {len(results)} conversations")
    
    # Save results
    output_file = save_evaluation_results(results, args.results_dir)
    
    # Print summary
    print_evaluation_summary(results)
    
    # Save to storage
    try:
        storage = get_storage(config.STORAGE_MODE)
        for result in results:
            storage.save_evaluation(result.to_dict())
        print(f"\n✅ Saved evaluations to {config.STORAGE_MODE} storage")
    except Exception as e:
        print(f"\n⚠️  Failed to save to storage: {e}")
    
    print(f"\n📊 Full results saved to: {output_file}")
    print(f"🔍 View traces at: https://wandb.ai/{config.WEAVE_PROJECT_NAME}/weave")


if __name__ == "__main__":
    main()

