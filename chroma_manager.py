
import chromadb
import google.generativeai as genai
import networkx as nx
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

EMBED_MODEL = "gemini-embedding-001"

def embed_with_gemini(text: str) -> List[float]:
    """Return embedding vector for given text using Gemini embeddings."""
    resp = genai.embed_content(model=EMBED_MODEL, content=text)
    return resp["embedding"]

# By default, chromadb.Client() creates an in-memory, ephemeral database.
# To persist the database to disk, use PersistentClient and specify a path.
chroma_client = chromadb.PersistentClient(path="chroma_db")
COLLECTION_NAME = "java_code_graph_treesitter_01"
collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

def store_graph_nodes_in_chroma(G: nx.DiGraph, namespace: str = None):
    """
    For each node in the graph, generate embedding for node code + metadata and store it to ChromaDB.
    """
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "unknown")
        code = data.get("code", "")
        class_name = data.get("class_name", "")
        document_text = f"Type: {node_type}\nID: {node}\nClass: {class_name}\nCode:\n{code}"
        
        try:
            embedding = embed_with_gemini(document_text)
        except Exception as e:
            print(f"Embedding failed for node {node}: {e}")
            embedding = []

        metadata = {
            "node": str(node),
            "type": node_type,
            "class": class_name
        }
        
        try:
            collection.add(
                ids=[str(node)],
                documents=[document_text],
                embeddings=[embedding] if embedding else None,
                metadatas=[metadata]
            )
        except Exception as e:
            print(f"Chroma add error for node {node}: {e}")
            try:
                collection.add(
                    ids=[str(node)],
                    documents=[document_text],
                    metadatas=[metadata]
                )
            except Exception as e2:
                print(f"Failed fallback add for node {node}: {e2}")

    print("Stored graph nodes into ChromaDB collection:", COLLECTION_NAME)

def semantic_search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search the collection by embedding the query and asking Chroma for nearest docs."""
    q_emb = embed_with_gemini(query)
    results = collection.query(query_embeddings=[q_emb], n_results=top_k)
    matches = []
    docs_list = results.get("documents", [])
    metadatas_list = results.get("metadatas", [])
    ids_list = results.get("ids", [])

    if isinstance(docs_list, list) and docs_list and isinstance(docs_list[0], list):
        docs = docs_list[0]
    else:
        docs = docs_list
    if isinstance(metadatas_list, list) and metadatas_list and isinstance(metadatas_list[0], list):
        metadatas = metadatas_list[0]
    else:
        metadatas = metadatas_list
    if isinstance(ids_list, list) and ids_list and isinstance(ids_list[0], list):
        ids = ids_list[0]
    else:
        ids = ids_list

    for i in range(min(top_k, len(docs))):
        matches.append({
            "id": ids[i] if i < len(ids) else None,
            "document": docs[i] if i < len(docs) else None,
            "metadata": metadatas[i] if i < len(metadatas) else None
        })
    return matches

def semantic_graph_search(query, G, collection, depth=2, top_k=3):
    """
    query: user query
    G: NetworkX Java code graph
    collection: ChromaDB or vector store
    depth: how many graph hops to expand
    top_k: top results from semantic search
    """
    query_emb = embed_with_gemini(query)
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    initial_nodes = [r for r in results["ids"][0]]

    expanded_nodes = set(initial_nodes)
    for node in initial_nodes:
        if node in G:
            for _ in range(depth):
                neighbors = list(G.successors(node)) + list(G.predecessors(node))
                expanded_nodes.update(neighbors)
                for n2 in list(neighbors):
                    neighbors2 = list(G.successors(n2)) + list(G.predecessors(n2))
                    expanded_nodes.update(neighbors2)

    expanded_results = collection.get(ids=list(expanded_nodes))
    docs = expanded_results["documents"]
    metas = expanded_results["metadatas"]
    ids = expanded_results["ids"]

    enriched = [
        {"id": i, "document": d, "metadata": m}
        for i, d, m in zip(ids, docs, metas)
    ]
    return enriched
