from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import BadRequest
import requests

# 🔥 Replace your Bot Token here
BOT_TOKEN = "7819839173:AAHrMlkSR7jwTTdUjQ9_sZidNGbZb8GZRxc"

# 🔥 Replace your Telegram Channel ID here (-100xxxxxxxxxx format)
CHANNEL_ID = -1807869811

# ✅ Function to check if user has joined the channel
def check_membership(user_id, context):
    try:
        member = context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except BadRequest:
        return False

# ✅ Start Command
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name

    if check_membership(user_id, context):
        update.message.reply_text(f"👋 Hello {first_name}! Welcome to the bot.\nUse /bin <bin_number> to check BIN info.")
    else:
        update.message.reply_text("❌ Pehle is channel ko join karo: https://t.me/+h3tJX-Wf2OM2MTk9")

# ✅ BIN Checker Function
def bin_check(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Channel Join Check
    if not check_membership(user_id, context):
        update.message.reply_text("❌ Pehle is channel ko join karo: https://t.me/+h3tJX-Wf2OM2MTk9")
        return

    if len(context.args) == 0:
        update.message.reply_text("❌ Please provide a BIN number. Example: /bin 457173")
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
            country_emoji = data.get("country", {}).get("emoji", "🏳")
            scheme = data.get("scheme", "N/A")
            card_type = data.get("type", "N/A")
            brand = data.get("brand", "N/A")
            currency = data.get("country", {}).get("currency", "N/A")
            latitude = data.get("country", {}).get("latitude", "N/A")
            longitude = data.get("country", {}).get("longitude", "N/A")
            prepaid = "✅ Yes" if data.get("prepaid", False) else "❌ No"

            # 3D Secure (VBV/MSC) & 2D Secure (Non-VBV) Check
            if card_type.lower() == "debit":
                security_check = "❌ **2D Secure (Non-VBV)**"
            else:
                security_check = "✅ **3D Secure (VBV/MSC)**"

            message = f"""🔍 **BIN Lookup**
💳 **BIN:** `{bin_number}`
🏦 **Bank:** `{bank_name}`
📞 **Bank Phone:** `{bank_phone}`
🌐 **Bank Website:** `{bank_website}`
🌍 **Country:** `{country} {country_emoji}`
📍 **Latitude:** `{latitude}`
📍 **Longitude:** `{longitude}`
🏷 **Scheme:** `{scheme}`
📌 **Brand:** `{brand}`
🔹 **Type:** `{card_type}`
💰 **Currency:** `{currency}`
💳 **Prepaid:** `{prepaid}`
🔒 **Security:** `{security_check}`

👁 Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)"""

            update.message.reply_text(message, parse_mode="Markdown")
        else:
            update.message.reply_text("❌ Invalid BIN or API error.")
    except Exception as e:
        update.message.reply_text("❌ Error fetching BIN data.")

# ✅ Main Function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bin", bin_check, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
