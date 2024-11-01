from flask import Flask, render_template, request,jsonify
from utils.pageRank import *
from utils.vis_graph import *
import os
import numpy as np

app = Flask(__name__)



@app.route('/', methods=["GET","POST"])
def home():
    pagerank = None
    graph_file = None
    if request.method == 'POST':
        input_type = request.form.get('input_type')
        
        if input_type == 'adjacency_matrix':
            try:
                matrix_input = request.form['adjacency_matrix']
                adjacency_matrix = np.array([list(map(float, row.split(','))) for row in matrix_input.strip().split('\n')])
                rank,nb_iter = adjacency_pageRanke(adjacency_matrix)
                graph = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph())
            except :
                error_message = """
                                    <div>Error: The Adjacency Matrix Format isn't correct.<br>
                                    Please ensure it follows the correct structure.<br>
                                    Here is an example of a valid Adjacency Matrix:</div>
                                    <pre>
                                    0,0,1
                                    0,1,1
                                    1,1,1
                                    </pre>
                                    <div>You can go back and try again.</div>
                                """
                return render_template('error.html', error_message=error_message), 400

        elif input_type == 'edge_list':
            try:
                edge_list_input = request.form['edge_list']
                edges = [tuple(map(str.strip, edge.split(','))) for edge in edge_list_input.strip().split('\n')]
                graph = nx.DiGraph()
                graph.add_edges_from(edges)
                nodes = graph.nodes
                rank,nb_iter = graph_pagerank(nodes,edges)
                print(edges)
            except:
                error_message = """
                                    <div>Error: The edge list Format isn't correct.<br>
                                    Please ensure it follows the correct structure.<br>
                                    Here is an example of a valid edge list:</div>
                                    <pre>
                                    A,B
                                    B,C
                                    C,D
                                    B,A
                                    </pre>
                                    <div>You can go back and try again.</div>
                                """
                return render_template('error.html', error_message=error_message), 400

        elif input_type == 'xml_file':
            xml_file = request.files['xml_file']
            if xml_file:
                rank,graph = xml_pageRank1(xml_file)
                    
                if len(rank)==0:
                     error_message = """
                                    <div>Error: The uploaded XML file is not well-formed.<br>
                                    Please ensure it follows the correct structure.<br>
                                    Here is an example of a valid XML file:</div>
                                    <pre>
                                &lt;graph&gt;
                                    &lt;node id='A'&gt;
                                        &lt;target&gt;B&lt;/target&gt;
                                        &lt;target&gt;C&lt;/target&gt;
                                    &lt;/node&gt;
                                    &lt;node id='B'&gt;
                                        &lt;target&gt;C&lt;/target&gt;
                                    &lt;/node&gt;
                                    &lt;node id='C'&gt;
                                        &lt;target&gt;A&lt;/target&gt;
                                    &lt;/node&gt;
                                &lt;/graph&gt;
                                    </pre>
                                    <div>You can go back and try again.</div>
                                """
                     return render_template('error.html', error_message=error_message), 400
            else:
                return "Error: No XML file uploaded.", 400
        else:
            return "Unsupported graph input type. Please use Adjacency Matrix , Edge List Or XML File."
        
        # Calculate PageRank
        pagerank = nx.pagerank(graph)

        # Visualize the graph
        graph_file = visualize_graph(graph,pagerank)

    return render_template("index.html",pagerank=pagerank ,graph_file=graph_file)



# Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)