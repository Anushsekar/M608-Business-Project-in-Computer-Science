import streamlit as st

def financial_loss(filtered_df, loss_df, selected_year, years, main_df):
    st.markdown("---")
    dataset_choice = st.radio(
        "Show financial loss from:",
        ["Main Incident Data", "LossFromNetCrime (Official Aggregate)"],
        horizontal=True,
    )

    if selected_year == "All Years":
        main_loss = main_df["Financial Loss (in Million $)"].dropna().sum()
        netcrime_loss = 0
        for col in loss_df.columns:
            if col.endswith("_Losses"):
                netcrime_loss += loss_df[col].sum()
    else:
        main_loss = main_df[main_df["Year"] == selected_year]["Financial Loss (in Million $)"].dropna().sum()
        netcrime_col = f"{selected_year}_Losses"
        netcrime_loss = loss_df[netcrime_col].sum() if netcrime_col in loss_df.columns else 0

    if dataset_choice == "Main Incident Data":
        st.metric("Financial Loss (Main Data)", f"${main_loss:,.0f}M ")
    else:
        st.metric("Financial Loss (LossFromNetCrime)", f"${netcrime_loss:,.0f}")

    with st.expander("Compare both loss datasets"):
        col1, col2 = st.columns(2)
        col1.metric("Main Incident Data", f"${main_loss:,.0f}M")
        col2.metric("LossFromNetCrime", f"${netcrime_loss:,.0f} USD")

def highlight_attack_type(val):
    color_map = {
        "Phishing": "#ff9800",
        "Ransomware": "#e53935",
        "DDoS": "#3949ab",
        "Man-in-the-Middle": "#43a047",
        "SQL Injection": "#00838f",
        "Other": "#757575"
    }
    color = color_map.get(val, "#757575")
    return f"color: white; background-color: {color}; border-radius: 4px; padding: 2px 6px;"

def show_event_table(filtered_df, selected_year, selected_attack, selected_country, loss_df):
    table_choice = st.radio(
        "Select table to view:",
        ("Filtered Incident Data", "Yearly Financial Losses (LossFromNetCrime)"),
        horizontal=True,
    )

    if table_choice == "Filtered Incident Data":

        styled_df = filtered_df.style.applymap(highlight_attack_type, subset=["Attack Type"])
        st.dataframe(styled_df, use_container_width=True)

        def clean(s):
            if isinstance(s, list):
                s = "_".join([str(i) for i in s])
            return str(s).replace(" ", "_").replace("/", "-")

        filename = f"cyberthreats_{clean(selected_year)}_{clean(selected_attack)}_{clean(selected_country)}.csv"
        csv = filtered_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name=filename,
            mime='text/csv'
        )

    else:  
        if selected_year == "All Years":
            df_show = loss_df
        else:
            year_cols = [col for col in loss_df.columns if str(selected_year) in col]
            df_show = loss_df[year_cols]
            if df_show.empty:
                st.info("No loss data available for the selected year in LossFromNetCrime.")
                return

        st.dataframe(df_show, use_container_width=True)
        loss_csv = df_show.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download loss data as CSV",
            data=loss_csv,
            file_name=f"lossfromnetcrime_{selected_year}.csv",
            mime='text/csv'
        )