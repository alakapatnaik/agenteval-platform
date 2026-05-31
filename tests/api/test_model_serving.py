import pytest
import time

def generate(client, endpoint, model, prompt):
    response = client.post(
        endpoint,
        json={"model":model, "prompt": prompt, "stream":False}
    )
    return response

class TestModelServing:

    def test_model_returns_200(self, model_client, model_endpoint, model_name):
        response = generate(model_client, model_endpoint, model_name, "Say Hello")
        assert response.status_code == 200

    def test_response_contains_text(self, model_client, model_endpoint, model_name):
        response = generate(model_client, model_endpoint, model_name, "What is 2+2")
        data = response.json()
        assert "response" in data
        assert len(data["response"].strip()) > 0

    def test_response_latency(self, model_client, model_endpoint, model_name, config):
        max_time = config["environments"]["local"]["max_response_time_seconds"]
        start = time.time()
        generate(model_client,model_endpoint, model_name, "Say Hello")
        elapsed = time.time() - start
        assert elapsed < max_time, f"Too slow:{elapsed:.2f}s (limit: {max_time}s)"

    def test_model_handles_empty_prompt(self, model_client, model_endpoint, model_name):
        response = generate(model_client, model_endpoint, model_name, "")
        assert response.status_code in [200, 400]

    def test_response_is_valid_json(self, model_client,model_endpoint,model_name):
        response = generate(model_client, model_endpoint, model_name, "Tell me a fact")
        try:
            response.json()
        except Exception:
            pytest.fail("Response is not valid Json")
            
