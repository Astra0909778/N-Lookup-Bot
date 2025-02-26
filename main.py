from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import BadRequest
import requests

# 🔥 Replace with your Bot Token
BOT_TOKEN = "7518220550:AAGnnmTxA9hJBDBf6QO7WfaeEB8t6k4p_dw"

# 🔥 Replace with your correct Channel ID
CHANNEL_ID = -1001807869811  # Apna sahi channel ID yahan daalo

# ✅ Function to check if user has joined the channel
def check_membership(user_id, context):
    try:
        member = context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except BadRequest:
        return False

# ✅ Start Command - Welcome Message & Channel Check
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if check_membership(user_id, context):
        update.message.reply_text("👋 Welcome! ✅ You have joined the channel. Use `/bin <bin_number>` to check BIN details.")
    else:
        update.message.reply_text(
            "❌ 𝗝𝗼𝗶𝗻 𝗳𝗶𝗿𝘀𝘁 𝗰𝗵𝗮𝗻𝗻𝗲𝗹: [JOIN NOW](https://t.me/+h3tJX-Wf2OM2MTk9)\n"
            "🔄 Phir `/start` command dobara use karo!",
            parse_mode=ParseMode.MARKDOWN
        )

# ✅ BIN Checker Function - Channel Link Show Nahi Hoga
def bin_check(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Pehle check karega ki user ne channel join kiya hai ya nahi
    if not check_membership(user_id, context):
        update.message.reply_text(
            "❌ Aapne abhi tak channel join nahi kiya!\n"
            "🔹 Pehle join karein: [JOIN NOW](https://t.me/+h3tJX-Wf2OM2MTk9)\n"
            "🔄 Phir `/bin` command try karein!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if len(context.args) == 0:
        update.message.reply_text("❌ Please provide a BIN number. Example: `/bin 457173`")
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

            # 3D Secure (VBV/MSC) & 2D Secure (Non-VBV) Check
            if card_type.lower() == "debit":
                security_check = "❌ **Non-3D Secure (2D)** 🔓"
            else:
                security_check = "✅ **3D Secure (VBV/MSC)** 🔒"

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

            update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
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
