import os
import json
import urllib.request

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = 1013671519

if not TOKEN:
    print("BOT_TOKEN bulunamadı.")
    exit()

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    if not data.get("result"):
        print("Henüz Telegram mesajı bulunamadı.")
    else:
        for update in data["result"]:
            message = update.get("message")

            if message:
                chat = message.get("chat")
                print("CHAT_ID =", chat.get("id"))
                print("Kullanıcı =", chat.get("first_name"))

except Exception as e:
    print("Hata:", e)
