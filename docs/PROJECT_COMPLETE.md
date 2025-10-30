# Arabic Customer Service AI Agents Evaluation Framework
## 🎉 PROJECT COMPLETE! 🎉

---

## 📊 Overview

A comprehensive evaluation framework for testing Arabic customer service AI agents using LLM-to-LLM interactions. The system evaluates three types of agents (E-commerce, Telecom, Banking) across 30 diverse scenarios using multiple LLM models.

---

## ✅ What We Built

### 1. **Three Agent Types with Dual Language Support**
- **Agent A: E-commerce** (`agents/agent_a_ecommerce.py`)
  - Handles orders, deliveries, returns, refunds
  - Arabic & English prompts (English for Gemini compatibility)
  
- **Agent B: Telecom** (`agents/agent_b_telecom.py`)
  - Handles internet issues, billing, packages, SIM cards
  
- **Agent C: Banking** (`agents/agent_c_banking.py`)
  - Handles accounts, cards, loans, transactions

### 2. **30 Rich Arabic Scenarios**
- **10 scenarios per agent** with diverse:
  - Customer personas (age, occupation, personality)
  - Complexity levels (simple, medium, high, critical)
  - Cultural contexts (Ramadan, Egyptian dialects, etc.)
  - Success criteria and evaluation dimensions

#### Agent A (E-commerce) Scenarios:
1. Late delivery - Urgent worker
2. Wrong product - Bride needs dress
3. Ramadan delivery timing
4. Laptop refund - University student
5. Address change after shipment
6. Large COD order concern
7. Damaged product - Angry customer
8. Elderly customer inquiry
9. Promotion confusion
10. Multiple order mix-up

#### Agent B (Telecom) Scenarios:
1. Slow internet - Remote worker
2. High bill complaint
3. SIM activation issue
4. Package upgrade request
5. No network coverage
6. International roaming confusion
7. Lost/stolen phone
8. Contract cancellation
9. Data package not working
10. Elderly customer - balance inquiry

#### Agent C (Banking) Scenarios:
1. Stolen card emergency
2. Online banking locked
3. Personal loan inquiry
4. Transaction dispute
5. New account opening
6. ATM card swallowed
7. Savings account interest
8. International transfer
9. Mobile banking setup
10. Elderly customer - pension inquiry

### 3. **LLM-to-LLM Testing System**
- **Customer Simulator** (`simulator/customer_simulator.py`)
  - Generates dynamic customer responses
  - Follows persona and goal
  - Natural Egyptian Arabic dialogue

- **Conversation Orchestrator** (`orchestrator.py`)
  - Manages multi-turn conversations
  - Tracks tokens, latency, success
  - Weave tracing integration

### 4. **Multi-Model Support**
- ✅ **Claude 3.5 Haiku** (Works perfectly with Arabic)
- ✅ **Gemini Flash Latest** (English prompts → Arabic output)
- ✅ **OpenAI GPT OSS 20B** (via W&B Inference)

### 5. **LLM-as-Judge Evaluation System** ⭐ NEW!
- **Automated quality assessment** (`evaluator/llm_judge.py`)
- **5 Core metrics** (0-10 scale):
  - Task Completion
  - Empathy
  - Clarity
  - Cultural Fit
  - Problem Solving
- **Qualitative feedback**:
  - Strengths, weaknesses, recommendations
  - Success criteria validation
  - Must-not-do violations

### 6. **Comprehensive Logging & Storage**
- **JSON Storage** - Local file-based storage
- **CSV Storage** - Spreadsheet-friendly format
- **Supabase Integration** - Cloud database with schema
- **Weave Tracing** - Full W&B integration for all LLM calls

### 7. **Benchmarking & Analytics**
- Model performance comparison
- Average scores by agent/scenario/model
- Success rate tracking
- Token usage and latency metrics
- Top/bottom performer identification

---

## 🚀 How to Use

### Step 1: Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env file (see ENV_SETUP.md)
cp ENV_SETUP.md .env
# Edit .env with your API keys
```

### Step 2: Run Full Evaluation Pipeline
```bash
# Test all scenarios with all models
python3 run_full_evaluation.py

# Test specific model only
python3 run_full_evaluation.py --models claude

# Test with specific agents and settings
python3 run_full_evaluation.py --agents agent_a agent_b --models claude gemini --max-turns 5
```

### Step 3: Evaluate Conversations with LLM Judge
```bash
# Evaluate all conversations in results/
python3 run_evaluation.py

