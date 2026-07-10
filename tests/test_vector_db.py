from app.services.embedding_service import get_text_embedding

embedding = get_text_embedding("dog")

print(type(embedding))
print(len(embedding))
print(embedding[:5])