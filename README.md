# 오늘 뭐 먹지? — 점심 추천 텔레그램 봇

새싹 성동캠퍼스 SW(AI핵심) 4기 10/16 실습용 시작 레포입니다. 어제(10/15) 손으로 만든 메아리 봇에서 이어집니다.

## 시작하기

1. 이 페이지 오른쪽 위 **Fork → Create fork** (내 계정에 `lunch-bot`이 생깁니다. 공개 레포입니다)
2. 내 레포를 clone합니다.

```bash
cd ~/SD4
git clone https://github.com/<내 아이디>/lunch-bot.git
cd lunch-bot
uv sync
```

3. `.env`를 만듭니다. Claude는 `.env`를 읽지 못하게 잠겨 있으니 **직접** 만듭니다.

```bash
cp .env.example .env
```

VS Code로 `.env`를 열어 `TELEGRAM_TOKEN`(BotFather가 준 토큰)과 `NGROK_URL`(내 ngrok 주소, `https://`부터)을 채웁니다. 어제 `echo-bot`의 `.env`가 있으면 거기서 토큰을 옮깁니다.

4. 봇 서버를 켜고(터미널 1), ngrok을 켭니다(터미널 2).

```bash
uv run uvicorn main:app --reload
ngrok http 8000 --url https://<내 ngrok 주소>
```

5. 텔레그램에 등록할 주소를 만듭니다(터미널 3).

```bash
uv run make_webhook_url.py
```

나온 주소 중 `setWebhook`을 브라우저에서 열고, `getWebhookInfo`의 `url`이 **내** ngrok 주소인지 확인합니다. 그다음 폰에서 `/start` `/help` `/lunch` `/lotto` `/weather`를 보내 봅니다.

## 무엇이 들어 있나

| 파일 | 상태 | 누가 채우나 |
| --- | --- | --- |
| `main.py` | 어제 친 메아리 + 명령(`/start` `/help` `/lunch` `/lotto`) + `/weather` | 내가 고친다 (`elif` 붙이기) |
| `make_webhook_url.py` | `.env`를 읽어 `getMe` · `setWebhook` · `getWebhookInfo` 주소를 만들어 준다 | — |
| `.env.example` | `.env`에 넣을 이름 목록 (값은 비어 있음) | — |
| `server.sh` | 서버(EC2 Ubuntu)에서 uv 설치 · `uv sync` · 봇 서버(uvicorn)와 ngrok을 `nohup`으로 켠다 (`bash server.sh` / `bash server.sh stop`) | — |
| `weather.py` | **채워져 있음** — `/weather`가 바로 된다 | — |
| `db.py` | 식사 기록 | Claude와 같이 |
| `ai.py` · `prompts.py` | AI 추천 | Claude와 같이 |
| `places.py` · `places_sample.csv` | 캠퍼스 주변 식당 찾기 | Claude와 같이 |
| `tests/` | 다 채웠는지 확인하는 시험지 | 고치지 않는다 |
| `CLAUDE.md` · `.claude/settings.json` · `.gitignore` | 어제 직접 만든 것의 강사 버전 | — |

`db.py` 같은 파일에는 **함수 이름과 설명만** 있고 내용은 비어 있습니다(`NotImplementedError`). 설명대로 채우고 시험을 돌려 통과하면 그 단계가 끝납니다.

```bash
uv run pytest tests/test_db.py
```

처음에는 실패(빨간색)입니다. 채우면 통과(초록색)로 바뀝니다. `tests/test_weather.py`는 처음부터 통과합니다.

## 올리면 안 되는 것

`.env`(봇 토큰 · API 키)와 `lunch.db`(내 기록)는 `.gitignore`에 들어 있어 Git에 올라가지 않습니다.

날씨 데이터: [Open-Meteo.com](https://open-meteo.com/) (CC BY 4.0) · 식당 데이터: 카카오맵에서 모은 40곳(2026-10-15~16, 각 줄의 출처 링크)
