import pytest
import yaml
import httpx

@pytest.fixture(scope ="session")
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

