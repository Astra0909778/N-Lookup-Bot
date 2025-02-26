import logging
from telegram.ext import Updater, CommandHandler
import requests

# Logging setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7819839173:AAHrMlkSR7jwTTdUjQ9_sZidNGbZb8GZRxc"

# Channel Join Check (Yeh `chat_id` use karega, taaki sahi work kare)
MANDATORY_CHANNEL_ID = -1001807869811  # <-- Isko apne channel ke chat ID se replace karna 

def is_user_in_channel(user_id, bot):
    try:
        chat_member = bot.get_chat_member(MANDATORY_CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# ✅ Start Command
def start(update, context):
    update.message.reply_text(
        "👋 Welcome to the **BIN Lookup Bot**!\n\n"
        "🔍 Type `/bin <BIN>` to get details.\n"
        "Example: `/bin 45717360`\n\n"
        "🚀 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**",
        parse_mode="Markdown"
    )

# ❌ BIN Lookup Command (Channel Join Check Fix)
def bin_lookup(update, context):
    user_id = update.message.from_user.id

    if not is_user_in_channel(user_id, context.bot):
        update.message.reply_text(
            f"🚨 **Aapko BIN check karne ke liye pehle hamare channel ko join karna hoga!**\n"
            f"🔗 [Join Here](https://t.me/YOUR_CHANNEL_USERNAME)\n\n"
            f"✅ **Join karne ke baad phir command use karein.**",
            parse_mode="Markdown"
        )
        return

    if len(context.args) == 0:
        update.message.reply_text("❌ Please provide a **BIN number**.\nExample: `/bin 45717360`")
        return

    bin_number = context.args[0]
    url = f"https://lookup.binlist.net/{bin_number}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "scheme" not in data:
            update.message.reply_text("⚠️ Invalid BIN number or not found in database.")
            return

        # Extract Data
        bank_name = data.get("bank", {}).get("name", "N/A")
        bank_phone = data.get("bank", {}).get("phone", "N/A")
        bank_website = data.get("bank", {}).get("url", "N/A")
        country = data.get("country", {}).get("name", "N/A")
        country_emoji = data.get("country", {}).get("emoji", "")
        currency = data.get("country", {}).get("currency", "N/A")
        card_type = data.get("type", "N/A")
        brand = data.get("brand", "N/A")
        scheme = data.get("scheme", "N/A")
        prepaid = "✅ Yes" if data.get("prepaid") else "❌ No"
        security_check = "✅ 3D Secure" if data.get("prepaid") else "❌ Not Secure"
        latitude = data.get("country", {}).get("latitude", "N/A")
        longitude = data.get("country", {}).get("longitude", "N/A")

        # Response Formatting
        result = (
            "━━━━━━━━━━━━━━━━━━━\n"
            "⚜️ **BIN CHECKER RESULT** ⚜️\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🟡 **BIN:** `{bin_number}`\n"
            f"🏦 **Bank Name:** `{bank_name}`\n"
            f"📞 **Phone:** `{bank_phone}`\n"
            f"🌍 **Country:** `{country} {country_emoji}`\n"
            f"🌐 **Bank Website:** `{bank_website}`\n"
            f"📍 **Latitude:** `{latitude}`\n"
            f"📍 **Longitude:** `{longitude}`\n\n"
            f"🛄 **Card Type:** `{card_type}`\n"
            f"🛑 **Card Brand:** `{brand}`\n"
            f"🎟 **Card Scheme:** `{scheme}`\n"
            f"💵 **Currency:** `{currency}`\n"
            f"💳 **Prepaid:** `{prepaid}`\n"
            f"🔐 **Security:** `{security_check}`\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "👨‍💻 **Developed by** [ Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)\n"
            "━━━━━━━━━━━━━━━━━━━"
        )

        update.message.reply_text(result, parse_mode="Markdown")

    except requests.exceptions.Timeout:
        logging.error("API request timeout ho gaya!")
        update.message.reply_text("⏳ API response slow hai, thodi der baad try karo.")

    except requests.exceptions.RequestException as e:
        logging.error(f"API Error: {e}")
        update.message.reply_text("❌ API error! Please try again later.")

    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        update.message.reply_text("❌ Unexpected error! Try again later.")

# Bot Setup
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))  
    dp.add_handler(CommandHandler("bin", bin_lookup))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
