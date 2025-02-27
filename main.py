import random
import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext

# 🔵 Telegram Bot Token & Channel Link
BOT_TOKEN = "7883008864:AAH_u7musCwKNR_Jj6fLuXmnkXame-1fvhw"
CHANNEL_LINK = "https://t.me/+h3tJX-Wf2OM2MTk9"

# Bot ke start hone par welcome message
def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "🤖 **Bot Status: Active ✅**\n\n"
        f"📢 **For announcements and updates, join us 👉 [here]({CHANNEL_LINK}).**\n\n"
        "💡 **Tip:** To use Astra in your group, make sure to set it as an admin.\n"
        "🔍 **Commands:** Use `/help`"
    )
    update.message.reply_text(welcome_message, parse_mode="Markdown")

# /help command
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "🛠 **Bot Commands:**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "✅ `/gen <BIN>` - Generate valid-looking cards with real BIN info.\n"
        "✅ `/bin <BIN>` - Check BIN details (Bank, Country, Type, Phone, Website, Location).\n"
        "✅ `/fake <Country> <State>` - Generate a real-looking fake address.\n"
        "✅ `/help` - Show this command list.\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**"
    )
    update.message.reply_text(help_text, parse_mode="Markdown")

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
        
        # Non-VBV & VBV Check
        vbv_status = "Unknown"
        if data.get("prepaid") is True:
            vbv_status = "✅ Non-VBV ( 2D Secure)"
        elif data.get("prepaid") is False:
            vbv_status = "🛑 VBV (3D Secure)"
        
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
            f"🔐 **VBV Status:** `{vbv_status}`\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️]()**"
        )
    else:
        result = "❌ Invalid BIN or API error. Try again later."

    update.message.reply_text(result, parse_mode="Markdown")


# Credit Card Generator
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
            + "\n".join(cards) +
            "\n━━━━━━━━━━━━━━━━━━━\n"
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

# Fake Address Generator
def fake_address(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text("❌ Usage: /fake <Country> <State>")
        return
    
    country = context.args[0].capitalize()
    state = " ".join(context.args[1:]).capitalize()

    # Random fake details
    street = f"{random.randint(100, 9999)} {random.choice(['Main St', 'Park Ave', 'Elm St', 'Maple Dr'])}"
    city = random.choice(["Los Angeles", "New York", "Houston", "Chicago"])
    zip_code = str(random.randint(10000, 99999))
    phone = f"+{random.randint(1, 99)} {random.randint(1000000000, 9999999999)}"

    result = (
        "📍 **Generated Fake Address:**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🏠 **Street:** `{street}`\n"
        f"🏙 **City:** `{city}`\n"
        f"🌍 **State:** `{state}`\n"
        f"📮 **ZIP Code:** `{zip_code}`\n"
        f"📞 **Phone:** `{phone}`\n"
        f"🇨🇴 **Country:** `{country}`\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️]**"
    )
    update.message.reply_text(result, parse_mode="Markdown")

# Bot Setup
updater = Updater(BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))
dp.add_handler(CommandHandler("bin", bin_lookup))
dp.add_handler(CommandHandler("gen", generate_cards))
dp.add_handler(CommandHandler("fake", fake_address))

updater.start_polling()
updater.idle()
