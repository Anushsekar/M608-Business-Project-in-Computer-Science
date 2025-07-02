import ipaddress
from config import DATA_DIR
import streamlit as st

@st.cache_data
def load_blocklist():
    with open(f"{DATA_DIR}/firehol_level1.netset") as f:
        ip_networks = [ipaddress.ip_network(line.strip()) for line in f if line.strip() and not line.startswith("#")]
    return ip_networks

def check_ip_blocklist(ip_input, ip_networks):
    try:
        ip_obj = ipaddress.ip_address(ip_input)
        is_blocked = any(ip_obj in net for net in ip_networks)
        return is_blocked
    except ValueError:
        return None
