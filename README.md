# agenteval-platform-openshift

A pytest-based AI/LLM test automation framework for validating
model serving, hallucination detection, and RAG pipeline quality
on Red Hat OpenShift AI.

## What This Tests

| Layer | What | Tools |
|-------|------|-------|
| Model Serving API | Inference endpoints, latency, edge cases | pytest, httpx |
| LLM Output Quality | Hallucination, prompt regression, relevancy | DeepEval |
| RAG Pipeline | Faithfulness, retrieval quality, context precision | Ragas, LangChain |
| OpenShift AI Integration | KServe endpoints, model lifecycle | httpx, OpenShift SDK |

## Why This Exists

AI systems fail differently from traditional software.
A model can return HTTP 200 and still hallucinate, fabricate
facts, or give irrelevant answers. This framework tests what
matters — the quality and reliability of AI behaviour,
not just whether the API responds.

## Tech Stack

- **Test execution** — pytest, httpx
- **LLM evaluation** — DeepEval, Ragas
- **Local LLM** — Ollama (llama3.2)
- **RAG agent** — LangChain + ChromaDB
- **CI pipeline** — GitHub Actions
- **Reporting** — Allure, pytest-html
- **Target platform** — Red Hat OpenShift AI

## Project Structure

agenteval-platform-openshift/
├── tests/
│   ├── api/              # Model serving API tests
│   ├── llm_eval/         # Hallucination + prompt regression
│   └── integration/      # RAG agent end-to-end tests
├── config/
│   └── test_config.yaml  # Thresholds, endpoints, model config
├── conftest.py           # Shared pytest fixtures
├── TEST_STRATEGY.md      # Full test strategy document
└── .github/workflows/    # GitHub Actions CI

## Quick Start

```bash
# Clone the repo
git clone https://github.com/alakapatnaik/agenteval-platform.git
cd agenteval-platform

# Create and activate venv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start local LLM
ollama serve &
ollama pull llama3.2

# Run tests
pytest tests/api/ -v --html=reports/report.html
```

## Test Results

| Suite | Tests | Status |
|-------|-------|--------|
| Model Serving API | 5 | ✅ Passing |
| Edge Cases | 5 | ✅ Passing |
| LLM Evaluation | 3 | 🔄 Day 5 |
| RAG Pipeline | 3 | 🔄 Day 6 |
| OpenShift AI | TBD | 🔄 Day 7 |

## Author

## Author

**Alaka Pattnaik**
14 years of Quality Engineering experience specialising in
cloud-native platforms, BigData testing, and AI/LLM test architecture.

Previously led QE at Epsilon for BigData pipeline validation
on cloud-native infrastructure (2020–2025).

During career break (June2025–Present): upskilled in AI/LLM test
automation, built this framework targeting Red Hat OpenShift AI,
and studying ods-ci open source QE codebase for contribution.

Currently seeking Staff SDET / Test Architect / Engineering
Manager QE roles in Bengaluru.

[LinkedIn](https://www.linkedin.com/in/alaka-pattnaik/) | 
[GitHub](https://github.com/alakapatnaik/agenteval-platform)

