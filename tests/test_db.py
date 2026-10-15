# 4단계 확인: uv run pytest tests/test_db.py
import re
import threading

import db


def test_now_format():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", db.now())


def test_save_and_recent():
    conn = db.connect(":memory:")
    assert db.recent_meals(conn) == []
    db.save_meal(conn, "김치찌개", "2026-10-15 12:31")
    db.save_meal(conn, "마라탕", "2026-10-16 12:40")
    assert db.recent_meals(conn) == [("2026-10-16 12:40", "마라탕"), ("2026-10-15 12:31", "김치찌개")]


def test_same_minute_keeps_order():
    conn = db.connect(":memory:")
    db.save_meal(conn, "김치찌개", "2026-10-15 12:31")
    db.save_meal(conn, "마라탕", "2026-10-15 12:31")
    assert db.recent_meals(conn)[0] == ("2026-10-15 12:31", "마라탕")


def test_limit():
    conn = db.connect(":memory:")
    for day in range(1, 8):
        db.save_meal(conn, f"메뉴{day}", f"2026-10-0{day} 12:00")
    assert len(db.recent_meals(conn)) == 5
    assert len(db.recent_meals(conn, limit=3)) == 3


def test_survives_reconnect(tmp_path):
    # 파일에 쓰고 연결을 끊었다가 다시 열어도 남는다 = 봇을 껐다 켜도 남는다
    path = str(tmp_path / "lunch.db")
    conn = db.connect(path)
    db.save_meal(conn, "김치찌개", "2026-10-15 12:31")
    conn.close()
    assert db.recent_meals(db.connect(path)) == [("2026-10-15 12:31", "김치찌개")]


def test_usable_from_another_thread():
    # FastAPI는 요청마다 다른 일꾼(스레드)이 처리한다. 다른 스레드에서 저장해도 에러가 나면 안 된다
    conn = db.connect(":memory:")
    errors = []

    def worker():
        try:
            db.save_meal(conn, "김치찌개", "2026-10-15 12:31")
        except Exception as e:
            errors.append(e)

    t = threading.Thread(target=worker)
    t.start()
    t.join()
    assert errors == []
    assert db.recent_meals(conn) == [("2026-10-15 12:31", "김치찌개")]
