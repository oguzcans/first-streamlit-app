import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os

st.title("📊 Passenger Satisfaction Analysis")

# Download data from Kaggle
@st.cache_data
def load_data():
    path = kagglehub.dataset_download("teejmahal20/airline-passenger-satisfaction")
    if path:
        files = os.listdir(path)
        csv_file = [f for f in files if f.endswith(".csv")]
        if csv_file:
            data_file = os.path.join(path, csv_file[0])  # Assuming only one CSV file
            return pd.read_csv(data_file)
        else:
            st.error("No CSV file found in the downloaded Kaggle dataset.")
            return None
    else:
        st.error("Failed to download the Kaggle dataset.")
        return None

df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filter Options")
    customer_type = st.sidebar.multiselect("Customer Type", options=df["Customer Type"].unique(), default=df["Customer Type"].unique())
    travel_type = st.sidebar.multiselect("Type of Travel", options=df["Type of Travel"].unique(), default=df["Type of Travel"].unique())
    travel_class = st.sidebar.multiselect("Class", options=df["Class"].unique(), default=df["Class"].unique())

    # Apply filters
    filtered_df = df[
        (df["Customer Type"].isin(customer_type)) &
        (df["Type of Travel"].isin(travel_type)) &
        (df["Class"].isin(travel_class))
    ]

    # Metrics
    st.subheader("📈 Key Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Total Passengers", len(filtered_df))
    col2.metric("Avg Flight Distance", f"{filtered_df['Flight Distance'].mean():.2f} km")

    # Charts
    st.subheader("🧭 Satisfaction Distribution")
    try:
        fig1 = px.histogram(filtered_df, x="satisfaction", color="satisfaction", barmode="group")
        st.plotly_chart(fig1, use_container_width=True)
    except ValueError as e:
        st.error(f"Error creating histogram: {e}")

    st.subheader("🧳 Flight Distance by Class and Satisfaction")
    try:
        fig2 = px.box(filtered_df, x="Class", y="Flight Distance", color="satisfaction")
        st.plotly_chart(fig2, use_container_width=True)
    except ValueError as e:
        st.error(f"Error creating box plot: {e}")