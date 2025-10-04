
import networkx as nx
from typing import Dict, Any

def build_graph_from_elements(elements: Dict[str, Any]) -> nx.DiGraph:
    """
    Build a directed graph where:
      - class nodes connect to their methods with edge 'contains'
      - method -> method edges for invocations with edge 'calls'
      - import edges: file -> import (optional)
    Node attributes include 'type' and 'code'
    """
    G = nx.DiGraph()

    for cls in elements.get("classes", []):
        name = cls["name"]
        G.add_node(name, type="class", code=cls.get("code", ""))

    for m in elements.get("methods", []):
        mid = m["id"]
        G.add_node(mid, type="method", code=m.get("code", ""), class_name=m.get("class"))
        cls_name = m.get("class")
        if cls_name:
            G.add_edge(cls_name, mid, relation="contains")

    for call in elements.get("method_calls", []):
        caller = call.get("caller")
        callee_name = call.get("call")
        
        if callee_name:
            candidates = [n for n in G.nodes if G.nodes[n].get("type") == "method" and n.endswith(f".{callee_name}")]
            chosen = None
            
            if caller:
                caller_nodes = [n for n in G.nodes if n.endswith(f".{caller}") or n == caller]
                caller_class = None
                if caller_nodes:
                    cn = caller_nodes[0]
                    if G.nodes[cn].get("type") == "method":
                        caller_class = G.nodes[cn].get("class_name")
                    elif G.nodes[cn].get("type") == "class":
                        caller_class = G.nodes[cn].get("name")
                
                for c in candidates:
                    if caller_class and G.nodes[c].get("class_name") == caller_class:
                        chosen = c
                        break
            
            if not chosen and candidates:
                chosen = candidates[0]
            
            if chosen:
                caller_node = None
                possible = [n for n in G.nodes if n.endswith(f".{caller}")] if caller else []
                if possible:
                    caller_node = possible[0]
                else:
                    caller_node = caller or f"caller::{caller}"
                    if caller_node not in G:
                        G.add_node(caller_node, type="unknown", code="")
                G.add_edge(caller_node, chosen, relation="calls")
            else:
                unresolved = f"unresolved::{callee_name}"
                if unresolved not in G:
                    G.add_node(unresolved, type="unresolved", code="")
                caller_node = caller or f"caller::{caller}"
                if caller_node not in G:
                    G.add_node(caller_node, type="unknown", code="")
                G.add_edge(caller_node, unresolved, relation="calls")

    return G
