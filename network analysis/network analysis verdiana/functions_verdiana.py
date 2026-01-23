

#--------------------------------------------------------------------------------------------------------------------------------------------


subthemes_colors = {
    'GHG Reduction - Buildings': '#DDEBF7',
    'GHG Reduction - Transports': '#DDEBF7',
    'GHG Reduction': '#DDEBF7',
    'GHG Removal': '#DDEBF7',
    'Climate Resilience': '#DDEBF7',
    'Methane': '#DDEBF7',

    'Renewable Energy - Hydrogen Production': '#FFF2CC',
    'Renewable Energy': '#FFF2CC',
    'Renewable Energy - Heating & Cooling': '#FFF2CC',
    'Energy Infrastructure': '#FFF2CC',
    'Energy Efficiency': '#FFF2CC',
    'Energy Efficiency - Buildings': '#FFF2CC',
    'Renewable Energy - Ocean/Offshore': '#FFF2CC',
    'Renewable Energy - Solar': '#FFF2CC',

    'Waste Reduction - Municipal Waste': '#FFC4C5',
    'Critical Raw Materials - Extraction & Import': '#FFC4C5',
    'Net-Zero Technology - Manufacturing': '#FFC4C5',
    'Circularity/Recycling - Critical Raw Materials - Batteries Recycling': '#FFC4C5',
    'Waste Reduction - Food Waste': '#FFC4C5',
    'Waste Reduction - Plastic & Packaging': '#FFC4C5',
    'Circularity/Recycling - Plastic & Packaging': '#FFC4C5',
    'Circularity/Recycling': '#FFC4C5',
    'Circularity/Recycling - Municipal Waste': '#FFC4C5',
    'Circularity/Recycling - Vehicle Circularity': '#FFC4C5',

    'Biofuels': '#E4CCEC',
    'Transport Logistics': '#E4CCEC',
    'Net-Zero Technology - Road Vehicles': '#E4CCEC',
    'Hydrogen Distribution': '#E4CCEC',
    'Urban Mobility': '#E4CCEC',
    'Other Low-Carbon Fuels': '#E4CCEC',

    'Biodiversity Protection & Conservation': '#C6F0CE',
    'Food quality': '#C6F0CE',
    'Social Security - Workers Protection': '#C6F0CE',
    'Competitive Agriculture': '#C6F0CE',
    'Food affordability': '#C6F0CE',
    'Food quality - Animal Welfare': '#C6F0CE',
    'Food quality - Healthy Food': '#C6F0CE',
    'Digitalisation': '#C6F0CE',
    'Improve Soils Health': '#C6F0CE',
    'Pesticides Reduction': '#C6F0CE',
    'Improve Water Quality': '#C6F0CE',

    'Terrestrial Ecosystems Restoration - Agricultural Ecosystems': '#DBCFC1',
    'Terrestrial Ecosystems Restoration - Forests': '#DBCFC1',
    'Terrestrial Ecosystems Restoration - Rivers': '#DBCFC1',
    'Biodiversity Protection & Conservation - Urban Nature': '#DBCFC1',
    'Biodiversity Protection & Conservation - Fisheries': '#DBCFC1',
    'Terrestrial Ecosystems Restoration': '#DBCFC1',
    'Marine Ecosystem Restoration': '#DBCFC1',
    'Biodiversity Protection & Conservation - Monitoring': '#DBCFC1',
    'Improve Air Quality': '#DBCFC1',

    'Noise Reduction': '#FCE4D6'
}
#--------------------------------------------------------------------------------------------------------------------------------------------


def build_node_to_subtheme(raw_df):
    source_map = raw_df[["source_target", "source_target_subtheme"]] \
        .rename(columns={"source_target": "node", "source_target_subtheme": "subtheme"})

    impact_map = raw_df[["impact_target", "impact_target_subtheme"]] \
        .rename(columns={"impact_target": "node", "impact_target_subtheme": "subtheme"})

    node_subtheme = pd.concat([source_map, impact_map], ignore_index=True)

    # Drop duplicates, keep first occurrence
    node_subtheme = node_subtheme.dropna().drop_duplicates(subset="node")

    return node_subtheme.set_index("node")["subtheme"].to_dict()

#--------------------------------------------------------------------------------------------------------------------------------------------


def node_color_from_subtheme(node, node_to_subtheme, default="#000000"):
    subtheme = node_to_subtheme.get(node)
    if subtheme is None:
        return default
    return subthemes_colors.get(subtheme, default)


