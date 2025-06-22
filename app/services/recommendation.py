from sentence_transformers import SentenceTransformer, util
from typing import List, Dict
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")

def recommend_events(user_profile: Dict, events: List[Dict], top_k=5):
    user_text = f"{user_profile['interests']} {user_profile['mood']} {user_profile['budget']} {user_profile['location']}"
    user_vec = model.encode(user_text, convert_to_tensor=True)

    event_texts = [f"{e['title']} {e['description']} {' '.join(e.get('tags', []))}" for e in events]
    event_vecs = model.encode(event_texts, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(user_vec, event_vecs)[0]
    top_idxs = torch.topk(scores, k=min(top_k, len(events))).indices

    return [events[i] for i in top_idxs]
