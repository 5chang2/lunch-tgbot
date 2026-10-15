# .env를 읽어서 브라우저에 붙여 넣을 텔레그램 주소를 만들어 준다
# 실행: uv run make_webhook_url.py
import os

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN", "").strip()
server_url = os.getenv("NGROK_URL", "").strip().rstrip("/")

if not token:
    print(".env에 TELEGRAM_TOKEN이 없어요. BotFather가 준 토큰을 넣어 주세요.")
    raise SystemExit(1)
if not server_url.startswith("https://"):
    print(".env의 NGROK_URL을 확인해 주세요. https:// 로 시작하는 내 ngrok 주소여야 해요.")
    print("예) NGROK_URL=https://내-주소.ngrok-free.dev")
    raise SystemExit(1)

base = f"https://api.telegram.org/bot{token}"

print("1) 내 봇 확인 (getMe)")
print(f"{base}/getMe\n")
print("2) 배달 주소 등록 (setWebhook)")
print(f"{base}/setWebhook?url={server_url}\n")
print("3) 배달 주소 확인 (getWebhookInfo) — url이 위의 내 ngrok 주소인지 본다")
print(f"{base}/getWebhookInfo\n")
print("주소에 토큰이 들어 있어요. 화면 공유·캡처할 때 조심하세요.")
