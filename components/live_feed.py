import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit_autorefresh import st_autorefresh

def show_live_feed_tab(filtered_df):
    API_KEY = "e2f88360f8c27cd4d8dada08e63993dcd1337e7c0de5e7f9c0d948b28456f61e"
    headers = {"X-OTX-API-KEY": API_KEY}
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        pulses = data.get("results", [])
        country_list = []
        for p in pulses:
            countries = p.get("targeted_countries", [])
            country_list.extend(countries)
        if country_list:
            country_counts = pd.Series(country_list).value_counts().reset_index()
            country_counts.columns = ['Country', 'Number of Threat Pulses']
            st.subheader("Live OTX Threats by Targeted Country")
            fig_map = px.scatter_geo(
                country_counts,
                locations="Country",
                locationmode="country names",
                size="Number of Threat Pulses",
                color="Number of Threat Pulses",
                projection="natural earth",
                title="Live OTX Threat Pulses by Country"
            )
            st.plotly_chart(fig_map)
        else:
            st.info("No targeted country data available in live OTX pulses.")
        
    else:
        st.error("Failed to fetch OTX data. Check your API key.")

    st.markdown("### 🚨 Simulated Live Attack Events")
    df_events = filtered_df.sample(frac=1).reset_index(drop=True)

    if 'live_table_index' not in st.session_state:
        st.session_state['live_table_index'] = 0

 
    if st.button("🔄 Refresh Live Feed"):
        st.session_state['live_table_index'] = (st.session_state['live_table_index'] + 5) % max(1, (len(df_events) - 4))

    N = 5
    start = st.session_state['live_table_index']
    end = min(start + N, len(df_events))
    live_events = df_events.iloc[start:end]

    cols_to_show = [col for col in live_events.columns if col in ['Year', 'Attack Type', 'Country', 'Financial Loss (in Million $)']]
    if not live_events.empty:
        st.dataframe(live_events[cols_to_show], use_container_width=True)
    else:
        st.info("No events to display.")
    st.caption("Click 'Refresh Live Feed' to see more events.")