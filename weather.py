# 지금 캠퍼스 날씨를 Open-Meteo에서 가져온다. 가입·키가 필요 없는 공개 API다.
# 날씨 데이터: Open-Meteo.com (CC BY 4.0) — 쓰는 곳에 출처를 밝혀야 한다
import requests

# 새싹 성동캠퍼스(장한평역 근처)의 대략 위치. 지도 앱에서 확인한 값으로 바꿔도 된다
LATITUDE = 37.56
LONGITUDE = 127.06
URL = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo는 날씨를 숫자(WMO 코드)로만 준다 → 우리가 글로 바꾼다
WEATHER_NAMES = {
    0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
    45: "안개", 48: "안개",
    51: "이슬비", 53: "이슬비", 55: "이슬비", 56: "어는 이슬비", 57: "어는 이슬비",
    61: "비", 63: "비", 65: "강한 비", 66: "어는 비", 67: "어는 비",
    71: "눈", 73: "눈", 75: "많은 눈", 77: "싸락눈",
    80: "소나기", 81: "소나기", 82: "강한 소나기", 85: "눈 소나기", 86: "눈 소나기",
    95: "뇌우", 96: "우박 뇌우", 97: "강한 뇌우", 99: "우박 뇌우",
}


def get_weather():
    """{'temperature': 14.6, 'precipitation': 0.0, 'code': 0} — 실패하면 None"""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,precipitation,weather_code",
        "timezone": "Asia/Seoul",
    }
    try:
        # timeout: 날씨 서버가 느려도 봇 전체가 멈춰 있지 않게 5초만 기다린다
        response = requests.get(URL, params=params, timeout=5)
        response.raise_for_status()  # 200이 아니면 에러로
    except requests.RequestException as e:
        print(f"[날씨 오류] {e}")
        return None
    current = response.json()["current"]  # JSON → 파이썬 dict
    return {
        "temperature": current["temperature_2m"],
        "precipitation": current["precipitation"],
        "code": current["weather_code"],
    }


def describe(weather):
    # 표에 없는 코드가 와도 멈추지 않게 get으로 꺼낸다
    name = WEATHER_NAMES.get(weather["code"], f"알 수 없음({weather['code']})")
    return f"{name}, {weather['temperature']}°C, 강수 {weather['precipitation']}mm"


def weather_text():
    weather = get_weather()
    if weather is None:
        return "지금은 날씨를 가져오지 못했어요."
    return f"지금 캠퍼스 날씨: {describe(weather)}\n(날씨 데이터: Open-Meteo.com)"
