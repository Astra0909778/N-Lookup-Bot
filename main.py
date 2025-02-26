import asyncio
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram.constants import ParseMode

# ✅ Bot Token (Apna bot token yahan daal)
BOT_TOKEN = "7819839173:AAHrMlkSR7jwTTdUjQ9_sZidNGbZb8GZRxc"

# ✅ Private Channel Details
CHANNEL_ID = -1001807869811  # 🔥 Apne private channel ka ID yahan daalo (Negative number hoga)
CHANNEL_INVITE_LINK = "https://t.me/+h3tJX-Wf2OM2MTk9"  # ✅ Private channel ka invite link

# ✅ Logger Setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# ✅ API Function (New API for BIN Lookup)
async def get_bin_info(bin_number):
    url = f"https://lookup.binlist.net/{bin_number}"
    headers = {"Accept-Version": "3"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # ✅ Extract required info
        bank_name = data.get("bank", {}).get("name", "N/A")
        bank_phone = data.get("bank", {}).get("phone", "N/A")
        bank_website = data.get("bank", {}).get("url", "N/A")
        country = data.get("country", {}).get("name", "N/A")
        country_emoji = data.get("country", {}).get("emoji", "🌍")
        card_type = data.get("type", "N/A")
        brand = data.get("brand", "N/A")
        scheme = data.get("scheme", "N/A")
        currency = data.get("country", {}).get("currency", "N/A")
        prepaid = "Yes" if data.get("prepaid", False) else "No"
        security_check = "Enabled" if data.get("bank") else "Disabled"

        # ✅ Final Message Format
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
        return message
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {e}"

# ✅ Function to Check User Subscription (For Private Channel)
async def is_user_joined(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

# ✅ Command Handler for "/bin"
async def bin_check(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("❌ Please provide a BIN number. Example: /bin 457173")
        return
    
    user_joined = await is_user_joined(update, context)
    
    if not user_joined:
        keyboard = [
            [InlineKeyboardButton("📢 Join Private Channel", url=CHANNEL_INVITE_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "❌ You must join our **private channel** first to use this bot!",
            reply_markup=reply_markup
        )
        return

    bin_number = context.args[0]
    result = await get_bin_info(bin_number)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

# ✅ Start Command (Welcome Message)
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("✅ Welcome to BIN Checker Bot!\nUse /bin <number> to check details.")

# ✅ Main Function (Asynchronous)
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bin", bin_check))

    logging.info("✅ Bot Started Successfully!")
    await app.run_polling()

# ✅ Proper Termux Handling
if __name__ == "__main__":
    import asyncio

    async def run_bot():
        await main()  # ✅ `main()` function ko call kar raha hai async way me

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # ✅ Termux me existing loop handle karega
    task = loop.create_task(run_bot())  
    try:
        loop.run_forever()  # ✅ Ab loop properly chalega, band nahi hoga
    except KeyboardInterrupt:
        task.cancel()
        loop.stop()
