import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("3D Warehouse Stock Visualizer")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Load and clean data
    xls = pd.ExcelFile(uploaded_file)
    df = xls.parse("Godown Stok", skiprows=5)

    # Drop rows with no Godown info
    df = df.dropna(subset=["Godown", "Party Name", "Quility"])

    # Fill missing Bora with 0
    df["Bora"] = pd.to_numeric(df["Bora"], errors='coerce').fillna(0)

    # Optional filters
    godowns = df["Godown"].unique()
    commodities = df["Quility"].unique()

    selected_godowns = st.multiselect("Select Godown(s)", godowns, default=list(godowns))
    selected_commodities = st.multiselect("Select Commodity(s)", commodities, default=list(commodities))

    filtered_df = df[
        df["Godown"].isin(selected_godowns) &
        df["Quility"].isin(selected_commodities)
    ]

    if not filtered_df.empty:
        # Plot 3D scatter plot
        fig = px.scatter_3d(
            filtered_df,
            x="Godown",
            y="Quility",
            z="Bora",
            color="Party Name",
            size="Bora",
            hover_name="Ref. Name/Firm Name",
            title="3D View of Warehouse Contents"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data found for selected filters.")
