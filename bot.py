import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Helper Functions ---

def generate_cc(bin_input: str, count: int = 30):
    results = []
    bin_input = bin_input.strip().replace("x", "X")

    for _ in range(count):
        cc = ""
        for char in bin_input:
            if char == "X":
                cc += str(random.randint(0, 9))
            else:
                cc += char

        mm = str(random.randint(1, 12)).zfill(2)
        yyyy = str(random.randint(2025, 2030))
        cvv = str(random.randint(100, 999))

        results.append(f"{cc}|{mm}|{yyyy}|{cvv}")
    return results

# --- Command Handler ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a BIN with Xs. Example:\n\n`414709XXXXXXXXXX`", parse_mode="Markdown")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a BIN. Example:\n`/gen 414709XXXXXXXXXX`", parse_mode="Markdown")
        return

    bin_input = context.args[0]
    cc_list = generate_cc(bin_input)

    msg = "\n".join(cc_list)
    await update.message.reply_text(f"✅ Generated 30 CCs:\n\n<code>{msg}</code>", parse_mode="HTML")

# --- Main Bot Setup ---

def main():
    app = ApplicationBuilder().token("8017193630:AAFaMRpJ7Hk-2MTibaWOR_71-NYuFgr_2_U").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", generate))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()