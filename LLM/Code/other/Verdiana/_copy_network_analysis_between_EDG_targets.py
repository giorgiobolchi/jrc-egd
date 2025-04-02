#!/usr/bin/env python
# coding: utf-8

# In[3]:


import networkx as nx
import pandas as pd
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text


# In[4]:


### NB this is the code for the third part of the network analysis of the SDGs,
# and looking at  interlinkages only within EGD targets
# type = n.a. is not considered


# In[5]:


# Read in the cleaned database for the edge list (edges are interlinkages, nodes are targets)
def load_data(file_path):
    return pd.read_excel(file_path)

# Load the data
file_path = r'C:\Users\verdy\Downloads\database_16052023.xlsx'
db_for_edgelist = load_data(file_path)


# In[6]:


# Drop all non-univoco rows + all rows with unspecified interlinkages
univoco_target = db_for_edgelist[
    (db_for_edgelist['Univoco_Target_Publication_Type_direction'] != 0) & 
    (db_for_edgelist['Interlink Type'] != 'n.a.')
]

# Define targets to keep
targets_to_keep = ["2.4", "3.9", "6.1", "6.2", "6.3", "6.6", "7.1", "7.2", "7.3", "7.a", "9.1", "9.4",  "11.2", "11.6", "11.7", "11.b",
                   "12.2", "12.3", "12.4","12.5", "13.2", "14.2", "14.4", "14.5", "14.a","15.1", "15.2", "15.3", "15.5",
]

# Filter dataframe using .query() 
filtered_df = univoco_target.query("TargetA in @targets_to_keep and TargetB in @targets_to_keep").copy()

# Keep only necessary columns, i.e, interlinkages attributes to put in the edgelist 
# only_nec_columns = filtered_df[['TargetA', 'TargetB', 'Interlink Type', 'Clear direction', 'Publication ID']].copy()

# Keep only necessary columns, i.e, interlinkages attributes to put in the edgelist with new weight 
# there is no need to keep the publication ID, we consider all links equal regardless of the number of publications where they appear
only_nec_columns = filtered_df[['TargetA', 'TargetB', 'Interlink Type']].copy()

# Drop duplicate rows
only_nec_columns = only_nec_columns.drop_duplicates()
print(only_nec_columns)
#might be needed: create a colum to store identifier of the interlinkage (key)
# Create a column to store identifier of the interlinkage (Key)
# only_nec_columns['Key'] = (
   # only_nec_columns['Publication ID'].astype(str) + '_' + 
   # only_nec_columns['TargetA'].astype(str) + '_' + 
   # only_nec_columns['TargetB'].astype(str))


# In[7]:


# Assign a weight to each edge by summing the occurrences of the same type
# only_nec_columns['weights'] = 1  # Add a column with value 1  
# only_nec_columns['weight'] = only_nec_columns.groupby(['TargetA', 'TargetB', 'Interlink Type'])['weights'].transform('sum')


# In[8]:


# Dictionary of weights for each target
weights_dict = {
    "2.4": 4, "3.9": 1, "6.2": 1, "6.3": 3, "6.6": 1, "7.1": 1, "7.2": 19, "7.3": 13,
    "9.1": 10, "9.4": 8, "11.6": 2, "11.7": 3, "12.2": 4, "12.3": 3, "12.4": 8, "12.5": 26,
    "13.2": 19, "14.2": 7, "14.4": 1, "14.5": 1, "15.1": 9, "15.2": 3, "15.3": 3, "15.5": 4,
    "11.b": 1, "14.a": 2, "6.1": 1, "11.2": 1, "7.a": 1
}

# Map the weights from the dictionary + Compute the total weight of each edge
only_nec_columns["weightA"] = only_nec_columns["TargetA"].map(weights_dict)
only_nec_columns["weightB"] = only_nec_columns["TargetB"].map(weights_dict)
only_nec_columns["weight"] = only_nec_columns["weightA"] + only_nec_columns["weightB"]

# Drop temporary columns if needed
only_nec_columns = only_nec_columns.drop(columns=["weightA", "weightB"])


# In[9]:


print(only_nec_columns)


# In[10]:


# Create the final edge list by grouping edges with the same type and summing weights
# edge_list = only_nec_columns.groupby(['TargetA', 'TargetB', 'Interlink Type', 'weight'], as_index=False).agg({
    #'Key': lambda x: '-'.join(map(str, x))  # Ensuring all keys are strings before joining
