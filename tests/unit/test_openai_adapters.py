import sys
from types import SimpleNamespace

from kernel_rag.embeddings.openai_embedder import OpenAIEmbedder
from kernel_rag.generation.llm_service import OpenAILLMService


class _FakeEmbeddingsAPI:
    def __init__(self):
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        data = [
            SimpleNamespace(index=1, embedding=[0.0, 1.0]),
            SimpleNamespace(index=0, embedding=[1.0, 0.0]),
        ]
        if len(kwargs["input"]) == 1:
            data = [SimpleNamespace(index=0, embedding=[1.0, 0.0])]
        return SimpleNamespace(data=data)


class _FakeResponsesAPI:
    def __init__(self):
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return SimpleNamespace(output_text=" grounded answer ")


class _FakeOpenAI:
    instances = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.embeddings = _FakeEmbeddingsAPI()
        self.responses = _FakeResponsesAPI()
        self.__class__.instances.append(self)


def test_embedding_adapter_uses_embeddings_api_and_preserves_input_order(monkeypatch):
    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=_FakeOpenAI))
    embedder = OpenAIEmbedder("test-key", "text-embedding-3-small")
    vectors = embedder.embed_documents(["one", "two"])
    assert vectors == [[1.0, 0.0], [0.0, 1.0]]
    client = _FakeOpenAI.instances[-1]
    assert client.embeddings.last_kwargs["model"] == "text-embedding-3-small"
    assert client.embeddings.last_kwargs["input"] == ["one", "two"]
    assert client.embeddings.last_kwargs["encoding_format"] == "float"


def test_llm_adapter_uses_responses_api(monkeypatch):
    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=_FakeOpenAI))
    llm = OpenAILLMService("test-key", "gpt-5.6-terra", reasoning_effort="low", max_output_tokens=500)
    result = llm.generate(instructions="ground it", input_text="question")
    assert result == "grounded answer"
    client = _FakeOpenAI.instances[-1]
    assert client.responses.last_kwargs == {
        "model": "gpt-5.6-terra",
        "instructions": "ground it",
        "input": "question",
        "reasoning": {"effort": "low"},
        "max_output_tokens": 500,
        "store": False,
    }
