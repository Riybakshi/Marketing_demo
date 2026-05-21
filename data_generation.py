import os
import numpy as np
import pandas as pd


def generate_marketing_data(n_rows: int = 500, excel_path: str = "data/marketing_data.xlsx") -> pd.DataFrame:
    """Generate a realistic marketing dataset and export it to Excel."""
    np.random.seed(42)

    platforms = ["Meta", "Google", "LinkedIn"]
    audience_segments = [
        "Tech Bros 25-34",
        "Soccer Moms",
        "Wellness Seekers",
        "Finance Pros",
        "Fashion Forward",
        "Homeowners 35-44",
        "Eco Conscious",
        "College Creatives",
    ]
    creatives = [
        "Spring Launch",
        "Holiday Boost",
        "Performance Push",
        "Brand Story",
        "Limited Offer",
        "Customer Testimonial",
        "New Arrival",
        "Conversion Funnel",
    ]

    # Force 2-3 underperforming segments
    bad_segments = ["Finance Pros", "Homeowners 35-44", "College Creatives"]

    records = []
    for i in range(n_rows):
        campaign_id = f"CMP-{1000 + i}"
        platform = np.random.choice(platforms, p=[0.45, 0.4, 0.15])
        segment = np.random.choice(audience_segments)
        creative = np.random.choice(creatives)

        spend = np.round(np.random.uniform(500, 9000), 2)
        impressions = int(np.random.uniform(5000, 200000))

        if segment in bad_segments:
            ctr = np.random.uniform(0.0015, 0.004)  # 0.15% - 0.40%
            conv_rate = np.random.uniform(0.007, 0.015)
        else:
            ctr = np.random.uniform(0.005, 0.025)  # 0.5% - 2.5%
            conv_rate = np.random.uniform(0.015, 0.08)

        clicks = max(1, int(impressions * ctr))
        conversions = max(1, int(clicks * conv_rate))

        records.append(
            {
                "Campaign ID": campaign_id,
                "Platform": platform,
                "Audience Segment": segment,
                "Ad Creative Name": creative,
                "Spend ($)": spend,
                "Impressions": impressions,
                "Clicks": clicks,
                "Conversions": conversions,
            }
        )

    df = pd.DataFrame(records)
    df["CTR"] = (df["Clicks"] / df["Impressions"]) * 100
    df["CPA ($)"] = df["Spend ($)"] / df["Conversions"]
    df["Revenue ($)"] = df["Conversions"] * np.random.uniform(80, 120, size=len(df))
    df["ROAS"] = df["Revenue ($)"] / df["Spend ($)"]

    # Round numeric columns for reporting clarity
    df["CTR"] = df["CTR"].round(2)
    df["CPA ($)"] = df["CPA ($)"].round(2)
    df["Revenue ($)"] = df["Revenue ($)"].round(2)
    df["ROAS"] = df["ROAS"].round(2)

    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    df.to_excel(excel_path, index=False)

    return df


def load_or_generate_data(excel_path: str = "data/marketing_data.xlsx") -> pd.DataFrame:
    """Load marketing data from Excel if it exists, otherwise generate a new file."""
    if os.path.exists(excel_path):
        return pd.read_excel(excel_path)
    return generate_marketing_data(excel_path=excel_path)
