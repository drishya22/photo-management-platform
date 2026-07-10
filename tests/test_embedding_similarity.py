# tests/check_embedding_similarity.py

from app.services.embedding_service import get_text_embedding
from app.services.vector_db import collection

results = collection.get(
    ids=[
        "f11344efc9b14e4ba57eb895c060eddf2349cdfb4b3d5d78c8ce9e47f420de85"
    ],
    include=["embeddings"]
)

dog_embedding = results["embeddings"][0]

print("Length:", len(dog_embedding))
print("First 10 values:")
print(dog_embedding[:10])