import plotly.graph_objects as go
import plotly.io as pio

# ------------------------------------------------------------
# 1. Nodes
# ------------------------------------------------------------
sources = ["Cr", "Mn", "Ni", "Pb", "Li", "Si", "Sn", "Zn"]
destinations = ["WindOn", "WindOff", "Solar", "Battery"]

nodes = sources + destinations

# Colors
node_colors = [
    "rgba(120,120,120,0.85)", "rgba(120,120,120,0.85)",
    "rgba(120,120,120,0.85)", "rgba(120,120,120,0.85)",
    "rgba(120,120,120,0.85)", "rgba(120,120,120,0.85)",
    "rgba(120,120,120,0.85)", "rgba(120,120,120,0.85)",

    "rgba(0,140,0,0.95)",      # WindOn (green)
    "rgba(0,200,70,0.95)",     # WindOff (bright green)
    "rgba(255,215,0,0.95)",    # Solar (yellow)
    "rgba(255,105,180,0.95)"   # Battery (pink)
]

# ------------------------------------------------------------
# 2. Define flows (custom example flows)
# ------------------------------------------------------------
links = {
    "Cr": [("WindOn", 2430), ("WindOff", 6591)],
    "Mn": [("WindOn", 285), ("WindOff", 773)],
    "Ni": [("WindOn", 1550), ("WindOff", 4204)],
    "Pb": [("WindOn", 29935), ("WindOff", 81195)],
    "Li": [("Battery", 20880)],
    "Si": [("Solar", 84000)],
    "Sn": [("WindOn", 450), ("WindOff", 1220), ("Solar", 1920)],
    "Zn": [("WindOn", 26280), ("WindOff", 71281)]
}

source_indices = []
target_indices = []
values = []
link_colors = []

# Compute totals per destination
totals = {d: 0 for d in destinations}

for src, flows in links.items():
    for dest, val in flows:
        source_indices.append(nodes.index(src))
        target_indices.append(nodes.index(dest))
        values.append(val)
        link_colors.append(node_colors[nodes.index(dest)])
        totals[dest] += val

# ------------------------------------------------------------
# 3. Build Sankey
# ------------------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=24,
        thickness=24,
        line=dict(color="black", width=0.8),
        label=nodes,
        color=node_colors
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values,
        color=link_colors
    )
)])

fig.update_layout(
    title="<b>Critical Minerals Flow to Renewable Technologies</b>",
    font=dict(size=16, family="Times New Roman"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=760,
    width=1180
)


# ------------------------------------------------------------
# 5. Save and open HTML
# ------------------------------------------------------------
pio.write_html(fig, "sankey_diagram.html", auto_open=True)
