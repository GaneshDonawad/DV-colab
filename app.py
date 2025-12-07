import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Global Economic Insights Dashboard", layout="wide")

# Custom Title for the Expo
st.title("🌏 Mixed-Mode Interactive Visualization Forum Dashboard")
st.markdown("### *5th Semester AIML - Interactive Forum Expo 2025*")

# 2. Sidebar File Uploader ( ब्राउज़ ऑप्शन )
st.sidebar.header("📁 Data Management")
uploaded_file = st.sidebar.file_uploader("Upload 'global_expo_data.xlsx'", type=["xlsx", "csv"])

if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
        # Real-time feature engineering: Trade Balance
        if 'Export Revenue (Billion USD)' in df.columns and 'Import Cost (Billion USD)' in df.columns:
            df['Trade Balance'] = df['Export Revenue (Billion USD)'] - df['Import Cost (Billion USD)']
        return df

    data = load_data(uploaded_file)

    # 3. SIDEBAR: 12 PROFESSIONAL FILTERS
    st.sidebar.divider()
    st.sidebar.subheader("🎛️ Dynamic Analysis Controls")
    
    with st.sidebar:
        # Categorical Selection (3 Filters)
        f_year = st.multiselect("1. Year Selection", options=sorted(data['Year'].unique()), default=sorted(data['Year'].unique()))
        f_reg = st.multiselect("2. Global Region", options=data['Region'].unique(), default=data['Region'].unique())
        f_country = st.multiselect("3. Focused Country", options=data['Country'].unique(), default=data['Country'].unique())

        # Quantitative Range Selection (9 Filters)
        f_gdp = st.slider("4. GDP Range ($B)", float(data['GDP (Billion USD)'].min()), float(data['GDP (Billion USD)'].max()), (float(data['GDP (Billion USD)'].min()), float(data['GDP (Billion USD)'].max())))
        f_grow = st.slider("5. Growth % Range", float(data['Economic Growth (%)'].min()), float(data['Economic Growth (%)'].max()), (float(data['Economic Growth (%)'].min()), float(data['Economic Growth (%)'].max())))
        f_inf = st.slider("6. Inflation % Range", float(data['Inflation (%)'].min()), float(data['Inflation (%)'].max()), (float(data['Inflation (%)'].min()), float(data['Inflation (%)'].max())))
        f_unem = st.slider("7. Unemployment % Range", float(data['Unemployment Rate (%)'].min()), float(data['Unemployment Rate (%)'].max()), (float(data['Unemployment Rate (%)'].min()), float(data['Unemployment Rate (%)'].max())))
        f_pop = st.slider("8. Population (M) Range", float(data['Population (Millions)'].min()), float(data['Population (Millions)'].max()), (float(data['Population (Millions)'].min()), float(data['Population (Millions)'].max())))
        f_man = st.slider("9. Manufacturing Level", float(data['Manufacturing Output (Million Units)'].min()), float(data['Manufacturing Output (Million Units)'].max()), (float(data['Manufacturing Output (Million Units)'].min()), float(data['Manufacturing Output (Million Units)'].max())))
        f_eng = st.slider("10. Energy GWh Range", float(data['Energy Consumption (GWh)'].min()), float(data['Energy Consumption (GWh)'].max()), (float(data['Energy Consumption (GWh)'].min()), float(data['Energy Consumption (GWh)'].max())))
        f_dig = st.slider("11. Digital Index Range", 0.0, 1.0, (0.0, 1.0))
        f_carb = st.slider("12. Carbon Emission (MT)", float(data['Carbon Emission (MT)'].min()), float(data['Carbon Emission (MT)'].max()), (float(data['Carbon Emission (MT)'].min()), float(data['Carbon Emission (MT)'].max())))

    # 4. Filter logic application
    mask = (
        data['Year'].isin(f_year) & data['Region'].isin(f_reg) & data['Country'].isin(f_country) &
        data['GDP (Billion USD)'].between(f_gdp[0], f_gdp[1]) &
        data['Economic Growth (%)'].between(f_grow[0], f_grow[1]) &
        data['Inflation (%)'].between(f_inf[0], f_inf[1]) &
        data['Unemployment Rate (%)'].between(f_unem[0], f_unem[1]) &
        data['Population (Millions)'].between(f_pop[0], f_pop[1]) &
        data['Manufacturing Output (Million Units)'].between(f_man[0], f_man[1]) &
        data['Energy Consumption (GWh)'].between(f_eng[0], f_eng[1]) &
        data['Digital Adoption Index (0-1)'].between(f_dig[0], f_dig[1]) &
        data['Carbon Emission (MT)'].between(f_carb[0], f_carb[1])
    )
    df = data[mask]

    # --- MAIN UI TABS ---
    tab1, tab2, tab3 = st.tabs(["🏠 Overview KPIs", "📊 Infrastructure Barometer", "🧠 Correlation Modeling"])

    with tab1:
        st.subheader("Global Health Indicators")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total GDP ($B)", f"${df['GDP (Billion USD)'].sum():,.1f}B")
        k2.metric("Avg Growth", f"{df['Economic Growth (%)'].mean():.2f}%")
        k3.metric("Trade Balance", f"${df['Trade Balance'].sum():,.1f}B")
        k4.metric("Samples Found", len(df))

        st.plotly_chart(px.line(df, x="Year", y="GDP (Billion USD)", color="Country", title="GDP Trends by Country"), use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.scatter(df, x="Energy Consumption (GWh)", y="Carbon Emission (MT)", size="GDP (Billion USD)", color="Country", title="Environmental Impact vs Economic Scale"), use_container_width=True)
        c2.plotly_chart(px.bar(df, x="Country", y="Manufacturing Output (Million Units)", color="Region", title="Industrial Power Rank"), use_container_width=True)

    with tab3:
        st.subheader("Statistical Correlation (Pearson Coeff)")
        st.plotly_chart(px.imshow(df.select_dtypes(include='number').corr(), text_auto=True, title="Pearson Correlation Heatmap"), use_container_width=True)
        st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ Pending Data: Use the Sidebar to upload your Expo Excel file to render visualizations.")
