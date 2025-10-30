# Arabic AI Customer Service Agents Evaluation Framework
# تقييم وكلاء خدمة العملاء المصريين بالذكاء الاصطناعي

A comprehensive LLM-to-LLM evaluation framework for testing Arabic customer service agents in the Egyptian market. Tests three agent types (E-commerce, Telecom, Banking) across three AI models (Gemini, Claude, Qwen).

## 🎯 Overview

This framework evaluates AI customer service agents through realistic conversations between:
- **Customer Simulator**: LLM playing the role of Egyptian customers with different personas
- **Service Agent**: LLM playing customer service representative roles
- **Evaluator**: Automated scoring based on multiple dimensions

### Agent Types
1. **Agent A**: E-commerce Order Support (دعم طلبات التجارة الإلكترونية)
2. **Agent B**: Telecom Technical Support (الدعم الفني للاتصالات)
3. **Agent C**: Banking Account Support (دعم الحسابات البنكية)

### AI Models Tested
1. **Google Gemini Flash 2.0**
2. **Anthropic Claude Sonnet 4**
3. **Qwen 2.5 72B** (via Weave inference)

## 📋 Prerequisites

- Python 3.9+
- API Keys:
  - Google Gemini API key
  - Anthropic Claude API key
  - Weave API key (for Qwen)
  - (Optional) Supabase account for database storage

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd "AI Arabic Evals"

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env_example.txt .env
```

Edit `.env` with your API keys:

```bash
# Google Gemini
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Weave (for Qwen)
WEAVE_API_KEY=your_weave_api_key_here
WEAVE_BASE_URL=https://your-weave-endpoint.com/v1

# Storage (optional - for database)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
STORAGE_MODE=csv  # Options: csv, supabase, both
```

### 3. Test the System

Run a demo conversation:

```bash
# Test first scenario with Gemini
python test_demo.py --scenario 0 --model gemini

# Test with Claude
python test_demo.py --scenario 0 --model claude

# List all available scenarios
python test_demo.py --list
```

## 📊 Project Structure

```
AI Arabic Evals/
├── agents/                 # Agent definitions
│   ├── base_agent.py      # Base agent class
│   ├── agent_a_ecommerce.py
│   ├── agent_b_telecom.py
│   └── agent_c_banking.py
├── models/                # AI model clients
│   ├── base_model.py
│   ├── gemini_client.py
│   ├── claude_client.py
│   └── weave_client.py
├── simulator/             # Customer simulator
│   └── customer_simulator.py
├── scenarios/             # Test scenarios
│   ├── scenario_loader.py
│   ├── agent_a_scenarios.py  # 10 e-commerce scenarios
│   ├── agent_b_scenarios.py  # 10 telecom scenarios (TODO)
│   └── agent_c_scenarios.py  # 10 banking scenarios (TODO)
├── storage/               # Results storage
│   └── results_storage.py
├── orchestrator.py        # Conversation orchestrator
├── config.py             # Configuration
├── test_demo.py          # Demo script
├── results/              # Output directory
│   ├── conversations.csv
│   ├── conversation_turns.csv
│   └── evaluations.csv
└── requirements.txt
```

## 🎬 How It Works

### 1. Scenario-Based Testing

Each scenario includes:
- **Customer Persona**: Age, personality, communication style, tech literacy
- **Customer Goal**: What they want to achieve
- **Initial Context**: Order numbers, account details, etc.
- **Evaluation Criteria**: Success metrics
- **Expected Behaviors**: What agent should do

### 2. LLM-to-LLM Conversation

```python
Customer Simulator (LLM) ←→ Service Agent (LLM being tested)
```

The conversation continues naturally until:
- Customer is satisfied and ends conversation
- Maximum turns reached (default: 10)
- Error occurs

### 3. Data Storage

All conversations are automatically saved to:
- **CSV Files**: `results/conversations.csv` and `results/conversation_turns.csv`
- **Supabase** (optional): Real-time database for analysis

Each record includes:
- Full conversation transcript
- Token usage and latency
- Success indicators
- Timestamps

## 📈 Example Scenarios

### Agent A - E-commerce (10 scenarios)

1. **Late Delivery** - Impatient young professional needs phone urgently
2. **Wrong Item** - Bride received wrong dress, wedding in 2 days
3. **Ramadan Timing** - Father ordering Eid gifts, concerned about delays
4. **Laptop Refund** - Tech-savvy student wants refund, not replacement
5. **Address Change** - Customer moved, order shipped to old address
6. **Large COD Order** - Customer prefers cash, worried about limits
7. **Damaged Delivery** - Angry customer received broken TV
8. **Elderly Customer** - First-time user needs help ordering gift
9. **Promo Confusion** - Discount code not working as advertised
10. **Multiple Orders** - Customer confused about status of 3 orders

## 🔧 Running Full Evaluation

```bash
# Run all scenarios for one agent with one model
python run_evaluation.py --agent agent_a --model gemini

