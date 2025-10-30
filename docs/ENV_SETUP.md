# Environment Variables Setup Guide

## Quick Start

1. Copy the template below to a file named `.env` in the project root
2. Replace all `your_*_here` values with your actual API keys
3. Run `python3 test_demo.py --scenario 0 --model claude` to test

---

## Environment Variables Template

```bash
# ==================== LLM Provider API Keys ====================

# Google Gemini API Key
# Get from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic Claude API Key  
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# ==================== Weights & Biases (W&B) ====================
# W&B is used for BOTH Weave Tracing AND W&B Inference

# W&B API Key (required for both tracing and inference)
# Get from: https://wandb.ai/settings
WANDB_API_KEY=your_wandb_api_key_here

# W&B Entity (your username or team name)
# Example: "ahmedbakr" or "g-tsvetkova-minerva-university"
WANDB_ENTITY=g-tsvetkova-minerva-university

# ==================== Weave Tracing Configuration ====================
# Weave logs all LLM calls and agent interactions

# Enable/disable Weave tracing
ENABLE_WEAVE_TRACING=true

# Weave project name (format: entity/project-name)
# Must match your W&B project: https://wandb.ai/ENTITY/PROJECT/weave
WEAVE_PROJECT_NAME=g-tsvetkova-minerva-university/Testing-ar

# ==================== W&B Inference (Optional) ====================
# Used for running open-source models via W&B Inference
# Uses the same WANDB_API_KEY as above
# No additional configuration needed - defaults work automatically

# ==================== Supabase Configuration (Optional) ====================
# For database storage of results

# Get from: https://supabase.com/dashboard
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# ==================== Storage Configuration ====================
# Where to save evaluation results
# Options: 'json', 'csv', 'supabase', or 'both' (json + supabase)
STORAGE_MODE=json
```

---

## Important Notes

### ✅ Working Setup (Verified)

**For Claude (Primary Model):**
```bash
ANTHROPIC_API_KEY=your_key
WANDB_API_KEY=your_key
WEAVE_PROJECT_NAME=g-tsvetkova-minerva-university/Testing-ar
STORAGE_MODE=json
```

**For W&B Inference (Open-Source Models):**
```bash
WANDB_API_KEY=your_key  # Same key as Weave tracing
WEAVE_PROJECT_NAME=g-tsvetkova-minerva-university/Testing-ar
# Model automatically uses: https://api.inference.wandb.ai/v1
```

### ⚠️ Common Mistakes

1. **Don't set `WEAVE_API_KEY`** - W&B Inference uses `WANDB_API_KEY`
2. **Project name format** must be `entity/project` (with slash)
3. **Entity** should match your W&B username or org
4. **WEAVE_BASE_URL** is auto-configured - don't set it unless using custom endpoint

### 🔗 Get Your API Keys

- **Google Gemini**: https://makersuite.google.com/app/apikey
- **Anthropic Claude**: https://console.anthropic.com/settings/keys
- **W&B API**: https://wandb.ai/settings (scroll to "API keys")
- **Supabase**: https://supabase.com/dashboard/project/_/settings/api

---

## Model Configuration

### Available Models on W&B Inference

From your W&B dashboard, these models are available:
- `OpenAI GPT OSS 120B` ✅ (Recommended open-source)
- `OpenAI GPT OSS 20B`
- `Qwen3 235B A22B-2507`
- `OpenPipe Qwen3 14B Instruct`
- `Qwen3 Coder 480B A35B`
- `Qwen2.5 14B Instruct`
- `Meta Llama 3.1 8B`
- `MoonshotAI Kimi K2`
- `Z.AI GLM 4.5`

### Current Model Setup (config.py)

```python
"claude": "claude-3-5-haiku-20241022"  # ✅ Working perfectly
"gemini": "gemini-1.5-flash"           # ⚠️ May have Arabic safety issues
"qwen": "OpenAI GPT OSS 120B"          # 🧪 Testing via W&B Inference
```

---

## Testing Your Setup

```bash
# Test Claude (should work)
python3 test_demo.py --scenario 0 --model claude

# Test W&B Inference open-source model
python3 test_demo.py --scenario 0 --model qwen

# Test Gemini (may have issues with Arabic)
python3 test_demo.py --scenario 0 --model gemini

# List all available scenarios
python3 test_demo.py --list
```

---

## Troubleshooting

### Weave Tracing Errors

**Error**: `permission denied` when initializing Weave
- **Fix**: Make sure `WANDB_ENTITY` matches your actual W&B username
- **Fix**: Ensure project name format is `entity/project` with slash

**Error**: `Unable to access ahmedbakr/Testing-ar`
- **Fix**: Update `WEAVE_PROJECT_NAME` to match your actual project
- **Example**: `g-tsvetkova-minerva-university/Testing-ar`

### W&B Inference Errors

**Error**: `401 Malformed token`
- **Fix**: Check `WANDB_API_KEY` is set correctly
- **Fix**: Don't use `WEAVE_API_KEY` - use `WANDB_API_KEY`

**Error**: `404 Resource not found`
- **Fix**: Model name must match exactly as shown in W&B dashboard
- **Fix**: Use `OpenAI GPT OSS 120B` (with exact spacing)

### Gemini Safety Errors

**Error**: `finish_reason: 2` (SAFETY block)
- **Issue**: Known problem with Gemini and Arabic content
- **Solution**: Use Claude instead (works perfectly with Arabic)
- **See**: `GEMINI_SAFETY_RESEARCH.md` for detailed analysis

---

## Minimal .env for Quick Start

```bash
# Minimal setup to get started with Claude
ANTHROPIC_API_KEY=sk-ant-xxxxx
WANDB_API_KEY=xxxxx
WEAVE_PROJECT_NAME=g-tsvetkova-minerva-university/Testing-ar
STORAGE_MODE=json
```

This is enough to run successful Arabic customer service evaluations with Claude!

