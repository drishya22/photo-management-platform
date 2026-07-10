# tests/test_norm.py

from app.services.embedding_service import get_text_embedding
import numpy as np

embedding = get_text_embedding("identity card")

print(np.linalg.norm(embedding))