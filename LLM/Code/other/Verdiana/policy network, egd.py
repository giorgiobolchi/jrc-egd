#!/usr/bin/env python
# coding: utf-8

# In[2]:


import networkx as nx
import pandas as pd
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text


# In[3]:


# Read in the cleaned database for the edge list (edges are interlinkages, nodes are targets)
def load_data(file_path):
    return pd.read_excel(file_path)

# Load the data
file_path = r'C:\Users\verdy\Downloads\database_16052023.xlsx'
db_for_edgelist = load_data(file_path)


# In[4]:


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


# In[6]:


# Assign colors to edges based on Interlink Type
edge_list=only_nec_columns
edge_list['edge_color'] = '#32FC5A'  # Default color for synergies
edge_list.loc[edge_list['Interlink Type'] == '-', 'edge_color'] = '#900D09'  # Trade-offs color


# In[14]:


print(edge_list)


# In[31]:


thematic_colors = {
    "Climate ambition": '#a2d327',
    "Clean, affordable and secure energy": '#f9f90b',
    "Industrial strategy for a clean and circular economy": '#f0ab0d',
    "Sustainable and smart mobility": '#39b1bb',
    "Greening the Common Agricultural Policy": '#A52A2A',
    "Preserving and protecting biodiversity": '#39bb46',
    "Towards a zero-pollution ambition for a toxic-free environment": '#a34df9'
}


# In[32]:


thematic_areas_policies = {
    "Climate ambition": ["Amending Directive 2003/87/EC","Amending Regulation (EU) 2018/842",
                         "Amending Regulations (EU) 2018/841","European Climate Law",
                         "On an EU Strategy to reduce methane emissions"
    ],
    "Clean, affordable and secure energy": ["A hydrogen strategy for a climate-neutral Europe","A Renovation Wave for Europe",
                                             "Amending Directive (EU) 2018/2001, Regulation (EU) 2018/1999 and Directive 98/70/EC - energy from renewable sources",
                                             "Concerning urban wastewater treatment (recast)","Delivering on the EU offshore renewable energy ambitions",
                                             "EU Solar Energy Strategy","On energy efficiency and amending Regulation (EU) 2023/955 (recast)",
                                             "On the Energy Performance of Buildings (recast)",
                                             "Powering a Climate neutrality economy:","REPowerEU Plan","Stepping up Europe’s 2030 climate ambition"
    ],
    "Industrial strategy for a clean and circular economy": ["A new Circular Economy Action Plan","Amending Directive 2008/98/EC on waste",
                                                             "Concerning batteries and waste batteries","On circularity requirements for vehicle design",
                                                             "Net Zero Industry Act","On packaging and packaging waste",
                                                             "On Sustainable Carbon Cycles","REGULATION (EU) 2024/1252  - critical raw materials"
    ],
    "Sustainable and smart mobility": ["Amending Council Directive 92/106/EEC","Amending Regulation (EU) 2019/1242",
                                       "Amending Directive (EU) 2018/2001, Regulation (EU) 2018/1999 and Directive 98/70/EC - energy from renewable sources",
                                       "On ensuring a level playing field for sustainable air transport","On the deployment of alternative fuels infrastructure",
                                       "On the Energy Transition of the EU Fisheries and Aquaculture sector",
                                       "On the use of renewable and low-carbon fuels in maritime transport",
                                       "Sustainable and Smart Mobility Strategy", "The new EU Urban Mobility Framework"
    ],
    "Greening the Common Agricultural Policy": ["A Farm to Fork Strategy",
    ],
    "Preserving and protecting biodiversity": ["EU Biodiversity Strategy for 2030","EU Soil Strategy for 2030",
                                               "On nature restoration and amending Regulation (EU) 2022/869",
                                               "The common fisheries policy today and tomorrow",
    ],
    "Towards a zero-pollution ambition for a toxic-free environment": ["Directive 2010/75/EU of the European Parliament and of the Council of 24 November 2010 on industrial emissions",
                                                                       "On ambient air quality and cleaner air for Europe",
                                                                       "On minimum requirements for water reuse",
                                                                       "On the quality of water intended for human consumption",
                                                                       "Pathway to a Healthy Planet for All EU Action Plan",
                                                                       "Proposal for a Directive on water quality", "EU Soil Strategy for 2030",
                                                                       "Concerning urban wastewater treatment (recast)"
    ]}


