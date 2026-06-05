# app.py — Nepal Government Budget Analyzer 2083/84

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Nepal Budget Analyzer 2083/84",
    page_icon="🇳🇵",
    layout="wide"
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #1c1f26;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #d32f2f;
        margin-bottom: 12px;
    }
    .metric-card h3 { 
        color: #ff6b6b; 
        font-size: 13px; 
        margin: 0; 
        letter-spacing: 1px;
    }
    .metric-card h2 { 
        color: #ffffff; 
        font-size: 26px; 
        margin: 6px 0 0 0; 
        font-weight: 700;
    }
    .answer-card {
        background: #e8f4fd;
        border-radius: 12px;
        padding: 24px;
        border-left: 4px solid #1976d2;
        margin: 16px 0;
    }
    .answer-card h3 { color: #1976d2; margin: 0 0 8px 0; }
    .answer-card p { color: #1a1a1a; font-size: 16px; margin: 0; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────
@st.cache_resource
def load_data():
    df = pd.read_csv("nepal_budget_clean.csv")
    df["amount_crore"] = pd.to_numeric(df["amount_crore"], errors="coerce").fillna(0)
    with open("sector_list.json") as f:
        sectors = json.load(f)
    return df, sectors

df, sectors = load_data()

# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 20px 0 10px 0'>
    <h1 style='color:white; font-size:36px; margin:0'>🇳🇵 Nepal Budget Analyzer</h1>
    <p style='color:#aaa; font-size:16px; margin:4px 0'>आर्थिक वर्ष २०८३/८४ — Fiscal Year 2026/27</p>
</div>
""", unsafe_allow_html=True)

# ─── Top Metrics ───────────────────────────────────────────────
total = df["amount_crore"].sum()
top_sector = df.groupby("sector")["amount_crore"].sum().idxmax()
total_entries = len(df)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class='metric-card'>
        <h3>TOTAL BUDGET CAPTURED</h3>
        <h2>Rs. {total:,.0f} Cr</h2>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class='metric-card'>
        <h3>TOP SECTOR</h3>
        <h2>{top_sector}</h2>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class='metric-card'>
        <h3>BUDGET ENTRIES</h3>
        <h2>{total_entries} items</h2>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ─── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Ask the Budget", "📊 Sector Explorer", "🗺️ Budget Overview"])

# ══════════════════════════════════════════════
# TAB 1 — Ask the Budget
# ══════════════════════════════════════════════
with tab1:
    st.markdown("### Ask anything about Nepal's 2083/84 Budget")
    st.markdown("<p style='color:#aaa'>Examples: 'how much for education', 'health budget', 'roads allocation'</p>",
                unsafe_allow_html=True)

    query = st.text_input("", placeholder="Type your question here...", key="search")

    if query:
        keywords = query.lower().split()

        # Keyword to sector mapping
        sector_map = {
            "education": "Education", "school": "Education", "university": "Education",
            "health": "Health", "hospital": "Health", "medical": "Health", "doctor": "Health",
            "road": "Roads", "highway": "Roads", "transport": "Roads", "bridge": "Roads",
            "energy": "Energy", "electricity": "Energy", "power": "Energy", "hydro": "Energy",
            "water": "Water", "sanitation": "Water", "drinking": "Water",
            "agriculture": "Agriculture", "farming": "Agriculture", "crop": "Agriculture",
            "security": "Social Security", "social": "Social Security", "pension": "Social Security",
            "ict": "ICT", "technology": "ICT", "digital": "ICT", "internet": "ICT",
            "forest": "Forest", "environment": "Environment", "green": "Forest",
            "sport": "Sports", "sports": "Sports", "stadium": "Sports",
            "irrigation": "Irrigation", "canal": "Irrigation",
            "tourism": "Tourism", "travel": "Tourism",
            "defense": "Defense", "army": "Defense", "military": "Defense",
            "industry": "Industry", "factory": "Industry",
        }

        # Find matching sector
        matched_sector = None
        for kw in keywords:
            if kw in sector_map:
                matched_sector = sector_map[kw]
                break

        # Search descriptions too
        mask = df["description"].str.lower().str.contains("|".join(keywords), na=False)
        sector_mask = df["sector"] == matched_sector if matched_sector else pd.Series([False] * len(df))
        results = df[mask | sector_mask].copy()

        if len(results) > 0:
            total_amount = results["amount_crore"].sum()
            st.markdown(f"""<div class='answer-card'>
                <h3>💡 Answer</h3>
                <p>Found <b>{len(results)}</b> budget entries matching "<b>{query}</b>"
                with a total allocation of <b>Rs. {total_amount:,.0f} crore</b>
                (Rs. {total_amount/100:.1f} billion) in fiscal year 2083/84.</p>
            </div>""", unsafe_allow_html=True)

            # Chart
            if matched_sector:
                sector_df = df[df["sector"] == matched_sector].nlargest(10, "amount_crore")
                fig = px.bar(
                    sector_df,
                    x="amount_crore",
                    y="description",
                    orientation="h",
                    title=f"{matched_sector} Budget Breakdown",
                    color="amount_crore",
                    color_continuous_scale="Reds",
                    labels={"amount_crore": "Amount (Crore NPR)", "description": ""}
                )
                fig.update_layout(
                    paper_bgcolor="#1c1f26",
                    plot_bgcolor="#1c1f26",
                    font=dict(color="white", size=12),
                    title_font=dict(color="white", size=16),
                    height=400,
                    showlegend=False,
                    xaxis=dict(color="white", gridcolor="#333"),
                    yaxis=dict(color="white", gridcolor="#333")
                )
                st.plotly_chart(fig, use_container_width=True)

            # Results table
            st.markdown("**Matching budget entries:**")
            display_df = results[["sector", "description", "amount_crore", "amount_type"]].copy()
            display_df.columns = ["Sector", "Description", "Amount (Crore)", "Type"]
            display_df = display_df.sort_values("Amount (Crore)", ascending=False)
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        else:
            st.warning(f"No budget entries found for '{query}'. Try keywords like: education, health, roads, energy, water, agriculture.")

# ══════════════════════════════════════════════
# TAB 2 — Sector Explorer
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### Explore Budget by Sector")

    selected_sector = st.selectbox("Select a sector", sorted(sectors))

    sector_data = df[df["sector"] == selected_sector].copy()
    sector_data = sector_data[sector_data["amount_crore"] > 0].sort_values("amount_crore", ascending=False)

    if len(sector_data) > 0:
        sector_total = sector_data["amount_crore"].sum()
        pct_of_total = (sector_total / total * 100) if total > 0 else 0

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class='metric-card'>
                <h3>SECTOR TOTAL</h3>
                <h2>Rs. {sector_total:,.0f} Cr</h2>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card'>
                <h3>% OF CAPTURED BUDGET</h3>
                <h2>{pct_of_total:.1f}%</h2>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'>
                <h3>NUMBER OF ENTRIES</h3>
                <h2>{len(sector_data)}</h2>
            </div>""", unsafe_allow_html=True)

        # Bar chart
        fig = px.bar(
            sector_data.head(15),
            x="amount_crore",
            y="description",
            orientation="h",
            title=f"Top allocations in {selected_sector}",
            color="amount_crore",
            color_continuous_scale="Blues",
            labels={"amount_crore": "Amount (Crore NPR)", "description": ""}
        )
        fig.update_layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font_color="white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        # Full table
        st.markdown("**All entries in this sector:**")
        display_df = sector_data[["description", "amount_crore", "amount_type"]].copy()
        display_df.columns = ["Description", "Amount (Crore NPR)", "Type"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    else:
        st.info(f"No allocation amounts found for {selected_sector}. This sector may have policy entries only.")

# ══════════════════════════════════════════════
# TAB 3 — Budget Overview
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### Nepal Budget 2083/84 — Full Overview")

    sector_summary = df.groupby("sector")["amount_crore"].sum().reset_index()
    sector_summary = sector_summary[sector_summary["amount_crore"] > 0]
    sector_summary = sector_summary.sort_values("amount_crore", ascending=False)

    c1, c2 = st.columns(2)

    with c1:
        fig_pie = px.pie(
            sector_summary,
            values="amount_crore",
            names="sector",
            title="Budget Distribution by Sector",
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_pie.update_layout(
            paper_bgcolor="#1c1f26",
            font=dict(color="white", size=12),
            title_font=dict(color="white", size=16),
            height=450,
            legend=dict(font=dict(color="white"))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        fig_bar = px.bar(
            sector_summary,
            x="sector",
            y="amount_crore",
            title="Sector-wise Allocation (Crore NPR)",
            color="amount_crore",
            color_continuous_scale="Reds",
            labels={"amount_crore": "Amount (Crore NPR)", "sector": ""}
        )
        fig_bar.update_layout(
            paper_bgcolor="#1c1f26",
            plot_bgcolor="#1c1f26",
            font=dict(color="white", size=12),
            title_font=dict(color="white", size=16),
            height=450,
            xaxis=dict(color="white", tickangle=-45, gridcolor="#333"),
            yaxis=dict(color="white", gridcolor="#333")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Summary table
    st.markdown("**Complete sector summary:**")
    sector_summary["Amount (Billion NPR)"] = (sector_summary["amount_crore"] / 100).round(2)
    sector_summary.columns = ["Sector", "Amount (Crore NPR)", "Amount (Billion NPR)"]
    st.dataframe(sector_summary, use_container_width=True, hide_index=True)

# ─── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; font-size:13px'>
    Data source: Nepal Ministry of Finance — Budget Speech 2083/84 | Built with Streamlit
</div>
""", unsafe_allow_html=True)