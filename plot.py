import pandas as pd
import matplotlib.pyplot as plt

def plot_flow_network(flow_file, title, nodes):
    flow = pd.read_csv(flow_file, sep=r"\s+", engine="python")
    active_flow = flow[flow["Flow"] > 0].copy()
    node_pos = nodes.set_index("Node")[["Longitude", "Latitude"]]

    crowded_nodes = {
        "GranvilleBroadway": "1",
        "OakBroadway": "2",
        "CambieBroadway": "3",
        "KingswayBroadway": "4",
        "BroadwayClark": "5",
        "MainTerminal": "6",
        "Clark1st": "7",
        "Granville41st": "8",
        "Oak41st": "9",
        "Cambie41st": "10",
        "MarineGranville": "11",
        "MarineOak": "12",
    }

    plt.figure(figsize=(11.5, 7.5))

    for _, row in active_flow.iterrows():
        i, j = row["i"], row["j"]
        x1, y1 = node_pos.loc[i]
        x2, y2 = node_pos.loc[j]

        width = 1 + 3.5 * row["Flow"] / active_flow["Flow"].max()

        plt.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                lw=width,
                color="tab:blue",
                alpha=0.75,
                shrinkA=6,
                shrinkB=6,
            ),
        )

    plt.scatter(nodes["Longitude"], nodes["Latitude"], s=45, color="black", zorder=3)

    for _, row in nodes.iterrows():
        node = row["Node"]
        x, y = row["Longitude"], row["Latitude"]

        if node in crowded_nodes:
            plt.text(
                x, y, crowded_nodes[node],
                fontsize=10,
                ha="center",
                va="center",
                bbox=dict(boxstyle="circle, pad=0.22", fc="white", ec="black", lw=0.8),
                zorder=4,
            )
        else:
            plt.text(x + 0.0003, y + 0.00025, node, fontsize=10, ha="left", va="bottom")

    legend_text = "\n".join([f"{v}: {k}" for k, v in crowded_nodes.items()])

    plt.text(
        0.02,
        0.02,
        legend_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.9),
    )

    plt.title(title, fontsize=18, fontweight="bold", pad=18, x=0.53)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

#----------------------------------------------------------------------------------------------

def plot_multicommodity_flow(flow_file, title, nodes):
    flow = pd.read_csv(flow_file, sep=r"\s+", engine="python")
    active_flow = flow[flow["Flow"] > 0].copy()

    # Combine destination-specific flows on each corridor
    edge_flow = (
        active_flow
        .groupby(["i", "j"], as_index=False)
        .agg(
            Flow=("Flow", "sum"),
            groups=("k", lambda x: set(x))
        )
    )

    node_pos = nodes.set_index("Node")[["Longitude", "Latitude"]]

    crowded_nodes = {
        "GranvilleBroadway": "1",
        "OakBroadway": "2",
        "CambieBroadway": "3",
        "KingswayBroadway": "4",
        "BroadwayClark": "5",
        "MainTerminal": "6",
        "Clark1st": "7",
        "Granville41st": "8",
        "Oak41st": "9",
        "Cambie41st": "10",
        "MarineGranville": "11",
        "MarineOak": "12",
    }

    plt.figure(figsize=(11.5, 7.5))

    for _, row in edge_flow.iterrows():
        i, j = row["i"], row["j"]
        x1, y1 = node_pos.loc[i]
        x2, y2 = node_pos.loc[j]

        if row["groups"] == {"Downtown"}:
            color = "tab:blue"
        elif row["groups"] == {"UBC"}:
            color = "tab:orange"
        else:
            color = "tab:purple"

        width = 1 + 3.5 * row["Flow"] / edge_flow["Flow"].max()

        plt.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                lw=width,
                color=color,
                alpha=0.75,
                shrinkA=6,
                shrinkB=6,
            ),
        )

    plt.scatter(nodes["Longitude"], nodes["Latitude"], s=45, color="black", zorder=3)

    for _, row in nodes.iterrows():
        node = row["Node"]
        x, y = row["Longitude"], row["Latitude"]

        if node in crowded_nodes:
            plt.text(
                x, y, crowded_nodes[node],
                fontsize=10,
                ha="center",
                va="center",
                bbox=dict(boxstyle="circle,pad=0.22", fc="white", ec="black", lw=0.8),
                zorder=4,
            )
        else:
            plt.text(x+0.0003, y+0.00025, node, fontsize=10, ha="left", va="bottom")

    legend_text = "\n".join([f"{v}: {k}" for k, v in crowded_nodes.items()])

    plt.text(
        0.02,
        0.02,
        legend_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.9),
    )

    plt.plot([], [], color="tab:blue", lw=3, label="Downtown-bound flow")
    plt.plot([], [], color="tab:orange", lw=3, label="UBC-bound flow")
    plt.plot([], [], color="tab:purple", lw=3, label="Shared corridor")
    plt.legend(
    loc="upper left",
    framealpha=0.9
    )

    plt.title(title, fontsize=18, fontweight="bold", pad=18, x=0.53)
    plt.axis("off")
    plt.tight_layout()
    plt.show()