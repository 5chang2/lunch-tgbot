# 3단계 확인: uv run pytest tests/test_weather.py  (진짜 인터넷은 부르지 않는다)
import requests

import weather


class FakeResponse:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"{self.status_code}")


def test_get_weather_reads_current(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        assert "open-meteo" in url
        assert params["timezone"] == "Asia/Seoul"
        return FakeResponse({"current": {"temperature_2m": 14.6, "precipitation": 0.0, "weather_code": 0}})

    monkeypatch.setattr(requests, "get", fake_get)
    assert weather.get_weather() == {"temperature": 14.6, "precipitation": 0.0, "code": 0}


def test_get_weather_returns_none_when_offline(monkeypatch):
    def broken_get(*args, **kwargs):
        raise requests.ConnectionError("인터넷 끊김")

    monkeypatch.setattr(requests, "get", broken_get)
    assert weather.get_weather() is None


def test_describe():
    assert weather.describe({"temperature": 14.6, "precipitation": 0.0, "code": 0}) == "맑음, 14.6°C, 강수 0.0mm"


def test_describe_unknown_code():
    assert "알 수 없음(52)" in weather.describe({"temperature": 1, "precipitation": 0, "code": 52})


def test_weather_text_ok(monkeypatch):
    monkeypatch.setattr(weather, "get_weather", lambda: {"temperature": 12.0, "precipitation": 3.0, "code": 61})
    text = weather.weather_text()
    assert text.startswith("지금 캠퍼스 날씨: 비, 12.0°C, 강수 3.0mm")
    assert "Open-Meteo.com" in text


def test_weather_text_when_fail(monkeypatch):
    monkeypatch.setattr(weather, "get_weather", lambda: None)
    assert weather.weather_text() == "지금은 날씨를 가져오지 못했어요."
