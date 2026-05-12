# AI/LLM Test Strategy — agenteval-platform-openshift

## What This Project Tests
End-to-end quality validation for LLM model serving pipelines,
targeting Red Hat OpenShift AI platform.

## Why AI Systems Need Different Testing
Traditional software returns deterministic outputs.
LLMs are non-deterministic — the same input can return
different outputs. This requires:
- Scoring responses, not just asserting equality
- Evaluating quality metrics, not just pass/fail
- Testing behaviour across multiple runs

## Test Layers

### Layer 1 — Model Serving API (Days 1–2)
- HTTP status codes and response structure
- Latency and SLA validation
- Edge case inputs (empty, long, special characters)
- Concurrent request handling

### Layer 2 — LLM Output Quality (Days 5–6)
- Hallucination detection using DeepEval
- Prompt regression — same prompt, consistent output
- Toxicity and bias scoring
- Response relevancy scoring

### Layer 3 — RAG Pipeline Quality (Days 6–7)
- Retrieval faithfulness using Ragas
- Answer relevancy scoring
- Context precision and recall
- End-to-end RAG agent validation

### Layer 4 — OpenShift AI Integration (Days 7–9)
- Model serving endpoint validation on real cluster
- KServe inference service health checks
- Model lifecycle testing (deploy, serve, scale, delete)
- Pipeline orchestration validation

## Tools
| Tool | Purpose |
|------|---------|
| pytest + httpx | API test execution |
| DeepEval | LLM output quality scoring |
| Ragas | RAG pipeline evaluation |
| LangChain + Ollama | Local RAG agent |
| ChromaDB | Vector store |
| Groq | Multi-provider testing |
| GitHub Actions | CI pipeline |
| Allure | Test reporting |

## Test Environments
| Environment | When | Purpose |
|-------------|------|---------|
| Local Ollama | Days 1–6 | Framework development |
| Red Hat Sandbox | Days 7–10 | Real OpenShift AI validation |

## Success Metrics
- Hallucination score below 0.3
- RAG faithfulness above 0.8
- API latency under 30 seconds
- Zero critical failures in CI pipeline