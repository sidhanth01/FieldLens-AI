import streamlit as st
from PIL import Image
from pathlib import Path
from core.database import save_visit, save_report
from core.gemini_service import generate_report

# ============================================================
# Premium Branding & Cohesive CSS Typography
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Subpage Unique Header Styling */
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
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #A7F3D0; 
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Helper UI Functions
# ============================================================
def render_debrief_section(title: str, items: list[str], empty_message: str, expanded: bool = True):
    """Abstraction helper to render markdown lists uniformly inside expanders."""
    with st.expander(title, expanded=expanded):
        if items:
            for item in items:
                st.markdown(f"• {item}")
        else:
            st.write(empty_message)

# ============================================================
# Page Header
# ============================================================
st.markdown('<h1 class="page-title">New Field Visit</h1>', unsafe_allow_html=True)
st.caption(
    "Capture field observations and generate an AI-powered debrief using Gemini."
)
st.info(
    "📱 Mobile-first design • Photo uploads supported • AI-powered structured field reports"
)
st.divider()

# ============================================================
# Session State Initialization
# ============================================================
if "generated_report" not in st.session_state:
    st.session_state.generated_report = None

if "visit_data" not in st.session_state:
    st.session_state.visit_data = None

# ============================================================
# Input Form Rendering
# ============================================================
with st.form("field_visit_form", clear_on_submit=False):
    st.markdown('<p class="custom-subheading">📋 Visit Details</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        program = st.text_input(
            "Program *",
            placeholder="Example: Farmer Support Program"
        )
    with col2:
        location = st.text_input(
            "Location *",
            placeholder="Example: Mysuru"
        )

    col3, col4 = st.columns(2)
    with col3:
        visit_date = st.date_input("Visit Date")
    with col4:
        stakeholders = st.text_input(
            "Stakeholders",
            placeholder="Farmers, SHG Members, Teachers..."
        )

    notes = st.text_area(
        "Field Notes *",
        height=220,
        placeholder="Example:\n• Farmers appreciated today's training.\n• Several members requested irrigation support.\n• Some mentioned delays in subsidy approvals.",
    )

    st.divider()
    st.markdown('<p class="custom-subheading">📎 Attachments (Optional)</p>', unsafe_allow_html=True)

    # Image Upload / Selection
    uploaded_image = st.file_uploader(
        "Upload Field Photo",
        type=["jpg", "jpeg", "png"],
        help="Upload a site image for AI visual analysis."
    )
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Staged Field Photo Preview", use_container_width=True)
    else:
        st.caption("📷 No image uploaded.")

    st.write("")

    # Audio Upload / Selection
    uploaded_audio = st.file_uploader(
        "Upload Voice Note",
        type=["mp3", "wav", "m4a"],
        help="Optional voice recording from the field."
    )
    if uploaded_audio is not None:
        st.audio(uploaded_audio)
    else:
        st.caption("🎤 No voice note uploaded.")

    st.divider()
    generate_button = st.form_submit_button(
        "🤖 Generate AI Debrief",
        use_container_width=True,
    )

# ============================================================
# Processing Loop: Input Validation & AI Inference
# ============================================================
if generate_button:
    if not program.strip():
        st.error("Program name is required.")
        st.stop()
    if not location.strip():
        st.error("Location is required.")
        st.stop()
    if not notes.strip():
        st.error("Field notes cannot be empty.")
        st.stop()

    pil_image = None
    if uploaded_image is not None:
        try:
            pil_image = Image.open(uploaded_image).convert("RGB")
        except Exception:
            st.error("Unable to read the uploaded image.")
            st.stop()

    st.session_state.visit_data = {
        "program": program,
        "location": location,
        "date": str(visit_date),
        "stakeholders": stakeholders,
        "notes": notes,
        "uploaded_image": uploaded_image,
        "uploaded_audio": uploaded_audio,
        "image": pil_image,
    }

    with st.spinner("🤖 AI is analyzing the field notes and generating insights..."):
        try:
            report = generate_report(
                program=st.session_state.visit_data["program"],
                location=st.session_state.visit_data["location"],
                stakeholders=st.session_state.visit_data["stakeholders"],
                notes=st.session_state.visit_data["notes"],
                image=st.session_state.visit_data["image"],
                audio_bytes=uploaded_audio.getvalue() if uploaded_audio else None,
            )
            st.session_state.generated_report = report
            st.success("✅ AI debrief generated successfully. Review it below before saving.")
        except Exception as e:
            st.session_state.generated_report = None
            st.error(f"Unable to generate AI report.\n\n{e}")

