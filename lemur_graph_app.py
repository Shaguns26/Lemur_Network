import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- 0. PAGE CONFIGURATION & AESTHETICS ---
st.set_page_config(
    page_title="Duke Lemur Center | Genetic Network",
    page_icon="🐒",
    layout="wide"
)

# --- CUSTOM CSS (The "Duke" Aesthetic) ---
st.markdown("""
<style>
    /* 1. MAIN BACKGROUND & FONTS */
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Open Sans', sans-serif;
    }

    /* 2. HEADER STYLING */
    h1 {
        color: #012169 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        border-bottom: 2px solid #00539B;
        padding-bottom: 10px;
    }
    h2, h3 { color: #00539B !important; }

    /* 3. METRIC CARDS */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #012169;
    }

    /* 4. DATAFRAME HIGHLIGHT */
    .stDataFrame { border: 1px solid #e0e0e0; border-radius: 5px; }

    /* Custom Banner */
    .header-banner {
        background: linear-gradient(90deg, #012169 0%, #00539B 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. SESSION STATE SETUP (For Interaction) ---
if 'selected_lemur_id' not in st.session_state:
    st.session_state.selected_lemur_id = None


def reset_selection():
    st.session_state.selected_lemur_id = None


# --- 2. LOAD & PREP DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("DataRecord_2_DLC_Animal_List_05Feb2019.csv", encoding="windows-1252")
    except FileNotFoundError:
        st.error("⚠️ Data file not found.")
        return pd.DataFrame()

    df = df[df['Taxon'] == 'LCAT'].copy()
    df['Birth_Year'] = pd.to_datetime(df['DOB'], format='%d%b%Y', errors='coerce').dt.year
    cols = ['DLC_ID', 'Name', 'Sex', 'Sire_ID', 'Dam_ID', 'Birth_Year']
    df = df[cols].copy()

    df['Name'] = df['Name'].fillna(df['DLC_ID'])
    # Convert all IDs to string
    for col in ['DLC_ID', 'Sire_ID', 'Dam_ID']:
        df[col] = df[col].astype(str)

    return df


df = load_data()
if df.empty: st.stop()

# --- 3. HEADER BANNER ---
st.markdown("""
<div class="header-banner">
    <h2 style="color:white !important; margin:0;">🐒 Duke Lemur Center Database</h2>
    <p style="margin:0; opacity:0.9;">Genetic Safety Net & Lineage Visualization</p>
</div>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.image("https://lemur.duke.edu/wordpress/wp-content/themes/dukelemur2013/images/new-nav-logo-feb-2025.png",
                 width=200)
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filter Options")

min_year = int(df['Birth_Year'].min())
max_year = int(df['Birth_Year'].max())

selected_years = st.sidebar.slider("Select Birth Era", min_year, max_year, (1980, 2010))

# Filter Dataframe
mask = (df['Birth_Year'] >= selected_years[0]) & (df['Birth_Year'] <= selected_years[1])
filtered_df = df[mask]

# Metrics
col1_side, col2_side = st.sidebar.columns(2)
col1_side.metric("Total Lemurs", len(df))
col2_side.metric("Current View", len(filtered_df))

# Initialize depth variable
connection_depth = 1

# Reset Button & Depth Slider in Sidebar
if st.session_state.selected_lemur_id:
    st.sidebar.markdown("---")
    st.sidebar.warning(f"Focusing on: **{st.session_state.selected_lemur_id}**")

    # NEW FEATURE: Depth Slider
    st.sidebar.markdown("**Family Tree Depth**")
    connection_depth = st.sidebar.slider(
        "Degrees of Separation",
        min_value=1,
        max_value=10,
        value=3,
        help="1=Parents/Children, 2=Grandparents/Siblings, 10=Entire Lineage"
    )

    st.sidebar.button("🔄 Reset to Full View", on_click=reset_selection, type="primary")

# --- 5. BUILD BASE NETWORK ---
# We build the full graph first, then decide if we filter it
G_full = nx.DiGraph()

# Add Nodes
for index, row in filtered_df.iterrows():
    color = "#D16488" if row['Sex'] == 'F' else "#5C88DA"
    G_full.add_node(
        row['DLC_ID'],
        label=row['Name'],
        title=f"ID: {row['DLC_ID']}\nBorn: {row['Birth_Year']}",
        color=color,
        shape="dot",
        size=15
    )

# Add Edges
valid_ids = set(filtered_df['DLC_ID'])
for index, row in filtered_df.iterrows():
    child = row['DLC_ID']
    sire = row['Sire_ID']
    dam = row['Dam_ID']
    if sire in valid_ids and sire != 'nan': G_full.add_edge(sire, child, color="#BDC3C7")
    if dam in valid_ids and dam != 'nan': G_full.add_edge(dam, child, color="#BDC3C7")

# Calculate Centrality
centrality = nx.degree_centrality(G_full)
for node, cent_val in centrality.items():
    G_full.nodes[node]['size'] = 15 + (cent_val * 150)

# --- 6. APPLY INTERACTIVE FILTER (EGO GRAPH) ---
# Check if a user selected something
if st.session_state.selected_lemur_id and st.session_state.selected_lemur_id in G_full.nodes:
    # EGO GRAPH: Get node + neighbors
    # radius=connection_depth allows finding 1st, 2nd, 3rd degree connections
    G_display = nx.ego_graph(
        G_full,
        st.session_state.selected_lemur_id,
        radius=connection_depth,
        undirected=True
    )
    graph_title = f"🔍 Family Focus: {st.session_state.selected_lemur_id} (Radius: {connection_depth})"
else:
    G_display = G_full
    graph_title = f"🧬 Lineage Network ({selected_years[0]} - {selected_years[1]})"

# --- 7. LAYOUT: GRAPH (Left) & LEADERBOARD (Right) ---
col_main, col_leader = st.columns([3, 1])

with col_main:
    st.subheader(graph_title)

    # PyVis Configuration
    net = Network(height='600px', width='100%', bgcolor='#ffffff', font_color='black')
    net.from_nx(G_display)
    net.repulsion(node_distance=120, spring_length=150)

    # Save & Render
    try:
        path = '/tmp'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')
    except:
        path = 'html_files'
        net.save_graph('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=620)

with col_leader:
    st.subheader("🏆 Select to Filter")
    st.caption("Click a row to isolate that family.")

    # Prepare Leaderboard Data
    if not filtered_df.empty and len(centrality) > 0:
        cent_df = pd.DataFrame.from_dict(centrality, orient='index', columns=['Score'])
        cent_df.index.name = 'DLC_ID'
        cent_df = cent_df.reset_index()

        leaderboard = pd.merge(cent_df, df[['DLC_ID', 'Name']], on='DLC_ID', how='left').drop_duplicates()
        leaderboard = leaderboard.sort_values(by='Score', ascending=False).head(15)

        # INTERACTIVE DATAFRAME
        event = st.dataframe(
            leaderboard[['Name', 'Score', 'DLC_ID']],
            hide_index=True,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row"
        )

        # HANDLE SELECTION EVENT
        if len(event.selection.rows) > 0:
            selected_index = event.selection.rows[0]
            new_selection = leaderboard.iloc[selected_index]['DLC_ID']
        else:
            new_selection = None

        if st.session_state.selected_lemur_id != new_selection:
            st.session_state.selected_lemur_id = new_selection
            st.rerun()

    else:
        st.warning("No data.")

if st.session_state.selected_lemur_id:
    st.info("💡 **Tip:** Use the 'Degrees of Separation' slider in the sidebar to expand the family tree.")
else:
    st.success(f"✅ Loaded {len(filtered_df)} individuals.")
