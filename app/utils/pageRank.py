import networkx as nx
import xmltodict
import xml.etree.ElementTree as ET
import numpy as np

def adjacency_pageRanke(A,alpha=0.83,eps=1e-6) :
    num_link_of_page  = np.sum(A,axis=1)

    D = np.zeros(A.shape)
    for i , num  in enumerate (num_link_of_page) : 
        if num == 0  :
            D[i] = 1/A.shape[0]
        else : 
            D[i] = (1-alpha) /A.shape[0]

    M= np.where(num_link_of_page[:, np.newaxis] == 0, 
             0, 
             A * alpha / num_link_of_page[:, np.newaxis])
    
    P =M+D
    R = np.ones(A.shape[0])/A.shape[0]

    l=0
    R1 = np.dot(R,P)
    norme = np.sum(np.abs(R - R1))
    while norme >=  eps :
        R = R1
        R1 = np.dot(R,P)
        norme = np.sum(np.abs(R - R1))
        l=l+1


    return np.round(R1 *100,2) ,l


def graph_pagerank(nodes,edges):
   n = len(nodes)

   adjacency_matrix = np.zeros((n, n))
   nodes = {v:i for i,v  in enumerate(nodes)}
   for i in edges:

        adjacency_matrix[nodes[i[0]], nodes[i[1]]] = 1
           
   rank,l= adjacency_pageRanke(adjacency_matrix.T,0.85,10 ** -6 ) 

   return  rank,l

def xml_pageRank(file_name):


    with open(file_name,"rb") as xml:
        data = xmltodict.parse(xml)

    # Extract the nodes and edges
    nodes = [node['@id'] for node in data['graph']['nodes']['node']]


    edges = {node: [] for node in nodes}
    for edge in data['graph']['edges']['edge']:
        source = edge['@source']
        target = edge['@target']
        edges[source].append(target)
    
    return graph_pagerank(nodes,edges)


def builInPageRank(edges):
    # Create a directed graph from the links
    G = nx.DiGraph()

    # Add edges to the graph
    for source, targets in edges.items():
        for target in targets:
            G.add_edge(source, target)

    # Calculate PageRank
    pagerank = nx.pagerank(G)

    # Add PageRank values to each node as an attribute
    for node in G.nodes():
        G.nodes[node]['pagerank'] = round(pagerank[node]*100,2)
    # Print PageRank values
    return([round(pagerank[i]*100,2) for i in sorted(pagerank)])

def xml_pageRank1(xml_file):
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

    return nx.pagerank(graph),graph