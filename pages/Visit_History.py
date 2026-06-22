import streamlit as st
from pathlib import Path
from config import BASE_DIR
from core.database import get_visit_history

# ============================================================
# Premium Branding & Cohesive CSS Typography
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Unified Emerald Mint Title Gradient */
    .page-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(45deg, #34D399, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
        padding-bottom: 0.2rem;
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


    /* Cohesive Mint Section Headers */
    .custom-subheading {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem !important;
        font-weight: 700;
        color: #A7F3D0; 
        margin-top: 1.5rem;
        margin-bottom: 1rem;
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
    st.markdown('<h1 class="page-title">Visit History</h1>', unsafe_allow_html=True)
    st.caption(
        "Browse all previously saved field visits and AI-generated reports."
    )

with control_col:
    st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.info(
    "Search through historical field visits, review AI insights, and revisit uploaded evidence."
)
st.divider()

# ============================================================
# Load Visit History
# ============================================================
try:
    visits = get_visit_history()
except Exception as e:
    st.error("Unable to load visit history.")
    st.exception(e)
    st.stop()

# ============================================================
# Search Filter
# ============================================================
search = st.text_input(
    "🔍 Search Logs",
    placeholder="Search by program, location or stakeholder..."
)

if search:
    keyword = search.lower()
    filtered_visits = []

    for visit in visits:
        searchable_text = " ".join([
            str(visit.get("program", "")),
            str(visit.get("location", "")),
            str(visit.get("stakeholders", "")),
        ]).lower()

        if keyword in searchable_text:
            filtered_visits.append(visit)

    visits = filtered_visits

st.caption(f"Total Saved Visits: {len(visits)}")
st.divider()

# ============================================================
# Empty State
# ============================================================
if not visits:
    st.info(
        """
        No matching field visits found.
        
        Create a new visit from the **New Field Visit** page.
        """
    )
    st.stop()

# ============================================================
# Historical Visit Feed
# ============================================================
for visit in visits:
    title = f"📍 {visit['program']} • {visit['location']} ({visit['date']})"

    with st.expander(title, expanded=False):
        # Metadata Layout inside an optimized container card block
        with st.container(border=True):
            st.markdown('<p class="custom-subheading" style="margin-top:0rem;">📋 Visit Information</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Visit ID:** {visit['id']}")
                st.write(f"**Program:** {visit['program']}")
                st.write(f"**Location:** {visit['location']}")

            with col2:
                st.write(f"**Visit Date:** {visit['date']}")
                st.write(f"**Stakeholders:** {visit['stakeholders'] or 'Not provided'}")

        st.write("") # Symmetrical padding layout separator

        # Collapsible Original Field Notes
        with st.expander("📝 Original Field Notes", expanded=False):
            if visit.get("notes"):
                st.write(visit["notes"])
            else:
                st.caption("No field notes available.")

        st.write("")

        # Structured Report Container Box
        with st.container(border=True):
            st.markdown('<p class="custom-subheading" style="margin-top:0.5rem;">🤖 AI Executive Summary</p>', unsafe_allow_html=True)
            if visit.get("summary"):
                st.info(visit["summary"])
            else:
                st.warning("AI report not available.")

            # Community Sentiment Section
            sentiment = visit.get("community_sentiment", "")
            if sentiment:
                st.markdown('**😊 Community Sentiment**')
                lower_sentiment = sentiment.lower()
                if lower_sentiment.startswith("positive"):
                    st.success(sentiment)
                elif lower_sentiment.startswith("negative"):
                    st.error(sentiment)
                else:
                    st.warning(sentiment)

            st.divider()

            # Split Column Grid Layout for deeper analytics metrics
            left_col, right_col = st.columns(2)

            with left_col:
                with st.expander("🔍 Key Findings", expanded=True):
                    findings = visit.get("key_findings", [])
                    if findings:
                        for item in findings: 
                            st.markdown(f"- {item}")
                    else:
                        st.caption("No findings available.")

                with st.expander("🚧 Blockers", expanded=True):
                    blockers = visit.get("blockers", [])
                    if blockers:
                        for item in blockers: 
                            st.markdown(f"- {item}")
                    else:
                        st.caption("No blockers identified.")

            with right_col:
                with st.expander("💡 Recommendations", expanded=True):
                    recommendations = visit.get("recommendations", [])
                    if recommendations:
                        for item in recommendations: 
                            st.markdown(f"- {item}")
                    else:
                        st.caption("No recommendations available.")

                with st.expander("📌 Follow-up Actions", expanded=True):
                    followups = visit.get("follow_ups", [])
                    if followups:
                        for item in followups: 
                            st.markdown(f"- {item}")
                    else:
                        st.caption("No follow-up actions suggested.")

            st.write("")

            # AI System Macro Tags Module
            with st.expander("⚠️ Issues Identified", expanded=False):
                issues = visit.get("issues_identified", [])
                if issues:
                    for issue in issues: 
                        st.markdown(f"- {issue}")
                else:
                    st.caption("No recurring macro issues identified.")

        st.write("")

        # Media Attachments Layout Vault Card
        with st.container(border=True):
            st.markdown('<p class="custom-subheading" style="margin-top:0.5rem;">📎 Attachments</p>', unsafe_allow_html=True)
            attachment_col1, attachment_col2 = st.columns(2)

            # Image Loader Panel
            with attachment_col1:
                st.write("**📷 Field Photo**")
                image_path = visit.get("image_path")
                if image_path:
                    full_image_path = Path(BASE_DIR) / image_path
                    if full_image_path.exists():
                        try:
                            st.image(
                                str(full_image_path),
                                caption="Logged Field Photo Evidence",
                                use_container_width=True,
                            )
                        except Exception:
                            st.warning("Unable to load the uploaded image.")
                    else:
                        st.warning("Image file not found.")
                else:
                    st.caption("No image uploaded.")

            # Audio Loader Panel
            with attachment_col2:
                st.write("**🎤 Voice Note**")
                audio_path = visit.get("audio_path")
                if audio_path:
                    full_audio_path = Path(BASE_DIR) / audio_path
                    if full_audio_path.exists():
                        try:
                            with open(full_audio_path, "rb") as audio_file:
                                st.audio(audio_file.read())
                        except Exception:
                            st.warning("Unable to load the uploaded audio.")
                    else:
                        st.warning("Audio file not found.")
                else:
                    st.caption("No voice note uploaded.")
        st.write("")

# ============================================================
# Footer Layout
# ============================================================
st.caption(
    "📍 FieldLens AI • Browse historical field visits, AI-generated reports and uploaded evidence."
)