# })


# In[11]:


edge_list = only_nec_columns 


# In[12]:


# Assign colors to edges based on Interlink Type
edge_list['edge_color'] = '#32FC5A'  # Default color for synergies
edge_list.loc[edge_list['Interlink Type'] == '-', 'edge_color'] = '#900D09'  # Trade-offs color


# In[13]:


# Convert TargetA and TargetB to strings to ensure consistent node coloring
# edge_list[['Targeta', 'Targetb']] = edge_list[['TargetA', 'TargetB']].astype(str)


# In[14]:


# Create separate DataFrames for synergies and trade-offs
edge_list_synergies = edge_list[edge_list['Interlink Type'] == '+'].copy()
edge_list_tradeoffs = edge_list[edge_list['Interlink Type'] == '-'].copy()


# In[15]:


print(edge_list)


# In[16]:


# Define a dictionary for SDG target colors
SDG_COLORS = {
    '1': '#E5243B', '2': '#DDA63A', '3': '#4C9F38', '4': '#C5192D', '5': '#FF3A21',
    '6': '#26BDE2', '7': '#FCC30B', '8': '#A21942', '9': '#FD6925', '10': '#DD1367',
    '11': '#FD9D24', '12': '#BF8B2E', '13': '#3F7E44', '14': '#0A97D9', '15': '#56C02B',
    '16': '#00689D', '17': '#19486A'
}

# Function to define node colors based on SDG target
def node_color(x):
    if isinstance(x, str):  # Ensure x is a string
        key = x.split('.')[0]  # Extract the main SDG number
        return SDG_COLORS.get(key, '#000000')  # Return color or default black if not found
    return '#000000'  # Default color for invalid inputs


# In[17]:


# Dictionary for SDG target RGB colors
SDG_RGB_COLORS = {
    '1': '229,36,59', '2': '221,166,58', '3': '76,159,56', '4': '197,25,45', '5': '255,58,33',
    '6': '38,189,226', '7': '252,195,11', '8': '162,25,66', '9': '253,105,37', '10': '221,19,103',
    '11': '253,157,36', '12': '191,139,46', '13': '63,126,68', '14': '10,151,217', '15': '86,192,43',
    '16': '0,104,157', '17': '25,72,106'
}

# Function to get RGB color based on SDG target
def node_color_RGB(x):
    if isinstance(x, str):  # Ensure x is a string
        key = x.split('.')[0]  # Extract main SDG number
        return SDG_RGB_COLORS.get(key, (0, 0, 0))  # Default black if not found
    return (0, 0, 0)


# In[18]:


# Nodes DataFrame

data = [
    (4, "2.4"), (1, "3.9"), (1, "6.2"), (3, "6.3"), (1, "6.6"), (1, "7.1"),
    (19, "7.2"), (13, "7.3"), (10, "9.1"), (8, "9.4"), (2, "11.6"), (3, "11.7"),
    (4, "12.2"), (3, "12.3"), (8, "12.4"), (26, "12.5"), (19, "13.2"), (7, "14.2"),
    (1, "14.4"), (1, "14.5"), (9, "15.1"), (3, "15.2"), (3, "15.3"), (4, "15.5"),
    (1, "11.b"), (2, "14.a"), (1, "6.1"), (1, "11.2"), (1, "7.a")
]

# Create the Nodes DataFrame
nodes = pd.DataFrame(data, columns=["weight", "node"])

# Function to create node DataFrame with color attributes

def create_node_df(edge_list):
    # Assign colors based on SDG target
    nodes['node_color'] = nodes['node'].apply(node_color)  # HEX color
    nodes['node_color_RGB'] = nodes['node'].apply(node_color_RGB)  # RGB color

    return nodes

# Create node DataFrames for synergies and trade-offs
nodes_synergies_df = create_node_df(edge_list_synergies)
nodes_tradeoffs_df = create_node_df(edge_list_tradeoffs)


# In[19]:


print(nodes)


# In[30]:


