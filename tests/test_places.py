# 6단계 확인: uv run pytest tests/test_places.py
from places import load_places, place_text, search


def test_load_sample():
    places = load_places("places_sample.csv")
    assert len(places) == 40
    assert places[0]["이름"] == "고향식당"


def test_search_jjajangmyeon():
    found = search("짜장면 먹고 싶어", load_places("places_sample.csv"))
    assert len(found) > 0
    for place in found:
        assert "짜장면" in place["대표 메뉴"]


def test_search_limit():
    found = search("분식", load_places("places_sample.csv"), limit=2)
    assert len(found) == 2


def test_search_cannot_find_eolkeun():
    # '얼큰한'은 목록 어디에도 없다. 뜻이 비슷한 '짬뽕'·'해장국'은 키워드 검색으로 못 찾는다
    assert search("얼큰한 거", load_places("places_sample.csv")) == []


def test_place_text_has_source():
    place = load_places("places_sample.csv")[0]
    assert "출처: https://place.map.kakao.com/11036200" in place_text(place)
