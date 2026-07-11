from app.services.embedding_service import get_text_embedding, get_image_embedding
import numpy as np
CATEGORIES = {
    "documents":"a document, ID card or screenshot",
    "prescription":"a medical prescription",
    "receipt":"a shopping receipt or bill",
    "person":"a photo of a person or selfie",
    "travel":"a travel photograph or tourist place",
    "pet":"a pet animal such as a dog or cat",
    "other":"other image"
}

CATEGORY_EMBEDDINGS = {}

for category, description in CATEGORIES.items():
    CATEGORY_EMBEDDINGS[category] = np.array(
        get_text_embedding(description)
    )


def classify_image(image_path):
    image_embedding=np.array(get_image_embedding(image_path))
    best_category="other"
    best_score=-1

    for category in CATEGORIES:
        category_embedding=CATEGORY_EMBEDDINGS[category]

        similarity=np.dot(image_embedding,category_embedding)

        if similarity>best_score:
            best_score=similarity
            best_category=category

    return {
        "category": best_category,
        "score":float(best_score)
    }