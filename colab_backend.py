"""
==============================================================================
  DeepSearch — Colab GPU Backend
  
  Copy this entire file into a Google Colab notebook cell and run it.
  It will:
    1. Install vLLM (OpenAI-compatible inference server)
    2. Download Qwen2.5-3B-Instruct (lightweight, 32k context)
    3. Start the server on port 8000
    4. Create a public ngrok tunnel
    5. Print the URL you paste into your local .env file
  
  REQUIREMENTS:
    - Google Colab with GPU runtime (T4 is enough for 3B model)
    - Free ngrok account (https://ngrok.com) for the auth token
    
  USAGE:
    Cell 1: Copy everything between the ═══ CELL 1 ═══ markers
    Cell 2: Copy everything between the ═══ CELL 2 ═══ markers
    Cell 3: Copy everything between the ═══ CELL 3 ═══ markers
==============================================================================
"""

# ═══════════════════════════════════════════════════════════════════════════
# ═══ CELL 1: Install Dependencies ═══
# Paste this into the FIRST cell of your Colab notebook and run it.
# This takes ~3-5 minutes on first run.
# ═══════════════════════════════════════════════════════════════════════════

CELL_1 = """
# ── Step 1: Install vLLM and ngrok ──
!pip install vllm -q
!pip install pyngrok -q

# Verify GPU is available
import torch
print(f"✅ CUDA Available: {torch.cuda.is_available()}")
print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
print(f"✅ VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")
"""

# ═══════════════════════════════════════════════════════════════════════════
# ═══ CELL 2: Configure ngrok ═══
# Paste this into the SECOND cell. Replace YOUR_NGROK_TOKEN.
# Get a free token at: https://dashboard.ngrok.com/get-started/your-authtoken
# ═══════════════════════════════════════════════════════════════════════════

CELL_2 = """
from pyngrok import ngrok
import os

# ┌─────────────────────────────────────────────────────────┐
# │  PASTE YOUR NGROK AUTH TOKEN BELOW                       │
# │  Get it free at: https://dashboard.ngrok.com/authtokens  │
# └─────────────────────────────────────────────────────────┘
NGROK_AUTH_TOKEN = "YOUR_NGROK_TOKEN_HERE"

ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Create tunnel to port 8000 (where vLLM will serve)
public_url = ngrok.connect(8000, "http").public_url
print()
print("=" * 60)
print("🚀 YOUR DEEPSEARCH BACKEND URL:")
print(f"   {public_url}/v1")
print("=" * 60)
print()
print("Copy the URL above and paste it into your local .env file:")
print(f'  LLM_BASE_URL={public_url}/v1')
print(f'  LLM_API_KEY=not-needed')
print(f'  LLM_BACKEND=colab')
print()
print("Keep this notebook running! Starting vLLM server next...")
"""

# ═══════════════════════════════════════════════════════════════════════════
# ═══ CELL 3: Start vLLM Server ═══
# Paste this into the THIRD cell and run it.
# This will download the model (~6GB) and start serving.
# The cell will keep running — that's normal. It IS your server.
# ═══════════════════════════════════════════════════════════════════════════

CELL_3 = """
import subprocess

# ┌─────────────────────────────────────────────────────────┐
# │  MODEL SELECTION                                         │
# │  Change this to test different models:                   │
# │                                                          │
# │  Lightweight (T4 GPU):                                   │
# │    "Qwen/Qwen2.5-3B-Instruct"     (~6 GB, fast)         │
# │    "Qwen/Qwen2.5-7B-Instruct-AWQ" (~4 GB, quantized)    │
# │                                                          │
# │  Medium (L4/A100 GPU):                                   │
# │    "Qwen/Qwen2.5-14B-Instruct-AWQ" (~8 GB, best value)  │
# │    "Qwen/Qwen2.5-32B-Instruct-AWQ" (~18 GB, powerful)   │
# │                                                          │
# │  Full Power (A100 80GB):                                 │
# │    "Qwen/Qwen2.5-72B-Instruct-AWQ" (~40 GB, research)   │
# └─────────────────────────────────────────────────────────┘
MODEL = "Qwen/Qwen2.5-3B-Instruct"

# Max model context length — Qwen2.5 supports up to 32k
MAX_MODEL_LEN = 16384  # 16k is safe for T4's 15GB VRAM with 3B

print(f"📦 Downloading and loading: {MODEL}")
print(f"📏 Context window: {MAX_MODEL_LEN} tokens")
print(f"⏳ This takes 3-8 minutes on first run (downloading weights)...")
print()

# Start the vLLM OpenAI-compatible API server
# This command blocks — the cell stays "running" = the server is alive
!python -m vllm.entrypoints.openai.api_server \\
    --model {MODEL} \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --max-model-len {MAX_MODEL_LEN} \\
    --dtype auto \\
    --trust-remote-code \\
    --enforce-eager
"""

# ═══════════════════════════════════════════════════════════════════════════
# ═══ OPTIONAL CELL 4: Health Check ═══
# Open a NEW cell and run this to verify the server is working.
# ═══════════════════════════════════════════════════════════════════════════

CELL_4_HEALTHCHECK = """
import requests

# Replace with YOUR ngrok URL from Cell 2
BASE_URL = "YOUR_NGROK_URL_HERE/v1"

# List available models
r = requests.get(f"{BASE_URL}/models")
print("Available models:", r.json())

# Test a chat completion
r = requests.post(f"{BASE_URL}/chat/completions", json={
    "model": "Qwen/Qwen2.5-3B-Instruct",
    "messages": [{"role": "user", "content": "What is 2+2? Answer in one word."}],
    "max_tokens": 10,
    "temperature": 0.0
})
print("Test response:", r.json()["choices"][0]["message"]["content"])
"""

if __name__ == "__main__":
    print("=" * 70)
    print("  DeepSearch Colab Backend — Instructions")
    print("=" * 70)
    print()
    print("This file contains the code for 3 Colab cells.")
    print("Open Google Colab, create a new notebook, and:")
    print()
    print("  1. Set runtime to GPU: Runtime → Change runtime type → T4 GPU")
    print("  2. Create 3 cells and paste the code from each CELL section")
    print("  3. Run them in order")
    print("  4. Copy the ngrok URL from Cell 2 output")
    print("  5. Paste it into your local DeepSearch/.env file")
    print("  6. Run DeepSearch locally!")
    print()
    print("Read the comments in this file for detailed instructions.")