thematic_areas = {
    "Climate ambition": ["13.2", "13.1"],
    "Clean, affordable and secure energy": ["13.2", "9.1", "7.2", "7.3", "7.a", "9.4"],
    "Industrial strategy for a clean and circular economy": ["11.6", "12.5", "12.2", "12.3", "9.4"],
    "Sustainable and smart mobility": ["7.2", "13.2", "7.3", "9.1", "9.4", "7.1"],
    "Greening the Common Agricultural Policy / Farm to Fork Strategy": ["12.3", "2.4", "12.4", "9.1"],
    "Preserving and protecting biodiversity": ["15.5", "12.4", "2.4", "15.2", "15.3", "6.6", "11.b","14.2", "14.4", "14.5", "15.1", "14.a", "11.7"],
    "Towards a zero-pollution ambition for a toxic-free environment": ["6.3", "6.2", "11.6", "9.4", "6.1", "12.4", "15.3", "3.9", "11.2"]
}


# In[40]:


from matplotlib.patches import Ellipse
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Function to draw the network with thematic areas
def create_network_with_thematic_areas(edge_list, nodes_df, thematic_areas, directed=True, visualize=True, filename="network.gexf", save_visualization=False, visualization_filename="network_visualization.png"):
    """
    Create a graph and overlay thematic areas as transparent clusters.
    Exports the graph as a GEXF file for Gephi.

    Returns:
    - G (nx.Graph or nx.DiGraph): The created network graph.
    - G_undirected (nx.Graph): Undirected version for centrality measures.
    - G_reversed (nx.DiGraph): Reversed version for directed analysis.
    - pos (dict): Node positions for visualization.
    """
    graph_type = nx.DiGraph() if directed else nx.Graph()
    G = nx.from_pandas_edgelist(edge_list, 'TargetA', 'TargetB',
                                edge_attr=["weight", "edge_color", "Interlink Type"], 
                                create_using=graph_type)

    G_undirected = G.to_undirected()
    G_reversed = G.reverse(copy=True) if directed else None

    # Compute node positions
    pos = nx.kamada_kawai_layout(G)

    # Assign node attributes
    weight = nodes_df.set_index('node')['weight'].to_dict()
    node_color_dict_hex = nodes_df.set_index('node')['node_color'].to_dict()
    node_color_dict_rgb = nodes_df.set_index('node')['node_color_RGB'].to_dict()

    nx.set_node_attributes(G, weight, 'weight')
    nx.set_node_attributes(G, node_color_dict_hex, 'color')
    nx.set_node_attributes(G, node_color_dict_rgb, 'node_color_RGB')

    # Define thematic area positions
    thematic_positions = {
        "Climate ambition": np.array([0.2, 0.4]),
        "Clean, affordable and secure energy": np.array([0.0, 0.3]),
        "Industrial strategy for a clean and circular economy": np.array([0.3, 0.3]),
        "Sustainable and smart mobility": np.array([0.0, 0.3]),
        "Greening the Common Agricultural Policy / Farm to Fork Strategy": np.array([-0.1, 0.0]),
        "Preserving and protecting biodiversity": np.array([0.3, -0.2]),
        "Towards a zero-pollution ambition for a toxic-free environment": np.array([-0.1, -0.2])
    }

    # Adjust SDG target positions to cluster around thematic areas
    thematic_bounds = {}
    
    for area, targets in thematic_areas.items():
        if area in thematic_positions:
            center_pos = thematic_positions[area]
            num_targets = len(targets)
            target_positions = []
            
            for i, target in enumerate(targets):
                if target in pos:
                    spread_factor = 0.3 + (i / (num_targets + 1)) * 0.5  
                    angle = (i / num_targets) * 2 * np.pi  
                    spread = np.array([np.cos(angle), np.sin(angle)]) * spread_factor
                    pos[target] = center_pos + spread  
                    target_positions.append(pos[target])

            # Compute bounding box for thematic area
            if target_positions:
                target_positions = np.array(target_positions)
                min_x, max_x = target_positions[:, 0].min(), target_positions[:, 0].max()
                min_y, max_y = target_positions[:, 1].min(), target_positions[:, 1].max()
                
                width = max_x - min_x + 0.3  # Extra padding
                height = max_y - min_y + 0.3  # Extra padding
                
                # Ensure minimum size for small thematic areas
                width = max(width, 0.5)  
                height = max(height, 0.5)

                thematic_bounds[area] = (center_pos, width, height)

    # Export to Gephi
    nx.write_gexf(G, filename, version="1.2draft")

    if visualize:
        fig, ax = plt.subplots(figsize=(12, 10))

        # Thematic area colors
        thematic_colors = {
            "Climate ambition": "#FF9999",
            "Clean, affordable and secure energy": "#99FF99",
            "Industrial strategy for a clean and circular economy": "#9999FF",
            "Sustainable and smart mobility": "#FFFF99",
            "Greening the Common Agricultural Policy / Farm to Fork Strategy": "#FFCC99",
            "Preserving and protecting biodiversity": "#CC99FF",
            "Towards a zero-pollution ambition for a toxic-free environment": "#99FFFF"
        }

        # Draw thematic area ellipses
        for area, (center_pos, width, height) in thematic_bounds.items():
            ellipse = Ellipse(xy=center_pos, width=width, height=height,
                              color=thematic_colors.get(area, "#CCCCCC"), alpha=0.2)
            ax.add_patch(ellipse)

        # Regular node colors & sizes
        node_colors_hex = [node_color_dict_hex.get(n, "#000000") for n in G.nodes()]
        node_sizes = [max(G.nodes[n].get('weight', 0) * 20, 0) for n in G.nodes()]

        # Draw nodes (excluding thematic areas)
        regular_nodes = [n for n in G.nodes() if n not in thematic_areas]
        nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes, node_color=node_colors_hex, node_size=node_sizes, alpha=0.9)
        nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

        # Edge transparency adjustment
        weights = [d['weight'] for _, _, d in G.edges(data=True)]
        max_weight, min_weight = max(weights, default=1), min(weights, default=1)
        alpha = [(d['weight'] - min_weight) / (max_weight - min_weight) if max_weight > min_weight else 0.5 
                 for _, _, d in G.edges(data=True)]
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, 
                               edge_color=[d['edge_color'] for _, _, d in G.edges(data=True)],
                               width=[max(d['weight'] / 8, 0.2) for _, _, d in G.edges(data=True)], 
                               alpha=alpha)

        # Hide axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)

        if save_visualization:
            plt.savefig(visualization_filename, format="PNG")  
            print(f"Network visualization saved as: {visualization_filename}")
        
        plt.show()

    return G, G_undirected, G_reversed, pos

