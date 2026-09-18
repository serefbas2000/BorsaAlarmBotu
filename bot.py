import asyncio
import yfinance as yf
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8809444190:AAFVwcptDodEoYWB51_TySfxKeowT2W2Qtc"

HEDEF_FIYAT = 30.50
CHAT_ID = None
alarm_hazir = True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID

    CHAT_ID = update.effective_chat.id

    await update.message.reply_text(
        "🤖 YEOTK Alarm Botu aktif!\n\n"
        "🎯 Alarm seviyesi: 30,50 TL\n"
        "📈 YEOTK 30,50 TL'yi yukarı geçerse sana haber vereceğim."
    )


def fiyat_getir():
    try:
        hisse = yf.Ticker("YEOTK.IS")
        veri = hisse.history(period="1d", interval="1m")

        if veri.empty:
            return None

        return float(veri["Close"].iloc[-1])

    except Exception as e:
        print("Fiyat alınamadı:", e)
        return None


async def alarm_kontrol():
    global alarm_hazir

    while True:
        try:
            if CHAT_ID is not None:
                fiyat = await asyncio.to_thread(fiyat_getir)

                if fiyat is not None:
                    print(f"YEOTK: {fiyat:.2f} TL")

                    if fiyat <= HEDEF_FIYAT:
                        alarm_hazir = True

                    elif fiyat > HEDEF_FIYAT and alarm_hazir:
                        await application.bot.send_message(
                            chat_id=CHAT_ID,
                            text=(
                                "🚨 YEOTK ALARM!\n\n"
                                f"📈 Fiyat: {fiyat:.2f} TL\n"
                                "🎯 30,50 TL seviyesi yukarı geçildi!"
                            )
                        )

                        alarm_hazir = False

        except Exception as e:
            print("Alarm hatası:", e)

        await asyncio.sleep(30)


async def main():
    global application

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    print("🤖 YEOTK Alarm Botu çalışıyor...")

    asyncio.create_task(alarm_kontrol())

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())