"""
---------------------------------------------------------
Web Traffic Analytics Dashboard
Author : Priyanshu Raj
Technology : Streamlit + Plotly + Pandas

Run:
streamlit run dashboard/dashboard.py
---------------------------------------------------------
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="Web Traffic Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#F8F9FA;
}

h1{
    color:#0F172A;
}

div[data-testid="metric-container"]{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.08);
}

section[data-testid="stSidebar"]{
    background:#FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

from pathlib import Path

@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_PATH = BASE_DIR / "data" / "raw" / "website_wata.csv"

    print("Loading:", DATA_PATH)

    return pd.read_csv(DATA_PATH)

df = load_data()
# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("📊 Web Traffic Analytics Dashboard")

st.write(
"""
This dashboard analyzes website traffic, user engagement,
bounce behavior and conversion performance.
"""
)

st.divider()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.title("Dashboard Filters")

st.sidebar.markdown("---")

# Traffic Source

traffic_source = st.sidebar.multiselect(

    "Traffic Source",

    options=sorted(df["Traffic Source"].unique()),

    default=sorted(df["Traffic Source"].unique())

)

# ----------------------------------------------------

page_views = st.sidebar.slider(

    "Page Views",

    min_value=int(df["Page Views"].min()),

    max_value=int(df["Page Views"].max()),

    value=(
        int(df["Page Views"].min()),
        int(df["Page Views"].max())
    )

)

# ----------------------------------------------------

session_duration = st.sidebar.slider(

    "Session Duration",

    min_value=float(df["Session Duration"].min()),

    max_value=float(df["Session Duration"].max()),

    value=(
        float(df["Session Duration"].min()),
        float(df["Session Duration"].max())
    )

)

# ----------------------------------------------------

bounce_rate = st.sidebar.slider(

    "Bounce Rate",

    min_value=float(df["Bounce Rate"].min()),

    max_value=float(df["Bounce Rate"].max()),

    value=(
        float(df["Bounce Rate"].min()),
        float(df["Bounce Rate"].max())
    )

)

# ----------------------------------------------------

previous_visits = st.sidebar.slider(

    "Previous Visits",

    min_value=int(df["Previous Visits"].min()),

    max_value=int(df["Previous Visits"].max()),

    value=(
        int(df["Previous Visits"].min()),
        int(df["Previous Visits"].max())
    )

)

# ----------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------

filtered_df = df[

    (df["Traffic Source"].isin(traffic_source))

    &

    (
        df["Page Views"].between(
            page_views[0],
            page_views[1]
        )
    )

    &

    (
        df["Session Duration"].between(
            session_duration[0],
            session_duration[1]
        )
    )

    &

    (
        df["Bounce Rate"].between(
            bounce_rate[0],
            bounce_rate[1]
        )
    )

    &

    (
        df["Previous Visits"].between(
            previous_visits[0],
            previous_visits[1]
        )
    )

]

if filtered_df.empty:

    st.warning("No records found for selected filters.")

    st.stop()

# ----------------------------------------------------
# KPI CALCULATIONS
# ----------------------------------------------------

total_sessions = len(filtered_df)

avg_page_views = filtered_df["Page Views"].mean()

avg_session_duration = filtered_df["Session Duration"].mean()

avg_time_on_page = filtered_df["Time on Page"].mean()

avg_bounce_rate = filtered_df["Bounce Rate"].mean()

avg_conversion_rate = filtered_df["Conversion Rate"].mean()

avg_previous_visits = filtered_df["Previous Visits"].mean()

# ----------------------------------------------------
# KPI SECTION
# ----------------------------------------------------

st.subheader("📌 Key Performance Indicators")

row1 = st.columns(3)

row2 = st.columns(3)

row1[0].metric(
    "Total Sessions",
    f"{total_sessions:,}"
)

row1[1].metric(
    "Average Page Views",
    f"{avg_page_views:.2f}"
)

row1[2].metric(
    "Average Session Duration",
    f"{avg_session_duration:.2f} sec"
)

row2[0].metric(
    "Average Bounce Rate",
    f"{avg_bounce_rate:.2%}"
)

row2[1].metric(
    "Average Conversion Rate",
    f"{avg_conversion_rate:.2%}"
)

row2[2].metric(
    "Average Time on Page",
    f"{avg_time_on_page:.2f} sec"
)

st.divider()
# ====================================================
# VISUALIZATION SECTION
# ====================================================

st.subheader("📈 Website Traffic Analysis")

# --------------------------------------------
# ROW 1
# --------------------------------------------

col1, col2 = st.columns(2)

# Traffic Source Distribution
with col1:

    traffic_counts = (
        filtered_df["Traffic Source"]
        .value_counts()
        .reset_index()
    )

    traffic_counts.columns = ["Traffic Source", "Sessions"]

    fig = px.bar(
        traffic_counts,
        x="Traffic Source",
        y="Sessions",
        color="Traffic Source",
        text="Sessions",
        title="Traffic Source Distribution"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Traffic Source",
        yaxis_title="Sessions",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Session Duration Histogram
with col2:

    fig = px.histogram(
        filtered_df,
        x="Session Duration",
        nbins=30,
        marginal="box",
        title="Session Duration Distribution"
    )

    fig.update_layout(
        xaxis_title="Session Duration (Seconds)",
        yaxis_title="Frequency",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------
# ROW 2
# --------------------------------------------

col3, col4 = st.columns(2)

# Page Views Distribution
with col3:

    fig = px.histogram(
        filtered_df,
        x="Page Views",
        nbins=25,
        marginal="box",
        title="Page Views Distribution"
    )

    fig.update_layout(
        xaxis_title="Page Views",
        yaxis_title="Frequency",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Bounce Rate Distribution
with col4:

    fig = px.histogram(
        filtered_df,
        x="Bounce Rate",
        nbins=30,
        marginal="box",
        title="Bounce Rate Distribution"
    )

    fig.update_layout(
        xaxis_title="Bounce Rate",
        yaxis_title="Frequency",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------
# ROW 3
# --------------------------------------------

col5, col6 = st.columns(2)

# Conversion Rate Distribution
with col5:

    fig = px.histogram(
        filtered_df,
        x="Conversion Rate",
        nbins=30,
        marginal="box",
        title="Conversion Rate Distribution"
    )

    fig.update_layout(
        xaxis_title="Conversion Rate",
        yaxis_title="Frequency",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Previous Visits
with col6:

    visits = (
        filtered_df["Previous Visits"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    visits.columns = [
        "Previous Visits",
        "Users"
    ]

    fig = px.bar(
        visits,
        x="Previous Visits",
        y="Users",
        text="Users",
        color="Users",
        title="Previous Visits Distribution"
    )

    fig.update_layout(
        showlegend=False,
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ====================================================
# SCATTER PLOTS
# ====================================================

st.subheader("🔍 Relationship Analysis")

left, right = st.columns(2)

# Page Views vs Session Duration
with left:

    fig = px.scatter(
        filtered_df,
        x="Page Views",
        y="Session Duration",
        color="Traffic Source",
        size="Conversion Rate",
        hover_data=[
            "Time on Page",
            "Previous Visits"
        ],
        title="Page Views vs Session Duration"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Session Duration vs Conversion Rate
with right:

    fig = px.scatter(
        filtered_df,
        x="Session Duration",
        y="Conversion Rate",
        color="Traffic Source",
        size="Page Views",
        hover_data=[
            "Bounce Rate",
            "Time on Page"
        ],
        title="Session Duration vs Conversion Rate"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ====================================================
# BOXPLOTS
# ====================================================

st.subheader("📦 Traffic Source Comparison")

left, right = st.columns(2)

with left:

    fig = px.box(
        filtered_df,
        x="Traffic Source",
        y="Session Duration",
        color="Traffic Source",
        title="Session Duration by Traffic Source"
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.box(
        filtered_df,
        x="Traffic Source",
        y="Conversion Rate",
        color="Traffic Source",
        title="Conversion Rate by Traffic Source"
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()
# =====================================================
# CORRELATION ANALYSIS
# =====================================================

st.subheader("🔥 Correlation Analysis")

corr = filtered_df.select_dtypes(include="number").corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r",
    title="Correlation Heatmap"
)

fig.update_layout(height=650)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# TRAFFIC SOURCE PERFORMANCE
# =====================================================

st.subheader("📊 Traffic Source Performance")

traffic_summary = (
    filtered_df
    .groupby("Traffic Source")
    .agg({
        "Page Views":"mean",
        "Session Duration":"mean",
        "Time on Page":"mean",
        "Bounce Rate":"mean",
        "Conversion Rate":"mean",
        "Previous Visits":"mean"
    })
    .round(2)
)

st.dataframe(
    traffic_summary,
    use_container_width=True
)

st.divider()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📈 Executive Summary")

best_conversion = (
    traffic_summary["Conversion Rate"]
    .idxmax()
)

best_conversion_rate = (
    traffic_summary["Conversion Rate"]
    .max()
)

highest_engagement = (
    traffic_summary["Session Duration"]
    .idxmax()
)

highest_engagement_time = (
    traffic_summary["Session Duration"]
    .max()
)

lowest_bounce = (
    traffic_summary["Bounce Rate"]
    .idxmin()
)

lowest_bounce_rate = (
    traffic_summary["Bounce Rate"]
    .min()
)

highest_page_views = (
    traffic_summary["Page Views"]
    .idxmax()
)

highest_page_views_value = (
    traffic_summary["Page Views"]
    .max()
)

highest_returning = (
    traffic_summary["Previous Visits"]
    .idxmax()
)

highest_returning_value = (
    traffic_summary["Previous Visits"]
    .max()
)

summary1, summary2 = st.columns(2)

with summary1:

    st.success(
        f"""
