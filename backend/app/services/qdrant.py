from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "devnexa_code"
VECTOR_SIZE = 384

client = QdrantClient(url=QDRANT_URL)


def create_collection() -> None:
    collections = client.get_collections().collections

    existing_names = {collection.name for collection in collections}

    if COLLECTION_NAME in existing_names:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )
