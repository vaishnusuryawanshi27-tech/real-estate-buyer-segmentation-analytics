import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------

# PAGE CONFIG

# -------------------

st.set_page_config(
    page_title="Buyer Intelligence Dashboard",
    page_icon="🏠",
    layout="wide"
)

# -------------------

# LOAD DATA

# -------------------

df = pd.read_csv("buyer_segmentation_final_dataset.csv")

# -------------------

# SIDEBAR

# -------------------

st.sidebar.title("🏠 Filters")

country = st.sidebar.multiselect(
    "Country",
    df["country"].unique(),
    default=df["country"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["region"].unique(),
    default=df["region"].unique()
)

segment = st.sidebar.multiselect(
    "Buyer Segment",
    df["buyer_segment"].unique(),
    default=df["buyer_segment"].unique()
)

filtered_df = df[
    (df["country"].isin(country)) &
    (df["region"].isin(region)) &
    (df["buyer_segment"].isin(segment))
]

# -------------------

# PAGE SELECTOR

# -------------------

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Executive Overview",
        "Investor Intelligence",
        "Geographic Analysis",
        "Buyer Persona Explorer",
        "Advanced Analytics"
    ]
)


csv = filtered_df.to_csv(index=False)

st.sidebar.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_buyer_data.csv",
    "text/csv"
)
# -------------------

# EXECUTIVE OVERVIEW

# -------------------