# Use Claude as judge with English prompts
python3 run_evaluation.py --judge-model claude --language english

# Limit evaluation to first 10 conversations
python3 run_evaluation.py --limit 10
```

### Step 4: Test Single Scenario (Quick Test)
```bash
# Test scenario 0 with Claude
python3 test_demo.py --scenario 0 --model claude

# Test scenario 5 with Gemini
python3 test_demo.py --scenario 5 --model gemini
```

---

## 📁 Project Structure

```
AI Arabic Evals/
├── agents/                    # Agent definitions
│   ├── base_agent.py
│   ├── agent_a_ecommerce.py  # E-commerce agent
│   ├── agent_b_telecom.py    # Telecom agent
│   └── agent_c_banking.py    # Banking agent
│
├── scenarios/                 # Test scenarios
│   ├── agent_a_scenarios.py  # 10 e-commerce scenarios
│   ├── agent_b_scenarios.py  # 10 telecom scenarios
│   ├── agent_c_scenarios.py  # 10 banking scenarios
│   └── scenario_loader.py
│
├── models/                    # LLM client wrappers
│   ├── base_model.py
│   ├── claude_client.py      # Anthropic Claude
│   ├── gemini_client.py      # Google Gemini
│   └── weave_client.py       # W&B Inference
│
├── simulator/                 # Customer simulator
│   └── customer_simulator.py
│
├── evaluator/                 # ⭐ LLM-as-Judge evaluation
│   ├── __init__.py
│   └── llm_judge.py          # Automated quality assessment
│
├── storage/                   # Results storage
│   └── results_storage.py    # JSON, CSV, Supabase
│
├── utils/                     # Utilities
│   └── weave_init.py         # Weave tracing setup
│
├── run_full_evaluation.py    # 🎯 Main testing pipeline
├── run_evaluation.py          # ⚖️ LLM judge evaluation runner
├── test_demo.py               # Quick single scenario test
├── orchestrator.py            # Conversation management
├── config.py                  # Central configuration
│
├── results/                   # Output directory
│   ├── conversations.json    # All conversations
│   ├── benchmark_*.json      # Performance benchmarks
│   └── evaluation_*.json     # LLM judge results
│
└── docs/
    ├── ENV_SETUP.md          # Environment setup guide
    ├── QUICKSTART.md         # Quick start guide
    ├── WEAVE_TRACING_GUIDE.md # Weave integration guide
    ├── GEMINI_SAFETY_RESEARCH.md # Gemini safety filters
    └── supabase_schema.sql   # Database schema
