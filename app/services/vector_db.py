import chromadb

client=chromadb.PersistentClient(
    path="chroma_db"
)

collection=client.get_or_create_collection(
    name="photos"
)

def add_embedding(image_id,embedding,filename):
    collection.add(
        ids=[image_id],
        embeddings=[embedding],
        metadatas=[{
            "filename":filename
        }],
        documents=[filename]
    )

def search_embeddings(embedding,top_k=5):
    results=collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results


def delete_embedding(image_id):
    collection.delete(ids=[image_id])