if page == "Executive Overview":

    st.title("🏠 Real Estate Buyer Intelligence Dashboard")
    st.caption(
        "Interactive dashboard • Filters apply to all visualizations"
    )

    st.markdown(
        "### Machine Learning Based Buyer Segmentation & Investment Profiling for Real Estate Market Intelligence"
    )

    # KPI CARDS
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Buyers",
        filtered_df["client_id"].nunique()
    )

    c2.metric(
        "Total Investment",
        f"${filtered_df['total_investment_value'].sum():,.0f}"
    )

    c3.metric(
        "Avg Sale Price",
        f"${filtered_df['sale_price'].mean():,.0f}"
    )

    c4.metric(
        "Avg Satisfaction",
        round(filtered_df["satisfaction_score"].mean(), 2)
    )

    st.markdown("---")

    # Chart 1 - Buyer Segment Distribution
    fig1 = px.pie(
        filtered_df,
        names="buyer_segment",
        hole=0.6,
        title="Buyer Segment Distribution"
    )

    fig1.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Chart 2 - Total Investment
    investment_seg = filtered_df.groupby(
        "buyer_segment"
    )["total_investment_value"].sum().reset_index()

    fig2 = px.bar(
        investment_seg,
        x="buyer_segment",
        y="total_investment_value",
        color="buyer_segment",
        title="Total Investment by Segment"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Chart 3 - Avg Sale Price
    sale_seg = filtered_df.groupby(
        "buyer_segment"
    )["sale_price"].mean().reset_index()

    fig3 = px.bar(
        sale_seg,
        x="buyer_segment",
        y="sale_price",
        color="buyer_segment",
        title="Average Sale Price by Segment"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # Chart 4 - Satisfaction
    sat_seg = filtered_df.groupby(
        "buyer_segment"
    )["satisfaction_score"].mean().reset_index()

    fig4 = px.bar(
        sat_seg,
        x="buyer_segment",
        y="satisfaction_score",
        color="buyer_segment",
        title="Customer Satisfaction by Segment"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )
    segment_rank = filtered_df.groupby(
        "buyer_segment"
    )[
        [
            "total_investment_value",
            "sale_price",
            "satisfaction_score"
        ]
    ].mean().round(2)

    st.subheader("Buyer Segment Performance Summary")

    st.dataframe(
        segment_rank,
        use_container_width=True
    )

# ----------------
# Dashboard 2

# -----------------
elif page == "Investor Intelligence":

    st.title("💰 Investor Intelligence Dashboard")

    st.caption(
        "Interactive dashboard • Filters apply to all visualizations"
    )

    invest_seg = filtered_df.groupby(
        "buyer_segment"
    )["total_investment_value"].mean().reset_index()

    fig1 = px.bar(
        invest_seg,
        x="buyer_segment",
        y="total_investment_value",
        color="buyer_segment",
        title="Average Investment Value by Segment"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )
    
    # Chart 2
    freq_seg = filtered_df.groupby(
        "buyer_segment"
    )["transaction_frequency"].mean().reset_index()

    fig2 = px.bar(
        freq_seg,
        x="buyer_segment",
        y="transaction_frequency",
        color="buyer_segment",
        title="Transaction Frequency by Segment"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Chart 3
    fig3 = px.scatter(
        filtered_df,
        x="total_investment_value",
        y="satisfaction_score",
        color="buyer_segment",
        size="properties_owned",
        hover_data=["country"],
        title="Investment vs Satisfaction"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Chart 4
    tenure = filtered_df.groupby(
        "buyer_segment"
    )["time_as_client"].mean().reset_index()

    fig4 = px.bar(
        tenure,
        x="buyer_segment",
        y="time_as_client",
        color="buyer_segment",
        title="Client Tenure by Segment"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # Chart 5
    high_value = filtered_df.groupby(
        "buyer_segment"
    )["high_value_property"].mean().reset_index()

    fig5 = px.bar(
        high_value,
        x="buyer_segment",
        y="high_value_property",
        color="buyer_segment",
        title="High Value Property Percentage by Segment"
    )

    st.plotly_chart(fig5, use_container_width=True)

    # Chart 6 
    properties = filtered_df.groupby(
        "buyer_segment"
    )["properties_owned"].mean().reset_index()

    fig6 = px.bar(
        properties,
        x="buyer_segment",
        y="properties_owned",
        color="buyer_segment",
        title="Average Properties Owned by Segment"
    )

    st.plotly_chart(fig6, use_container_width=True)

    # Chart 7
    avg_value = filtered_df.groupby(
        "buyer_segment"
    )["avg_property_value_per_client"].mean().reset_index()

    fig7 = px.bar(
        avg_value,
        x="buyer_segment",
        y="avg_property_value_per_client",
        color="buyer_segment",
        title="Average Property Value per Client"
    )

    st.plotly_chart(fig7, use_container_width=True)



# -------------------
# Dashboard 3
# --------------------

elif page == "Geographic Analysis":

    st.title("🌍 Geographic Buyer Analysis")
    st.caption(
        "Interactive dashboard • Filters apply to all visualizations"
    )

    # Chart 1
    country_buyers = filtered_df.groupby(
        "country"
    )["client_id"].count().reset_index()

    fig1 = px.bar(
        country_buyers,
        x="country",
        y="client_id",
        color="country",
        title="Number of Buyers by Country"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2
    region_investment = filtered_df.groupby(
        "region"
    )["total_investment_value"].sum().reset_index()

    fig2 = px.bar(
        region_investment,
        x="region",
        y="total_investment_value",
        color="region",
        title="Total Investment by Region"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Chart 3
    region_segment = filtered_df.groupby(
        ["region", "buyer_segment"]
    )["client_id"].count().reset_index()

    fig3 = px.bar(
        region_segment,
        x="region",
        y="client_id",
        color="buyer_segment",
        barmode="stack",
        title="Buyer Segment Distribution by Region"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Chart 4
    country_price = filtered_df.groupby(
        "country"
    )["sale_price"].mean().reset_index()

    fig4 = px.bar(
        country_price,
        x="country",
        y="sale_price",
        color="country",
        title="Average Sale Price by Country"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # Chart 5
    region_satisfaction = filtered_df.groupby(
        "region"
    )["satisfaction_score"].mean().reset_index()

    fig5 = px.bar(
        region_satisfaction,
        x="region",
        y="satisfaction_score",
        color="region",
        title="Average Satisfaction Score by Region"
    )

    st.plotly_chart(fig5, use_container_width=True)

# -------------------
# Dashboard 4
# -------------------

elif page == "Buyer Persona Explorer":

    st.title("🧑‍💼 Buyer Persona Explorer")
    st.caption(
        "Interactive dashboard • Filters apply to all visualizations"
    )

    selected_segment = st.selectbox(
        "Select Buyer Segment",
        sorted(filtered_df["buyer_segment"].unique())
    )

    persona_df = filtered_df[
        filtered_df["buyer_segment"] == selected_segment
    ]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Avg Age",
        round(persona_df["age"].mean(), 1)
    )

    c2.metric(
        "Avg Sale Price",
        f"${persona_df['sale_price'].mean():,.0f}"
    )

    c3.metric(
        "Avg Investment",
        f"${persona_df['total_investment_value'].mean():,.0f}"
    )

    c4.metric(
        "Avg Satisfaction",
        round(persona_df["satisfaction_score"].mean(), 2)
    )

    # Chart 1
    owned = persona_df["properties_owned"].mean()

    st.subheader("Average Properties Owned")

    st.metric(
        "Properties Owned",
        round(owned, 2)
    )

    # Chart 2
    client_type = persona_df.groupby(
        "client_type"
    )["client_id"].count().reset_index()

    fig1 = px.pie(
        client_type,
        names="client_type",
        values="client_id",
        hole=0.5,
        title="Client Type Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Chart 3
    purpose = persona_df.groupby(
        "acquisition_purpose"
    )["client_id"].count().reset_index()

    fig2 = px.bar(
        purpose,
        x="acquisition_purpose",
        y="client_id",
        color="acquisition_purpose",
        title="Acquisition Purpose Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Chart 4
    referral = persona_df.groupby(
        "referral_channel"
    )["client_id"].count().reset_index()

    fig3 = px.bar(
        referral,
        x="referral_channel",
        y="client_id",
        color="referral_channel",
        title="Referral Channel Analysis"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Chart 5
    country_dist = persona_df.groupby(
        "country"
    )["client_id"].count().reset_index()

    fig4 = px.bar(
        country_dist,
        x="country",
        y="client_id",
        color="country",
        title="Country Distribution"
    )

    st.plotly_chart(fig4, use_container_width=True)


# -----------------
# Dashboard 5
# -----------------

elif page == "Advanced Analytics":

    st.title("📊 Advanced Analytics")
    st.caption(
        "Interactive dashboard • Filters apply to all visualizations"
    )

    # Chart 1
    fig1 = px.scatter(
        filtered_df,
        x="sale_price",
        y="total_investment_value",
        color="buyer_segment",
        size="properties_owned",
        hover_data=["country"],
        title="Sale Price vs Total Investment Value"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2
    fig2 = px.scatter(
        filtered_df,
        x="age",
        y="total_investment_value",
        color="buyer_segment",
        size="properties_owned",
        title="Age vs Total Investment Value"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Chart 3
    fig3 = px.histogram(
        filtered_df,
        x="sale_price",
        color="buyer_segment",
        title="Sale Price Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Chart 4
    fig4 = px.histogram(
        filtered_df,
        x="age",
        color="buyer_segment",
        title="Age Distribution by Segment"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # Chart 5
    corr_df = filtered_df[
        [
            "age",
            "satisfaction_score",
            "sale_price",
            "price_per_sqft",
            "properties_owned",
            "total_investment_value",
            "transaction_frequency",
            "time_as_client"
        ]
    ]

    corr = corr_df.corr(numeric_only=True)

    fig5 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig5, use_container_width=True)
