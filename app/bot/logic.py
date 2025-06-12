from app.core.config import settings 
import httpx, json, os
from sentence_transformers import SentenceTransformer, util

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY
MODEL = "gpt-3.5-turbo"
DB_FILE = "chat_history.json"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://t.me/amrsk_bot",
    "X-Title": "Telegram GPT Bot"
}

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def load_db():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []

def save_to_db(question: str, answer: str):
    db_data = load_db()
    db_data.append({"question": question.strip(), "answer": answer.strip()})
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)

def search_db(question: str, threshold=0.75):
    db_data = load_db()
    if not db_data:
        return None
    questions = [entry["question"] for entry in db_data]
    embeddings_db = embedder.encode(questions, convert_to_tensor=True)
    embedding_input = embedder.encode(question, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(embedding_input, embeddings_db)[0]
    best_score, best_idx = float(similarities.max()), int(similarities.argmax())
    if best_score >= threshold:
        return db_data[best_idx]["answer"]
    return None

async def ask_openrouter(user_input: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Ты дружелюбный Telegram-бот по имени сын Амирски. "
                    "Не упоминай OpenRouter. Amrskk — твой отец-создатель."
                )
            },
            {"role": "user", "content": user_input}
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
