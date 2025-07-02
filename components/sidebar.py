import streamlit as st

def sidebar_filters(df):

    years = sorted(df['Year'].unique())
    years = ['All Years'] + years  
    attack_types = sorted(df['Attack Type'].unique())
    countries = ['All'] + sorted(df['Country'].unique())
    selected_year = st.selectbox("Year", years, key="sidebar_year")
    selected_attack = st.multiselect("Attack Types", attack_types, default=attack_types, key="sidebar_attack_types")
    selected_country = st.selectbox("Country", countries, key="sidebar_country")
    return selected_year, selected_attack, selected_country

