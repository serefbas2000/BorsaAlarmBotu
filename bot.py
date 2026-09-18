import os
import yfinance as yf
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")

CHAT_ID = None

HEDEF_FIYAT = 30.50
HISSE = "YEOTK.IS"


def fiyat_getir():
    try:
        hisse = yf.Ticker(HISSE)
        veri = hisse.history(period="1d", interval="1m")

        if veri.empty:
            return None

        return float(veri["Close"].iloc[-1])

    except Exception as e:
        print("Fiyat alınamadı:", e)
        return None


def main():
    fiyat = fiyat_getir()

    if fiyat is None:
        print("Fiyat alınamadı.")
        return

    print(f"YEOTK fiyatı: {fiyat:.2f} TL")

    if fiyat > HEDEF_FIYAT:
        print("Alarm koşulu oluştu.")

        if TOKEN and CHAT_ID:
            import asyncio

            async def mesaj_gonder():
                bot = Bot(token=TOKEN)

                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=(
                        "🚨 YEOTK ALARM!\n\n"
                        f"📈 Fiyat: {fiyat:.2f} TL\n"
                        "🎯 30,50 TL seviyesi yukarı geçildi!"
                    )
                )

            asyncio.run(mesaj_gonder())

    else:
        print("Alarm koşulu oluşmadı.")


if __name__ == "__main__":
    main()
