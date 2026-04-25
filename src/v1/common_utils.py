import json
import os


def save_chunks(text_chunks, path="chunks.json"):
    # chunks = [{"id": f"chunk_{i}", "text": text} for i, text in enumerate(text_chunks)]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(text_chunks, f)

def load_chunks(path="chunks.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None