import json
import os
from datetime import datetime

def save_chat_log(session_id, profile_data, user_message, bot_response,log_dir="logs"):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    today_str = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join(log_dir, f"chat_log_{today_str}.jsonl")

    log_data = {
        "timestamp":datetime.now().isoformat(),
        "session_id": session_id,
        "profile": profile_data,
        "chat": {
            "question": user_message,
            "answer": bot_response
        }
    }

    with open(file_path,"a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

        