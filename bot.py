import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Helper Function ---

def generate_cc(bin_prefix: str, count: int = 30):
    results = []
    bin_prefix = bin_prefix.strip()

    if not bin_prefix.isdigit() or len(bin_prefix) < 4 or len(bin_prefix) > 15:
        return ["❌ Invalid BIN! Please provide 4 to 15 digit numeric BIN."]

    for _ in range(count):
        # Calculate how many digits we need to complete 16-digit card
        fill_length = 16 - len(bin_prefix)
        cc = bin_prefix + ''.join([str(random.randint(0, 9)) for _ in range(fill_length)])

        mm = str(random.randint(1, 12)).zfill(2)
        yyyy = str(random.randint(2025, 2030))
        cvv = str(random.randint(100, 999))

        results.append(f"{cc}|{mm}|{yyyy}|{cvv}")
    return results

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to Fake CC Generator Bot!*\n\n"
        "Send a BIN using the command below:\n"
        "`/gen 4147` or `/gen 51` or `/gen 414709`",
        parse_mode="Markdown"
    )

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a BIN. Example:\n`/gen 4147`", parse_mode="Markdown")
        return

    bin_input = context.args[0]
    cc_list = generate_cc(bin_input)

    msg = "\n".join(cc_list)
    await update.message.reply_text(f"<code>{msg}</code>", parse_mode="HTML")

# --- Main Bot Setup ---

def main():
    app = ApplicationBuilder().token("8017193630:AAFaMRpJ7Hk-2MTibaWOR_71-NYuFgr_2_U").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", generate))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()