# Run specific scenario multiple times
python run_evaluation.py --scenario A1_late_delivery --model gemini --runs 3

# Run full benchmark (all agents, all models, all scenarios)
python run_full_benchmark.py
```

## 📊 Results Analysis

### CSV Output

The system generates three CSV files:

1. **conversations.csv**: Metadata for each conversation
   - scenario_id, model_name, total_turns, success, tokens, latency

2. **conversation_turns.csv**: Individual turns
   - conversation_id, turn_number, customer_message, agent_message

3. **evaluations.csv**: Evaluation scores
   - task_completion, empathy, clarity, cultural_fit, overall_score

### Export to Excel

```python
from storage.results_storage import CSVStorage

storage = CSVStorage()
storage.export_summary("summary.xlsx")
```

## 🎯 Evaluation Dimensions

Each conversation is evaluated on:

1. **Task Completion** (0-10): Did the agent solve the customer's problem?
2. **Empathy** (0-10): Did the agent show understanding and care?
3. **Clarity** (0-10): Were responses clear and easy to understand?
4. **Cultural Fit** (0-10): Appropriate for Egyptian context?
5. **Problem Solving** (0-10): Quality of solutions offered

## 🗄️ Supabase Setup (Optional)

If using Supabase for storage, create these tables:

```sql
-- Conversations table
CREATE TABLE conversations (
  id BIGSERIAL PRIMARY KEY,
  conversation_id TEXT UNIQUE NOT NULL,
  scenario_id TEXT NOT NULL,
  agent_type TEXT NOT NULL,
  model_name TEXT NOT NULL,
  customer_persona TEXT,
  customer_goal TEXT,
  total_turns INTEGER,
  success BOOLEAN,
  end_reason TEXT,
  total_tokens INTEGER,
  total_latency FLOAT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversation turns table
CREATE TABLE conversation_turns (
  id BIGSERIAL PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  turn_number INTEGER NOT NULL,
  customer_message TEXT,
  agent_message TEXT,
  customer_tokens INTEGER,
  agent_tokens INTEGER,
  turn_latency FLOAT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
);

-- Evaluations table
CREATE TABLE evaluations (
  id BIGSERIAL PRIMARY KEY,
  conversation_id TEXT,
  scenario_id TEXT NOT NULL,
  model_name TEXT NOT NULL,
  task_completion FLOAT,
  empathy FLOAT,
  clarity FLOAT,
  cultural_fit FLOAT,
  problem_solving FLOAT,
  overall_score FLOAT,
  evaluator_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🤝 Contributing

This is an evaluation framework for research and testing. Feel free to:
- Add more scenarios
- Modify evaluation criteria
- Test with different models
- Extend to other languages/markets

## 📝 License

MIT License - Free to use for research and evaluation purposes.

## 🙏 Acknowledgments

Built for evaluating Arabic customer service AI agents in the Egyptian market, focusing on cultural appropriateness, empathy, and task completion.

---

**Happy Testing! 🚀**

