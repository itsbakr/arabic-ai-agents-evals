# Arabic Customer Service AI Agents Evaluation Framework
# 🤖 إطار تقييم وكلاء خدمة العملاء بالذكاء الاصطناعي

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Weave](https://img.shields.io/badge/weave-tracing-orange.svg)](https://wandb.ai/site/weave)

A comprehensive LLM-to-LLM evaluation framework for testing Arabic customer service AI agents. Evaluates three agent types (E-commerce, Telecom, Banking) across 30 diverse scenarios using multiple LLM models with automated quality assessment.

---

## 🎯 Overview

This framework evaluates AI customer service agents through **realistic, multi-turn conversations** between:
- **👤 Customer Simulator**: LLM playing Egyptian customers with diverse personas
- **🤖 Service Agent**: LLM playing customer service representatives
- **⚖️ LLM-as-Judge**: Automated quality evaluation across 5 dimensions

### Key Features

✅ **30 Rich Arabic Scenarios** - Diverse, culturally-aware test cases  
✅ **3 Agent Types** - E-commerce, Telecom, Banking  
✅ **3 LLM Models** - Claude, Gemini, OpenAI GPT (via W&B)  
✅ **LLM-as-Judge Evaluation** - Automated scoring & feedback  
✅ **Weave Tracing** - Full observability for all LLM calls  
✅ **Multi-Storage** - JSON, CSV, and Supabase support  
✅ **Benchmarking** - Model performance comparison  
✅ **Production-Ready** - Complete testing pipeline  

---

## 📋 Agent Types & Scenarios

### 🛒 Agent A: E-commerce (10 scenarios)
Customer service for Egyptian online marketplace

1. **Late Delivery** - Urgent worker needs phone for meeting
2. **Wrong Product** - Bride received wrong dress, wedding soon
3. **Ramadan Timing** - Father ordering Eid gifts with concerns
4. **Laptop Refund** - Tech-savvy student demanding refund
5. **Address Change** - Customer moved after order shipped
6. **Large COD Order** - Worried about cash-on-delivery limits
7. **Damaged Product** - Angry customer received broken TV
8. **Elderly Customer** - First-time user needs simple help
9. **Promotion Confusion** - Discount code not working
10. **Multiple Orders** - Customer confused about 3 orders

### 📱 Agent B: Telecom (10 scenarios)
Technical support for Egyptian telecommunications

1. **Slow Internet** - Remote worker with critical need
2. **High Bill** - Customer shocked by unexpected charges
3. **SIM Activation** - New SIM not working before interview
4. **Package Upgrade** - Sales employee needs more data
5. **No Coverage** - New area with weak signal
6. **Roaming Confusion** - Traveling abroad, worried about costs
7. **Lost Phone** - Stolen phone, needs line blocked urgently
8. **Contract Cancellation** - Moving abroad permanently
9. **Data Not Working** - Student needs internet for exam
10. **Elderly Inquiry** - Senior citizen checking balance

### 🏦 Agent C: Banking (10 scenarios)
Account support for Egyptian bank customers

1. **Stolen Card** - Suspicious transactions, urgent block
2. **Online Banking Locked** - Forgot password, needs access
3. **Loan Inquiry** - First-time borrower, wants car loan
4. **Transaction Dispute** - Unknown charge on account
5. **New Account** - Fresh graduate opening first account
6. **ATM Card Stuck** - Card swallowed, needs cash urgently
7. **Savings Interest** - Teacher planning for kids' education
8. **International Transfer** - Mother sending money abroad
9. **Mobile Banking Setup** - Programmer wants app access
10. **Pension Inquiry** - Elderly customer about retirement

---

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to project directory
cd "AI Arabic Evals"

# Install dependencies
pip install -r requirements.txt
```

**Dependencies:**
- `anthropic` - Claude API
- `google-generativeai` - Gemini API
- `openai` - OpenAI/W&B Inference API
- `weave` - Weights & Biases tracing
- `supabase` - Database storage (optional)
- `pandas` - Data analysis
- `python-dotenv` - Environment management

### 2. Configuration

Create `.env` file with your API keys:

```bash
# LLM API Keys
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
WANDB_API_KEY=your_wandb_api_key

# Weave Tracing
WEAVE_PROJECT_NAME=your-entity/your-project
ENABLE_WEAVE_TRACING=true

# Storage Configuration
STORAGE_MODE=json  # Options: json, csv, supabase, or both
SUPABASE_URL=your_supabase_url  # Optional
SUPABASE_KEY=your_supabase_key  # Optional

# Results Directory
RESULTS_DIR=results
LOGS_DIR=logs
```

### 3. Quick Test

Test a single scenario:

```bash
# Test with Claude (recommended)
python3 test_demo.py --scenario 0 --model claude

# Test with Gemini
python3 test_demo.py --scenario 0 --model gemini

# Test with OpenAI GPT OSS
python3 test_demo.py --scenario 0 --model qwen
```

---

## 🎬 Usage

### Run Full Evaluation Pipeline

Evaluate all scenarios across models:

```bash
# Run all Agent A scenarios with Claude (3 turns each)
python3 run_full_evaluation.py --agents agent_a --models claude --max-turns 3

# Run with all models
python3 run_full_evaluation.py --models claude gemini openai_gpt --max-turns 5

# Run specific agents only
python3 run_full_evaluation.py --agents agent_a agent_b --models claude --max-turns 5

# Full benchmark (all agents, all models)
python3 run_full_evaluation.py --max-turns 5
```

**Output:**
- Conversation logs (JSON)
- Performance benchmarks
- Token usage & latency metrics
- Success rates per model

### Run LLM-as-Judge Evaluation

Automatically evaluate conversations:

```bash
# Evaluate all conversations with Claude as judge
python3 run_evaluation.py --judge-model claude

# Evaluate with Gemini as judge
python3 run_evaluation.py --judge-model gemini

# Use Arabic evaluation prompts
python3 run_evaluation.py --judge-model claude --language arabic

# Evaluate limited number for testing
python3 run_evaluation.py --limit 10
```

**Evaluation Metrics (0-10 scale):**
- **Task Completion** - Did the agent solve the problem?
- **Empathy** - Did the agent show understanding?
- **Clarity** - Were responses clear and understandable?
- **Cultural Fit** - Appropriate for Egyptian context?
- **Problem Solving** - Quality of solutions offered

---

## 📊 Project Structure

```
AI Arabic Evals/
├── agents/                        # Agent implementations
│   ├── base_agent.py             # Base agent class
│   ├── agent_a_ecommerce.py      # E-commerce agent (Arabic & English)
│   ├── agent_b_telecom.py        # Telecom agent
│   └── agent_c_banking.py        # Banking agent
│
├── scenarios/                     # Test scenarios
│   ├── scenario_loader.py        # Scenario loading utilities
│   ├── agent_a_scenarios.py      # 10 e-commerce scenarios ✅
│   ├── agent_b_scenarios.py      # 10 telecom scenarios ✅
│   └── agent_c_scenarios.py      # 10 banking scenarios ✅
│
├── models/                        # LLM client wrappers
│   ├── base_model.py             # Base model interface
│   ├── claude_client.py          # Anthropic Claude
│   ├── gemini_client.py          # Google Gemini
│   └── weave_client.py           # W&B Inference (OpenAI GPT OSS)
│
├── simulator/                     # Customer simulation
│   └── customer_simulator.py     # Dynamic customer persona simulator
│
├── evaluator/                     # LLM-as-Judge evaluation ⭐
│   ├── __init__.py
│   └── llm_judge.py              # Automated quality assessment
│
├── storage/                       # Results storage
│   └── results_storage.py        # JSON, CSV, Supabase support
│
├── utils/                         # Utilities
│   └── weave_init.py             # Weave tracing initialization
│
├── orchestrator.py                # Conversation orchestration
├── config.py                      # Central configuration
│
├── run_full_evaluation.py         # 🎯 Main testing pipeline
├── run_evaluation.py              # ⚖️ LLM judge evaluation
├── test_demo.py                   # Quick single scenario test
├── test_wandb_inference.py        # W&B diagnostics
│
├── results/                       # Output directory
│   ├── conversations.json        # All conversation logs
│   ├── benchmark_*.json          # Performance benchmarks
│   └── evaluation_*.json         # LLM judge results
│
└── requirements.txt               # Python dependencies
```

---

## 🤖 Supported Models

### 1. Claude 3.5 Haiku (Anthropic)
- **Status**: ✅ Fully working
- **Performance**: Excellent with Arabic
- **Best for**: Production use, most reliable

```python
# Configuration
ANTHROPIC_API_KEY=your_key
model_name: "claude-3-5-haiku-20241022"
```

### 2. Gemini Flash Latest (Google)
- **Status**: ✅ Working (with workaround)
- **Performance**: Good, uses English prompts → Arabic output
- **Note**: Safety filters addressed with system instructions

```python
# Configuration
GOOGLE_API_KEY=your_key
model_name: "gemini-flash-latest"
```

### 3. OpenAI GPT OSS 20B (W&B Inference)
- **Status**: ✅ Working
- **Performance**: Good for open-source model
- **Access**: Via Weights & Biases Inference

```python
# Configuration
WANDB_API_KEY=your_key
model_name: "openai/gpt-oss-20b"
```

---

## 📈 Results & Benchmarking

### Sample Benchmark Output

```json
{
  "by_model": {
    "claude-3-5-haiku-20241022": {
      "total_tests": 10,
      "successful_tests": 10,
      "success_rate": 100.0,
      "avg_turns": 6.2,
      "avg_tokens": 1234,
      "avg_time": 12.5
    }
  },
  "overall_metrics": {
    "avg_turns": 5.8,
    "avg_tokens": 1150,
    "avg_time": 11.2,
    "success_rate": 93.3
  }
}
```

### Sample Evaluation Output

```json
{
  "conversation_id": "A1_late_delivery_claude_20251028_120000",
  "overall_score": 8.5,
  "scores": {
    "task_completion": 9.0,
    "empathy": 8.5,
    "clarity": 9.0,
    "cultural_fit": 8.0,
    "problem_solving": 8.0
  },
  "strengths": [
    "Excellent empathy with urgent situation",
    "Clear communication about delivery status",
    "Proactive solution with escalation"
  ],
  "weaknesses": [
    "Could have offered compensation sooner"
  ]
}
```

### View Results

```bash
# View latest benchmark
cat results/benchmark_report_*.json | jq

# View evaluation results
cat results/evaluation_results_*.json | jq

# View Weave traces
open "https://wandb.ai/your-entity/your-project/weave"
```

---

## 🔍 Weave Tracing

All LLM calls are automatically traced in Weights & Biases:

- **Customer messages** - Persona-driven generation
- **Agent responses** - Model outputs with context
- **Evaluations** - LLM judge assessments
- **Metrics** - Tokens, latency, costs

**Access traces:**
```
https://wandb.ai/{your-entity}/{your-project}/weave
```

**Features:**
- Real-time monitoring
- Cost tracking
- Performance analysis
- Debugging support

---

## 🐛 Troubleshooting

### Gemini Safety Filters

**Issue**: `finish_reason: 2` (SAFETY block)

**Solution**: ✅ Already fixed!
- Uses English prompts with explicit instructions to respond in Arabic
- Safety settings configured to `BLOCK_NONE`
- System instruction provides research context

**If still issues**: Use Claude instead (most reliable)

### W&B Inference Errors

**Issue**: "Malformed token" or "Resource not found"

**Solutions**:
1. Verify `WANDB_API_KEY` is set correctly
2. Check project name: `WEAVE_PROJECT_NAME=entity/project`
3. Use correct model names: `openai/gpt-oss-20b`
4. Ensure W&B account has inference access

**Diagnostic script**:
```bash
python3 test_wandb_inference.py
```

### Storage Errors

**Issue**: Supabase connection failures

**Solution**:
```bash
# Use JSON storage for testing
STORAGE_MODE=json

# Or create Supabase tables (see documentation)
```

### No Results Showing

**Check**:
```bash
# Ensure results directory exists
mkdir -p results

# Check file permissions
ls -la results/

# Verify .env configuration
cat .env
```

---

## 📚 Documentation

Detailed guides available:

- **Setup Guide**: Environment configuration
- **Usage Examples**: Common workflows
- **Model Comparison**: Performance analysis
- **API Reference**: Code documentation
- **Best Practices**: Testing recommendations

---

## 🎯 Use Cases

### Research & Publication
- Evaluate Arabic LLM capabilities
- Compare model performance
- Analyze cultural appropriateness
- Generate publication-ready data

### Product Development
- Test customer service chatbots
- Benchmark agent implementations
- Identify improvement areas
- A/B test different approaches

### Quality Assurance
- Automated agent testing
- Regression testing for updates
- Performance monitoring
- Compliance validation

---

## 📊 Evaluation Methodology

### LLM-to-LLM Testing
1. **Customer Simulator** generates realistic queries
2. **Agent** responds with solutions
3. **Conversation** continues naturally (up to 10 turns)
4. **Results** captured with full tracing

### Automated Evaluation
1. **LLM Judge** analyzes conversation
2. **Scores** assigned across 5 dimensions
3. **Feedback** generated (strengths, weaknesses)
4. **Validation** against success criteria

### Metrics Calculated
- Task completion rate
- Average conversation turns
- Token usage per conversation
- Response latency
- Quality scores by dimension
- Model comparison statistics

---

## 🤝 Contributing

We welcome contributions!

**Add scenarios**:
- Edit `scenarios/agent_*_scenarios.py`
- Follow existing pattern
- Include persona and success criteria

**Add models**:
- Create client in `models/`
- Implement `BaseModel` interface
- Add to `config.py`

**Improve evaluation**:
- Modify `evaluator/llm_judge.py`
- Add new metrics
- Enhance prompts

---

## 🚀 Getting Started Checklist

- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Configure `.env` with API keys
- [ ] Run quick test (`python3 test_demo.py --scenario 0 --model claude`)
- [ ] Run full evaluation (`python3 run_full_evaluation.py --models claude --max-turns 3`)
- [ ] Evaluate with LLM judge (`python3 run_evaluation.py`)
- [ ] View results (`cat results/benchmark_*.json`)
- [ ] Check Weave traces (open W&B link)

---

**Built with ❤️ for evaluating Arabic AI customer service agents**

**Ready to test? Let's go! 🚀**

```bash
# Start your evaluation now:
python3 test_demo.py --scenario 0 --model claude
```
