import streamlit as st
import ipaddress
from utils.blocklist import load_blocklist, check_ip_blocklist

def show_ip_lookup():
    st.markdown("## 🔎 IP Blocklist Checker (FireHOL Level 1)")
    st.markdown("""
    Enter an IPv4 or IPv6 address to check if it's listed in the FireHOL Level 1 blocklist.

    **Sample IPs to try:** 
    - Malicious / Likely to Be Blocked:
        `192.168.1.1`
        `10.0.0.5`

    - Clean / Well-Known Public (Not Blocked):
        `8.8.8.8` (Google DNS)
        `1.1.1.1` (Cloudflare DNS)

    - Invalid or Private (should warn, not block):
        `256.1.1.1` 
    """)

    ip_input = st.text_input("Enter an IP address to check:", "")

    check_btn = st.button("Check IP Blocklist Status")
    if check_btn:
        if not ip_input.strip():
            st.info("Please enter an IP address.")
        else:
            ip_networks = load_blocklist()
            result = check_ip_blocklist(ip_input.strip(), ip_networks)
            if result is None:
                st.warning("Please enter a valid IPv4 or IPv6 address.")
            elif result:
                st.error(f"🚫 {ip_input} **is listed in FireHOL Level 1 blocklist!**")
            else:
                st.success(f"✅ {ip_input} is NOT listed in FireHOL Level 1 blocklist.")

    st.caption("Data source: [FireHOL Level 1 Blocklist](https://firehol.org/)")
