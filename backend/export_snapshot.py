"""
Exports all facts from the ChromaDB vector store into a single JSON snapshot.
"""

import os
import json
import chromadb
from chromadb.config import Settings

# Vector store directory (same as in rag_pipeline.py)
VSTORE_DIR = os.getenv("AGRI_VECTORSTORE_DIR", os.path.join(os.path.dirname(__file__), "..", "vectorstore"))

# Snapshot file path
SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "agriagent_snapshot.json")

def main():
    # Connect to vector DB
    client = chromadb.PersistentClient(path=VSTORE_DIR, settings=Settings(allow_reset=False))
    
    # Get collection
    collection = client.get_or_create_collection(name="agri_facts")
    
    # Retrieve ALL facts
    results = collection.get(include=["documents", "metadatas"])
    
    docs = results.get("documents", [])
    metas = results.get("metadatas", [])

    # Combine into list of dicts
    snapshot_data = []
    for doc, meta in zip(docs, metas):
        snapshot_data.append({
            "fact": doc,
            "metadata": meta
        })

    # Save to JSON
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Snapshot exported: {SNAPSHOT_PATH}")
    print(f"   Total facts: {len(snapshot_data)}")

if __name__ == "__main__":
    main()
