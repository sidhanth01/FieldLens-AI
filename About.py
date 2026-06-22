import streamlit as st
from core.database import init_db, get_dashboard_metrics

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="FieldLens AI",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database tables on startup
init_db()

# Load Dashboard Metrics securely
try:
    metrics = get_dashboard_metrics()
except Exception as e:
    metrics = {
        "total_visits": 0,
        "programs_covered": 0,
        "ai_reports": 0,
        "most_common_issue": "None Detected",
    }

# ============================================================
# Premium Branding & Customized CSS Typography
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Main Hero Headers */
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4.9rem !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #C92A2A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 0rem;
        margin-bottom: 0rem;
    }
    
    .main-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 0.8rem !important;
        text-align: center;
        color: #A3B4AB;
        font-weight: 500;
        margin-top: 0rem;
        margin-bottom: 2.5rem;
    }
    
    /* Professional Soft-Gold Subheadings */
    .custom-subheading {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #A7F3D0; 
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Clean Centered Minimalist Value Pills */
    .hero-badge-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin-bottom: 2.5rem;
    }
    
    .hero-badge {
        background-color: #1E222B;
        border: 1px solid #065F46;
        padding: 10px 22px;
        border-radius: 50px;
        font-family: 'Poppins', sans-serif;
        font-size: 0.95rem;
        color: #E4E7EB;
        font-weight: 600;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.12);
    }
    
    /* ---- Premium Sidebar Customizations ---- */
    /* Increases the font size and weights of the navigation links */
    [data-testid="stSidebarNavItems"] span {
        font-family: 'Poppins', sans-serif !important;
        font-size: 1.15rem !important; 
        font-weight: 500 !important;
        color: #E4E7EB !important;
    }
    
    /* Adds clean padding between the sidebar link rows */
    [data-testid="stSidebarNavItems"] li {
        padding-top: 6px !important;
        padding-bottom: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Centered Hero Section
# ============================================================
st.markdown('<h1 class="main-title">📍 FieldLens AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">AI-Powered Field Reporting for The Nudge Institute</p>', unsafe_allow_html=True)

# Clean, structured capsule pill replacements for the old green box
st.markdown(
    """
    <div class="hero-badge-container">
        <div class="hero-badge">Capture Notes</div>
        <div class="hero-badge">Instant AI Debriefs</div>
        <div class="hero-badge">Secure SQLite Storage</div>
        <div class="hero-badge">Operational Trends</div>
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()

# ============================================================
# Live System Overview (Upgraded Card Grid Layout)
# ============================================================
st.markdown('<p class="custom-subheading">Live System Overview</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric("Total Field Visits", metrics["total_visits"])

with col2:
    with st.container(border=True):
        st.metric("Programs Covered", metrics["programs_covered"])

with col3:
    with st.container(border=True):
        st.metric("AI Reports Generated", metrics["ai_reports"])

with col4:
    with st.container(border=True):
        st.metric("Top Reported Issue", metrics["most_common_issue"])

st.divider()

# ============================================================
# Product Positioning
# ============================================================
st.markdown('<p class="custom-subheading">Why FieldLens AI?</p>', unsafe_allow_html=True)
st.write(
    "Traditional field reporting often requires hours of manual note consolidation, making it difficult "
    "to quickly identify structural bottlenecks or track trends across regions. "
    "FieldLens AI eliminates this administrative overhead, transforming free-form observations and "
    "media attachments into unified, queryable intelligence in seconds."
)
st.divider()

# ============================================================
# Core Capabilities (Symmetrical Spaced Layout)
# ============================================================
st.markdown('<p class="custom-subheading">Core Capabilities</p>', unsafe_allow_html=True)

col_feat1, col_feat2 = st.columns(2)

with col_feat1:
    with st.container(border=True):
        st.markdown("#### 📝 Field Visit Capture")
        st.markdown("""
        * **Metadata Ingestion:** Record visit dates, locations, and stakeholders on the ground seamlessly.
        * **Unstructured Notes:** Ingest free-form text observations without rigid database structure limits.
        * **Multimodal Attachments:** Capture live field photos and record audio voice notes on the fly.
        """)

    st.write("") # Layout padding spacer

    with st.container(border=True):
        st.markdown("#### 🤖 Structured AI Insights")
        st.markdown("""
        * **Automated Summaries:** Instantly synthesize dense ground field observations into crisp briefs.
        * **Operational Blockers:** Automatically isolate logistics, timeline, and infrastructure roadblocks.
        * **Strategic Follow-ups:** Extract real action items and community sentiment matrices instantly.
        """)

with col_feat2:
    with st.container(border=True):
        st.markdown("#### 📈 Operational Dashboard")
        st.markdown("""
        * **Real-Time Aggregation:** Keep immediate tabs on macro field deployments and metrics.
        * **Trend Categorization:** Instantly target recurring system issues logged by the AI engine.
        * **Dynamic State Syncing:** Watch system-wide KPIs update automatically as soon as a form is saved.
        """)

    st.write("") # Layout padding spacer

    with st.container(border=True):
        st.markdown("#### 📚 Visit History Vault")
        st.markdown("""
        * **Global Search Engine:** Instantly isolate logs by program name, location, or active personnel.
        * **Embedded Asset Media:** Play back recorded audio memos and render ground site photographs safely.
        * **Historical Archives:** Revisit full structured breakdowns and technical summaries anytime.
        """)
st.divider()

# ============================================================
# Platform Architecture Workflow
# ============================================================
st.markdown('<p class="custom-subheading">Platform Architecture Workflow</p>', unsafe_allow_html=True)

w_col1, w_col2, w_col3, w_col4 = st.columns(4)

with w_col1:
    with st.container(border=True):
        st.markdown("#### 📥 1. Ingestion")
        st.caption("Field teams capture text notes, live camera images, or voice clips directly from location coordinates.")

with w_col2:
    with st.container(border=True):
        st.markdown("#### 🧠 2. Synthesis")
        st.caption("Gemini 2.5 Flash maps multimodal data streams into strict, structured Pydantic schemas using system rules.")

with w_col3:
    with st.container(border=True):
        st.markdown("#### 🔍 3. Verification")
        st.caption("Officers review generated summaries, findings, sentiment metrics, and core trends on a staging panel.")

with w_col4:
    with st.container(border=True):
        st.markdown("#### 💾 4. Persistence")
        st.caption("Validated files write directly to local SQLite storage engines, immediately refreshing active view counters.")

st.divider()

# ============================================================
# Technology Stack
# ============================================================
st.markdown('<p class="custom-subheading">Technical Architecture</p>', unsafe_allow_html=True)
tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.info("🖥️ **Frontend Engine**\n\nStreamlit Framework")
with tech2:
    st.info("🤖 **AI Orchestration**\n\nGemini 2.5 Flash API")
with tech3:
    st.info("🗄️ **Database Storage**\n\nSQLite 3 Engine")
with tech4:
    st.info("✅ **Schema Validation**\n\nPydantic v2 Core")

st.divider()

# ============================================================
# Navigation Sidebar Guidance
# ============================================================
st.markdown('<p class="custom-subheading">Next Steps</p>', unsafe_allow_html=True)
st.info("👈 Use the navigation options positioned on the left sidebar to start exploring application sections.")

st.caption("📍 FieldLens AI • Streamlit • Gemini 2.5 Flash • SQLite • Pydantic")