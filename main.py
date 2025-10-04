
import os
import glob
# Set gRPC log level to ERROR to avoid noisy startup logs from google-generativeai.
# This should be done before importing the library.
os.environ['GRPC_VERBOSITY'] = 'ERROR'

import networkx as nx
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv()

from tree_sitter_parser import parse_source
from graph_builder import build_graph_from_elements
from chroma_manager import store_graph_nodes_in_chroma, semantic_search, semantic_graph_search, collection
from visualizer import visualize_graph_interactive, visualize_graph

def parse_project_folder(root_folder: str, language: str) -> Tuple[nx.DiGraph, List[Dict[str, Any]]]:
    """
    Walks root_folder recursively, parse all source files for the given language, 
    build a combined graph and return it.
    """
    all_elements = {"classes": [], "methods": [], "imports": [], "method_calls": []}
    file_extension = f".{language}"
    for path in glob.glob(os.path.join(root_folder, "**", f"*{file_extension}"), recursive=True):
        try:
            with open(path, "r", encoding="utf-8") as f:
                src = f.read()
            elems = parse_source(src, language)
            for c in elems.get("classes", []):
                c["file"] = path
            for m in elems.get("methods", []):
                m["file"] = path
            for mc in elems.get("method_calls", []):
                mc["file"] = path
            all_elements["classes"].extend(elems.get("classes", []))
            all_elements["methods"].extend(elems.get("methods", []))
            all_elements["imports"].extend(elems.get("imports", []))
            all_elements["method_calls"].extend(elems.get("method_calls", []))
        except Exception as e:
            print(f"Failed to parse {path}: {e}")

    G = build_graph_from_elements(all_elements)
    return G, all_elements

if __name__ == "__main__":
    # Specify the language to parse
    language = "java"
    project_folder = "./ejb/ejb/src/java/com" 
    G_proj, elems_proj = parse_project_folder(project_folder, language)
    store_graph_nodes_in_chroma(G_proj)
    print("Done for project.")
    
    #print("Graph nodes:", list(G_proj.nodes(data=True)))
    #print("Graph edges:", list(G_proj.edges(data=True)))

    print(f"Nodes: {len(G_proj.nodes())}, Edges: {len(G_proj.edges())}")
    
    # Generate both interactive HTML and static PNG visualizations
    visualize_graph_interactive(G_proj, output_html="./project_code_graph.html")
    visualize_graph(G_proj, output_png="project_code_graph.png")

    print("Storing nodes in ChromaDB (this will call Gemini embedding API)...")
    store_graph_nodes_in_chroma(G_proj)

    print("Semantic search for 'customer' ...")
    results = semantic_search("method spcific for customer", top_k=3)
    for r in results:
        print(">>> ID:", r["id"])
        print(r["document"])
        print("metadata:", r["metadata"])
        print("---")

    print("Semantic customer...")
    results = semantic_graph_search(
        "customer",
        G=G_proj,
        collection=collection,
        depth=3,
        top_k=2
    )

    for r in results:
        print(">>> ID:", r["id"])
        print(r["document"])
        print("metadata:", r["metadata"])
        print("---")
