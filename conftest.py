import pytest
import yaml
import httpx
from deepeval.models.base_model import DeepEvalBaseLLM
from groq import Groq
import os



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


@pytest.fixture(scope="session")
def ollama_Response(model_client, model_endpoint, model_name):
    """ Helper to get model response as plain text """
    def _generate(prompt):
        r = model_client.post(
            model_endpoint,
            json={"model":model_name, "prompt":prompt, "stream":False}
        )
    return r.json()["response"]
return _generate


class GroqJudge(DeepEvalBaseLLM):
    def __init__(self):
        self.client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

    def load_model(self):
        return self.client
    
    def generate(self, prompt: str) -> str:
        response= self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user", "content": prompt}]
        )
        return response.choices[0].message.content

    async def a_generate(self, prompt: str)-> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return "groq-llama3"

@pytest.fixture(scope="session")
def judge_model():
    return GroqJudge()


