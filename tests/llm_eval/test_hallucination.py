import pytest
from groq import Groq
import os


def judge_response(question: str, answer: str, context: str = None) -> dict:
    """Use Groq directly as judge to evaluate LLM response quality"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    if context:
        prompt = f"""You are an AI evaluation judge.

Question: {question}
Context: {context}
Answer: {answer}

Evaluate the answer on these criteria and respond ONLY in this exact format with no extra text:
RELEVANCY: <number between 0 and 1>
FAITHFULNESS: <number between 0 and 1>
HALLUCINATION: <number between 0 and 1>
REASON: <one line explanation>"""
    else:
        prompt = f"""You are an AI evaluation judge.

Question: {question}
Answer: {answer}

Evaluate the answer and respond ONLY in this exact format with no extra text:
RELEVANCY: <number between 0 and 1>
FAITHFULNESS: 0.9
HALLUCINATION: <number between 0 and 1>
REASON: <one line explanation>"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    print(f"\nJudge raw output:\n{raw}")

    scores = {}
    for line in raw.strip().split("\n"):
        try:
            if line.startswith("RELEVANCY:"):
                scores["relevancy"] = float(line.split(":")[1].strip())
            elif line.startswith("FAITHFULNESS:"):
                scores["faithfulness"] = float(line.split(":")[1].strip())
            elif line.startswith("HALLUCINATION:"):
                scores["hallucination"] = float(line.split(":")[1].strip())
            elif line.startswith("REASON:"):
                scores["reason"] = line.split(":", 1)[1].strip()
        except (ValueError, IndexError):
            continue

    return scores


class TestHallucination:

    def test_answer_relevancy(self, ollama_response):
        """Model answer must be relevant to the question asked"""
        prompt = "What is Red Hat OpenShift?"
        actual_output = ollama_response(prompt)

        print(f"\nModel output: {actual_output[:200]}")
        scores = judge_response(question=prompt, answer=actual_output)

        relevancy = scores.get("relevancy", 0)
        print(f"Relevancy score: {relevancy}")
        print(f"Reason: {scores.get('reason', 'N/A')}")
        assert relevancy >= 0.7, f"Relevancy too low: {relevancy}"

    def test_no_hallucination_with_context(self, ollama_response):
        """Model must not hallucinate beyond provided context"""
        context = (
            "Red Hat OpenShift AI is a platform for running "
            "AI/ML workloads on Kubernetes. It supports model "
            "serving using KServe and integrates with Jupyter notebooks."
        )
        prompt = "What does Red Hat OpenShift AI support?"
        actual_output = ollama_response(prompt)

        print(f"\nModel output: {actual_output[:200]}")
        scores = judge_response(
            question=prompt,
            answer=actual_output,
            context=context
        )

        hallucination = scores.get("hallucination", 1)
        print(f"Hallucination score: {hallucination}")
        print(f"Reason: {scores.get('reason', 'N/A')}")
        assert hallucination <= 0.5, f"Hallucination too high: {hallucination}"

    def test_faithfulness_to_context(self, ollama_response):
        """Model response must be faithful to retrieved context"""
        context = (
            "KServe is a Kubernetes-native model inference platform. "
            "It supports TensorFlow, PyTorch, and scikit-learn models. "
            "KServe handles autoscaling and canary rollouts."
        )
        prompt = "What models does KServe support?"
        actual_output = ollama_response(prompt)

        print(f"\nModel output: {actual_output[:200]}")
        scores = judge_response(
            question=prompt,
            answer=actual_output,
            context=context
        )

        faithfulness = scores.get("faithfulness", 0)
        print(f"Faithfulness score: {faithfulness}")
        print(f"Reason: {scores.get('reason', 'N/A')}")
        assert faithfulness >= 0.5, f"Faithfulness too low: {faithfulness}"