# app.py — Nepal Government Budget Analyzer 2083/84

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
    .bi { vertical-align: middle; margin-right: 6px; }
</style>
""", unsafe_allow_html=True)


def bi(icon_name, color="#ffffff", size="18px"):
    return f'<i class="bi {icon_name}" style="color:{color}; font-size:{size}; margin-right:6px; vertical-align:middle;"></i>'

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

    /* Responsive fixes */
    @media (max-width: 768px) {
        .metric-card h2 {
            font-size: 18px;
        }
        .metric-card h3 {
            font-size: 11px;
        }
        .answer-card p {
            font-size: 14px;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    df = pd.read_csv("nepal_budget_clean.csv")
    df["amount_crore"] = pd.to_numeric(df["amount_crore"], errors="coerce").fillna(0)
    
    # Sectors to exclude from charts (summary/transfer rows)
    exclude = ["Budget Summary", "Fiscal Transfer", "Overall"]
    
    # For charts — only sector totals, no sub-items, no summary rows
    df_chart = df[
        (df["amount_type"] == "sector_total") &
        (~df["sector"].isin(exclude))
    ].copy()
    
    # For search — all rows except summary
    df_search = df[~df["sector"].isin(exclude)].copy()
    
    with open("sector_list.json") as f:
        sectors = json.load(f)
    
    # Remove summary sectors from dropdown
    sectors = [s for s in sectors if s not in exclude]
    
    return df_search, df_chart, sectors

df, df_chart, sectors = load_data()

# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 24px 0 16px 0; background: linear-gradient(90deg, #1a0a0a, #0a1a2a); border-radius: 12px; margin-bottom: 16px;'>
    <h1 style='color:#ff6b6b; font-size:38px; margin:0; font-weight:800; letter-spacing:0.5px;'>Nepal Budget Analyzer</h1>
    <p style='color:#a0b4c8; font-size:16px; margin:8px 0 0 0'>आर्थिक वर्ष २०८३/८४ — Fiscal Year 2026/27</p>
</div>
""", unsafe_allow_html=True)

# ─── Top Metrics ───────────────────────────────────────────────
# Use only sector totals for the headline number
total = df_chart[df_chart["amount_type"] == "sector_total"]["amount_crore"].sum()
top_sector = df_chart.groupby("sector")["amount_crore"].sum().idxmax()
total_entries = len(df)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class='metric-card'>
        <h3>{bi('bi-cash-coin', '#ff6b6b')} TOTAL BUDGET CAPTURED</h3>
        <h2>Rs. {total:,.0f} Cr</h2>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class='metric-card'>
        <h3>{bi('bi-bar-chart-line', '#ff6b6b')} TOP SECTOR</h3>
        <h2>{top_sector}</h2>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class='metric-card'>
        <h3>{bi('bi-list-check', '#ff6b6b')} BUDGET ENTRIES</h3>
        <h2>{total_entries} items</h2>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ─── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Ask the Budget", "Sector Explorer", "Budget Overview"])

