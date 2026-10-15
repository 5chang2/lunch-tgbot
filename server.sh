#!/usr/bin/env bash
# 서버(EC2 Ubuntu)에서 봇을 켠다 — 봇 서버(uvicorn)와 ngrok을 nohup으로 띄운다
# 켜기: bash server.sh    끄기: bash server.sh stop    봇 기록 보기: tail -f bot.log
set -u
cd "$(dirname "$0")"

stop() {
  pkill -f "uvicorn main:app"
  pkill -x ngrok
}

if [ "${1:-}" = "stop" ]; then
  stop
  sleep 2
  echo "봇 서버(uvicorn)와 ngrok을 껐어요."
  exit 0
fi

# 1. .env — 토큰과 내 ngrok 주소
if [ ! -f .env ]; then
  echo ".env가 없어요. vi .env 로 만들고, 노트북 .env 내용을 붙여 넣으세요."
  exit 1
fi
chmod 600 .env  # 키가 든 파일은 나만 읽게
if ! grep -q '^TELEGRAM_TOKEN=.' .env; then
  echo ".env에 TELEGRAM_TOKEN이 비어 있어요."
  exit 1
fi
NGROK_URL=$(grep '^NGROK_URL=' .env | cut -d= -f2- | tr -d '\r" ')
NGROK_URL=${NGROK_URL%/}
case "$NGROK_URL" in
  https://*) ;;
  *) echo ".env의 NGROK_URL을 확인해 주세요. https:// 로 시작하는 내 ngrok 주소여야 해요."; exit 1 ;;
esac

# 2. ngrok — 설치와 토큰은 ngrok 대시보드의 Linux 명령을 복사해서 한다
if ! command -v ngrok >/dev/null; then
  echo "ngrok이 없어요. ngrok 대시보드 › Getting Started › Linux 탭의 설치 명령을 붙여 넣고, 다시 bash server.sh"
  exit 1
fi
NGROK_YML=$(ngrok config check 2>/dev/null | sed -n 's/^Valid configuration file at //p')
if ! grep -qs 'authtoken' "$NGROK_YML"; then
  echo "ngrok 토큰이 없어요. 대시보드의 ngrok config add-authtoken ... 줄을 붙여 넣고, 다시 bash server.sh"
  exit 1
fi

# 3. uv — 노트북에서 한 그 설치 명령 (이미 있으면 건너뛴다)
UV="$HOME/.local/bin/uv"
if [ ! -x "$UV" ] && command -v uv >/dev/null; then
  UV=$(command -v uv)
fi
if [ ! -x "$UV" ]; then
  echo "[설치] uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 4. 재료 — uv.lock대로 다시 만든다 (파이썬 3.12도 여기서 받는다)
echo "[준비] uv sync"
"$UV" sync -q || exit 1

# 5. 켜기 — 이미 떠 있으면 끄고 다시. nohup = 창을 닫아도 끄지 마
stop 2>/dev/null
sleep 1
nohup "$UV" run uvicorn main:app > bot.log 2>&1 &
nohup ngrok http 8000 --url "$NGROK_URL" --log stdout > ngrok.log 2>&1 &
echo "[켜는 중] 5초 기다려요..."
sleep 5

# 6. 상태
if pgrep -f "uvicorn main:app" >/dev/null; then
  echo "봇 서버(uvicorn): 켜짐"
else
  echo "봇 서버(uvicorn): 안 켜짐 — bot.log 마지막 줄:"
  tail -n 5 bot.log
  exit 1
fi
if grep -q 'ERR_NGROK_334' ngrok.log; then
  echo "ngrok: 안 켜짐 — 같은 주소가 다른 곳에서 켜져 있어요. 노트북의 ngrok을 먼저 끄고, 다시 bash server.sh"
  exit 1
elif pgrep -x ngrok >/dev/null; then
  echo "ngrok: $NGROK_URL"
else
  echo "ngrok: 안 켜짐 — ngrok.log 마지막 줄:"
  tail -n 5 ngrok.log
  exit 1
fi
echo
echo "폰에서 /weather 를 보내 보세요. 봇 기록: tail -f bot.log  (빠져나오기: Ctrl+C)"