# In[33]:


sdg_target_links = {
    "Amending Directive 2003/87/EC": ["13.2"],
    "A hydrogen strategy for a climate-neutral Europe": ["9.1"],
    "A Renovation Wave for Europe": ["7.3", "13.2"],
    "Amending Directive (EU) 2018/2001, Regulation (EU) 2018/1999 and Directive 98/70/EC - energy from renewable sources" : ["7.1","7.2","9.4", "13.2", "7.a"],
    "A Farm to Fork Strategy": ["2.4", "9.1", "12.3", "12.4"],
    "EU Biodiversity Strategy for 2030": ["2.4", "12.4", "14.5", "15.1", "15.5", "11.b"],
    "Circular Economy Action Plan": ["11.6", "12.5"],
    "Delivering on the EU offshore renewable energy ambitions": ["7.2"],
    "Pathway to a Healthy Planet for All EU Action Plan": ["3.9", "6.3", "11.6", "12.4"],
    "EU Soil Strategy for 2030": ["12.4", "15.3"],
    "Proposal for a Directive on water quality": ["6.3"],
    "REPowerEU Plan": ["7.3", "9.1","9.4"],
    "On an EU Strategy to reduce methane emissions": ["13.2"],
    "Amending Regulation (EU) 2018/842": ["13.2"],
    "Amending Regulations (EU) 2018/841": ["13.2"],
    "European Climate Law": ["13.2"],
    "On energy efficiency and amending Regulation (EU) 2023/955 (recast)": ["7.3"],
    "On the Energy Performance of Buildings": ["7.3"],
    "Powering a Climate neutrality economy": ["7.2"],
    "Stepping up Europe’s 2030 climate ambition": ["7.3"],
    "On the Energy Transition of the EU Fisheries and Aquaculture sector": ["7.3"],
    "On the use of renewable and low-carbon fuels in maritime transport": ["7.2"],
    "On ensuring a level playing field for sustainable air transport": ["13.2"],
    "On the deployment of alternative fuels infrastructure": ["7.2","9.1","9.4"],
    "The new EU Urban Mobility Framework": ["13.2"],
    "On circularity requirements for vehicle design": ["12.5"],
    "On packaging and packaging waste": ["12.5"],
    "On Sustainable Carbon Cycles": ["9.4"],
    "REGULATION (EU) 2024/1252  - critical raw materials": ["12.2"],
    "Concerning urban wastewater treatment (recast)": ["13.2", "6.2"],
    "On the quality of water intended for human consumption": ["6.1"],
    "On ambient air quality and cleaner air for Europe": ["11.6"],
    "On minimum requirements for water reuse": ["6.3"],
    "Amending Regulation (EU) 2019/1242": ["13.2"],
    "Net Zero Industry Act": ["9.4"],
    "EU Solar Energy Strategy": ["7.2"], 
    "Amending Directive 2008/98/EC on waste": ["12.3"],
    "Concerning batteries and waste batteries": ["12.5"],
    "Amending Council Directive 92/106/EEC": ["9.1"],
    "Sustainable and Smart Mobility Strategy": ["13.2"],
    "On nature restoration and amending Regulation (EU) 2022/869": ["2.4", "6.6", "11.7", "14.2", "14.a", "15.1", "15.2", "15.3", "15.5"],
    "The common fisheries policy today and tomorrow": ["14.4"],
    "Directive 2010/75/EU of the European Parliament and of the Council": ["9.4"] 
}


