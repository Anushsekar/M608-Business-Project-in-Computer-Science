import streamlit as st
import plotly.express as px

import pydeck as pdk
from utils.geo import add_lat_lon


def show_map_tab(filtered_df, selected_year, attack_colors):
    def hex_to_rgba(hex_color, alpha=180):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return [r, g, b, alpha]

    grouped = filtered_df.groupby(['Country', 'Attack Type']).size().reset_index(name='Count')
    grouped = add_lat_lon(grouped)
    grouped = grouped.dropna(subset=['lat', 'lon'])

    grouped["color"] = grouped["Attack Type"].map(
        lambda x: hex_to_rgba(attack_colors.get(x, "#757575"))
    )
    grouped["radius"] = grouped["Count"].apply(lambda x: 50000 + x * 8000)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=grouped,
        get_position='[lon, lat]',
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
        auto_highlight=True,
        opacity=0.75,
    )

    view_state = pdk.ViewState(
        latitude=25, longitude=0, zoom=1.2, pitch=0
    )

    st.subheader(f"🌍 Attack Types per Country in {selected_year}")
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Country: {Country}\nAttack Type: {Attack Type}\nIncidents: {Count}"},
        map_style="dark"
    ))

    st.markdown("#### Attack Type Legend")
    legend_html = "<div style='display: flex; flex-wrap: wrap;'>"
    for attack_type, color in attack_colors.items():
        legend_html += (
            f"<div style='display: flex; align-items: center; margin-right: 25px; margin-bottom: 6px;'>"
            f"<span style='display: inline-block; width: 18px; height: 18px; border-radius: 50%; background: {color}; margin-right: 7px; border: 1.5px solid #444;'></span>"
            f"<span style='font-size: 1rem; color: #eee; letter-spacing: 0.5px;'>{attack_type}</span>"
            f"</div>"
        )
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)
