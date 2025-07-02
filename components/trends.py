import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def show_trends_tab(df, selected_attack, attack_colors):
    st.markdown("#### 📊 Attack Type Trends Over Years (Multi-Line, Dark Mode)")
    attacks_trend_type = (
        df.groupby(["Year", "Attack Type"])
        .size()
        .reset_index(name="Count")
        .pivot(index="Year", columns="Attack Type", values="Count")
        .fillna(0)
    )
    fig = go.Figure()
    types_to_plot = selected_attack if selected_attack else attacks_trend_type.columns.tolist()
    color_palette = list(attack_colors.values()) + ["#fa8231", "#9c27b0", "#00bcd4"]
    for i, attack_type in enumerate(types_to_plot):
        if attack_type in attacks_trend_type.columns:
            color = color_palette[i % len(color_palette)]
            fig.add_trace(
                go.Scatter(
                    x=attacks_trend_type.index,
                    y=attacks_trend_type[attack_type],
                    mode="lines+markers",
                    name=attack_type,
                    line=dict(width=3, color=color),
                    marker=dict(size=8, color=color),
                )
            )
    fig.update_layout(
        title="Attack Types Over the Years",
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Number of Attacks",
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(title="Attack Type", orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor="#181b26",
        paper_bgcolor="#181b26",
        font=dict(family="Segoe UI, Arial", size=15, color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

def show_industry_chart(df, selected_year, industry_colors):
 
    industry_col = "Industry"
    if industry_col not in df.columns:
        candidates = [col for col in df.columns if 'industr' in col.lower() or 'sector' in col.lower()]
        if candidates:
            industry_col = candidates[0]
        else:
            st.info("No industry/sector column found in data.")
            return
    if selected_year != 'All Years':
        df = df[df["Year"] == selected_year]
    industry_counts = df[industry_col].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Attack Count"]
    fig = px.bar(
        industry_counts,
        x="Industry",
        y="Attack Count",
        color="Industry",
        color_discrete_map=industry_colors,
        title=f"Attacks by Industry in {selected_year}",
        template="plotly_dark"
    )
    fig.update_layout(
        font=dict(family="Orbitron, Segoe UI, Arial", size=16, color="#F8F8F8"),
        plot_bgcolor="#0D0116",
        paper_bgcolor="#0D0116",
        xaxis=dict(
            gridcolor="#222244",
            zerolinecolor="#FE53BB",
            color="#08F7FE",
            linecolor="#08F7FE",
            tickfont=dict(color="#F5D300"),
            title="Industry"
        ),
        yaxis=dict(
            gridcolor="#222244",
            zerolinecolor="#FE53BB",
            color="#08F7FE",
            linecolor="#08F7FE",
            tickfont=dict(color="#F5D300"),
            title="Number of Attacks"
        ),
        legend=dict(
            font=dict(color="#F5D300", size=15),
            bgcolor="rgba(20,0,40,0.8)",
            bordercolor="#FE53BB",
            borderwidth=2
        ),
        margin=dict(l=50, r=30, t=60, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

def show_defense_mechanism_chart(df, selected_year, defense_colors, top_n=None):

    colname = "Defense Mechanism"
    if colname not in df.columns:
        candidates = [col for col in df.columns if 'defens' in col.lower() or 'mitig' in col.lower() or 'control' in col.lower()]
        if candidates:
            colname = candidates[0]
        else:
            st.info("No defense/mitigation column found in data.")
            return
    if selected_year != 'All Years':
        df = df[df['Year'] == selected_year]
        df = df[df[colname].notna() & (df[colname].astype(str).str.strip() != '')]
    counts = df[colname].value_counts()
    if top_n:
        counts = counts.head(top_n)
    defense_counts = counts.reset_index()
    defense_counts.columns = ["Defense Mechanism", "Number of Incidents"]
    if defense_counts.empty:
        st.info("No data available for the selected year or defense mechanisms.")
        return
    fig = px.bar(
        defense_counts,
        x="Defense Mechanism",
        y="Number of Incidents",
        color="Defense Mechanism",
        color_discrete_map=defense_colors,
        title=f"Defense Mechanisms Used in {selected_year}",
        template="plotly_dark"
    )
    fig.update_layout(
        font=dict(family="Orbitron, Segoe UI, Arial", size=16, color="#F8F8F8"),
        plot_bgcolor="#0D0116",
        paper_bgcolor="#0D0116",
        xaxis=dict(
            gridcolor="#222244",
            zerolinecolor="#FE53BB",
            color="#08F7FE",
            linecolor="#08F7FE",
            tickfont=dict(color="#F5D300"),
            title="Defense Mechanism"
        ),
        yaxis=dict(
            gridcolor="#222244",
            zerolinecolor="#FE53BB",
            color="#08F7FE",
            linecolor="#08F7FE",
            tickfont=dict(color="#F5D300"),
            title="Number of Incidents"
        ),
        legend=dict(
            font=dict(color="#F5D300", size=15),
            bgcolor="rgba(20,0,40,0.8)",
            bordercolor="#FE53BB",
            borderwidth=2
        ),
        margin=dict(l=50, r=30, t=60, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

def show_vulnerability_chart(df, selected_year=None, top_n=10):

    vuln_col = "Vulnerability Used"
    if vuln_col not in df.columns:
        candidates = [col for col in df.columns if 'vuln' in col.lower() or 'cve' in col.lower() or 'exploit' in col.lower()]
        if candidates:
            vuln_col = candidates[0]
        else:
            st.info("No vulnerability column found.")
            return
    if selected_year != 'All Years':
        df = df[df['Year'] == selected_year]
    vuln_counts = df[vuln_col].value_counts().head(top_n).reset_index()
    vuln_counts.columns = ["Vulnerability", "Attack Count"]
    fig = px.bar(
        vuln_counts,
        x="Vulnerability",
        y="Attack Count",
        title=f"Vulnerabilities Used in Attacks{' in ' + str(selected_year) if selected_year else ''}",
        color="Attack Count",
        color_continuous_scale="Inferno",
        template="plotly_dark"
    )
    fig.update_layout(
        font=dict(family="Orbitron, Segoe UI, Arial", size=16, color="#F8F8F8"),
        plot_bgcolor="#0D0116",
        paper_bgcolor="#0D0116",
        xaxis=dict(
            gridcolor="#222244",
            zerolinecolor="#FE53BB",
            color="#08F7FE",
            linecolor="#08F7FE",
            tickfont=dict(color="#F5D300"),
            title="Vulnerability"
        ),
        yaxis=dict(
            gridcolor="#222244",
            zerolinecolor="#FE53BB",
            color="#08F7FE",
            linecolor="#08F7FE",
            tickfont=dict(color="#F5D300"),
            title="Attack Count"
        ),
        legend=dict(
            font=dict(color="#F5D300", size=15),
            bgcolor="rgba(20,0,40,0.8)",
            bordercolor="#FE53BB",
            borderwidth=2
        ),
        margin=dict(l=50, r=30, t=60, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)
