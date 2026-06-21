import requests
import json
import re

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN"
CHAT_ID = "7616099379"

STATE_FILE = "state.json"


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def get_prices(html):
    return [int(p.replace(",", "")) for p in re.findall(r'([\d,]{6,})\s*تومان', html)]


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def run():
    products = json.load(open("products.json", encoding="utf-8"))
    state = load_state()

    for p in products:
        try:
            html = requests.get(p["url"], timeout=15).text
            prices = get_prices(html)

            if not prices:
                continue

            best = min(prices)
            old = state.get(p["name"])

            if old == best:
                continue

            send(f"""🔥 تغییر بازار

محصول: {p['name']}
💰 کمترین قیمت: {best:,} تومان
""")

            state[p["name"]] = best

        except Exception as e:
            print("error:", e)

    save_state(state)


run()