### Best Converting Channel

**{best_conversion}**

Conversion Rate:
**{best_conversion_rate:.2%}**
"""
    )

    st.info(
        f"""
### Highest User Engagement

**{highest_engagement}**

Average Session Duration:
**{highest_engagement_time:.2f} seconds**
"""
    )

    st.warning(
        f"""
### Lowest Bounce Rate

**{lowest_bounce}**

Bounce Rate:
**{lowest_bounce_rate:.2%}**
"""
    )

with summary2:

    st.success(
        f"""
### Highest Average Page Views

**{highest_page_views}**

Average Page Views:
**{highest_page_views_value:.2f}**
"""
    )

    st.info(
        f"""
### Highest Returning Visitors

**{highest_returning}**

Average Previous Visits:
**{highest_returning_value:.2f}**
"""
    )

    st.metric(
        "Overall Average Conversion",
        f"{filtered_df['Conversion Rate'].mean():.2%}"
    )

st.divider()

# =====================================================
# BUSINESS RECOMMENDATIONS
# =====================================================

st.subheader("💡 Business Recommendations")

recommendations = []

if filtered_df["Bounce Rate"].mean() > 0.50:
    recommendations.append(
        "High bounce rate detected. Improve landing page content and loading speed."
    )

if filtered_df["Session Duration"].mean() < 180:
    recommendations.append(
        "Users spend relatively little time on the website. Consider improving content quality and internal linking."
    )

if filtered_df["Conversion Rate"].mean() < 0.20:
    recommendations.append(
        "Conversion rate is relatively low. Review CTAs, pricing strategy, and checkout experience."
    )

if filtered_df["Page Views"].mean() < 4:
    recommendations.append(
        "Users explore only a few pages. Improve navigation and recommend related content."
    )

if filtered_df["Previous Visits"].mean() < 2:
    recommendations.append(
        "Returning visitor count is low. Consider remarketing campaigns and email newsletters."
    )

if len(recommendations) == 0:
    recommendations.append(
        "Website engagement metrics are healthy. Continue monitoring performance and optimize marketing campaigns."
    )

for i, recommendation in enumerate(recommendations, start=1):

    st.markdown(f"**{i}.** {recommendation}")

st.divider()

# =====================================================
# TOP 5 RECORDS
# =====================================================

st.subheader("🏆 Highest Converting Sessions")

top_sessions = (
    filtered_df
    .sort_values(
        by="Conversion Rate",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_sessions,
    use_container_width=True
)

st.divider()

# =====================================================
# METRIC SUMMARY TABLE
# =====================================================

st.subheader("📋 KPI Summary")

summary = pd.DataFrame({

    "Metric":[
        "Total Sessions",
        "Average Page Views",
        "Average Session Duration",
        "Average Time on Page",
        "Average Bounce Rate",
        "Average Conversion Rate",
        "Average Previous Visits"
    ],

    "Value":[
        len(filtered_df),
        round(filtered_df["Page Views"].mean(),2),
        round(filtered_df["Session Duration"].mean(),2),
        round(filtered_df["Time on Page"].mean(),2),
        f"{filtered_df['Bounce Rate'].mean():.2%}",
        f"{filtered_df['Conversion Rate'].mean():.2%}",
        round(filtered_df["Previous Visits"].mean(),2)
    ]

})

st.table(summary)

st.divider()

# =====================================================
# DATA EXPLORER
# =====================================================

st.subheader("📂 Explore Filtered Dataset")

with st.expander("View Filtered Data", expanded=False):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# =====================================================
# DOWNLOAD SECTION
# =====================================================

st.subheader("📥 Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Dataset (CSV)",
    data=csv,
    file_name="filtered_website_traffic.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# =====================================================
# DATASET INFORMATION
# =====================================================

st.subheader("📊 Dataset Overview")

info_col1, info_col2, info_col3 = st.columns(3)

info_col1.metric(
    "Rows",
    f"{filtered_df.shape[0]:,}"
)

info_col2.metric(
    "Columns",
    filtered_df.shape[1]
)

memory_usage = (
    filtered_df.memory_usage(deep=True).sum()
    / 1024
)

info_col3.metric(
    "Memory Usage",
    f"{memory_usage:.2f} KB"
)

st.divider()

# =====================================================
# NUMERICAL SUMMARY
# =====================================================

st.subheader("📈 Statistical Summary")

st.dataframe(
    filtered_df.describe().T,
    use_container_width=True
)

st.divider()

# =====================================================
# PROJECT INFORMATION
# =====================================================

st.subheader("📌 Project Information")

st.markdown(
"""
### Web Traffic Analytics Dashboard

This dashboard provides insights into website performance using
interactive visualizations and KPI reporting.

#### Features

- Interactive filtering
- KPI dashboard
- Traffic source analysis
- User engagement analysis
- Conversion analysis
- Correlation analysis
- Business recommendations
- CSV export

#### Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

#### Developed For

Data Analytics Internship Project
"""
)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
---
<center>

**Web Traffic Analytics Dashboard**

Built using **Python**, **Streamlit**, **Pandas**, and **Plotly**

© 2026 Priyanshu Raj

</center>
""",
unsafe_allow_html=True
)