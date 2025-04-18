import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🛫 Istanbul Flight Explorer", layout="wide")

st.title("🛫 Istanbul Airport Flight Explorer")
st.write("Explore simulated flight data from Istanbul Airport — delays, airlines, and destinations.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Istanbul_Flight_Data_Simulated.csv")

df = load_data()

# Filters
st.sidebar.header("✈️ Filters")
airlines = st.sidebar.multiselect("Select Airline(s)", df["Airline"].unique(), default=df["Airline"].unique())
destinations = st.sidebar.multiselect("Select Destination(s)", df["Destination"].unique(), default=df["Destination"].unique())
months = st.sidebar.multiselect("Select Month(s)", sorted(df["Month"].unique()), default=sorted(df["Month"].unique()))

filtered_df = df[
    df["Airline"].isin(airlines) &
    df["Destination"].isin(destinations) &
    df["Month"].isin(months)
]

# KPIs
st.subheader("📊 Flight Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Flights", len(filtered_df))
col2.metric("Avg Dep. Delay (min)", round(filtered_df["Departure Delay"].mean(), 2))
col3.metric("Cancelled Flights", filtered_df["Status"].value_counts().get("Cancelled", 0))

# Delay Distribution
st.subheader("🕑 Delay Distribution")
fig1 = px.histogram(filtered_df, x="Departure Delay", nbins=30, title="Distribution of Departure Delays")
st.plotly_chart(fig1, use_container_width=True)

# Delay by Destination
st.subheader("📍 Average Arrival Delay by Destination")
fig2 = px.bar(filtered_df.groupby("Destination")["Arrival Delay"].mean().reset_index(),
              x="Destination", y="Arrival Delay", color="Destination", title="Avg Arrival Delay by Destination")
st.plotly_chart(fig2, use_container_width=True)

# Flights over time
st.subheader("📆 Flights by Month")
monthly_counts = filtered_df.groupby("Month").size().reset_index(name="Flights")
fig3 = px.line(monthly_counts, x="Month", y="Flights", markers=True, title="Flights per Month")
st.plotly_chart(fig3, use_container_width=True)