# ══════════════════════════════════════════════
# TAB 1 — Ask the Budget
# ══════════════════════════════════════════════
with tab1:
    st.markdown(f"### {bi('bi-search', '#4fc3f7')} Ask anything about Nepal's 2083/84 Budget", unsafe_allow_html=True)
    st.markdown("<p style='color:#aaa'>Examples: 'how much for education', 'health budget', 'roads allocation'</p>",
                unsafe_allow_html=True)

    query = st.text_input("Search", placeholder="Type your question here...",
                          key="search", label_visibility="collapsed")

    if query:
        keywords = query.lower().split()

        # Keyword to sector mapping
        sector_map = {
            "education": "Education", "school": "Education", "university": "Education",
            "scholarship": "Education", "student": "Education",
            "health": "Health", "hospital": "Health", "medical": "Health",
            "doctor": "Health", "nurse": "Health", "insurance": "Health",
            "road": "Roads & Urban", "highway": "Roads & Urban",
            "transport": "Roads & Urban", "bridge": "Roads & Urban",
            "urban": "Roads & Urban", "rajmarg": "Roads & Urban",
            "energy": "Energy", "electricity": "Energy", "power": "Energy",
            "hydro": "Energy", "transmission": "Energy",
            "water": "Water", "sanitation": "Water", "drinking": "Water",
            "melamchi": "Water", "wastewater": "Water",
            "agriculture": "Agriculture", "farming": "Agriculture",
            "fertilizer": "Agriculture", "crop": "Agriculture", "livestock": "Agriculture",
            "security": "Social Security", "social": "Social Security",
            "pension": "Social Security", "dalit": "Social Security",
            "ict": "ICT", "technology": "ICT", "digital": "ICT",
            "internet": "ICT", "communication": "ICT",
            "forest": "Forest", "environment": "Forest", "climate": "Forest",
            "sport": "Sports", "sports": "Sports", "stadium": "Sports",
            "cricket": "Sports", "football": "Sports",
            "irrigation": "Irrigation", "canal": "Irrigation", "dam": "Irrigation",
            "tourism": "Culture & Tourism", "travel": "Culture & Tourism",
            "culture": "Culture & Tourism", "lumbini": "Culture & Tourism",
            "defense": "Defense", "army": "Defense", "military": "Defense",
            "industry": "Industry", "factory": "Industry", "startup": "Industry",
            "labor": "Labor", "employment": "Labor", "worker": "Labor",
            "aviation": "Aviation", "airport": "Aviation", "flight": "Aviation",
            "science": "Science & Tech", "innovation": "Science & Tech",
            "women": "Women & Children", "children": "Women & Children",
            "child": "Women & Children", "gender": "Women & Children",
        }

        # Find matched sector
        matched_sector = None
        for kw in keywords:
            if kw in sector_map:
                matched_sector = sector_map[kw]
                break

        if matched_sector:
            # Get sector total first
            sector_data = df[df["sector"] == matched_sector].copy()
            sector_totals = sector_data[sector_data["amount_type"] == "sector_total"]
            sector_subs = sector_data[sector_data["amount_type"] == "allocation"]

            if not sector_totals.empty:
                answer_amount = sector_totals["amount_crore"].max()
                answer_text = f"Rs. {answer_amount:,.0f} crore (Rs. {answer_amount/100:.1f} billion) has been allocated to <b>{matched_sector}</b> in fiscal year 2083/84."

                st.markdown(f"""<div class='answer-card'>
                    <h3>{bi('bi-lightbulb', '#1976d2')} Answer</h3>
                    <p>{answer_text}</p>
                    <p style='color:#888; font-size:13px; margin-top:8px'>
                    {bi('bi-exclamation-triangle', '#ff9800')} This shows the total allocation for the <b>{matched_sector}</b> sector. 
                    Specific line items like individual salaries, allowances, or sub-programs 
                    may exist within this budget but could not be extracted as separate figures 
                    from the budget speech text.
                    </p>
                </div>""", unsafe_allow_html=True)

                # Chart — sub-items only
                if not sector_subs.empty:
                    fig = px.bar(
                        sector_subs.sort_values("amount_crore"),
                        x="amount_crore",
                        y="description",
                        orientation="h",
                        title=f"{matched_sector} — Budget Breakdown",
                        color="amount_crore",
                        color_continuous_scale="Reds",
                        labels={"amount_crore": "Amount (Crore NPR)", "description": ""}
                    )
                    fig.update_layout(
                        paper_bgcolor="#1c1f26",
                        plot_bgcolor="#1c1f26",
                        font=dict(color="white", size=12),
                        title_font=dict(color="white", size=16),
                        height=350,
                        margin=dict(l=0, r=10, t=40, b=40),
                        autosize=True,
                        showlegend=False,
                        xaxis=dict(color="white", gridcolor="#333"),
                        yaxis=dict(color="white", gridcolor="#333", automargin=True)
                    )
                    st.plotly_chart(fig, width="stretch")

                # Show sector total + breakdown note
                st.markdown(f"**Sector total: Rs. {answer_amount:,.0f} crore** — breakdown below (sub-items are included within the total, not additional):")
                display_df = sector_subs[["description", "amount_crore"]].copy()
                display_df.columns = ["Description", "Amount (Crore NPR)"]
                display_df = display_df.sort_values("Amount (Crore NPR)", ascending=False)
                st.dataframe(display_df, width="stretch", hide_index=True)

            else:
                # No sector total — show sub-items
                st.markdown(f"""<div class='answer-card'>
                    <h3>{bi('bi-lightbulb', '#1976d2')} Answer</h3>
                    <p>Found <b>{len(sector_subs)}</b> entries for <b>{matched_sector}</b>
                    totalling Rs. {sector_subs['amount_crore'].sum():,.0f} crore.</p>
                </div>""", unsafe_allow_html=True)
                st.dataframe(sector_subs[["description", "amount_crore"]],
                           width="stretch", hide_index=True)

        else:
            # No sector match — search descriptions
            mask = df["description"].str.lower().str.contains(
                "|".join(keywords), na=False)
            results = df[mask].copy()

            if len(results) > 0:
                totals = results[results["amount_type"] == "sector_total"]
                answer_amount = totals["amount_crore"].sum() if not totals.empty else results["amount_crore"].sum()

                st.markdown(f"""<div class='answer-card'>
                    <h3>{bi('bi-lightbulb', '#1976d2')} Answer</h3>
                    <p>Found <b>{len(results)}</b> budget entries matching
                    "<b>{query}</b>" with a total of
                    <b>Rs. {answer_amount:,.0f} crore</b>.</p>
                </div>""", unsafe_allow_html=True)

                display_df = results[["sector", "description", "amount_crore", "amount_type"]].copy()
                display_df.columns = ["Sector", "Description", "Amount (Crore)", "Type"]
                display_df = display_df.sort_values("Amount (Crore)", ascending=False)
                st.dataframe(display_df, width="stretch", hide_index=True)
            else:
                st.warning(f"No entries found for '{query}'. Try: education, health, roads, energy, water, agriculture.")