#--------------------------------------------------------------------------------------------------------------------------------------------

def build_node_to_thematic_area(raw_df):
    src = raw_df[["source_target", "source_thematic_area"]] \
        .rename(columns={"source_target": "node", "source_thematic_area": "area"})

    tgt = raw_df[["impact_target", "impact_thematic_area"]] \
        .rename(columns={"impact_target": "node", "impact_thematic_area": "area"})

    node_area = pd.concat([src, tgt], ignore_index=True)
    node_area = node_area.dropna().drop_duplicates(subset="node")

    return node_area.set_index("node")["area"].to_dict()

#--------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd

def convert_data_to_verdiana_syntax(raw_df):
    edge_list = raw_df.rename(columns={
        "source_target": "TargetA",
        "impact_target": "TargetB",
        "impact_type": "Interlink Type",
        "impact_color": "edge_color",
        "impact_weight": "weight"
    })[["TargetA", "TargetB", "Interlink Type", "edge_color", "weight"]].copy()

    all_nodes = pd.unique(edge_list[["TargetA", "TargetB"]].values.ravel())
    nodes_df = pd.DataFrame({"node": all_nodes})

    node_to_subtheme = build_node_to_subtheme(raw_df)

    nodes_df["subtheme"] = nodes_df["node"].map(node_to_subtheme)
    nodes_df["node_color"] = nodes_df["node"].apply(
        lambda n: node_color_from_subtheme(n, node_to_subtheme)
    )

    nodes_df["node_color_RGB"] = nodes_df["node_color"].str.lstrip('#').apply(
        lambda x: ','.join(str(int(x[i:i+2], 16)) for i in (0, 2, 4)) if isinstance(x, str) else "0,0,0"
    )

    nodes_df["weight"] = 1  # or any logic you want

    return edge_list, nodes_df

#--------------------------------------------------------------------------------------------------------------------------------------------

from collections import defaultdict

def build_thematic_areas_dict(node_to_area):
    thematic_areas = defaultdict(list)
    for node, area in node_to_area.items():
        thematic_areas[area].append(node)
    return dict(thematic_areas)

#--------------------------------------------------------------------------------------------------------------------------------------------

def clean_area_name(area):
    if isinstance(area, str) and " - " in area:
        return area.split(" - ", 1)[1]
    return area



#--------------------------------------------------------------------------------------------------------------------------------------------

from matplotlib.patches import Ellipse
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


# Function to draw the network with thematic areas
def create_network_with_thematic_areas(edge_list, nodes_df, thematic_areas, directed=True, visualize=True, 
                                       filename="network.gexf", save_visualization=False, visualization_filename="network_visualization.png"):
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
        "TA1 - Climate ambition": np.array([0.2, 0.4]),
        "TA2 - Clean, affordable and secure energy": np.array([0.0, 0.3]),
        "TA3 - Industrial strategy for a clean and circular economy": np.array([0.3, 0.3]),
        "TA4 - Sustainable and smart mobility": np.array([0.0, 0.3]),
        "TA5 - Greening the Common Agricultural Policy / Farm to Fork Strategy": np.array([-0.1, 0.0]),
        "TA6 - Preserving and protecting biodiversity": np.array([0.3, -0.2]),
        "TA7 - Towards a zero-pollution ambition for a toxic-free environment": np.array([-0.1, -0.2])
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
            "TA1 - Climate ambition": "#FF9999",
            "TA2 - Clean, affordable and secure energy": "#99FF99",
            "TA3 - Industrial strategy for a clean and circular economy": "#9999FF",
            "TA4 - Sustainable and smart mobility": "#FFFF99",
            "TA5 - Greening the Common Agricultural Policy / Farm to Fork Strategy": "#FFCC99",
            "TA6 - Preserving and protecting biodiversity": "#CC99FF",
            "TA7 - Towards a zero-pollution ambition for a toxic free environment": "#99FFFF"
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


#--------------------------------------------------------------------------------------------------------------------------------------------

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


#--------------------------------------------------------------------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------------------------------------------------------------------


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


#--------------------------------------------------------------------------------------------------------------------------------------------


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



#--------------------------------------------------------------------------------------------------------------------------------------------

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



#--------------------------------------------------------------------------------------------------------------------------------------------


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

#--------------------------------------------------------------------------------------------------------------------------------------------


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


#--------------------------------------------------------------------------------------------------------------------------------------------


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



#--------------------------------------------------------------------------------------------------------------------------------------------


