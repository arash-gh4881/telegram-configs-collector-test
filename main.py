
import json
import re
import html
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from base64 import b64encode

def json_load(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def tg_channel_messages(channel_user):
    try:
        response = requests.get(f"https://t.me/s/{channel_user}")
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("div", class_="tgme_widget_message")
    except Exception:
        return []

def tg_message_text(div_message):
    div_text = div_message.find("div", class_="tgme_widget_message_text")
    if div_text:
        return div_text.prettify()
    return ""

def find_matches(text_content):
    pattern_vmess = r"(?<![\w-])(vmess://[^\s<>#]+)"
    pattern_ss = r"(?<![\w-])(ss://[^\s<>#]+)"
    pattern_trojan = r"(?<![\w-])(trojan://[^\s<>#]+)"
    vmess = re.findall(pattern_vmess, text_content, re.IGNORECASE)
    ss = re.findall(pattern_ss, text_content, re.IGNORECASE)
    trojan = re.findall(pattern_trojan, text_content, re.IGNORECASE)
    return [*vmess, *ss, *trojan]

def main():
    telegram_channels = json_load('telegram channels.json')
    collected_configs = []

    for channel_url in telegram_channels:
        username = channel_url.strip().split("/")[-1]
        messages = tg_channel_messages(username)
        for msg in messages:
            text = tg_message_text(msg)
            matches = find_matches(text)
            collected_configs.extend(matches)

    # حذف تکراری‌ها
    collected_configs = list(set(collected_configs))

    # رمزنگاری base64 و ذخیره
    encoded = b64encode("\n".join(collected_configs).encode("utf-8")).decode("utf-8")
    with open("splitted/channels", "w", encoding="utf-8") as f:
        f.write(encoded)

if __name__ == "__main__":
    main()
