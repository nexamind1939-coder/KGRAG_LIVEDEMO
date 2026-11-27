"""
Knowledge Graph example using NetworkX.

Install:
    python -m pip install networkx matplotlib

Run:
    python knowledge_graph_networkx.py

Outputs:
    knowledge_graph_networkx.graphml
    knowledge_graph_networkx.png
"""

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Nodes: (node name, node type)
nodes = [
    ("Vikram Rao", {"label": "Person"}),
    ("Ananya Sharma", {"label": "Person"}),
    ("India", {"label": "Company"}),
    ("50 Mw Microgrid Project", {"label": "Project"}),
    ("Karnataka", {"label": "Location"}),
]
G.add_nodes_from(nodes)

# Directed relationships
edges = [
    ("Vikram Rao", "India", {"relationship": "WORKS_AT"}),
    ("Vikram Rao", "Ananya Sharma", {"relationship": "REPORTS_TO"}),
    ("50 Mw Microgrid Project", "Karnataka", {"relationship": "LOCATED_IN"}),
]
G.add_edges_from(edges)

# Print graph contents
print("Nodes:")
for node, attributes in G.nodes(data=True):
    print(f"  {node}: {attributes}")

print("\\nRelationships:")
for source, target, attributes in G.edges(data=True):
    print(f"  {source} --{attributes['relationship']}--> {target}")

# Export for other graph tools
nx.write_graphml(G, "knowledge_graph_networkx.graphml")
print("\\nSaved: knowledge_graph_networkx.graphml")

# Draw and save a visual network diagram
plt.figure(figsize=(12, 7))
pos = nx.spring_layout(G, seed=42)

nx.draw_networkx_nodes(G, pos, node_size=2400)
nx.draw_networkx_labels(G, pos, font_size=9)
nx.draw_networkx_edges(
    G, pos, arrows=True, arrowsize=20,
    connectionstyle="arc3,rad=0.08"
)

edge_labels = {
    (source, target): attributes["relationship"]
    for source, target, attributes in G.edges(data=True)
}
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_size=8
)

plt.title("Knowledge Graph - NetworkX")
plt.axis("off")
plt.tight_layout()
plt.savefig("knowledge_graph_networkx.png", dpi=200)
plt.show()

print("Saved: knowledge_graph_networkx.png")