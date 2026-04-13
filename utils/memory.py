import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

load_dotenv()

def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

def get_collection_name():
    return "trusthariz_memoire"

def ensure_collection_exists():
    client = get_qdrant_client()
    collection_name = get_collection_name()
    try:
        collections = client.get_collections().collections
        names = [c.name for c in collections]
        if collection_name not in names:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=4, distance=Distance.COSINE),
            )
    except Exception:
        pass

def write_memory(text: str, metadata: dict = None):
    client = get_qdrant_client()
    ensure_collection_exists()
    collection_name = get_collection_name()
    doc_id = str(uuid.uuid4())
    vector = [0.1, 0.2, 0.3, 0.4]
    payload = {"text": text, **(metadata or {})}
    client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=doc_id, vector=vector, payload=payload)]
    )
    return doc_id

def search_memory(query: str, limit: int = 3):
    client = get_qdrant_client()
    ensure_collection_exists()
    collection_name = get_collection_name()
    query_vector = [0.1, 0.2, 0.3, 0.4]
    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit
    )
    memories = []
    for item in response.points:
        memories.append({
            "id": str(item.id),
            "score": item.score,
            "payload": item.payload
        })
    return memories