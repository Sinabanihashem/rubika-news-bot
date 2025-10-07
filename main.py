from rubpy import Client
import requests
import re

bot = Client('sina')

@bot.on_message_updates()
async def main(message):
    if not message.text:
        return

    text = message.text.strip()

    if text == "اخبار":
        try:
            response = requests.get("https://sina-news.onrender.com/news", timeout=10)
            data = response.json()

            news_list = data.get("news", [])
            if not news_list:
                await message.reply("❌ خبری یافت نشد.")
                return

            result = "📰 آخرین اخبار:\n\n"
            for item in news_list:
                result += f"🔸 {item['title']}\n🔗 {item['link']}\n\n"

            await message.reply(result[:4000])

        except Exception as e:
            await message.reply("❌ خطا در دریافت اخبار")

    elif text.startswith("+"):
        prompt = text[1:].strip()
        try:
            response = requests.get(
                f"https://chatgpt.apinepdev.workers.dev/?question={prompt}",
                timeout=10
            )
            answer = response.json().get("answer", response.text)
            clean_answer = re.sub(r"🔗 Join our community:.*$", "", answer)
            await message.reply(f"🤖 {clean_answer[:4000]}")
        except:
            await message.reply("❌ خطا در اتصال")

bot.run()