# In[39]:


# Function to get node color for policies with multiple areas (return a list of colors)
def get_policy_colors(policy):
    areas = [area for area, policies in thematic_areas_policies.items() if policy in policies]
    colors = [thematic_colors.get(area, 'gray') for area in areas]
    return colors

# 1. Create separate SDG interlinkage graphs for + and -
G_sdg_pos = nx.Graph()
G_sdg_neg = nx.Graph()

for _, row in edge_list.iterrows():
    if row['Interlink Type'] == '+':
        G_sdg_pos.add_edge(row['TargetA'], row['TargetB'])
    else:
        G_sdg_neg.add_edge(row['TargetA'], row['TargetB'])

# 2. Function to create policy networks based on an SDG graph
def create_policy_network(G_sdg):
    G_policy = nx.Graph()
    edges_direct = []
    edges_indirect = []

    # Add policy nodes
    for policy, targets in sdg_target_links.items():
        G_policy.add_node(policy, type='policy', colors=get_policy_colors(policy))

    # Create direct and indirect links between policies
    for policy1, targets1 in sdg_target_links.items():
        for policy2, targets2 in sdg_target_links.items():
            if policy1 != policy2:
                shared_targets = set(targets1) & set(targets2)
                if shared_targets:
                    G_policy.add_edge(policy1, policy2, reason='shared_target')
                    edges_direct.append((policy1, policy2))

                for t1 in targets1:
                    for t2 in targets2:
                        if G_sdg.has_edge(t1, t2):
                            G_policy.add_edge(policy1, policy2, reason='sdg_interlink')
                            edges_indirect.append((policy1, policy2))

    return G_policy, edges_direct, edges_indirect

# Create policy networks for + and - interlinkages
G_policy_pos, edges_direct_pos, edges_indirect_pos = create_policy_network(G_sdg_pos)
G_policy_neg, edges_direct_neg, edges_indirect_neg = create_policy_network(G_sdg_neg)

# Function to plot the network
def plot_policy_network(G_policy, edges_indirect, title):
    pos = nx.kamada_kawai_layout(G_policy)
    plt.figure(figsize=(12, 12))
    plt.title(title, size=15)

    # Loop through all the nodes to set the colors
    for node in G_policy.nodes():
        x, y = pos[node]
        # Get the thematic areas associated with the policy node
        node_colors = []
        areas = [area for area, policies in thematic_areas_policies.items() if node in policies]
        
        if areas:
            # Assign color for nodes based on thematic areas
            node_colors = [thematic_colors[area] for area in areas if area in thematic_colors]
        
        # Skip nodes that do not belong to any thematic area
        if not node_colors:
            continue  # Skip this node if no thematic color is found
        
        # If only one color is assigned, use scatter to plot the node
        if len(node_colors) == 1:
            plt.scatter(x, y, s=2000, c=node_colors[0], edgecolors='w', linewidth=2)
        else:
            # For nodes with multiple thematic areas, use pie chart trick
            wedges, _ = plt.pie([1] * len(node_colors), colors=node_colors, radius=0.1, center=(x, y), wedgeprops=dict(width=0.1, edgecolor='w'))

    # Draw edges
    #nx.draw_networkx_edges(G_policy, pos, edgelist=edges_direct, edge_color='lightgreen', width=1, style="dashed", label="Direct links")
    nx.draw_networkx_edges(G_policy, pos, edgelist=edges_indirect, edge_color='lightblue', width=1, style="solid", label="Indirect links")

    # Draw labels
    nx.draw_networkx_labels(G_policy, pos, font_size=10, font_color='black')

    # Show the plot
    plt.show()
    
# 4. Plot both graphs
plot_policy_network(G_policy_pos, edges_indirect_pos, "Positive SDG Interlinkages")
plot_policy_network(G_policy_neg, edges_indirect_neg, "Negative SDG Interlinkages")


# In[ ]:




