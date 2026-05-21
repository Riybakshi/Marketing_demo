import streamlit as st
import pandas as pd
import plotly.express as px

from data.data_generation import load_or_generate_data


st.set_page_config(
    page_title="Agentic Campaign Optimization Engine",
    page_icon="🚀",
    layout="wide",
)


def load_data() -> pd.DataFrame:
    """Load or generate the marketing dataset."""
    return load_or_generate_data()


def campaign_dashboard(df: pd.DataFrame) -> None:
    st.title("Agentic Campaign Optimization Engine")
    st.markdown(
        """
        ## Campaign Dashboard
        This dashboard shows the marketing dataset the AI agent is monitoring.
        The agent uses these metrics to identify underperforming campaigns and make optimization recommendations.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        fig_spend_conv = px.scatter(
            df,
            x="Spend ($)",
            y="Conversions",
            color="Platform",
            hover_data=["Campaign ID", "Audience Segment", "CPA ($)", "ROAS"],
            title="Spend vs Conversions",
            trendline="ols",
        )
        st.plotly_chart(fig_spend_conv, use_container_width=True)

    with col2:
        cpa_by_platform = df.groupby("Platform")["CPA ($)"].mean().reset_index()
        fig_cpa = px.bar(
            cpa_by_platform,
            x="Platform",
            y="CPA ($)",
            title="Average CPA by Platform",
            text="CPA ($)",
        )
        fig_cpa.update_traces(texttemplate="$%{text:.2f}", textposition="outside")
        st.plotly_chart(fig_cpa, use_container_width=True)


def anomaly_detection(df: pd.DataFrame) -> None:
    st.title("Anomaly Detection: Identifying Underperformers")
    st.markdown(
        """
        The AI agent scans this dataset for segments with poor results. It highlights campaigns that are spending too much for too few conversions.
        """
    )

    underperf = df[(df["CPA ($)"] > 50) | (df["CTR"] < 0.5)].copy()
    underperf = underperf.sort_values(by=["CPA ($)", "CTR"], ascending=[False, True])

    st.metric("Underperforming Rows", len(underperf))
    st.dataframe(underperf.head(20), use_container_width=True)


def creative_optimization(df: pd.DataFrame) -> None:
    st.title("Agentic Creative Optimization")
    st.markdown(
        """
        Choose an underperforming segment and let the AI agent diagnose the creative performance.
        The agent will propose new ad copy variants tailored to the audience.
        """
    )

    underperf_segments = (
        df[(df["CPA ($)"] > 50) | (df["CTR"] < 0.5)]["Audience Segment"].unique()
    )
    selected_segment = st.selectbox("Select an underperforming audience segment:", underperf_segments)

    if st.button("Run AI Agent"):
        with st.spinner("Agent is analyzing performance and generating fresh creative..."):
            st.success("Agent execution complete.")
            st.markdown("### Agent Analysis")
            st.write(
                f"The selected audience segment **{selected_segment}** is showing weak engagement and high acquisition costs. "
                "The current creative likely misses the audience's motivations and lacks a strong, relevant call-to-action."
            )
            st.markdown("### Recommended Ad Copy Variants")
            for idx in range(1, 4):
                st.markdown(f"**Variant {idx}**")
                st.write("- Headline: \"[Headline that speaks to urgency and value]\"")
                st.write("- Primary Text: \"[Primary text that addresses the segment's core pain points and includes a strong offer]\"")
                st.write("---")


def budget_reallocation(df: pd.DataFrame) -> None:
    st.title("Budget Reallocation Engine")
    st.markdown(
        """
        The AI agent recommends shifting budget away from underperforming segments toward the best-performing campaigns.
        It then estimates how many more conversions this reallocation could drive.
        """
    )

    perf_summary = df.groupby("Audience Segment").agg(
        total_spend=("Spend ($)", "sum"),
        conversions=("Conversions", "sum"),
    )
    perf_summary["CPA ($)"] = perf_summary["total_spend"] / perf_summary["conversions"]
    perf_summary = perf_summary.sort_values("CPA ($)")

    current = perf_summary.reset_index()
    top_segments = current.head(3)
    under_segments = current[current["CPA ($)"] > 50].head(3)

    st.write("### Current Budget Allocation")
    st.dataframe(current, use_container_width=True)

    if not under_segments.empty:
        shift_amount = under_segments["total_spend"].sum() * 0.2
        budget_share = shift_amount / top_segments["total_spend"].sum()

        recommended = current.copy()
        recommended.loc[recommended.index.isin(under_segments.index), "total_spend"] *= 0.8
        recommended.loc[recommended.index.isin(top_segments.index), "total_spend"] *= 1 + budget_share
        recommended["projected_conversions"] = (
            recommended["total_spend"] / recommended["CPA ($)"]
        ).round(0)

        st.write("### Agent Recommended Allocation")
        st.dataframe(recommended.reset_index(drop=True), use_container_width=True)
        projected_gain = recommended["projected_conversions"].sum() - current["conversions"].sum()
        st.metric("Projected Conversion Gain", int(projected_gain))
    else:
        st.info("No clear underperforming segments found to reallocate budget from.")


def campaign_experience() -> None:
    st.title("Campaign Experience: Video & Animation Ads")
    st.markdown(
        """
        This page showcases how the campaign looks and feels through ad mockups and motion content.
        Use these previews to explain the creative direction behind the optimization engine.
        """
    )

    st.markdown("### Video Ad Preview")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.video("https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4")
        st.caption("Example campaign-style video ad animation.")

    with col2:
        st.metric("Creative Focus", "Audience-first storytelling")
        st.metric("Mood", "Energetic, premium, urgent")
        st.markdown(
            """
            - Motion design creates rapid attention on mobile feeds.
            - The agent captures audience motivations and highlights value quickly.
            - This page helps stakeholders see the campaign as an experience, not just numbers.
            """
        )

    st.markdown("---")
    st.markdown("### Animated Ad Cards")
    gif_cards = [
        (
            "Launch Moment",
            "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
            "High-energy product reveal animation for an audience-first campaign.",
        ),
        (
            "Audience Hook",
            "https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif",
            "A fast-moving motion sequence designed to capture attention quickly.",
        ),
        (
            "Performance Story",
            "https://media.giphy.com/media/xUOxf48fzHxU1BKq4g/giphy.gif",
            "A visual narrative showing budget and conversion momentum.",
        ),
    ]

    cols = st.columns(3)
    for (title, gif_url, caption), col in zip(gif_cards, cols):
        with col:
            st.image(gif_url, caption=title, use_column_width=True)
            st.write(caption)

    st.markdown(
        """
        ### Why this matters
        Animation and video are powerful tools in the campaign toolkit. They make the story memorable,
        increase engagement, and help the AI agent explain why creative updates matter.
        """
    )


def main() -> None:
    df = load_data()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        [
            "Campaign Dashboard",
            "Anomaly Detection",
            "Agentic Creative Optimization",
            "Budget Reallocation Engine",
            "Campaign Experience",
        ],
    )

    if page == "Campaign Dashboard":
        campaign_dashboard(df)
    elif page == "Anomaly Detection":
        anomaly_detection(df)
    elif page == "Agentic Creative Optimization":
        creative_optimization(df)
    elif page == "Budget Reallocation Engine":
        budget_reallocation(df)
    elif page == "Campaign Experience":
        campaign_experience()


if __name__ == "__main__":
    main()
