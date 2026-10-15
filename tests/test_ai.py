# 5단계 확인: uv run pytest tests/test_ai.py  (진짜 AI는 부르지 않는다)
import ai


def test_fake(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "fake")
    assert ai.ask_ai("지침", "배고파") == ai.FAKE_ANSWER


def test_empty_provider_is_fake(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "")
    assert ai.ask_ai("지침", "배고파") == ai.FAKE_ANSWER


def test_openai_without_model(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "openai")
    monkeypatch.delenv("AI_MODEL", raising=False)
    assert ai.ask_ai("지침", "배고파") == "AI_MODEL이 .env에 없어요."


def test_openai_without_key(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "openai")
    monkeypatch.setenv("AI_MODEL", "gpt-6-luna")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert ai.ask_ai("지침", "배고파") == "OPENAI_API_KEY가 .env에 없어요."
