import networkx as nx
from pyvis.network import Network
import html
import matplotlib.pyplot as plt

def visualize_graph_interactive(G: nx.DiGraph, output_html="./java_code_graph.html"):
    """
    Create an interactive, draggable HTML graph visualization using PyVis (Vis.js).
    """
    # Setting cdn_resources to 'in_line' makes the HTML file self-contained
    net = Network(height="750px", width="100%", directed=True, notebook=True, cdn_resources='in_line')
    net.force_atlas_2based()  # A nice layout algorithm

    # Map node types to colors for better visual distinction
    color_map = {
        "class": "#68a7f7",       # blue
        "method": "#7ddf7d",      # green
        "unresolved": "#f27b7b",  # red
        "unknown": "#cccccc"      # grey
    }

    # Add nodes to the PyVis network
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "unknown")
        color = color_map.get(node_type, "#ccc")
        label = str(node)
        # Create a rich HTML title for hover tooltips
        code_snippet = html.escape(data.get('code', '')[:300])
        title = f"<b>{label}</b><br>Type: {node_type}<br><pre>{code_snippet}</pre>"
        net.add_node(node, label=label, title=title, color=color)

    # Add edges to the PyVis network
    for src, dst, edata in G.edges(data=True):
        relation = edata.get("relation", "")
        color = "#888"  # Default edge color
        if relation == "contains":
            color = "#0074D9"
        elif relation == "calls":
            color = "#FF4136"
        net.add_edge(src, dst, title=relation, color=color, arrows="to")

    # Manually write the HTML to a file with UTF-8 encoding to prevent UnicodeEncodeError on Windows.
    # The net.html attribute contains the generated HTML content.
    # net.show(output_html)
    print(f"Saving interactive graph to: {output_html}")
    # Sample code to write HTML content to a file
    print("Writing HTML file..." + net.html[:1000] + "..."  )
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(net.html)
        
    print(f"✅ Interactive graph saved to: {output_html}")




def visualize_graph(G: nx.DiGraph, title: str = "Java Code Graph", output_png: str = None):
    """
    Visualize the Java code graph (class-method-call relations)
    using NetworkX and Matplotlib. If output_png is provided, saves the
    visualization to a file instead of displaying it.
    """
    plt.figure(figsize=(12, 8))

    # layout: spring_layout spreads nodes naturally
    pos = nx.spring_layout(G, seed=42, k=0.6)

    # separate nodes by type
    class_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "class"]
    method_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "method"]
    unresolved_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "unresolved"]
    unknown_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "unknown"]

    # draw edges first
    nx.draw_networkx_edges(G, pos, alpha=0.4, arrows=True, edge_color="gray")

    # draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=class_nodes, node_color="#68a7f7", node_size=1200, label="Class")
    nx.draw_networkx_nodes(G, pos, nodelist=method_nodes, node_color="#7ddf7d", node_size=800, label="Method")
    nx.draw_networkx_nodes(G, pos, nodelist=unresolved_nodes, node_color="#f27b7b", node_size=700, label="Unresolved")
    nx.draw_networkx_nodes(G, pos, nodelist=unknown_nodes, node_color="#cccccc", node_size=700, label="Unknown")

    # labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

    # legend and title
    plt.legend(scatterpoints=1, loc="best")
    plt.title(title)
    plt.axis("off")

    if output_png:
        plt.savefig(output_png, format="PNG", dpi=300, bbox_inches='tight')
        print(f"✅ Static graph saved to: {output_png}")
        plt.close()  # Close the plot to free up memory
    else:
        plt.show()