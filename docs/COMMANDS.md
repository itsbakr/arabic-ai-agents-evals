# Quick Command Reference

## 🚀 Essential Commands

### Full Evaluation Pipeline
```bash
# Run all scenarios with Claude (recommended)
python3 run_full_evaluation.py --models claude --max-turns 5

# Run all scenarios with all models
python3 run_full_evaluation.py --max-turns 5

# Run specific agents only
python3 run_full_evaluation.py --agents agent_a --models claude --max-turns 3
```

### LLM-as-Judge Evaluation
```bash
# Evaluate all conversations with Claude as judge
python3 run_evaluation.py --judge-model claude

# Evaluate with Gemini as judge
python3 run_evaluation.py --judge-model gemini

# Evaluate in Arabic (prompts in Arabic)
python3 run_evaluation.py --judge-model claude --language arabic

# Evaluate limited number
python3 run_evaluation.py --limit 10
```

### Quick Testing (Single Scenario)
```bash
# Test scenario 0 with Claude
python3 test_demo.py --scenario 0 --model claude

# Test scenario 5 with Gemini
python3 test_demo.py --scenario 5 --model gemini

# Test scenario 3 with OpenAI GPT
python3 test_demo.py --scenario 3 --model qwen
```

## 📊 View Results

```bash
# View latest benchmark
cat results/benchmark_report_*.json | jq

# View latest evaluation results
cat results/evaluation_results_*.json | jq

# List all results
ls -ltr results/

# View conversations
cat results/conversations.json | jq
```

## 🔍 Weave Traces

Open in browser:
```
https://wandb.ai/g-tsvetkova-minerva-university/Testing-ar/weave
```

## 🐛 Troubleshooting

### Check API Keys
```bash
# Verify .env file
cat .env

# Test Claude
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Claude:', os.getenv('ANTHROPIC_API_KEY')[:10] if os.getenv('ANTHROPIC_API_KEY') else 'NOT SET')"

# Test Gemini  
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Gemini:', os.getenv('GOOGLE_API_KEY')[:10] if os.getenv('GOOGLE_API_KEY') else 'NOT SET')"

# Test W&B
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('W&B:', os.getenv('WANDB_API_KEY')[:10] if os.getenv('WANDB_API_KEY') else 'NOT SET')"
```

### Check Model Availability
```bash
# List available Gemini models
python3 -c "import google.generativeai as genai; import os; from dotenv import load_dotenv; load_dotenv(); genai.configure(api_key=os.getenv('GOOGLE_API_KEY')); [print(m.name) for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]"
```

### Clear Results
```bash
# Backup current results
mkdir -p backups
cp -r results backups/results_$(date +%Y%m%d_%H%M%S)

# Clear results directory
rm -f results/*.json results/*.csv
```

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install specific packages if needed
pip install anthropic google-generativeai weave openai supabase pandas python-dotenv
```

## ⚙️ Configuration

```bash
# Copy environment template
cp ENV_SETUP.md .env

# Edit with your keys
nano .env  # or vi .env or code .env
```

## 🎯 Recommended Workflow

### 1. Initial Test (Quick validation)
```bash
python3 test_demo.py --scenario 0 --model claude
```

### 2. Small-Scale Evaluation
```bash
python3 run_full_evaluation.py --agents agent_a --models claude --max-turns 3
```

### 3. Full Evaluation
```bash
python3 run_full_evaluation.py --models claude gemini --max-turns 5
```

### 4. LLM Judge Evaluation
```bash
python3 run_evaluation.py --judge-model claude
```

### 5. Analyze Results
```bash
# View benchmarks
cat results/benchmark_report_*.json | jq '.by_model'

# View evaluations
cat results/evaluation_results_*.json | jq '.[0:3]'

# Check Weave
open "https://wandb.ai/g-tsvetkova-minerva-university/Testing-ar/weave"
```

## 🎨 Customization

### Change Models
Edit `config.py`:
```python
MODELS_CONFIG = {
    "gemini": {
        "name": "gemini-flash-latest",  # Change this
        ...
    }
}
```

### Change Storage Mode
Edit `.env`:
```bash
STORAGE_MODE=json  # or csv, supabase, both
```

### Add New Scenarios
Edit `scenarios/agent_a_scenarios.py` (or b, c):
```python
scenarios.append(Scenario(
    scenario_id="A11_new_scenario",
    # ... add your scenario
))
```

## 💡 Tips

1. **Start with Claude** - Most reliable for Arabic
2. **Use max-turns=3** for quick tests
3. **Check Weave traces** for debugging
4. **Save results** before re-running
5. **Use English prompts** for Gemini (already configured)

## 🆘 Common Issues

### Gemini Safety Blocks
Already fixed with English prompts! If still issues:
- Check `GEMINI_SAFETY_RESEARCH.md`
- Use Claude instead

### W&B Inference Errors
- Verify `WANDB_API_KEY` is set
- Check project name in config
- Use correct model names

### Storage Errors
- Ensure directories exist: `mkdir -p results`
- Check Supabase credentials
- Try `STORAGE_MODE=json` for testing