```

---

## 🎯 Key Features

### ✅ Completed Features

1. **✅ Multi-Agent System**
   - 3 specialized agents (E-commerce, Telecom, Banking)
   - Arabic & English prompt support
   - Context-aware responses

2. **✅ Rich Scenario Library**
   - 30 total scenarios (10 per agent)
   - Diverse customer personas
   - Cultural context integration
   - Success criteria & evaluation dimensions

3. **✅ LLM-to-LLM Testing**
   - Dynamic customer simulation
   - Multi-turn conversations
   - Natural dialogue flow

4. **✅ Multi-Model Evaluation**
   - Claude 3.5 Haiku ✅ (Best performance)
   - Gemini Flash Latest ✅ (English→Arabic workaround)
   - OpenAI GPT OSS 20B ✅ (W&B Inference)

5. **✅ LLM-as-Judge Evaluation**
   - Automated quality scoring (5 metrics)
   - Qualitative feedback generation
   - Success criteria validation
   - Comparative analysis

6. **✅ Comprehensive Logging**
   - Weave tracing integration
   - Multi-storage support (JSON, CSV, Supabase)
   - Token & latency tracking

7. **✅ Benchmarking**
   - Model performance comparison
   - Scenario difficulty analysis
   - Success rate tracking
   - Top/bottom performers

---

## 📈 Sample Results

### Model Performance (Example)

| Model | Tests | Success Rate | Avg Turns | Avg Tokens | Avg Score |
|-------|-------|--------------|-----------|------------|-----------|
| Claude 3.5 Haiku | 10 | 100% | 6.2 | 1,234 | 8.5/10 |
| Gemini Flash | 10 | 90% | 5.8 | 1,100 | 7.8/10 |
| GPT OSS 20B | 10 | 80% | 4.5 | 890 | 7.2/10 |

### Evaluation Metrics (Example)

| Metric | Claude | Gemini | GPT OSS |
|--------|--------|--------|---------|
| Task Completion | 8.7 | 8.2 | 7.5 |
| Empathy | 9.1 | 7.8 | 7.0 |
| Clarity | 8.9 | 8.5 | 7.8 |
| Cultural Fit | 8.6 | 8.0 | 6.9 |
| Problem Solving | 8.4 | 7.9 | 7.3 |

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# LLM API Keys
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
WANDB_API_KEY=your_wandb_api_key

# Weave Tracing
WEAVE_PROJECT_NAME=your-entity/your-project
ENABLE_WEAVE_TRACING=true

# Storage
STORAGE_MODE=both  # json, csv, supabase, or both
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

See `ENV_SETUP.md` for detailed configuration guide.

---

## 🐛 Known Issues & Solutions

### 1. Gemini Safety Filters
**Issue**: Gemini blocks Arabic content (finish_reason: 2)
**Solution**: Use English prompts with explicit instructions to respond in Arabic
**Status**: ✅ Resolved (see `GEMINI_SAFETY_RESEARCH.md`)

### 2. W&B Inference Configuration
**Issue**: Model not found / malformed token errors
**Solution**: Use correct model names and `X-WANDB-PROJECT` header
**Status**: ✅ Resolved

### 3. Supabase Integration
**Issue**: save_conversation() parameter mismatch
**Solution**: Updated storage interface to use dict parameter
**Status**: ✅ Resolved

---

## 📚 Documentation

- **`ENV_SETUP.md`** - Complete environment setup guide
- **`QUICKSTART.md`** - Quick start tutorial
- **`WEAVE_TRACING_GUIDE.md`** - Weave integration guide
- **`GEMINI_SAFETY_RESEARCH.md`** - Gemini safety filter analysis
- **`supabase_schema.sql`** - Database schema for Supabase

---

## 🎓 Publishing Your Research

This evaluation framework is designed for publication-quality testing. You have:

1. ✅ **30 Rich Scenarios** across 3 domains
2. ✅ **Multi-Model Comparison** (Claude, Gemini, GPT)
3. ✅ **Automated Evaluation** with LLM-as-Judge
4. ✅ **Quantitative Metrics** (5 dimensions, 0-10 scale)
5. ✅ **Qualitative Analysis** (strengths, weaknesses, recommendations)
6. ✅ **Full Traceability** via Weave
7. ✅ **Reproducible Pipeline** with benchmarking

### Suggested Research Paper Structure:
1. **Introduction** - Arabic AI agent evaluation challenges
2. **Methodology** - LLM-to-LLM testing approach
3. **Scenarios** - 30 scenarios across 3 domains
4. **Evaluation Framework** - LLM-as-Judge metrics
5. **Results** - Model performance comparison
6. **Analysis** - Strengths, weaknesses, insights
7. **Conclusion** - Recommendations for Arabic AI development

---

## 🚀 Next Steps

### To Run Your First Evaluation:

```bash
# 1. Setup
pip install -r requirements.txt
cp ENV_SETUP.md .env
# Edit .env with your API keys

# 2. Run evaluation (Claude recommended)
python3 run_full_evaluation.py --models claude --max-turns 5

# 3. Evaluate with LLM judge
python3 run_evaluation.py --judge-model claude

# 4. View results
ls -ltr results/
cat results/benchmark_report_*.json
cat results/evaluation_results_*.json

# 5. View traces
# Open: https://wandb.ai/your-entity/your-project/weave
```

---

## 📊 Weave Tracing

All LLM calls are traced in Weights & Biases:
- **Customer messages** - Persona-driven generation
- **Agent responses** - Model responses with context
- **Evaluations** - LLM judge assessments
- **Performance metrics** - Tokens, latency, costs

View at: `https://wandb.ai/{your-entity}/{your-project}/weave`

---

## 🎉 Conclusion

This is a **complete, production-ready evaluation framework** for Arabic customer service AI agents. It includes:

- ✅ 30 diverse, culturally-aware scenarios
- ✅ 3 specialized agent types
- ✅ Multi-model testing (Claude, Gemini, GPT)
- ✅ LLM-to-LLM interactions
- ✅ Automated LLM-as-Judge evaluation
- ✅ Comprehensive metrics & benchmarking
- ✅ Full tracing & logging
- ✅ Publication-ready structure

**Ready to test and publish your research! 🚀**

---

## 📞 Support

For issues or questions:
1. Check documentation in `/docs`
2. Review `GEMINI_SAFETY_RESEARCH.md` for Gemini issues
3. Check Weave traces for debugging
4. Review error logs in results/

**Happy Testing! 🎯**

