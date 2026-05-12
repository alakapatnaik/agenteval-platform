import pytest
import time
import httpx
def generate(client, endpoint, model, prompt):
    return client.post(
        endpoint,
        json= {"model": model, "prompt":prompt,"stream":False}
    )

class TestModelEdgeCases:
    def test_long_prompt(self, model_client, model_endpoint, model_name):
        long_prompt = "Explain artificial intelligence. " * 50
        r = generate(model_client, model_endpoint, model_name, long_prompt)
        assert r.status_code == 200

    def test_special_characters(self, model_client, model_endpoint, model_name):
        r = generate(model_client, model_endpoint, model_name,"What is 2+2? <test> {json} @#$%")
        assert r.status_code == 200

    def test_multilingual_prompt(self, model_client, model_endpoint, model_name):
        r = generate(model_client, model_endpoint, model_name,
        "Bonjour, comment allez-vous?")
        assert r.status_code == 200
        data= r.json()
        assert len(data["response"].strip())> 0

    def test_response_has_no_null_fields(self, model_client, model_endpoint, model_name):
        r = generate(model_client, model_endpoint, model_name, "Say Hello")
        data = r.json()
        assert data.get("model") is not None
        assert data.get("response") is not None
        assert data.get("done") is not None
    
    def test_concurrent_requests(self, model_endpoint, model_name):
        # model should handle multiple simultaneous requests
        import threading
        results =[]

        def call_model():
            client = httpx.Client(timeout = 60.0)
            r = client.post(
                model_endpoint,
                json={"model":model_name, "prompt":"Say Hello", "stram":false}
            )
            results.append(r.status_code)
            client.close()

            threads = [threading.Thread(target=call_model) for _ in range(3)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            assert all(code == 200 for code in results), f"some requests failed: {results}"



    