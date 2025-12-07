import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Global Analytics Expo 2025", layout="wide")

# 2. Data Loading
@st.cache_data
def load_data():
    # Ensure your excel file name matches this exactly
    df = pd.read_excel("global_expo_data.xlsx")
    # Calculate Trade Balance on the fly
    df['Trade Balance'] = df['Export Revenue (Billion USD)'] - df['Import Cost (Billion USD)']
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# 3. Sidebar Filters (Maximum Filters as requested)
st.sidebar.title("🎛️ Dashboard Controls")

with st.sidebar:
    st.subheader("Primary Filters")
    years = st.multiselect("Select Years", options=sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
    regions = st.multiselect("Select Regions", options=df['Region'].unique(), default=df['Region'].unique())
    countries = st.multiselect("Select Countries", options=df['Country'].unique(), default=['India', 'USA', 'China', 'Germany'])

    st.subheader("Advanced Metrics Filters")
    gdp_range = st.slider("GDP Range ($B)", float(df['GDP (Billion USD)'].min()), float(df['GDP (Billion USD)'].max()), (0.0, 30000.0))
    digital_range = st.slider("Digital Adoption Index", 0.0, 1.0, (0.0, 1.0))
    
    st.divider()
    st.info("Interactive Visualization Forum Expo - AIML 5th Sem")

# Filter logic
mask = (df['Year'].isin(years)) & \
       (df['Region'].isin(regions)) & \
       (df['Country'].isin(countries)) & \
       (df['GDP (Billion USD)'].between(gdp_range[0], gdp_range[1])) & \
       (df['Digital Adoption Index (0-1)'].between(digital_range[0], digital_range[1]))

filtered_df = df[mask]

# 4. Main Dashboard Layout
st.title("🌍 Global Economic & Industrial Mixed-Mode Dashboard")

# Page Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home / KPIs", "📊 Country Analysis", "🚢 Trade & Industry", "🧠 Advanced Insights"])

# --- TAB 1: HOME / KPI SUMMARY ---
with tab1:
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Global GDP ($B)", f"${filtered_df['GDP (Billion USD)'].sum():,.0f}")
    kpi2.metric("Avg Inflation", f"{filtered_df['Inflation (%)'].mean():.2f}%")
    kpi3.metric("Avg Digital Index", f"{filtered_df['Digital Adoption Index (0-1)'].mean():.2f}")
    kpi4.metric("Total Carbon Emission", f"{filtered_df['Carbon Emission (MT)'].sum():,.0f} MT")

    col_a, col_b = st.columns(2)
    with col_a:
        fig_gdp_trend = px.line(filtered_df, x="Year", y="GDP (Billion USD)", color="Country", title="GDP Growth Trend (2018-2024)")
        st.plotly_chart(fig_gdp_trend, use_container_width=True)
    with col_b:
        fig_pie = px.pie(filtered_df[filtered_df['Year'] == max(years)], values='GDP (Billion USD)', names='Country', title=f"Market Share in {max(years)}")
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: COUNTRY ANALYSIS ---
with tab2:
    col_c, col_d = st.columns(2)
    with col_c:
        fig_scatter = px.scatter(filtered_df, x="Inflation (%)", y="Unemployment Rate (%)", size="GDP (Billion USD)", color="Country", title="Inflation vs Unemployment (Bubble Size = GDP)")
        st.plotly_chart(fig_scatter, use_container_width=True)
    with col_d:
        fig_radar = px.line_polar(filtered_df, r="Digital Adoption Index (0-1)", theta="Country", line_close=True, title="Digital Adoption Radar Chart")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- TAB 3: TRADE & INDUSTRY ---
with tab3:
    col_e, col_f = st.columns(2)
    with col_e:
        fig_trade = px.bar(filtered_df, x="Country", y=["Export Revenue (Billion USD)", "Import Cost (Billion USD)"], barmode="group", title="Export vs Import Analysis")
        st.plotly_chart(fig_trade, use_container_width=True)
    with col_f:
        fig_energy = px.scatter(filtered_df, x="Energy Consumption (GWh)", y="Carbon Emission (MT)", color="Country", trendline="ols", title="Energy Consumption vs Carbon Footprint")
        st.plotly_chart(fig_energy, use_container_width=True)

# --- TAB 4: ADVANCED INSIGHTS ---
with tab4:
    st.subheader("Correlation Matrix")
    numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    fig_heat = px.imshow(corr, text_auto=True, aspect="auto", title="Feature Correlation Heatmap")
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.subheader("Filtered Raw Data Explorer")
    st.dataframe(filtered_df, use_container_width=True)