# Synergies
thematic_areas = {
    "Climate ambition": ["13.2", "13.1"],
    "Clean, affordable and secure energy": ["13.2", "9.1", "7.2", "7.3", "7.1", "7.a", "9.4"],
    "Industrial strategy for a clean and circular economy": ["11.6", "12.5", "12.6", "12.2", "12.3", "9.4"],
    "Sustainable and smart mobility": ["7.2", "13.2", "7.3", "9.1", "9.4", "11.2", "3.6", "7.1"],
    "Greening the Common Agricultural Policy / Farm to Fork Strategy": ["12.3", "2.4", "12.4", "14.4", "13.2"],
    "Preserving and protecting biodiversity": ["15.1", "14.5", "15.5", "12.4", "2.4"],
    "Towards a zero-pollution ambition for a toxic-free environment": ["6.3", "6.2", "11.6", "9.4", "6.1"]
}

network_syn, network_syn_undirected, network_syn_rev, pos_syn = create_network_with_thematic_areas(
    edge_list_synergies, nodes_synergies_df, thematic_areas, directed=True, visualize=True
)

#print(f"Gephi file for synergies saved as: {gephi_file_syn}")

# Create and save the trade-offs network
network_tradeoff, network_tradeoff_undirected, network_tradeoff_rev, pos_tradeoff = create_network_with_thematic_areas(
    edge_list_tradeoffs, nodes_tradeoffs_df, thematic_areas, directed=True, visualize=True
    #filename="tradeoffs.gexf",
    #save_visualization=True, visualization_filename="tradeoffs_network_visualization.png"
)


#print(f"Gephi file for trade-offs saved as: {gephi_file_tradeoff}")



# In[37]:


# Create networks for trade-offs using the formula
network_trade, network_trade_undirected, network_trade_rev, pos_trade = create_network_with_thematic_areas(
    edge_list_tradeoffs, nodes_tradeoffs_df, directed=True, visualize=False
)


# In[ ]:


# # # checking if the network is strongly connected, i.e., if all components are. if not, it means that
# some nodes are not linked - in this case, nodes that are not connected in both directions  since all nodes 
# in the network are part of a strongly connected component (SCC). 


# In[ ]:


