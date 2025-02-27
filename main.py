import logging
import random
import requests
from telegram.ext import Updater, CommandHandler

# Logging Setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7883008864:AAH_u7musCwKNR_Jj6fLuXmnkXame-1fvhw"

# Channel Invite Link (Optional)
CHANNEL_LINK = "https://t.me/+h3tJX-Wf2OM2MTk9"

# Start Command
def start(update, context):
    update.message.reply_text(
        f"👋 **Welcome to the BIN & CC Generator Bot!**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "🔍 **Commands:**\n"
        "📌 `/bin <BIN>` - Check BIN information\n"
        "📌 `/gen <BIN>` - Generate fake credit cards\n"
        "📌 `/fake <Country> <State>` - Get a fake address\n"
        "📌 `/help` - View all commands\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"📢 **Join Our Channel for Updates!**\n"
        f"🔗 [Join Here]({CHANNEL_LINK}) *(Joining is optional, but recommended!)*\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**\n"
        "━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown"
    )

# Help Command
def help_command(update, context):
    update.message.reply_text(
        "📖 **Available Commands:**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "📌 `/bin <BIN>` - Check BIN details\n"
        "📌 `/gen <BIN>` - Generate credit cards\n"
        "📌 `/fake <Country> <State>` - Generate fake address\n"
        "📌 `/help` - Show this help message\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**\n"
        "━━━━━━━━━━━━━━━━━━━", parse_mode="Markdown"
    )

# BIN Lookup Command
def bin_lookup(update, context):
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

        bank_name = data.get("bank", {}).get("name", "N/A")
        phone = data.get("bank", {}).get("phone", "N/A")
        website = data.get("bank", {}).get("url", "N/A")
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

        result = (
            "━━━━━━━━━━━━━━━━━━━\n"
            "⚜️ **BIN CHECKER RESULT** ⚜️\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🟡 **BIN:** `{bin_number}`\n"
            f"🏦 **Bank Name:** `{bank_name}`\n"
            f"📞 **Phone:** `{phone}`\n"
            f"🌍 **Country:** `{country} {country_emoji}`\n"
            f"🌐 **Bank Website:** `{website}`\n"
            f"📍 **Latitude:** `{latitude}`\n"
            f"📍 **Longitude:** `{longitude}`\n\n"
            f"🛄 **Card Type:** `{card_type}`\n"
            f"🛑 **Card Brand:** `{brand}`\n"
            f"🎟 **Card Scheme:** `{scheme}`\n"
            f"💵 **Currency:** `{currency}`\n"
            f"💳 **Prepaid:** `{prepaid}`\n"
            f"🔐 **Security:** `{security_check}`\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**\n"
            "━━━━━━━━━━━━━━━━━━━"
        )
        update.message.reply_text(result, parse_mode="Markdown")

    except requests.exceptions.RequestException as e:
        logging.error(f"API Error: {e}")
        update.message.reply_text("❌ API error! Please try again later.")

# Fake Credit Card Generator
def generate_cc(update, context):
    if len(context.args) == 0:
        update.message.reply_text("❌ Please provide a **BIN number**.\nExample: `/gen 45717360`")
        return

    bin_number = context.args[0]
    cards = []

    for _ in range(10):
        card_number = bin_number + "".join(str(random.randint(0, 9)) for _ in range(16 - len(bin_number)))
        exp_month = str(random.randint(1, 12)).zfill(2)
        exp_year = str(random.randint(2026, 2035))
        cards.append(f"{card_number}|{exp_month}|{exp_year}")

    result = (
        "🟢 **Generated Credit Cards:** 🟢\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        + "\n".join(cards) +
        "\n━━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**\n"
        "━━━━━━━━━━━━━━━━━━━"
    )
    update.message.reply_text(result, parse_mode="Markdown")

# Fake Address Generator
def generate_fake_address(update, context):
    if len(context.args) < 2:
        update.message.reply_text("❌ Please provide a **Country and State**.\nExample: `/fake India Maharashtra`")
        return

    country = context.args[0].capitalize()
    state = " ".join(context.args[1:]).capitalize()
    city = random.choice(["Mumbai", "Pune", "Nagpur", "Nashik"]) if state == "Maharashtra" else "Random City"
    zip_code = random.randint(100000, 999999)
    address = f"{random.randint(1, 999)}, {random.choice(['MG Road', 'Park Street', 'Main Street'])}"
    phone = f"+{random.randint(1, 99)} {random.randint(6000000000, 9999999999)}"

    result = (
        f"📍 **Random Fake Address**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🏠 **Address:** {address}\n"
        f"🏙 **City:** {city}\n"
        f"🌆 **State:** {state}\n"
        f"📮 **ZIP Code:** {zip_code}\n"
        f"🌍 **Country:** {country}\n"
        f"📞 **Phone:** {phone}\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 **Developed by [Δ𝗦𝗧Ɍ𝗔™ 👁️‍🗨️](https://t.me/AsTra032)**\n"
        "━━━━━━━━━━━━━━━━━━━"
    )
    update.message.reply_text(result, parse_mode="Markdown")

# Bot Setup
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("bin", bin_lookup))
    dp.add_handler(CommandHandler("gen", generate_cc))
    dp.add_handler(CommandHandler("fake", generate_fake_address))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
