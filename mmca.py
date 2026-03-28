import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community

st.set_page_config(page_title="Fan Network Analysis", layout="centered")

# ---------------- PAGE SELECTOR ----------------
page = st.sidebar.radio("📂 Select Page", ["🏠 Main App", "📖 Explanation"])

# ---------------- EXPLANATION PAGE ----------------
if page == "📖 Explanation":

    st.title("📖 Project Explanation")

    st.header("🎬 Entertainment Fan Network Analysis")

    st.write("""
This project models how fans interact in online communities using Graph Theory.

Each fan is represented as a node, and connections between fans are represented as edges.
""")

    st.subheader("🔹 Key Concepts")

    st.write("""
**1. Graph Theory**
- Fans = Nodes  
- Connections = Edges  

**2. Community Detection**
- The app uses the Greedy Modularity Algorithm  
- It groups fans into communities based on strong connections  

**3. Influencer Ranking**
- Uses Degree Centrality  
- Fans with more connections are more influential  

**4. Fan Categories**
- Each fan is assigned a type like:
  - Marvel  
  - Anime  
  - K-pop  
  - Bollywood  
  - Gaming  

**5. Network Statistics**
- Total Fans → Number of users  
- Connections → Relationships  
- Density → How connected the network is  
""")

    st.subheader("🎯 Real-Life Application")

    st.write("""
- Social media analysis (Instagram, Twitter)
- Marketing strategies (target influencers)
- Understanding fan communities
- Recommendation systems
""")

    st.subheader("🛠 Technologies Used")

    st.write("""
- Python  
- Streamlit  
- NetworkX  
- Matplotlib  
""")

    st.success("✅ This project demonstrates real-world network analysis in a simple and interactive way.")

# ---------------- MAIN APP ----------------
else:

    st.title("🎬 Entertainment Fan Network Analysis")

    # Initialize graph
    if "G" not in st.session_state:
        st.session_state.G = nx.Graph()

    G = st.session_state.G

    st.sidebar.header("⚙️ Controls")

    # Fan Type
    fan_type = st.sidebar.selectbox(
        "Select Fan Type",
        ["Marvel", "Anime", "K-pop", "Bollywood", "Gaming"]
    )

    # Add Fan
    fan = st.sidebar.text_input("Enter Fan Name")

    if st.sidebar.button("➕ Add Fan"):
        if fan:
            G.add_node(fan, category=fan_type)
            st.sidebar.success(f"{fan} added!")

    # Add Connection
    st.sidebar.subheader("🔗 Connect Fans")

    nodes = list(G.nodes())

    if len(nodes) >= 2:
        fan1 = st.sidebar.selectbox("Fan 1", nodes)
        fan2 = st.sidebar.selectbox("Fan 2", nodes)

        if st.sidebar.button("Connect"):
            if fan1 != fan2:
                G.add_edge(fan1, fan2)
                st.sidebar.success(f"{fan1} ↔ {fan2} connected!")
            else:
                st.sidebar.warning("Choose different fans")

    # Delete Fan
    st.sidebar.subheader("🗑 Remove Fan")

    if nodes:
        remove_fan = st.sidebar.selectbox("Select Fan", nodes, key="remove_fan")

        if st.sidebar.button("Delete Fan"):
            G.remove_node(remove_fan)
            st.sidebar.success(f"{remove_fan} removed!")

    # Delete Edge
    st.sidebar.subheader("❌ Remove Connection")

    edges = list(G.edges())

    if edges:
        remove_edge = st.sidebar.selectbox("Select Connection", edges)

        if st.sidebar.button("Delete Connection"):
            G.remove_edge(*remove_edge)
            st.sidebar.success(f"{remove_edge} removed!")

    # Reset
    if st.sidebar.button("🔄 Reset Network"):
        st.session_state.G = nx.Graph()
        st.sidebar.warning("Network cleared!")

    # ---------------- MAIN CONTENT ----------------
    if len(G.nodes()) > 0:

        st.subheader("📊 Network Statistics")

        st.write(f"👥 Total Fans: {G.number_of_nodes()}")
        st.write(f"🔗 Total Connections: {G.number_of_edges()}")
        st.write(f"📉 Density: {round(nx.density(G), 3)}")

        col1, col2 = st.columns(2)

        # Influencers
        with col1:
            st.subheader("⭐ Influencers")

            centrality = nx.degree_centrality(G)
            sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

            for fan, score in sorted_centrality:
                st.write(f"{fan} → {round(score, 2)}")

        # Communities
        with col2:
            st.subheader("👥 Communities")

            if len(G.edges()) > 0:
                comm = list(community.greedy_modularity_communities(G))

                for i, c in enumerate(comm, 1):
                    st.write(f"Group {i}: {list(c)}")
            else:
                st.info("No connections yet")

        # Graph
        st.subheader("📈 Network Graph")

        fig, ax = plt.subplots()
        pos = nx.spring_layout(G, seed=42)

        if len(G.edges()) > 0:
            comm = list(community.greedy_modularity_communities(G))
            colors = ["red", "blue", "green", "orange", "purple"]

            color_map = {}
            for i, group in enumerate(comm):
                for node in group:
                    color_map[node] = colors[i % len(colors)]

            node_colors = [color_map[node] for node in G.nodes()]
        else:
            node_colors = "skyblue"

        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, ax=ax)

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("Add fans and connections to begin 🚀")