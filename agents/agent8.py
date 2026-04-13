import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

def agent8_run(mission: str):
    qdrant_url = os.getenv("QDRANT_URL", "http://172.17.0.1:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "")

    try:
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key if qdrant_api_key else None
        )

        collection_name = "trusthariz_memoire"

        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=4, distance=Distance.COSINE),
            )

        doc_id = str(uuid.uuid4())
        vecteur_simule = [0.1, 0.2, 0.3, 0.4]

        client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=doc_id,
                    vector=vecteur_simule,
                    payload={"mission": mission, "status": "archivé"}
                )
            ]
        )

        return {
            "status": "✅ Stocké dans Qdrant",
            "id_document": doc_id[:8] + "...",
            "resume": "La mission est désormais gravée dans la mémoire."
        }

    except Exception as e:
        return {
            "status": "❌ Erreur Qdrant",
            "erreur": str(e),
            "resume": "Problème de connexion au coffre-fort."
        }