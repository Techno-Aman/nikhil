import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community

st.set_page_config(page_title="Dynamic Network Analysis", layout="centered")

st.title("📊Social Network Analysis")

# Initialize graph in session state
if "G" not in st.session_state:
    st.session_state.G = nx.Graph()

G = st.session_state.G

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

# Add Node
new_node = st.sidebar.text_input("Add Node")
if st.sidebar.button("➕ Add Node"):
    if new_node:
        G.add_node(new_node)
        st.sidebar.success(f"Node '{new_node}' added!")

# Add Edge
st.sidebar.subheader("Add Connection")
nodes = list(G.nodes())

node1 = st.sidebar.selectbox("Node 1", nodes)
node2 = st.sidebar.selectbox("Node 2", nodes)

if st.sidebar.button("🔗 Add Edge"):
    if node1 and node2:
        G.add_edge(node1, node2)
        st.sidebar.success(f"Edge ({node1}, {node2}) added!")

# Reset Graph
if st.sidebar.button("🗑 Reset Graph"):
    st.session_state.G = nx.Graph()
    st.sidebar.warning("Graph reset!")


# ---------------- DELETE NODE ----------------
st.sidebar.subheader("🗑 Delete Node")

nodes = list(G.nodes())

if nodes:
    del_node = st.sidebar.selectbox("Select Node to Delete", nodes, key="del_node")

    if st.sidebar.button("❌ Delete Node"):
        G.remove_node(del_node)
        st.sidebar.success(f"Node '{del_node}' deleted!")
else:
    st.sidebar.info("No nodes to delete")


# ---------------- DELETE EDGE ----------------
st.sidebar.subheader("🔗 Delete Connection")

edges = list(G.edges())

if edges:
    del_edge = st.sidebar.selectbox("Select Edge to Delete", edges, key="del_edge")

    if st.sidebar.button("❌ Delete Edge"):
        G.remove_edge(*del_edge)
        st.sidebar.success(f"Edge {del_edge} deleted!")
else:
    st.sidebar.info("No edges to delete")

# ---------------- MAIN CONTENT ----------------

# Show Nodes & Edges
col2, col3 = st.columns(2)

# ---------------- COLUMN 2 ----------------
with col2:
    if len(G.nodes()) > 0:
        st.subheader("⭐ Influencer Ranking")
        centrality = nx.degree_centrality(G)

        for fan, score in centrality.items():
            st.write(f"{fan} : {round(score, 2)}")

# ---------------- COLUMN 3 ----------------
with col3:
    if len(G.nodes()) > 0:
        st.subheader("👥 Communities")
        communities = community.greedy_modularity_communities(G)

        for i, c in enumerate(communities, 1):
            st.write(f"Community {i}: {list(c)}")

# Draw Graph
if len(G.nodes()) > 0:
    st.subheader("📈 Network Visualization")

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G,seed= 42)

    nx.draw(G, pos, with_labels=True, node_color="lightblue", ax=ax)

    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("Add nodes and edges from sidebar to start 🚀")