import pytest
import httpx
import time
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
))


def call_model(client, endpoint, model_name, prompt, protocol):
    """
    Unified model caller — handles both Ollama and KServe
    protocols transparently
    """
    if protocol == "ollama":
        response = client.post(
            endpoint,
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        return response, response.json().get("response", "")

    elif protocol == "kserve":
        response = client.post(
            endpoint,
            json={
                "inputs": [{
                    "name": "text_input",
                    "shape": [1],
                    "datatype": "BYTES",
                    "data": [prompt]
                }]
            }
        )
        outputs = response.json().get("outputs", [{}])
        text = outputs[0].get("data", [""])[0]
        return response, text

    else:
        raise ValueError(f"Unknown protocol: {protocol}")


class TestOpenShiftAIServing:

    def test_model_endpoint_reachable(
        self, model_client, model_endpoint,
        model_name, protocol
    ):
        """Model serving endpoint must be reachable"""
        response, text = call_model(
            model_client, model_endpoint,
            model_name, "Say hello", protocol
        )
        assert response.status_code == 200, (
            f"Endpoint unreachable: {response.status_code}"
        )
        print(f"\nEndpoint: {model_endpoint}")
        print(f"Protocol: {protocol}")
        print(f"Response: {text[:100]}")

    def test_model_response_not_empty(
        self, model_client, model_endpoint,
        model_name, protocol
    ):
        """Model must return non-empty response"""
        response, text = call_model(
            model_client, model_endpoint,
            model_name, "What is Kubernetes?", protocol
        )
        assert response.status_code == 200
        assert len(text.strip()) > 0, "Empty response from model"
        print(f"\nResponse length: {len(text)} chars")

    def test_model_latency_within_sla(
        self, model_client, model_endpoint,
        model_name, protocol, config
    ):
        """Model must respond within configured SLA"""
        env_name = config.get("environment", "local")
        max_time = config["environments"][env_name][
            "max_response_time_seconds"
        ]

        start = time.time()
        call_model(
            model_client, model_endpoint,
            model_name, "Say hello", protocol
        )
        elapsed = time.time() - start

        print(f"\nLatency: {elapsed:.2f}s (SLA: {max_time}s)")
        assert elapsed < max_time, (
            f"Latency {elapsed:.2f}s exceeds SLA {max_time}s"
        )

    def test_model_handles_openshift_ai_question(
        self, model_client, model_endpoint,
        model_name, protocol
    ):
        """Model must answer OpenShift AI domain questions"""
        response, text = call_model(
            model_client, model_endpoint,
            model_name,
            "What is Red Hat OpenShift AI?",
            protocol
        )
        assert response.status_code == 200
        keywords = ["openshift", "kubernetes", "ai", "model"]
        text_lower = text.lower()
        matched = [kw for kw in keywords if kw in text_lower]
        print(f"\nMatched keywords: {matched}")
        assert len(matched) >= 1, (
            f"Response doesn't mention OpenShift AI concepts. "
            f"Got: {text[:200]}"
        )

    def test_model_schema_validation(
        self, model_client, model_endpoint,
        model_name, protocol
    ):
        """Response schema must match expected protocol format"""
        if protocol == "ollama":
            response, _ = call_model(
                model_client, model_endpoint,
                model_name, "Say hello", protocol
            )
            data = response.json()
            assert "response" in data
            assert "model" in data
            assert "done" in data
            print(f"\nOllama schema valid: {list(data.keys())}")

        elif protocol == "kserve":
            response, _ = call_model(
                model_client, model_endpoint,
                model_name, "Say hello", protocol
            )
            data = response.json()
            assert "outputs" in data, (
                f"KServe response missing 'outputs': {data}"
            )
            print(f"\nKServe schema valid: {list(data.keys())}")

    def test_concurrent_requests(
        self, model_endpoint, model_name, protocol
    ):
        """Model must handle 3 concurrent requests"""
        import threading
        results = []
        errors = []

        def call():
            try:
                client = httpx.Client(timeout=60.0)
                response, text = call_model(
                    client, model_endpoint,
                    model_name, "Say hello", protocol
                )
                results.append(response.status_code)
                client.close()
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=call)
                   for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print(f"\nConcurrent results: {results}")
        assert not errors, f"Errors: {errors}"
        assert all(s == 200 for s in results), (
            f"Some failed: {results}"
        )