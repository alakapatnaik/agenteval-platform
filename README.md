# agenteval-platform-openshift

[![CI](https://github.com/alakapatnaik/agenteval-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/alakapatnaik/agenteval-platform/actions)
[![Allure Report](https://img.shields.io/badge/Allure-Report-green)](https://alakapatnaik.github.io/agenteval-platform/)
[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![pytest](https://img.shields.io/badge/pytest-9.0-orange)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> "AI systems fail differently from traditional software —
> this framework tests what matters: hallucination, faithfulness,
> RAG quality, and model serving reliability."

A pytest-based open source AI/LLM test automation framework
for validating model serving, hallucination detection, and
RAG pipeline quality — targeting Red Hat OpenShift AI.

---

## 🎯 What This Tests

| Layer | What | Tools |
|-------|------|-------|
| Model Serving API | Inference endpoints, latency, edge cases | pytest, httpx |
| LLM Output Quality | Hallucination, faithfulness, relevancy | Custom Groq Judge |
| RAG Pipeline | Retrieval quality, answer faithfulness | LangChain, ChromaDB |
| RAG Evaluation | Faithfulness, relevancy, precision scoring | Custom Groq Evaluator |
| OpenShift AI | KServe protocol, multi-environment | pytest, httpx |

---

## 🚀 Why This Exists

Traditional API testing misses the most critical AI failures.
A model can return HTTP 200 and still:
- Hallucinate facts confidently
- Give irrelevant answers
- Fail RAG retrieval silently
- Degrade across model versions

This framework tests **AI behaviour** — not just API responses.

---

## 📊 Test Results

| Suite | Tests | Status |
|-------|-------|--------|
| Model Serving API | 5 | ✅ Passing |
| Edge Cases | 5 | ✅ Passing |
| LLM Evaluation | 6 | ✅ Passing |
| RAG Pipeline | 6 | ✅ Passing |
| RAG Evaluation | 5 | ✅ Passing |
| OpenShift AI Serving | 6 | ✅ Passing |
| **Total** | **36** | ✅ **100% Pass Rate** |

### Live Allure Report
🔗 [View Full Test Report](https://alakapatnaik.github.io/agenteval-platform/)

---

## 🌍 Environments Tested

| Environment | Status |
|-------------|--------|
| Local — Ollama llama3.2 | ✅ Passing |
| Red Hat OpenShift AI Sandbox | ✅ Model deployed, 5/5 containers running |

---

## 📈 LLM Evaluation Scores

| Metric | Score | Threshold |
|--------|-------|-----------|
| Hallucination | < 0.3 | < 0.5 |
| Faithfulness | > 0.7 | > 0.3 |
| Answer Relevancy | > 0.8 | > 0.3 |
| Context Precision | > 0.6 | > 0.3 |

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Test execution | pytest, httpx |
| Local LLM | Ollama — llama3.2 |
| Judge LLM | Groq — llama-3.3-70b-versatile |
| RAG pipeline | LangChain, ChromaDB, nomic-embed-text |
| LLM evaluation | Custom Groq judge |
| CI pipeline | GitHub Actions |
| Reporting | Allure, pytest-html |
| Target platform | Red Hat OpenShift AI |
| Environments | Local + OpenShift AI sandbox |

---

## Project Structure


agenteval-platform-openshift/
│
├── tests/
│   ├── api/
│   │   ├── test_model_serving.py      # Model API health, latency, schema
│   │   └── test_model_edge_cases.py   # Edge cases, concurrent requests
│   │
│   ├── llm_eval/
│   │   ├── test_hallucination.py      # Hallucination, faithfulness, relevancy
│   │   └── test_prompt_regression.py  # Prompt consistency, safety testing
│   │
│   └── integration/
│       ├── rag_pipeline.py            # LangChain + ChromaDB RAG agent
│       ├── test_rag_agent.py          # RAG retrieval + answer quality
│       ├── test_ragas_evaluation.py   # Custom Groq RAG scoring
│       └── test_openshift_ai.py       # OpenShift AI + KServe protocol tests
│
├── config/
│   └── test_config.yaml              # Thresholds, endpoints, environments
│
├── conftest.py                        # Shared fixtures, Groq judge, env config
├── pytest.ini                         # pytest config, plugin settings
├── requirements.txt                   # Pinned dependencies
├── TEST_STRATEGY.md                   # Full test strategy document
├── .github/workflows/ci.yml          # GitHub Actions CI pipeline
└── docs/                             # Allure report (GitHub Pages)


---

## ⚡ Quick Start

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
ollama pull nomic-embed-text

# Set Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run all tests
pytest tests/ -v --html=reports/report.html

# Generate Allure report
allure generate reports/allure-results \
  --output reports/allure-report --clean
allure open reports/allure-report
```

---

## 🔧 Configuration

Switch environments in `config/test_config.yaml`:

```yaml
# Switch between local and OpenShift AI
environment: "local"  # or "openshift"

environments:
  local:
    model_name: "llama3.2"
    endpoint: "http://localhost:11434/api/generate"
    protocol: "ollama"
    max_response_time_seconds: 30

  openshift:
    model_name: "llama"
    endpoint: "https://YOUR-KSERVE-ENDPOINT/v2/models/llama/infer"
    protocol: "kserve"
    max_response_time_seconds: 60
```

---

## 🧪 Run Specific Test Layers

```bash
# API tests only
pytest tests/api/ -v

# LLM evaluation only
pytest tests/llm_eval/ -v

# RAG pipeline only
pytest tests/integration/ -v

# Single test file
pytest tests/llm_eval/test_hallucination.py -v

# With Allure reporting
pytest tests/ -v --alluredir=reports/allure-results
```

---

## 📖 Test Strategy

See [TEST_STRATEGY.md](TEST_STRATEGY.md) for full test
strategy including:
- Test layer definitions
- Evaluation metric thresholds
- Environment configuration
- Tool selection rationale

---

## 🤝 Related Projects

- [red-hat-data-services/ods-ci](https://github.com/red-hat-data-services/ods-ci)
  — Red Hat's official OpenShift AI QE repository
  (studied for patterns and contribution opportunities)

---

## 👤 Author

**Alaka Pattnaik**
QA & Engineering Leader | 14+ Years | AI/LLM Test Automation

📍 Bengaluru, India | Immediate Joiner

### Background
- 14+ years Quality Engineering experience
- Led QE at **Epsilon** (2020–2025) — BigData pipeline
  testing on cloud-native infrastructure at scale
- Built this framework during focused sabbatical
  targeting AI/LLM quality engineering

### Expertise
- AI/LLM testing — hallucination detection, RAG
  evaluation, prompt regression
- BigData validation — Kafka, Spark, PySpark, Cassandra
- Cloud-native QE — Kubernetes, OpenShift AI, AWS
- Python/pytest automation frameworks
- CI/CD quality gates — GitHub Actions, Jenkins

### Open To
- Engineering Manager — Quality Engineering
- Staff SDET / Test Architect
- Principal SDET
- AI/LLM QE Leadership roles in Bengaluru

### Connect
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/YOUR-LINKEDIN)
[![GitHub](https://img.shields.IO/badge/GitHub-Follow-black)](https://github.com/alakapatnaik)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## Author

**Alaka Pattnaik**
QA & Engineering Leader | 14+ Years | AI/LLM Test Automation

📍 Bengaluru, India | Immediate Joiner

### Background
- 14+ years of Quality Engineering experience
- Led QE at **Epsilon** (2020–2025) — BigData pipeline testing 
  on cloud-native infrastructure at scale
- Currently building open source AI/LLM test automation 
  frameworks targeting Red Hat OpenShift AI

### Expertise
- AI/LLM testing — hallucination detection, RAG evaluation, 
  prompt regression
- BigData validation — Kafka, Spark, PySpark, Cassandra
- Cloud-native QE — Kubernetes, OpenShift, AWS
- Python/pytest automation frameworks
- CI/CD quality gates — GitHub Actions, Jenkins

### Open To
- Engineering Manager — Quality Engineering
- Staff SDET / Test Architect
- Principal SDET
- AI/LLM QE Leadership roles

### Connect
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/alaka-pattnaik/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/alakapatnaik/agenteval-platform/)

> "AI systems fail differently from traditional software — 
> my framework tests what matters: hallucination, faithfulness, 
> RAG quality, and model serving reliability."