# Check if nodes are part of strongly connected components (they all are since the list is empty)
def analyze_connectivity(graph, name="Network"):
    """
    Analyzes the connectivity of the directed graph.
    
    Parameters:
    - graph (nx.DiGraph): The directed network graph to analyze.
    - name (str): Name of the network (for print statements).
    
    Returns:
    - dict: A dictionary containing strong/weak connectivity results.
    """
    results = {}

    # Check if the entire graph is strongly connected 
    # A strongly connected network means every node can reach every other node in both directions
    if nx.is_strongly_connected(graph):
        print(f"{name} is strongly connected.")
        results["strongly_connected"] = True
        results["disconnected_nodes"] = set()
    else:
        print(f"{name} is NOT strongly connected.")
        results["strongly_connected"] = False

        # Get all strongly connected components (SCCs)
        sccs = list(nx.strongly_connected_components(graph))
        largest_scc = max(sccs, key=len)  # Find the largest SCC

        # Find nodes not in the largest SCC (most disconnected ones, 
        # these nodes are not part of the largest SCC. 
        # However, they may still be part of smaller SCCs or weakly connected components.
        disconnected_nodes = set(graph.nodes) - largest_scc
        print(f"Nodes not in the largest SCC ({len(largest_scc)} nodes): {disconnected_nodes}")

        results["disconnected_nodes"] = disconnected_nodes

    # Check weak connectivity
    # A weakly connected network means that if we ignore the direction of edges,
    # all nodes are still part of a single connected component.
    wccs = list(nx.weakly_connected_components(graph))
    not_fully_connected_nodes = set()

    for wcc in wccs:
        subgraph = graph.subgraph(wcc)
        if not nx.is_strongly_connected(subgraph):  # If weakly connected but not strongly
            not_fully_connected_nodes.update(wcc)

    print(f"Nodes not fully connected in both directions: {not_fully_connected_nodes}")

    results["not_fully_connected_nodes"] = not_fully_connected_nodes

    return results

# Run analysis for synergies network
synergies_results = analyze_connectivity(network_syn, "Synergies Network")


# In[ ]:


# Repeat for connectivity in trade-offs network


# In[ ]:


# Run analysis for tradeoffs network
tradeoffs_results = analyze_connectivity(network_trade, "tradeoffs Network")


# In[ ]:


# Obtain various centrality measures

## Eigenvector centrality
def compute_eigenvector_centrality(graph, name="Graph"):
    """
    Computes eigenvector centrality for a given directed/undirected graph.

    Parameters:
    - graph (nx.Graph or nx.DiGraph): The input network graph.
    - name (str): Name of the network (for print statements).

    Returns:
    - pd.DataFrame: DataFrame with eigenvector centrality values.
    """
    try:
        eigen = nx.eigenvector_centrality(graph, max_iter=1000, tol=1e-06, weight="weight") 
        #to compute eigenvector centrality without weights, modify the function by setting weight=None
        df = pd.DataFrame(eigen.items(), columns=['target', 'eigen_centr'])
        return df.sort_values(by=['eigen_centr'], ascending=False)
    except nx.PowerIterationFailedConvergence:
        print(f"Eigenvector centrality did not converge for {name}. Consider using Katz centrality instead.")
        return pd.DataFrame(columns=['target', 'eigen_centr'])

# Compute Eigenvector Centrality Synergies
# For directed graphs nx.eigenvector_centrality is “left” eigenvector centrality 
# which corresponds to the in-edges in the graph. For out-edges eigenvector centrality use reversed df
eigen_df_dir = compute_eigenvector_centrality(network_syn, "Synergies Network")
eigen_df_dir_out = compute_eigenvector_centrality(network_syn_rev, "Reversed Synergies Network")

# Compute Eigenvector Centrality Tradeoffs
eigen_df_dir_trade = compute_eigenvector_centrality(network_trade, "Tradeoffs Network")
eigen_df_dir_out_trade = compute_eigenvector_centrality(network_trade_rev, "Reversed Tradeoffs Network")


# In[ ]:


##in_degree; the in-degree centrality for a node v is the fraction of nodes its incoming edges are connected to.

def compute_in_degree_centrality(graph, name="Graph"):
    """
    Computes in-degree centrality for a directed graph.

    Parameters:
    - graph (nx.DiGraph): The input directed network graph.
    - name (str): Name of the network (for print statements).

    Returns:
    - pd.DataFrame: DataFrame with in-degree centrality values.
    """
    in_degree = nx.in_degree_centrality(graph)
    df = pd.DataFrame(in_degree.items(), columns=['target', 'in_degree_centr'])
    return df.sort_values(by=['in_degree_centr'], ascending=False)

# Compute In-Degree Centrality for Synergies Network
in_degree_df = compute_in_degree_centrality(network_syn, "Synergies Network")

