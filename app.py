import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
st.title("📦 गोदाम में भंडारण का 3D दृश्य (Warehouse 3D View in Hindi)")

uploaded_file = st.file_uploader("एक्सेल फ़ाइल अपलोड करें", type=["xlsx"])

# Mapping godown names to physical layout positions
godown_positions = {
    "Old Godown 1": (0, 0),
    "Old Godown 2": (60, 0),
    "Old Godown 3": (120, 0),
    "New Godown 1": (0, 120),
    "New Godown 2": (60, 120),
    "New Godown 3": (120, 120)
}

# Size of godown unit
unit_width = 50
unit_depth = 100

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    df = xls.parse("Godown Stok", skiprows=5)
    df = df.dropna(subset=["Godown", "Party Name", "Quility"])

    df = df.copy()
    df["Bora"] = pd.to_numeric(df["Bora"], errors='coerce').fillna(0)

    df = df[df["Bora"] > 0]

    # Dropdowns
    selected_godowns = st.multiselect("गोडाउन चुनें", df["Godown"].unique(), default=list(df["Godown"].unique()))
    selected_commodities = st.multiselect("अनाज चुनें", df["Quility"].unique(), default=list(df["Quility"].unique()))

    filtered_df = df[
        df["Godown"].isin(selected_godowns) &
        df["Quility"].isin(selected_commodities)
    ]

    if not filtered_df.empty:
        fig = go.Figure()

        # Plot godown boxes
        for godown, (gx, gy) in godown_positions.items():
            fig.add_trace(go.Scatter3d(
                x=[gx, gx + unit_width],
                y=[gy, gy + unit_depth],
                z=[0, 0],
                mode="markers",
                marker=dict(size=1),
                name=f"{godown}"
            ))

        # Plot bags as bars
        for i, row in filtered_df.iterrows():
            godown = row["Godown"]
            if godown not in godown_positions:
                continue
            gx, gy = godown_positions[godown]

            # Random placement within godown bounds
            x_pos = gx + np.random.uniform(5, unit_width - 5)
            y_pos = gy + np.random.uniform(5, unit_depth - 5)
            height = row["Bora"] / 50  # scale height

            fig.add_trace(go.Bar3d(
                x=[x_pos],
                y=[y_pos],
                z=[0],
                dx=3,
                dy=3,
                dz=[height],
                name=row["Party Name"],
                text=f"पार्टी: {row['Party Name']}<br>अनाज: {row['Quility']}<br>बोरी: {row['Bora']}",
                hoverinfo="text",
                opacity=0.8
            ))

        fig.update_layout(
            scene=dict(
                xaxis_title="🔲 गोडाउन चौड़ाई",
                yaxis_title="🔳 गोडाउन लंबाई",
                zaxis_title="⬆️ ऊँचाई (बोरी संख्या)",
            ),
            height=800,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("चयनित फ़िल्टर के लिए कोई डेटा नहीं मिला।")