if st.session_state.generated_report is None:
    st.info("Fill in the visit details and click **Generate AI Debrief** to create a structured report.")

# ============================================================
# Display Block & Database Operations
# ============================================================
report = st.session_state.generated_report

if report:
    st.divider()
    with st.container(border=True):
        st.markdown('<p class="custom-subheading" style="margin-top:0.5rem;">🤖 AI Debrief Report</p>', unsafe_allow_html=True)
        st.caption("This report was generated using Gemini based on the field notes and uploaded media.")

        # Summary Breakdown
        st.subheader("📄 Executive Summary")
        st.info(report["summary"])

        # Community Sentiment Rendering Badge
        st.subheader("😊 Community Sentiment")
        sentiment = report["community_sentiment"]
        if sentiment.lower().startswith("positive"):
            st.success(sentiment)
        elif sentiment.lower().startswith("negative"):
            st.error(sentiment)
        else:
            st.warning(sentiment)

        st.divider()

        # Dynamic Grid System Output Panel
        left_col, right_col = st.columns(2)

        with left_col:
            render_debrief_section("🔍 Key Findings", report.get("key_findings", []), "No findings generated.")
            render_debrief_section("🚧 Blockers", report.get("blockers", []), "No blockers identified.")

        with right_col:
            render_debrief_section("💡 Recommendations", report.get("recommendations", []), "No recommendations generated.")
            render_debrief_section("📌 Suggested Follow-ups", report.get("follow_ups", []), "No follow-up actions generated.")

        st.divider()

        # System Label Flags Module
        render_debrief_section("⚠️ Issues Identified", report.get("issues_identified", []), "No macro themes flagged.", expanded=False)

        st.info("Review the AI-generated debrief carefully before saving it to the database.")

    # Storage Persistence Block Trigger
    st.divider()
    st.markdown('<p class="custom-subheading">💾 Save Field Visit</p>', unsafe_allow_html=True)
    st.write("The AI report looks good. Click **Save Field Visit** to permanently store this record.")

    left, center, right = st.columns([1, 2, 1])
    with center:
        save_button = st.button("💾 Save Field Visit", type="primary", use_container_width=True)

    if save_button:
        try:
            visit = st.session_state.visit_data
            
            image_bytes = visit["uploaded_image"].getvalue() if visit["uploaded_image"] else None
            image_extension = Path(visit["uploaded_image"].name).suffix if visit["uploaded_image"] else ".jpg"

            audio_bytes = visit["uploaded_audio"].getvalue() if visit["uploaded_audio"] else None
            audio_extension = Path(visit["uploaded_audio"].name).suffix if visit["uploaded_audio"] else ".mp3"

            visit_id = save_visit(
                visit_data={
                    "program": visit["program"],
                    "location": visit["location"],
                    "date": visit["date"],
                    "stakeholders": visit["stakeholders"],
                    "notes": visit["notes"],
                },
                image_bytes=image_bytes,
                audio_bytes=audio_bytes,
                image_extension=image_extension,
                audio_extension=audio_extension,
            )

            save_report(visit_id=visit_id, report=report)

            st.success(f"✅ Visit successfully saved. AI report has been added to your field records.")
            st.toast("AI report saved successfully 🎉", icon="✅")
            st.balloons()

            st.session_state.generated_report = None
            st.session_state.visit_data = None
            st.rerun()

        except Exception as e:
            st.error("Failed to save the visit.")
            st.exception(e)

# ============================================================
# Educational Help Closures
# ============================================================
st.divider()
with st.expander("💡 Tips for Better AI Reports", expanded=False):
    st.markdown("""
### Write Better Field Notes
The quality of the AI report depends directly on the depth of information you provide.
- Mention what exactly occurred during the target field visit.
- Include transparent community feedback quotes or issues.
- Describe any unexpected physical, financial, or climate challenges faced.
- Explicitly log important stakeholder names or roles met on-site.
- Upload clear site pictures whenever possible so the Gemini vision engine can parse visual details.
""")

st.caption("📍 FieldLens AI • AI-powered field reporting platform built using Streamlit, Gemini 2.5 Flash and SQLite.")