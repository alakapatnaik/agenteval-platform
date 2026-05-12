import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import(
    AnswerRelevancyMetric,
    FaithfullnessMetric,
    HallucinationMetric
)

class TestHallucination:

    @pytest.mark.skip(reason ="DeepEval integration")
    def test_model_does_not_hallucinate_facts(self):
        """Model response should be factually grounded"""
        pass

    @pytest.mark.skip(reason="DeepEval integration")
    def test_hallucination_score_below_threshold(self):
        """Hallucination score must stay below configured threshold"""
        pass

    @pytest.mark.skip(reason = "DeepEval integration")
    def test_response_faithful_to_context(self):
        """Response must be faithful to provide context"""
        pass

    def test_answer_relevancy(self, ollama_response):
        """ MOdel answer must be relevant to the question asked"""
        prompt = " What is Red Hat OpenShift"
        actual_output = ollama_response(prompt)

        metric = AnswerRelevancyMetric(
            threshold= 0.7,
            model="gpt-4o",
            include_reason=True
        )
        test_case = LLMTestCase(
            input = prompt,
            actual_output= actual_output
        )
        metric.measure(test_case)

        print(f"\nRelevancy score: {metric.score}")
        print(f"reason: {metric.reason}")
        assert metric.score >= 0.7, f"Relevancy too low: {metric.score}"

    def test_no_hallucination_with_context(self, ollama_response):
        """ Model must not hallucinate beyond provided context"""
        context = [
            "Red Hat Openshift AI is a platform for running"
            "AI/ML workloads on kubernetes. It supports model"
            "serving using KServe and integrates with Jupyter notebooks."
        ]
        prompt = "What does Red Hat Openshift AI support?"
        actual_output = ollama_response(prompt)

        metric = HallucinationMetric(
            threshold=0.3,
            model="gpt-4o",
        )
        test_case = LLMTestCase(
            input= prompt,
            actual_output= actual_output,
            context=context
        )
        metric.measure(test_case)

        print(f"\nhallucination score: {metric.score}")
        print(f"\nReason: {metric.reason}")
        assert metric.score <= 0.3, f"Hallucination too high: {metric.score}"


    def test_faithfulness_to_context(self, ollama_response):
        """ Model response must be faithful to retrieved context """
        retrieval_context= [
            "KServe is a Kubernetes-native model inference platform."
            "It supports Tensorflow, pytorch and scikit-learn models"
            "KServe handles autoscaling and canary rollouts"
        ]
        prompt = "What model does Kserve support?"
        actual_output = ollama_response(prompt)

        metric = FaithfulnessMetric(
            threshold=0.8,
            model="gpt-4o"
        )
        test_case = LLMTestCase(
            input = prompt,
            actual_output = actual_output,
            retrieval_context= retrieval_context
        )
        metric.measure(test_case)

        print(f"\nFaithfulness score: {metric.score}")
        print(f"Reason: {metric.reason}")
        assert metric.score >= 0.8, f"Faithfullness too low: {metric.score}"
