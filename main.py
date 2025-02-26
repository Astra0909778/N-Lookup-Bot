import asyncio
import logging
import requests
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram.constants import ParseMode
from telegram.error import BadRequest

# 🔥 Bot Token & Channel ID (Change as needed)
BOT_TOKEN = "7518220550:AAGnnmTxA9hJBDBf6QO7WfaeEB8t6k4p_dw"
CHANNEL_ID = -1001807869811  # ✅ Apne channel ki ID yahan daalo

# ✅ Logger Setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# ✅ Function to check if user is in the channel
async def check_membership(user_id, bot: Bot):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except BadRequest:
        return False

# ✅ /start Command - Welcome & Check Membership
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    bot = context.bot

    if await check_membership(user_id, bot):
        await update.message.reply_text("👋 Welcome! ✅ Aapne channel join kar liya hai.\nUse `/bin <bin_number>` to check BIN details.")
    else:
        await update.message.reply_text(
            "❌ 𝗝𝗼𝗶𝗻 𝗳𝗶𝗿𝘀𝘁 𝗰𝗵𝗮𝗻𝗻𝗲𝗹: [JOIN NOW](https://t.me/+h3tJX-Wf2OM2MTk9)\n"
            "🔄 Phir `/start` command dobara use karo!",
            parse_mode=ParseMode.MARKDOWN
        )

# ✅ BIN Checker - No Channel Link if Already Joined
async def bin_check(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    bot = context.bot

    if not await check_membership(user_id, bot):
        await update.message.reply_text(
            "❌ Aapne abhi tak channel join nahi kiya!\n"
            "🔹 Pehle join karein: [JOIN NOW](https://t.me/+h3tJX-Wf2OM2MTk9)\n"
            "🔄 Phir `/bin` command try karein!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if len(context.args) == 0:
        await update.message.reply_text("❌ Please provide a BIN number. Example: `/bin 457173`")
        return

    bin_number = context.args[0]
    url = f"https://lookup.binlist.net/{bin_number}"
    headers = {"Accept-Version": "3"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            bank_name = data.get("bank", {}).get("name", "N/A")
            bank_phone = data.get("bank", {}).get("phone", "N/A")
            bank_website = data.get("bank", {}).get("url", "N/A")
            country = data.get("country", {}).get("name", "N/A")
            country_emoji = data.get("country", {}).get("emoji", "🌍")
            scheme = data.get("scheme", "N/A")
            card_type = data.get("type", "N/A")
            brand = data.get("brand", "N/A")
            currency = data.get("country", {}).get("currency", "N/A")
            prepaid = "✅ Yes" if data.get("prepaid", False) else "❌ No"

            # 🔐 3D Secure (VBV/MSC) & 2D Secure (Non-VBV)
            security_check = "✅ **3D Secure (VBV/MSC)** 🔒" if card_type.lower() == "credit" else "❌ **Non-3D Secure (2D)** 🔓"

            message = f"""
━━━━━━━━━━━━━━━━━━━
⚜️ **BIN CHECKER RESULT** ⚜️
━━━━━━━━━━━━━━━━━━━

🟡 **BIN:** `{bin_number}`
🏦 **Bank Name:** `{bank_name}`
📞 **Phone:** `{bank_phone}`
🌍 **Country:** `{country} {country_emoji}`
🌐 **Bank Website:** `{bank_website}`

🛄 **Card Type:** `{card_type}`
🛑 **Card Brand:** `{brand}`
🎟 **Card Scheme:** `{scheme}`
💵 **Currency:** `{currency}`
💳 **Prepaid:** `{prepaid}`
🔐 **Security:** `{security_check}`

━━━━━━━━━━━━━━━━━━━
👨‍💻 **Developed by** [⚡ Δ𝗦𝗧Ɍ𝗔™ ⚡](https://t.me/AsTra032)
━━━━━━━━━━━━━━━━━━━
"""
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("❌ Invalid BIN or API error.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching BIN data: {e}")

# ✅ Main Function (Asynchronous)
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bin", bin_check))

    logging.info("✅ Bot Started Successfully!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
