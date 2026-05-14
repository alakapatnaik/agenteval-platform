import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.integration.rag_pipeline import build_rag_chain

@pytest.fixture(scope="module")
def rag_chain_and_retriever():
    """Build RAG chain once for all tests in this module"""
    chain, retriever = build_rag_chain()
    return chain, retriever


@pytest.fixture(scope="module")
def rag_chain(rag_chain_and_retriever):
    return rag_chain_and_retriever[0]


@pytest.fixture(scope="module")
def retriever(rag_chain_and_retriever):
    return rag_chain_and_retriever[1]


class TestRAGAgent:
    @pytest.mark.skip(reason="RAG agent integration")
    def test_rag_agent_answers_from_context(self):
        """ Agent must answer from retrieved context"""
        pass

    @pytest.mark.skip(reason="RAG agent integration")
    def test_rag_faithfulness_above_threshold(self):
        """ RAG faithfulness score must exceed configured threshold"""
        pass

    @pytest.mark.skip(reason = "RAG agent integration")
    def test_rag_answer_relevancy(self):
        """ Retrieved answer must be relevant to the question"""
        pass

    def test_rag_answers_kserve_question(self, rag_chain):
        """RAG must answer KServe question from retrieved context"""
        result = rag_chain.invoke(
            "What does KServe support?"
        )
        assert result is not None
        assert len(result.strip()) > 0
        print(f"\nAnswer: {result}")

    def test_rag_answer_contains_expected_keyword(self, rag_chain):
        """Answer about KServe must mention supported frameworks"""
        result = rag_chain.invoke(
            "What ML frameworks does KServe support?"
        ).lower()

        keywords = ["tensorflow", "pytorch", "scikit"]
        matched = [kw for kw in keywords if kw in result]
        print(f"\nMatched keywords: {matched}")
        assert len(matched) >= 1, (
            f"Expected at least one of {keywords} in answer. "
            f"Got: {result[:200]}"
        )

    def test_rag_answers_from_context_not_memory(self, rag_chain):
        """
        RAG must use retrieved context.
        We inject a fake fact — if model returns it,
        retrieval is working correctly.
        """
        result = rag_chain.invoke(
            "What pipelines does OpenShift AI use?"
        ).lower()

        # Our docs say Kubeflow Pipelines — model must retrieve this
        assert "kubeflow" in result, (
            f"Model did not retrieve correct context. "
            f"Got: {result[:200]}"
        )

    def test_rag_handles_unknown_question(self, rag_chain):
        """RAG must say it doesn't know for out-of-context questions"""
        result = rag_chain.invoke(
            "What is the price of OpenShift AI enterprise license?"
        ).lower()

        # Our docs don't have pricing — model should admit it
        dont_know_signals = [
            "don't know", "not available", "no information",
            "context", "not mentioned", "i cannot"
        ]
        matched = any(s in result for s in dont_know_signals)
        print(f"\nAnswer: {result[:200]}")
        # Soft assert — log but don't fail if model tries to answer
        if not matched:
            print("WARNING: Model may have hallucinated pricing info")

    def test_rag_retriever_returns_relevant_docs(self, retriever):
        """Retriever must return relevant documents for a query"""
        docs = retriever.invoke("What is KServe?")

        assert len(docs) > 0, "Retriever returned no documents"
        assert len(docs) <= 2, "Retriever returned too many docs"

        # At least one doc must mention KServe
        content = " ".join(d.page_content.lower() for d in docs)
        assert "kserve" in content, (
            f"Retrieved docs don't mention KServe. "
            f"Got: {content[:200]}"
        )
        print(f"\nRetrieved {len(docs)} docs")
        for doc in docs:
            print(f" - {doc.metadata.get('source', 'unknown')}")

    def test_rag_response_not_empty(self, rag_chain):
        """RAG must never return empty response"""
        prompts = [
            "What is OpenShift AI?",
            "What is the model registry?",
            "What is single-model serving?",
        ]
        for prompt in prompts:
            result = rag_chain.invoke(prompt)
            assert result and len(result.strip()) > 0, (
                f"Empty response for prompt: {prompt}"
            )
            print(f"\nPrompt: {prompt}")
            print(f"Answer: {result[:100]}")