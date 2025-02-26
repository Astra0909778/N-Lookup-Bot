import asyncio
import logging
import requests
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram.constants import ParseMode
from telegram.error import BadRequest
from requests.exceptions import Timeout, ConnectionError, RequestException
import json

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
        await update.message.reply_text(
            "👋 Welcome! ✅ Aapne channel join kar liya hai.\nUse `/bin <bin_number>` to check BIN details."
        )
    else:
        await update.message.reply_text(
            "❌ 𝗝𝗼𝗶𝗻 𝗳𝗶𝗿𝘀𝘁 𝗰𝗵𝗮𝗻𝗻𝗲𝗹: [JOIN NOW](https://t.me/+h3tJX-Wf2OM2MTk9)\n"
            "🔄 Phir `/start` command dobara use karo!",
            parse_mode=ParseMode.MARKDOWN
        )

# ✅ BIN Checker Command
async def bin_check(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    bot = context.bot

    # ✅ Membership Check
    if not await check_membership(user_id, bot):
        await update.message.reply_text(
            "❌ Aapne abhi tak channel join nahi kiya!\n"
            "🔹 Pehle join karein: [JOIN NOW](https://t.me/+h3tJX-Wf2OM2MTk9)\n"
            "🔄 Phir `/bin` command try karein!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # ✅ BIN Argument Check
    if len(context.args) == 0:
        await update.message.reply_text("❌ Please provide a BIN number. Example: `/bin 457173`")
        return

    bin_number = context.args[0]
    url = f"https://lookup.binlist.net/{bin_number}"
    headers = {"Accept-Version": "3"}

    try:
        # ✅ API Request with Timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Agar status code 4xx ya 5xx hoga to error raise karega
        data = response.json()

        # ✅ Extracting Data
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

        # 🔐 3D Secure (VBV/MSC) Check
        security_check = "✅ **3D Secure (VBV/MSC)** 🔒" if card_type.lower() == "credit" else "❌ **Non-3D Secure (2D)** 🔓"

        # ✅ Final Message
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

    except Timeout:
        await update.message.reply_text("❌ BIN lookup request timed out. Please try again later.")
    except ConnectionError:
        await update.message.reply_text("❌ Network issue. Please check your connection and try again.")
    except json.JSONDecodeError:
        await update.message.reply_text("❌ Error decoding API response. Please try again later.")
    except KeyError:
        await update.message.reply_text("❌ Invalid BIN data received. Please try another BIN.")
    except RequestException as e:
        await update.message.reply_text(f"❌ API Error: {e}")

# ✅ Main Function (Asynchronous)
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bin", bin_check))

    logging.info("✅ Bot Started Successfully!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
