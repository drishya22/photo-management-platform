from app.services.category_service import classify_image

images = [
    "uploads/dog.jpg",
    "uploads/cat.jpg",
    "uploads/selfie.jpg",
    "uploads/building.jpg",
    "uploads/gym.jpg",
    "uploads/ICARD MSIT.jpg",
    "uploads/Screenshot (1).png"
]

for image in images:
    print(image)
    print(classify_image(image))
    print("-" * 30)