from sentence_transformers import SentenceTransformer
from PIL import Image

model=SentenceTransformer("clip-ViT-B-32")

def get_text_embedding(text):
    embedding=model.encode(text)
    return embedding.tolist()

def get_image_embedding(image_path):
    image=Image.open(image_path)
    embedding=model.encode(image)
    return embedding.tolist()
