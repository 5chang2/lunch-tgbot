"""6단계 — 캠퍼스 주변 식당 목록을 읽고, 질문에 맞는 식당을 찾는다

- places_sample.csv: 카카오맵에서 모은 40곳 (2026-10-15~16 기준)
- 열: 이름, 분류, 대표 메뉴, 영업시간, 주소, 캠퍼스에서 직선거리(m), 출처
- 확인: uv run pytest tests/test_places.py
"""


def load_places(path):
    """CSV 파일을 [{"이름": ..., "분류": ..., ...}, ...]로 읽는다.

    - 첫 줄(열 이름)을 열쇠로 쓴다 (csv.DictReader)
    - encoding="utf-8" (안 적으면 Windows에서 한글이 깨진다)
    """
    raise NotImplementedError("Claude와 같이 채울 곳")


def search(question, places, limit=5):
    """질문에 맞는 식당을 찾는다 (간단한 키워드 검색).

    - 질문을 띄어쓰기로 나누고 두 글자 이상 단어만 쓴다
    - 이름 · 분류 · 대표 메뉴를 이어 붙인 글에 단어가 들어 있으면 1점씩
    - 1점 이상인 식당을 점수 높은 순으로 limit개. 점수가 같으면 목록 순서대로
    """
    raise NotImplementedError("Claude와 같이 채울 곳")


def place_text(place):
    """식당 하나를 AI 지침에 넣을 한 줄로.

    모양: "{이름}({분류}) — 대표 메뉴: {대표 메뉴} · 영업: {영업시간} · 캠퍼스에서 직선 {거리}m · 출처: {출처}"
    """
    raise NotImplementedError("Claude와 같이 채울 곳")
