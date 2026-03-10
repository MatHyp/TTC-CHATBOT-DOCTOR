import os
import re
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
# import ollamapip


EMBED_MODEL      = "all-MiniLM-L6-v2"     # model do embeddingów
CHROMA_PATH      = "./chroma_db"          # lokalna baza wektorowa
COLLECTION_NAME  = "knowledge_base"
CHUNK_SIZE       = 500                    # znaki na chunk
CHUNK_OVERLAP    = 50
TOP_K            = 5                      # ile fragmentów pobierać

model = SentenceTransformer(EMBED_MODEL)

def chunk_text(text: str, source: str) -> List[Dict]:
    """Dzieli tekst na nakładające się fragmenty."""
    chunks = []
    start = 0
    i = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if chunk.strip():
            chunk_id = hashlib.md5(f"{source}_{i}".encode()).hexdigest()
            chunks.append({
                "id":       chunk_id,
                "text":     chunk,
                "source":   source,
                "chunk_no": i
            })
            i += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def get_collection():
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False)
    )
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def add_documents(chunks: List[Dict]):
    """Zapisuje chunki + embeddingi do ChromaDB."""
    if not chunks:
        return

    collection = get_collection()

    existing = set(collection.get()["ids"])
    new_chunks = [c for c in chunks if c["id"] not in existing]

    if not new_chunks:
        print(f"  ↩  Wszystkie chunki już istnieją w bazie, pomijam.")
        return

    print(f"  ✦  Generuję embeddingi dla {len(new_chunks)} fragmentów…")
    texts    = [c["text"]   for c in new_chunks]
    vectors  = embed(texts)
    ids      = [c["id"]     for c in new_chunks]
    metas    = [{"source": c["source"], "chunk_no": c["chunk_no"]} for c in new_chunks]

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=metas
    )
    print(f"  ✔  Dodano {len(new_chunks)} fragmentów do bazy.")


def embed(texts: List[str]) -> List[List[float]]:
    return model.encode(texts).tolist()

def load_text(path: str):
    path = Path(path)
    print(f"📃 Ładuję plik tekstowy: {path.name}")
    text = path.read_text(encoding="utf-8", errors="replace")
    chunks = chunk_text(text, source=f"txt:{path.name}")
    add_documents(chunks)
    print(f"✅ Plik '{path.name}' zaindeksowany ({len(chunks)} fragmentów).")
    
def load_folder(folder: str):
    folder = Path(folder)
    if not folder.exists():
        print(f"❌ Folder nie istnieje: {folder}")
        return

    loaders = {
        ".txt":  load_text,
    }

    found = 0
    for file in sorted(folder.rglob("*")):
        if file.suffix.lower() in loaders:
            loaders[file.suffix.lower()](str(file))
            found += 1

    if found == 0:
        print(f"⚠️  Brak obsługiwanych plików w folderze '{folder}'.")
    else:
        print(f"\n📦 Załadowano {found} plików z folderu '{folder}'.")

test = load_folder('folder')

print(test)