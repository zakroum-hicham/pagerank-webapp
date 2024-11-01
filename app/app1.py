from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import networkx as nx
import os
from pyvis.network import Network

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    pagerank = None
    graph_file = None
    if request.method == 'POST':
        graph_input_type = request.form.get('input_type')
        
        if graph_input_type == 'adjacency_matrix':
            matrix_input = request.form['adjacency_matrix']
            adjacency_matrix = np.array([list(map(float, row.split(','))) for row in matrix_input.strip().split('\n')])
            graph = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph())
        
        elif graph_input_type == 'edge_list':
            edge_list_input = request.form['edge_list']
            edges = [tuple(map(str.strip, edge.split(','))) for edge in edge_list_input.strip().split('\n')]
            graph = nx.DiGraph()
            graph.add_edges_from(edges)
        
        elif graph_input_type == 'xml_file':
            xml_file = request.files['xml_file']
            if xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                # Parse the XML to extract edges or an adjacency matrix
                edges = []
                for node in root.findall('node'):
                    node_id = node.get('id')
                    for target in node.findall('target'):
                        edges.append((node_id, target.text.strip()))

                graph = nx.DiGraph()
                graph.add_edges_from(edges)
        
        else:
            return "Unsupported graph input type. Please use Adjacency Matrix , Edge List."

        # Calculate PageRank
        pagerank = nx.pagerank(graph)

        # Visualize the graph
        graph_file = visualize_graph(graph)

    return render_template('index.html', pagerank=pagerank, graph_file=graph_file)

def visualize_graph(graph):
    net = Network(notebook=True)
    net.from_nx(graph)

    # Save the visualization as an HTML file
    visualization_file = os.path.join('static', 'pagerank_network.html')
    net.save_graph(visualization_file)

    return 'pagerank_network.html'

if __name__ == '__main__':
    app.run(debug=True)
