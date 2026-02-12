import networkx as nx
import matplotlib.pyplot as plt


def visualize_langgraph(nodes, edges, entry_points):
    G = nx.DiGraph()

    # Add nodes
    for node in nodes:
        G.add_node(node)

    # Add edges
    for src, dst in edges:
        G.add_edge(src, dst)

    # Layout
    pos = nx.spring_layout(G, seed=42)

    # Color logic
    node_colors = []
    for node in G.nodes():
        if node in entry_points:
            node_colors.append("lightgreen")   # entry nodes
        else:
            node_colors.append("skyblue")

    # Draw
    plt.figure(figsize=(10, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color=node_colors,
        font_size=12,
        font_weight="bold",
        arrows=True,
        edge_color="gray"
    )

    plt.title("LangGraph Parallel Workflow Visualization")
    plt.show()
