import requests
import time
import os
from dotenv import load_dotenv

# ==== TẢI BIẾN MÔI TRƯỜNG ====
load_dotenv()
token = os.getenv("TOKEN")
channel_id = os.getenv("CHANNEL_ID")
batch_size = 5
delay = 5

if not token or not channel_id:
    print("❌ Lỗi: TOKEN hoặc CHANNEL_ID chưa được khai báo trong biến môi trường.")
    exit(1)

headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}

# ==== ĐỌC DỮ LIỆU ====
with open("user_ids.txt", "r") as f:
    user_ids = [line.strip() for line in f if line.strip()]

with open("noidung.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f if line.strip()]

# ==== GỬI TIN NHẮN ====
for message in messages:
    for i in range(0, len(user_ids), batch_size):
        batch = user_ids[i:i + batch_size]
        mentions = ' '.join([f"<@{uid}>" for uid in batch])
        content = f"{mentions} {message}"

        payload = {
            "content": content,
            "tts": False
        }

        response = requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            print(f"✅ Gửi thành công: {content}")
        else:
            print(f"❌ Thất bại ({response.status_code}): {response.text}")

        time.sleep(delay)