# ══════════════════════════════════════════════
# TAB 2 — Sector Explorer
# ══════════════════════════════════════════════
with tab2:
    st.markdown(f"### {bi('bi-pie-chart', '#4fc3f7')} Explore Budget by Sector", unsafe_allow_html=True)

    selected_sector = st.selectbox("Select a sector", sorted(sectors))

    sector_data = df[df["sector"] == selected_sector].copy()
    sector_data = sector_data[sector_data["amount_crore"] > 0].sort_values("amount_crore", ascending=False)

    if len(sector_data) > 0:
        sector_totals_only = sector_data[sector_data["amount_type"] == "sector_total"]
        sector_total = sector_totals_only["amount_crore"].sum() if not sector_totals_only.empty else sector_data["amount_crore"].sum()
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
            height=350,
            margin=dict(l=0, r=10, t=40, b=40),
            autosize=True,
            yaxis=dict(color="white", gridcolor="#333", automargin=True)
        )
        st.plotly_chart(fig, width='stretch')

        # Full table
        st.markdown("**All entries in this sector:**")
        display_df = sector_data[["description", "amount_crore", "amount_type"]].copy()
        display_df.columns = ["Description", "Amount (Crore NPR)", "Type"]
        st.dataframe(display_df, width='stretch', hide_index=True)

    else:
        st.info(f"No allocation amounts found for {selected_sector}. This sector may have policy entries only.")

# ══════════════════════════════════════════════
# TAB 3 — Budget Overview
# ══════════════════════════════════════════════
with tab3:
    st.markdown(f"### {bi('bi-map', '#4fc3f7')} Nepal Budget 2083/84 — Full Overview", unsafe_allow_html=True)

    sector_summary = df_chart.groupby("sector")["amount_crore"].sum().reset_index()
    sector_summary = sector_summary[sector_summary["amount_crore"] > 0]
    sector_summary = sector_summary.sort_values("amount_crore", ascending=False)

    c1, c2 = st.columns(2)

    with c1:
        fig_pie = px.pie(
            sector_summary,
            values="amount_crore",
            names="sector",
            title="Budget Distribution by Sector (% of captured allocations)",
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_pie.update_layout(
            paper_bgcolor="#1c1f26",
            font=dict(color="white", size=12),
            title_font=dict(color="white", size=16),
            height=450,
            margin=dict(l=0, r=10, t=40, b=40),
            autosize=True,
            legend=dict(font=dict(color="white"))
        )
        st.plotly_chart(fig_pie, width='stretch')

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
            margin=dict(l=0, r=10, t=40, b=40),
            autosize=True,
            xaxis=dict(color="white", tickangle=-45, gridcolor="#333"),
            yaxis=dict(color="white", gridcolor="#333", automargin=True)
        )
        st.plotly_chart(fig_bar, width='stretch')

    # Summary table
    st.markdown("**Complete sector summary:**")
    sector_summary = df_chart.groupby("sector")["amount_crore"].sum().reset_index()
    sector_summary = sector_summary[sector_summary["amount_crore"] > 0]
    sector_summary = sector_summary.sort_values("amount_crore", ascending=False)
    st.dataframe(sector_summary, width='stretch', hide_index=True)

# ─── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; font-size:13px'>
    Data source: Nepal Ministry of Finance — Budget Speech 2083/84 | Built with Streamlit
</div>
""", unsafe_allow_html=True)