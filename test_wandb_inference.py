#!/usr/bin/env python3
"""
Diagnostic script to test W&B Inference configuration
"""

import os
import sys
from dotenv import load_dotenv
import requests
from openai import OpenAI

print("="*80)
print("W&B INFERENCE DIAGNOSTIC TEST")
print("="*80)

# Load environment
load_dotenv()

# Test 1: Check API Key
print("\n1️⃣  Testing API Key...")
wandb_key = os.getenv("WANDB_API_KEY")
if not wandb_key:
    print("   ❌ WANDB_API_KEY not found in environment")
    print("   Check your .env file!")
    sys.exit(1)
else:
    print(f"   ✅ WANDB_API_KEY found: {wandb_key[:10]}...{wandb_key[-4:]}")

# Test 2: Check Project Name
print("\n2️⃣  Testing Project Configuration...")
project = os.getenv("WEAVE_PROJECT_NAME", "Testing-ar")
print(f"   Project: {project}")

# Test 3: Direct API Test with requests
print("\n3️⃣  Testing W&B Inference API (Direct HTTP)...")
base_url = "https://api.inference.wandb.ai/v1"
print(f"   Endpoint: {base_url}")

headers = {
    "Authorization": f"Bearer {wandb_key}",
    "Content-Type": "application/json",
    "X-WANDB-PROJECT": project
}

# List models endpoint
try:
    print("\n   Attempting to list available models...")
    response = requests.get(f"{base_url}/models", headers=headers, timeout=10)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ API connection successful!")
        models = response.json()
        print(f"\n   Available models ({len(models.get('data', []))}):")
        for model in models.get('data', [])[:5]:
            print(f"      - {model.get('id', 'unknown')}")
    else:
        print(f"   ❌ API Error: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")

# Test 4: OpenAI Client Test
print("\n4️⃣  Testing OpenAI Client (Python SDK)...")
try:
    client = OpenAI(
        api_key=wandb_key,
        base_url=base_url,
        default_headers={"X-WANDB-PROJECT": project}
    )
    print("   ✅ Client initialized")
    
    # Try listing models
    print("\n   Attempting to list models with OpenAI client...")
    models = client.models.list()
    print(f"   ✅ Models retrieved: {len(models.data)} models")
    print("\n   First 5 models:")
    for model in models.data[:5]:
        print(f"      - {model.id}")
        
except Exception as e:
    print(f"   ❌ Client error: {e}")

# Test 5: Try actual inference
print("\n5️⃣  Testing Inference with 'OpenAI GPT OSS 120B'...")
try:
    client = OpenAI(
        api_key=wandb_key,
        base_url=base_url,
        default_headers={"X-WANDB-PROJECT": project}
    )
    
    response = client.chat.completions.create(
        model="OpenAI GPT OSS 120B",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello' in Arabic"}
        ],
        max_tokens=50
    )
    
    print("   ✅ Inference successful!")
    print(f"   Model used: {response.model}")
    print(f"   Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"   ❌ Inference failed: {e}")
    print(f"   Error type: {type(e).__name__}")
    
    # Try to get more details
    if hasattr(e, 'response'):
        print(f"   Response status: {e.response.status_code}")
        print(f"   Response body: {e.response.text}")

# Test 6: Check config.py setup
print("\n6️⃣  Testing config.py integration...")
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import config
    
    print(f"   WANDB_API_KEY in config: {'✅ Set' if config.WANDB_API_KEY else '❌ Empty'}")
    print(f"   WEAVE_API_KEY in config: {'✅ Set' if config.WEAVE_API_KEY else '❌ Empty'}")
    print(f"   Keys match: {'✅ Yes' if config.WANDB_API_KEY == config.WEAVE_API_KEY else '❌ No'}")
    print(f"   Model name: {config.MODELS_CONFIG['qwen']['name']}")
    print(f"   API key env: {config.MODELS_CONFIG['qwen']['api_key_env']}")
    
    # Verify the key is actually being used
    key_from_config = getattr(config, config.MODELS_CONFIG['qwen']['api_key_env'])
    print(f"   Key accessible: {'✅ Yes' if key_from_config else '❌ No'}")
    
except Exception as e:
    print(f"   ❌ Config import failed: {e}")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)

