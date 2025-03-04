import random
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 🔵 Telegram Bot Token & Channel Link
BOT_TOKEN = "7883008864:AAH_u7musCwKNR_Jj6fLuXmnkXame-1fvhw"
CHANNEL_LINK = "https://t.me/+h3tJX-Wf2OM2MTk9"


# 📌 Start Command
def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
    "🤖 **Bot Status: Active ✅**\n\n"
    "📢 **For announcements and updates, join us 👉 [here](https://t.me/your_channel_link)**\n\n"
    "💡 **Tip:** To use Astra in your group, make sure to set it as an admin.\n"
    "🔍 **Commands:** Use `/help`"
)
update.message.reply_text(welcome_message, parse_mode="Markdown")


# 📌 Help Command
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "🛠 **Bot Commands:**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "✅ `/gen <BIN>` - Generate valid-looking cards.\n"
        "✅ `/bin <BIN>` - Check BIN details.\n"
        "✅ `/fake <Country>` - Generate a real-looking fake address.\n"
        "✅ `/help` - Show this command list.\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨]()**"
    )
    update.message.reply_text(help_text, parse_mode="Markdown")

# 📌 BIN Checker
# BIN Checker
def bin_lookup(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text("❌ Usage: /bin <BIN>")
        return
    
    bin_number = context.args[0]
    response = requests.get(f"https://lookup.binlist.net/{bin_number}")

    if response.status_code == 200:
        data = response.json()
        bank = data.get("bank", {}).get("name", "N/A")
        country = data.get("country", {}).get("name", "Unknown")
        flag = data.get("country", {}).get("emoji", "🏳")
        phone = data.get("bank", {}).get("phone", "N/A")
        website = data.get("bank", {}).get("url", "N/A")
        latitude = data.get("country", {}).get("latitude", "N/A")
        longitude = data.get("country", {}).get("longitude", "N/A")
        scheme = data.get("scheme", "Unknown").upper()
        card_type = data.get("type", "Unknown").upper()
        brand = data.get("brand", "Unknown").upper()
        prepaid = "✅ Yes" if data.get("prepaid") else "❌ No"

        result = (
            "━━━━━━━━━━━━━━━━━━━\n"
            "⚜️ **BIN CHECKER RESULT** ⚜️\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"🟡 **BIN:** `{bin_number}`\n"
            f"🏦 **Bank Name:** `{bank}`\n"
            f"📞 **Phone:** `{phone}`\n"
            f"🌍 **Country:** `{country} {flag}`\n"
            f"🌐 **Bank Website:** `{website}`\n"
            f"📍 **Latitude:** `{latitude}`\n"
            f"📍 **Longitude:** `{longitude}`\n"
            f"🛄 **Card Type:** `{card_type}`\n"
            f"🛑 **Card Brand:** `{brand}`\n"
            f"🎟 **Card Scheme:** `{scheme}`\n"
            f"💳 **Prepaid:** `{prepaid}`\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️]()**"
        )
    else:
        result = "❌ Invalid BIN or API error. Try again later."

    update.message.reply_text(result, parse_mode="Markdown")
    
# 📌 Credit Card Generator
def generate_cards(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text("❌ Usage: /gen <BIN>")
        return

    bin_number = context.args[0]
    response = requests.get(f"https://lookup.binlist.net/{bin_number}")

    if response.status_code == 200:
        data = response.json()
        scheme = data.get("scheme", "Unknown").upper()
        card_type = data.get("type", "Unknown").upper()
        brand = data.get("brand", "Unknown").upper()
        bank = data.get("bank", {}).get("name", "Unknown")
        country = data.get("country", {}).get("name", "Unknown")
        flag = data.get("country", {}).get("emoji", "🏳")

        cards = []
        for _ in range(10):
            card_number = bin_number + "".join(str(random.randint(0, 9)) for _ in range(16 - len(bin_number)))
            exp_month = str(random.randint(1, 12)).zfill(2)
            exp_year = str(random.randint(2026, 2035))
            cvv = str(random.randint(100, 999))
            cards.append(f"{card_number}|{exp_month}|{exp_year}|{cvv}")

        result = (
            "🟢 **LIVE Credit Cards:** 🟢\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"```{chr(10).join(cards)}```\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"**BIN:** `{bin_number}`\n"
            f"**Scheme:** `{scheme}`\n"
            f"**Type:** `{card_type}`\n"
            f"**Brand:** `{brand}`\n"
            f"**Bank:** `{bank}`\n"
            f"**Country:** `{country} {flag}`\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ **Disclaimer:** This bot does not support illegal activities. The generated data is random and for educational purposes only."
        )
    else:
        result = "❌ Invalid BIN or API error."

    update.message.reply_text(result, parse_mode="Markdown")

# 📌 Country Code Mapping for Phone Numbers
COUNTRY_CODES = {
    "India": "+91",
    "USA": "+1",
    "UK": "+44",
    "Canada": "+1",
    "Australia": "+61",
    "Germany": "+49",
}

# 📌 Fake Address Generator (Using RandomUser API)
def fake_address(update: Update, context: CallbackContext) -> None:
    url = "https://randomuser.me/api/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()['results'][0]
        
        street = f"{data['location']['street']['number']} {data['location']['street']['name']}"
        city = data['location']['city']
        state = data['location']['state']
        zip_code = data['location']['postcode']
        country = data['location']['country']
        
        # Correct phone number format for country
        phone_code = COUNTRY_CODES.get(country, "+999")
        phone = f"{phone_code} {data['phone']}"

        result = (
            "📍 **Generated Fake Address:**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"🏠 **Street:** `{street}`\n"
            f"🏙 **City:** `{city}`\n"
            f"🌍 **State:** `{state}`\n"
            f"📮 **ZIP Code:** `{zip_code}`\n"
            f"📞 **Phone:** `{phone}`\n"
            f"🏳️ **Country:** `{country}`\n"
            "━━━━━━━━━━━━━━━━━━━"
        )
    else:
        result = "❌ API Error! Try Again Later."

    update.message.reply_text(result, parse_mode="Markdown")


# 📌 Bot Setup
updater = Updater(BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))
dp.add_handler(CommandHandler("bin", bin_lookup))
dp.add_handler(CommandHandler("gen", generate_cards))
dp.add_handler(CommandHandler("fake", fake_address))

updater.start_polling()
updater.idle()