# Display top 10 results
print(in_degree_df.head(10))


# In[ ]:


## tradeoffs
in_degree_tradeoffs_df = compute_in_degree_centrality(network_trade, "Tradeoffs Network")
print(in_degree_tradeoffs_df.head(10))


# In[ ]:


## Out_degree; the out-degree centrality for a node v is the fraction of nodes its  outgoing edges are connected to.

def compute_out_degree_centrality(graph, name="Graph"):
    """
    Computes out-degree centrality for a directed graph.

    Parameters:
    - graph (nx.DiGraph): The input directed network graph.
    - name (str): Name of the network (for print statements).

    Returns:
    - pd.DataFrame: DataFrame with out-degree centrality values.
    """
    out_degree = nx.out_degree_centrality(graph)
    df = pd.DataFrame(out_degree.items(), columns=['target', 'out_degree_centr'])
    return df.sort_values(by=['out_degree_centr'], ascending=False)

# Compute Out-Degree Centrality for Synergies Network
out_degree_df = compute_out_degree_centrality(network_syn, "Synergies Network")

# Display top 10 results
print(out_degree_df.head(10))


# In[ ]:


# Compute Out-Degree Centrality for Tradeoffs Network
out_degree_df_trade = compute_out_degree_centrality(network_trade, "Tradeoffs Network")

# Display top 10 results
print(out_degree_df_trade.head(10))


# In[ ]:


def calculate_closeness_with_distance(network):
    """
    Calculate both inward and outward closeness centrality for a given network using distance 
    (reciprocal of edge weight) and return the results as sorted DataFrames for both.

    Parameters:
    network (networkx.Graph): The input network (graph).

    Returns:
    pd.DataFrame, pd.DataFrame: DataFrames containing the nodes and their corresponding
                                inward and outward closeness centralities, sorted in descending order.
    """
    
    # Create the 'distance' attribute for each edge in the original graph
    network_syn_distance_dict = {
        (e1, e2): 1 / weight if weight != 0 else float('inf')  # Handle zero weights
        for e1, e2, weight in network.edges(data='weight')
    }

    # Set the 'distance' attribute for the edges in the graph
    nx.set_edge_attributes(network, network_syn_distance_dict, 'distance')

    # Calculate inward closeness centrality (using the original graph)
    closen_w_in = nx.closeness_centrality(network, u=None, distance='distance', wf_improved=True)

    # Reverse the graph for outward closeness centrality
    network_rev = network.reverse()

    # Calculate outward closeness centrality (using the reversed graph)
    closen_w_out = nx.closeness_centrality(network_rev, u=None, distance='distance', wf_improved=True)

    # Create DataFrames for the closeness centrality results (both inward and outward)
    closen_w_in_df = pd.DataFrame(closen_w_in.items(), columns=['target', 'closen_centr_w_in'])
    closen_w_out_df = pd.DataFrame(closen_w_out.items(), columns=['target', 'closen_centr_w_out'])

    # Sort both DataFrames by closeness centrality in descending order
    closen_w_in_df_sorted = closen_w_in_df.sort_values(by=['closen_centr_w_in'], ascending=False)
    closen_w_out_df_sorted = closen_w_out_df.sort_values(by=['closen_centr_w_out'], ascending=False)

    return closen_w_in_df_sorted, closen_w_out_df_sorted

# Create df for synergies
closen_w_in_df_sorted, closen_w_out_df_sorted = calculate_closeness_with_distance(network_syn)
print(closen_w_in_df_sorted)
print(closen_w_out_df_sorted)

# Create df for tradeoffs
closen_w_in_df_sorted_trade, closen_w_out_df_sorted_trade = calculate_closeness_with_distance(network_trade)
print(closen_w_in_df_sorted_trade)
print(closen_w_out_df_sorted_trade)


# In[ ]:


def compute_betweenness(graph, use_distance=True, name="Graph"):
    """
    Computes betweenness centrality.

    Parameters:
    - graph (nx.Graph or nx.DiGraph): The input network graph.
    - use_distance (bool): If True, uses 'distance' (1/weight); otherwise, uses 'weight'.
    - name (str): Name of the network (for debugging output).

    Returns:
    - pd.DataFrame: Betweenness centrality values.
    """
    weight_attr = 'distance' if use_distance else 'weight'

    graph = graph.copy()  # Prevent modifying the original graph
    for u, v, d in graph.edges(data=True):
        if "weight" in d and d["weight"] > 0:
            d["distance"] = 1 / d["weight"]  # Compute reciprocal weight
        else:
            d["distance"] = float("inf")  # Prevent division errors

    # Compute betweenness centrality
    betweenness = nx.betweenness_centrality(graph, weight=weight_attr, normalized=True)
    
    # Convert results to DataFrame
    df = pd.DataFrame(betweenness.items(), columns=['target', f'betweenness_{weight_attr}'])
    return df

