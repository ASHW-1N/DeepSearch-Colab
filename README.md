# Deep Search Agent Swarm 🤖🔍

An autonomous multi-agent deep research swarm designed to analyze complex topics across the internet, cross-reference data, and build comprehensive, cited markdown reports without hallucinating.

Powered by Groq's blazing-fast inference (specifically Qwen 3 32B).

## Features
- **Multi-Agent Setup:** Orchestrator, Searchers, Analyzer, Reporter.
- **Deep Web Search:** Uses `DuckDuckGo` (API-free) paired with `Trafilatura` (intelligent HTML extraction).
- **Anti-Hallucination:** Strict source-grounding, fact cross-referencing, and focus tracking.
- **Graceful Limits:** Built-in Token Bucket Rate Limiter and automatic fallback for Groq limits.

## How to Run

Before running, make sure your `.env` contains your API key:
```
GROQ_API_KEY=your_key_here
```

### Option 1: Start the Web UI (Recommended)
You can start a clean, dynamic Web Interface that streams agent logs in real-time.
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```
Then open your browser to `http://127.0.0.1:8000`.

### Option 2: Run directly in Terminal (CLI Mode)
You can launch deep searches directly from your terminal and save the resulting Markdown file in the `output/` folder.
```bash
python main.py "Your research topic here" --searchers 2 --rounds 2
```
_Parameters:_
- `--searchers`: The number of parallel web-scraping agents to use (default: 2)
- `--rounds`: How deep the search rabbit hole goes (default: 2)
