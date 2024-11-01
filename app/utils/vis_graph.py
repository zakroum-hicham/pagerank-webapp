from pyvis.network import Network
import os

def visualize_graph(G,pagerank):

    # Add PageRank values to each node as an attribute
    for node in G.nodes():
        G.nodes[node]['pagerank'] = round(pagerank[node]*100,2)

    nt = Network(height="640px", width="100%", directed=True,select_menu=True)
    # Add nodes and edges to the Pyvis network
    for node in G.nodes():
        # Add the node with PageRank value as a title
        nt.add_node(node, label=f"{node}\n{round(pagerank[node] * 100, 2)}%", value=pagerank[node])

    for source, target in G.edges():
        nt.add_edge(source, target)
    
    # Customize the layout
    nt.force_atlas_2based(central_gravity=0.015, gravity=-40)

    # Save the visualization as an HTML file
    visualization_file = os.path.join(os.getcwd(), 'static','pagerank_network.html')
    nt.save_graph(visualization_file)

    return 'pagerank_network.html'