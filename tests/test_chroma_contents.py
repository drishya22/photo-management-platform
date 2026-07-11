# tests/test_chroma_contents.py

from app.services.vector_db import collection

results = collection.get(
    include=["embeddings","metadatas","documents"]
)

print("Total:", len(results["ids"]))

print("First embedding length:")
print(len(results["embeddings"][0]))

print("\nFirst metadata:")
print(results["metadatas"][0])

print("\nFirst document:")
print(results["documents"][0])