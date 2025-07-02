import streamlit as st
from config import ATTACK_COLORS, INDUSTRY_COLORS, DEFENSE_COLORS
from utils.data_loader import load_data
from utils.filtering import filter_data
from utils.blocklist import load_blocklist, check_ip_blocklist
from components.sidebar import sidebar_filters
from components.live_feed import show_live_feed_tab
from components.trends import show_trends_tab, show_industry_chart, show_vulnerability_chart,show_defense_mechanism_chart
from components.map_tab import show_map_tab
from components.event_table import show_event_table, financial_loss
from components.ip_checker import show_ip_lookup

st.set_page_config(page_title="Global Cyber Threat Dashboard", layout="wide")

# Custom styles
st.markdown("""
<style>
    .block-container {padding-top: 2rem;}
    .metric {border-radius: 12px; box-shadow: 0 1px 8px #e1e1e1;}
    .sidebar-content {font-size: 1.05em;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Welcome")
    st.caption("_Track cyber incidents worldwide. Use filters below._")
    df, loss_df = load_data()
    selected_year, selected_attack, selected_country = sidebar_filters(df)
    filtered_df = filter_data(df, selected_year, selected_attack, selected_country)
    years = sorted(df['Year'].unique())

st.title("🌐 Global Cyber Threat Dashboard")
st.info("🚨 3 new CISA alerts this week. Click [here](https://www.cisa.gov/news-events/cybersecurity-advisories) for details.")

tab0, tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Map", "Event Table", "IP Lookup", "Live OTX Feed"])

with tab0:
    show_trends_tab(df if selected_country == "All" else df[df['Country'] == selected_country], selected_attack, ATTACK_COLORS)
    show_industry_chart(filtered_df, selected_year, INDUSTRY_COLORS)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stContainer">', unsafe_allow_html=True)
        st.markdown("##### 🛡️ Defense Mechanisms")
        show_defense_mechanism_chart(filtered_df, selected_year, DEFENSE_COLORS)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stContainer">', unsafe_allow_html=True)
        st.markdown("##### 🐞 Vulnerabilities Used")
        show_vulnerability_chart(filtered_df, selected_year)
        st.markdown('</div>', unsafe_allow_html=True)

with tab1:
    show_map_tab(filtered_df, selected_year, ATTACK_COLORS)

with tab2:
    financial_loss(filtered_df, loss_df, selected_year, years,df)
    show_event_table(filtered_df, selected_year, selected_attack, selected_country, loss_df)

with tab3:
    show_ip_lookup()

with tab4:
    show_live_feed_tab(filtered_df)

with st.expander("About & Data Sources"):
    st.markdown("""
    This dashboard provides interactive insights into global cyber threats, economic losses from netcrime, and live threat intelligence.

    **Data sources:**
    - **Global Cybersecurity Threats 2015–2024**  
    Major cyber attacks, countries, industries, attack types, and losses.  
    Source: [Kaggle](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)

    - **Global Losses From Netcrime (2019–2024)**  
    Annual reported financial losses due to cybercrime.  
    Source: [Kaggle](https://www.kaggle.com/datasets/huzpsb/cybersecurity-incidents-dataset)

    - **FireHOL Level 1 IP Blocklist**  
    Continuously updated list of known malicious IP addresses.  
    Source: [FireHOL Project](https://iplists.firehol.org/)

    - **AlienVault OTX (Open Threat Exchange) API**  
    Provides live cyber threat intelligence feeds.  
    Source: [otx.alienvault.com](https://otx.alienvault.com/)

    ---
    """)
st.markdown("---")
container = st.container(border=True)
container.caption("Developed for Gisma University project. Powered by Streamlit.")
