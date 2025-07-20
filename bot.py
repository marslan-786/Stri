import stripe
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🛡️ Replace with your Stripe test secret key

stripe.api_key = os.environ["MY_SECRET"]

# 🟢 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot is live!\n\n📥 Send your card(s) in this format:\n"
        "`4242424242424242|12|2025|123`\n\n"
        "You can also send multiple cards (one per line).",
        parse_mode="Markdown"
    )

# 🔍 Main Card Checker
import html

async def check_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = update.message.text.strip().split("\n")
    results = []

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) != 4:
            results.append(f"❌ Invalid format: {html.escape(line)}")
            continue

        number, month, year, cvc = parts
        bin_number = number[:6]

        # 🔎 BIN Info Lookup
        try:
            res = requests.get(f"https://lookup.binlist.net/{bin_number}")
            if res.status_code == 200:
                data = res.json()
                brand = data.get("scheme", "N/A").title()
                bank = data.get("bank", {}).get("name", "N/A")
                country = data.get("country", {}).get("name", "N/A")
                bin_info = f"{brand} - {bank} ({country})"
            else:
                bin_info = "Unknown BIN"
        except:
            bin_info = "BIN Lookup Failed"

        # ✅ Stripe Auth Check (No capture, no redirect)
        try:
            intent = stripe.PaymentIntent.create(
                amount=100,
                currency="usd",
                payment_method_data={
                    "type": "card",
                    "card": {
                        "number": number,
                        "exp_month": int(month),
                        "exp_year": int(year),
                        "cvc": cvc,
                    },
                },
                confirm=True,
                capture_method="manual",
                automatic_payment_methods={
                    "enabled": True,
                    "allow_redirects": "never"
                }
            )

            if intent.status == "requires_capture":
                result = f"✅ Approved | <code>{number[:6]}******{number[-4:]}</code> | {html.escape(bin_info)}"
            else:
                result = f"⚠️ Failed ({intent.status}) | <code>{number[:6]}******{number[-4:]}</code> | {html.escape(bin_info)}"

        except stripe.error.CardError as e:
            result = f"❌ Declined: {html.escape(e.user_message)} | <code>{number[:6]}******{number[-4:]}</code> | {html.escape(bin_info)}"
        except Exception as e:
            result = f"❌ Error: {html.escape(str(e))} | <code>{number[:6]}******{number[-4:]}</code> | {html.escape(bin_info)}"

        results.append(result)

    # 📤 Send combined reply safely
    reply = "\n\n".join(results)
    await update.message.reply_text(reply, parse_mode="HTML")

# 🚀 Bot Launcher
if __name__ == "__main__":
    app = Application.builder().token("8017193630:AAFaMRpJ7Hk-2MTibaWOR_71-NYuFgr_2_U").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_card))

    print("🤖 Bot is running...")
    app.run_polling()