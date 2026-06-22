import streamlit as st
from core.database import get_dashboard_metrics

# ============================================================
# Premium Branding & Advanced CSS Layouts
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Matching Title Gradient */
    .page-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.8rem !important;
        font-weight: 800;
        background: linear-gradient(45deg, #34D399, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
        padding-bottom: 0.2rem;
    }
    
    /* Cohesive Mint Section Headers */
    .custom-subheading {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #A7F3D0; 
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* Custom Premium KPI Card Styling */
    .kpi-card {
        background-color: #1A1E24;
        border: 1px solid #2A323D;
        border-radius: 12px;
        padding: 22px;
        text-align: left;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 15px;
    }

    /* ---- Premium Sidebar Customizations ---- */
    [data-testid="stSidebarNavItems"] span {
        font-family: 'Poppins', sans-serif !important;
        font-size: 1.15rem !important; 
        font-weight: 500 !important;
        color: #E4E7EB !important;
    }
    
    [data-testid="stSidebarNavItems"] li {
        padding-top: 6px !important;
        padding-bottom: 6px !important;
    }


    
    .kpi-card:hover {
        border-color: #34D399;
        transform: translateY(-2px);
    }
    .kpi-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        color: #8B949E;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .kpi-icon {
        font-size: 1.6rem;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Page Header & Controls
# ============================================================
header_col, control_col = st.columns([6, 1])

with header_col:
    st.markdown('<h1 class="page-title">Dashboard</h1>', unsafe_allow_html=True)
    st.caption(
        "Monitor field activities and AI-generated insights across all recorded visits."
    )

with control_col:
    st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.info(
    "📊 Track operational metrics, recent field visits, and AI-generated reports."
)
st.divider()

# ============================================================
# Load Metrics with Robust Exception Handling
# ============================================================
try:
    metrics = get_dashboard_metrics()
except Exception as e:
    st.error("Unable to load dashboard data due to a database exception.")
    st.exception(e)
    st.stop()

# ============================================================
# Custom High-End KPI Cards (2x2 Balanced Layout Grid)
# ============================================================
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Total Field Visits</div>
            <div class="kpi-value">{metrics["total_visits"]}</div>
        </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🌱</div>
            <div class="kpi-label">Programs Covered</div>
            <div class="kpi-value">{metrics["programs_covered"]}</div>
        </div>
    """, unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🧠</div>
            <div class="kpi-label">AI Reports Generated</div>
            <div class="kpi-value">{metrics["ai_reports"]}</div>
        </div>
    """, unsafe_allow_html=True)

with row2_col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Top Reported Issue</div>
            <div class="kpi-value" style="font-size: 1.8rem; color: #FF6B6B;">{metrics["most_common_issue"]}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================
# Recent Visits Feed Segment
# ============================================================
st.markdown('<p class="custom-subheading">Recent Field Visits</p>', unsafe_allow_html=True)

recent_visits = metrics.get("recent_visits", [])
st.caption(f"Showing {len(recent_visits)} recent visit(s).")

if not recent_visits:
    st.info(
        """
        No field visits available.
        
        Start by creating a new field visit from the **New Field Visit** page.
        """
    )
else:
    for visit in recent_visits:
        with st.container(border=True):
            col_content, col_summary = st.columns([1.8, 1])

            with col_content:
                st.markdown(f"### {visit['program']}")
                st.caption(f"🆔 Visit ID: {visit['id']}")
                st.caption(f"📍 {visit['location']}")
                st.caption(f"📅 {visit['date']}")

            with col_summary:
                st.write("**AI Summary Preview**")
                summary = visit.get("summary", "")
                if summary:
                    preview = summary[:150] + "..." if len(summary) > 150 else summary
                    st.info(preview)
                else:
                    st.warning("AI report not available yet.")

st.divider()

# ============================================================
# Standardized Product Footer
# ============================================================
st.caption(
    "📍 FieldLens AI • AI-powered field reporting platform built using Streamlit, Gemini 2.5 Flash and SQLite."
)