# # Compute Betweenness for Synergie Network
between_wd_df = compute_betweenness(network_syn, use_distance=True, name="Synergies Network (Reciprocal Weight)")
# Compute Outgoing Betweenness Using Reversed Graph
between_wd_out_df = compute_betweenness(network_syn_rev, use_distance=True, name="Synergies Network (Outgoing)")


# Compute Betweenness for Trade-offs Network
between_wd_df_trade = compute_betweenness(network_trade, use_distance=True, name="Tradeoffs Network (Reciprocal Weight)")
# Compute Outgoing Betweenness Using Reversed Graph
between_wd_out_df_trade = compute_betweenness(network_trade_rev, use_distance=True, name="Tradeoffs Network (Outgoing)")


# In[ ]:


# Hubs and Authorities
def compute_hits(graph, name="Graph"):
    """
    Computes HITS (Hubs and Authorities) centrality for a directed graph.

    Parameters:
    - graph (nx.DiGraph): The directed network graph.
    - name (str): Name of the network (for debugging output).

    Returns:
    - pd.DataFrame: DataFrame containing hub and authority scores.
    """
    try:
        hubs, authorities = nx.hits(graph, max_iter=100, tol=1e-08, normalized=True)

        # Convert to DataFrame
        hubs_df = pd.DataFrame.from_dict(hubs, orient='index', columns=['hub'])
        auth_df = pd.DataFrame.from_dict(authorities, orient='index', columns=['authority'])

        # Merge results
        hits_df = hubs_df.join(auth_df)

        return hits_df  # Sorting should be done at analysis time
    except nx.PowerIterationFailedConvergence:
        print(f"HITS did not converge for {name}. Try increasing `max_iter` or using another centrality measure.")
        return pd.DataFrame(columns=['hub', 'authority'])

# Compute HITS for Synergies and Trade-Offs Networks
hits_auts_syn_df = compute_hits(network_syn, "Synergies Network")
hits_auts_trade_df = compute_hits(network_trade, "Tradeoffs Network")

# Display Top 10 Nodes by Hub and Authority Scores
print("\nTop Hubs (Synergies Network):")
print(hits_auts_syn_df.sort_values(by=['hub'], ascending=False).head(10))

print("\nTop Authorities (Synergies Network):")
print(hits_auts_syn_df.sort_values(by=['authority'], ascending=False).head(10))


# In[ ]:


## Edge betweeness centrality to highlight link were the most shortest paths pass from. check wheter to use or not
import networkx as nx
import pandas as pd

def compute_edge_betweenness(graph, use_distance=True, name="Graph"):
    """
    Computes edge betweenness centrality for a network.

    Parameters:
    - graph (nx.Graph or nx.DiGraph): The input network graph.
    - use_distance (bool): If True, uses 'distance' (1/weight); otherwise, uses 'weight'.
    - name (str): Name of the network (for debugging output).

    Returns:
    - pd.DataFrame: DataFrame with edge betweenness centrality values.
    """
    weight_attr = 'distance' if use_distance else 'weight'
    
    # Ensure weight attribute exists before calculation
    if not any(weight_attr in d for _, _, d in graph.edges(data=True)):
        print(f"Warning: '{weight_attr}' not found in edges of {name}. Using unweighted betweenness.")
        weight_attr = None  # Fall back to unweighted
    
    edge_betweenness = nx.edge_betweenness_centrality(graph, weight=weight_attr)
    df = pd.DataFrame(list(edge_betweenness.items()), columns=['Edge', 'Betweenness Centrality'])
    return df.sort_values(by=['Betweenness Centrality'], ascending=False)

# Precompute distance attribute (1/weight) for synergies network
for u, v, d in network_syn.edges(data=True):
    d["distance"] = 1 / d["weight"] if d["weight"] > 0 else float("inf")

