import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="गोदाम दृश्य", layout="wide")
st.title("📦 गोदाम दृश्य (Warehouse Visualizer)")

tab1, tab2 = st.tabs(["📊 हिंदी स्टॉक दृश्य", "🧱 Three.js 3D Warehouse"])

with tab1:
    st.subheader("📄 एक्सेल से स्टॉक देखें")

    uploaded_file = st.file_uploader("एक्सेल फ़ाइल अपलोड करें", type=["xlsx"])

    godown_positions = {
        "Old Godown 1": (0, 0),
        "Old Godown 2": (60, 0),
        "Old Godown 3": (120, 0),
        "New Godown 1": (0, 120),
        "New Godown 2": (60, 120),
        "New Godown 3": (120, 120)
    }

    unit_width = 50
    unit_depth = 100
    cell_size = 5

    if uploaded_file:
        xls = pd.ExcelFile(uploaded_file)
        df = xls.parse("Godown Stok", skiprows=5)
        df = df.dropna(subset=["Godown", "Party Name", "Quility"])
        df["Bora"] = pd.to_numeric(df["Bora"], errors='coerce').fillna(0)
        df = df[df["Bora"] > 0]

        selected_godowns = st.multiselect("गोडाउन चुनें", df["Godown"].unique(), default=list(df["Godown"].unique()))
        selected_commodities = st.multiselect("अनाज चुनें", df["Quility"].unique(), default=list(df["Quility"].unique()))

        filtered_df = df[
            df["Godown"].isin(selected_godowns) &
            df["Quility"].isin(selected_commodities)
        ]

        if not filtered_df.empty:
            fig = go.Figure()
            cell_map = {key: [] for key in godown_positions.keys()}

            for i, row in filtered_df.iterrows():
                godown = row["Godown"]
                if godown not in godown_positions:
                    continue
                gx, gy = godown_positions[godown]
                base_x, base_y = gx, gy

                used_cells = cell_map[godown]
                placed = False
                for cx in range(0, unit_width, cell_size):
                    for cy in range(0, unit_depth, cell_size):
                        if (cx, cy) not in used_cells:
                            used_cells.append((cx, cy))
                            cell_map[godown] = used_cells
                            x_pos = base_x + cx + cell_size / 2
                            y_pos = base_y + cy + cell_size / 2
                            placed = True
                            break
                    if placed:
                        break

                height = row["Bora"] / 50

                fig.add_trace(go.Bar3d(
                    x=[x_pos],
                    y=[y_pos],
                    z=[0],
                    dx=cell_size * 0.8,
                    dy=cell_size * 0.8,
                    dz=[height],
                    name=row["Party Name"],
                    text=f"पार्टी: {row['Party Name']}<br>अनाज: {row['Quility']}<br>बोरी: {row['Bora']}",
                    hoverinfo="text",
                    opacity=0.9
                ))

            for godown, (gx, gy) in godown_positions.items():
                fig.add_trace(go.Scatter3d(
                    x=[gx + unit_width / 2],
                    y=[gy + unit_depth / 2],
                    z=[0],
                    mode="text",
                    text=[godown],
                    textposition="top center",
                    showlegend=False
                ))

            fig.update_layout(
                scene=dict(
                    xaxis_title="🔲 गोडाउन चौड़ाई",
                    yaxis_title="🔳 गोडाउन लंबाई",
                    zaxis_title="⬆️ ऊँचाई (बोरी संख्या)",
                ),
                height=850,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("चयनित फ़िल्टर के लिए कोई डेटा नहीं मिला।")

with tab2:
    st.subheader("🧱 इंटरेक्टिव थ्री.जे.एस दृश्य")
    try:
        components.html(open("warehouse_view.html", encoding="utf-8").read(), height=700)
    except FileNotFoundError:
        st.error("warehouse_view.html फाइल नहीं मिली। कृपया उसे साथ अपलोड करें।")
