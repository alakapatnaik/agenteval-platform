from dotenv import load_dotenv
load_dotenv()

import os
os.environ["OPENAI_API_KEY"] = "dummy-key-not-used"

import pytest
import yaml
import httpx


@pytest.fixture(scope="session")
def config():
    with open("config/test_config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def model_client():
    client = httpx.Client(timeout=60.0)
    yield client
    client.close()

@pytest.fixture(scope="session")
def model_name(config):
    return config["model"]["name"]

@pytest.fixture(scope="session")
def model_endpoint(config):
    return config["model"]["endpoint"]

@pytest.fixture(scope="session")
def ollama_response(model_client, model_endpoint, model_name):
    """Helper to get model response as plain text"""
    def _generate(prompt):
        r = model_client.post(
            model_endpoint,
            json={"model": model_name, "prompt": prompt, "stream": False}
        )
        return r.json()["response"]
    return _generate