# Compute Edge Betweenness Centrality (Using Distance)
edge_betweenness_syn_df = compute_edge_betweenness(network_syn, use_distance=True, name="Synergies Network")

# Compute Edge Betweenness Centrality (Using Weight Directly)
edge_betweenness_syn_weight_df = compute_edge_betweenness(network_syn, use_distance=False, name="Synergies Network (Weight-Based)")

# Compute Edge Betweenness for Tradeoffs Network
for u, v, d in network_trade.edges(data=True):
    d["distance"] = 1 / d["weight"] if d["weight"] > 0 else float("inf")

edge_betweenness_trade_df = compute_edge_betweenness(network_trade, use_distance=True, name="Tradeoffs Network")

# Display top results
print(edge_betweenness_syn_df.head(10))
print(edge_betweenness_trade_df.head(10))


# In[ ]:


## Export the excel files for synergies and tradeoffs with the centrality measures selected


# In[ ]:


# Store values in excel

# Output file path
output_file = Path("centrality_measures_EGD_synergies.xlsx")

# Create a dictionary of dfs with corresponding sheet names
dfs_to_export = {
    "eigen_dir": eigen_df_dir,
    "eigen_dir_out": eigen_df_dir_out,
    "closen_w": closen_w_in_df_sorted,
    "closen_w_out": closen_w_out_df_sorted,
    "between_wd": between_wd_df,
    "between_wd_out": between_wd_out_df,
    "out_degree": out_degree_df,  # Ensure no duplicate writes
    "in_degree": in_degree_df,  # Ensure no duplicate writes
    "hits": hits_auts_syn_df,
    # "edge_betweenness": edge_betweenness_syn_df,  # Uncomment if needed
}

# Write to Excel
try:
    with pd.ExcelWriter(output_file) as writer:
        for sheet_name, df in dfs_to_export.items():
            if df.empty:  # Skip empty DataFrames
                continue
            if sheet_name == "hits":  # Special handling for the 'hits' DataFrame
                df.to_excel(writer, sheet_name=sheet_name, index=True) # Write with index, because index = sdg target
            else:
                df.to_excel(writer, sheet_name=sheet_name, index=False) # Write without index
    print(f"Successfully saved centrality measures to: {output_file}")
except Exception as e:
    print(f"Error writing to Excel: {e}")


# In[ ]:


# Store values in excel for tradeoffs

# Output file path
output_file = Path("centrality_measures_EGD_tradeoffs.xlsx")

# Create a dictionary of dfs with corresponding sheet names
dfs_to_export = {
    "eigen_dir": eigen_df_dir_trade,
    "eigen_dir_out": eigen_df_dir_out_trade,
    "closen_w": closen_w_in_df_sorted_trade,
    "closen_w_out": closen_w_out_df_sorted_trade,
    "between_wd": between_wd_df_trade,
    "between_wd_out": between_wd_out_df_trade,
    "out_degree": out_degree_df_trade, 
    "in_degree": in_degree_tradeoffs_df,  
    "hits": hits_auts_trade_df,
    # "edge_betweenness": edge_betweenness_trade_df,  # Uncomment if needed
}

# Write to Excel
try:
    with pd.ExcelWriter(output_file) as writer:
        for sheet_name, df in dfs_to_export.items():
            if df.empty:  # Skip empty DataFrames
                continue
            if sheet_name == "hits":  # Special handling for the 'hits' DataFrame
                df.to_excel(writer, sheet_name=sheet_name, index=True) # Write with index, because index = sdg target
            else:
                df.to_excel(writer, sheet_name=sheet_name, index=False) # Write without index
    print(f"Successfully saved centrality measures to: {output_file}")
except Exception as e:
    print(f"Error writing to Excel: {e}")


# In[ ]:


# Export the nodes and edges list for synergies and trade-offs to use them in gephi (nicer visuals)
# Remember to go back and assign node_color_RGB rather than node_color before downloading the data
# for gephi, as gephi requires RGB data


# In[ ]:


nx.write_gexf(network_syn, 'syn_graph_EGDintra.gexf', encoding='utf-8', prettyprint=True)

# nx.write_gexf(network_trade, "trade_graph_egd_intra.gexf",  encoding='utf-8', prettyprint=True)

#NOTE THAT THE COLORS OF THE NODES WILL NEED TO BE ADJUSTED IN GEPHI by duplicating the color column and USING THE NECESSARY PLUGIN
nx.write_graphml(network_syn, "test.graphml")


# In[ ]:




