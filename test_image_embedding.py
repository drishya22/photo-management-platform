from app.services.embedding_service import (
    get_image_embedding
)

embedding = get_image_embedding(
    "uploads/ICARD MSIT.jpg"
)

print(type(embedding))
print(len(embedding))
print(embedding[:5])