from app.services.vector_db import collection
print("Total images:",collection.count())
print(collection.get())