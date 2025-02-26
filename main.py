import logging
from telegram.ext import Updater, CommandHandler
import requests

# Logging setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7819839173:AAHrMlkSR7jwTTdUjQ9_sZidNGbZb8GZRxc"

# Channel Join Check
MANDATORY_CHANNEL = "@h3tJX_Wf2OM2MTk9"

def is_user_in_channel(user_id, bot):
    try:
        chat_member = bot.get_chat_member(MANDATORY_CHANNEL, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# ✅ Start Command (Yeh hamesha chalega)
def start(update, context):
    update.message.reply_text(
        "👋 Welcome to the **BIN Lookup Bot**!\n\n"
        "🔍 Type `/bin <BIN>` to get details.\n"
        "Example: `/bin 45717360`\n\n"
        "🚀 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**",
        parse_mode="Markdown"
    )

# ❌ BIN Lookup Command (Yeh tab tak kaam nahi karega jab tak user channel join na kare)
def bin_lookup(update, context):
    user_id = update.message.from_user.id

    if not is_user_in_channel(user_id, context.bot):
        update.message.reply_text(
            f"🚨 **Aapko BIN check karne ke liye pehle hamare channel ko join karna hoga!**\n"
            f"🔗 [Join Here](https://t.me/+h3tJX-Wf2OM2MTk9)\n\n"
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

        # Response Formatting
        result = f"💳 **BIN Lookup Result**\n\n"
        result += f"🏦 **Scheme:** {data.get('scheme', 'N/A')}\n"
        result += f"💳 **Type:** {data.get('type', 'N/A')}\n"
        result += f"🏢 **Brand:** {data.get('brand', 'N/A')}\n"
        result += f"🏦 **Bank:** {data.get('bank', {}).get('name', 'N/A')}\n"
        result += f"📍 **Country:** {data.get('country', {}).get('name', 'N/A')} {data.get('country', {}).get('emoji', '')}\n"
        result += f"🌎 **Currency:** {data.get('country', {}).get('currency', 'N/A')}\n"
        result += f"📞 **Bank Contact:** {data.get('bank', {}).get('phone', 'N/A')}\n"
        result += f"🌐 **Bank Website:** {data.get('bank', {}).get('url', 'N/A')}\n\n"
        result += "🚀 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**"

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