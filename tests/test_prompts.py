# 6단계 확인: uv run pytest tests/test_prompts.py
from prompts import build_prompt_v2, build_prompt_v3


def test_v2_has_weather_and_meals():
    system = build_prompt_v2("비, 12.0°C, 강수 3.0mm", [("2026-10-15 12:31", "김치찌개")])
    assert "비, 12.0°C" in system
    assert "김치찌개" in system


def test_v2_without_meals():
    assert "기록 없음" in build_prompt_v2("맑음", [])


def test_v3_lists_found_places():
    place = {"이름": "청해루", "분류": "중국요리", "대표 메뉴": "짜장 7,000원", "영업시간": "11:00~21:00",
             "주소": "성동구 자동차시장1길 24-1 2층", "캠퍼스에서 직선거리(m)": "389",
             "출처": "https://place.map.kakao.com/9515299"}
    system = build_prompt_v3("맑음", [], [place])
    assert "청해루" in system
    assert "https://place.map.kakao.com/9515299" in system


def test_v3_says_when_nothing_found():
    assert "찾지 못했다" in build_prompt_v3("맑음", [], [])
