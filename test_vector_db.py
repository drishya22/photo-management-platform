from app.services.vector_db import (
    add_embedding,
    search_embeddings
)

from app.services.embedding_service import (
    get_text_embedding
)

embedding = get_text_embedding("dog")

add_embedding(
    image_id="1",
    embedding=embedding,
    filename="dog.jpg"
)

results = search_embeddings(
    embedding
)

print(results)