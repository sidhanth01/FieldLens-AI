# 📍 FieldLens AI

> **AI-Powered Field Reporting Platform for NGOs**
>
> Built for **The Nudge Institute**

FieldLens AI is an intelligent field reporting platform that helps NGO field officers capture observations, upload field evidence, and automatically generate structured AI-powered reports.

Instead of spending hours manually writing debriefs after every field visit, users can simply record their observations, attach photos or voice notes, and receive an organized report within seconds.

---

## 🔗 Live Application Link

**Live Demo on Streamlit Cloud:** (https://fieldlens-ai.streamlit.app/Dashboard)
*(Note: Streamlit Community Cloud operates on an ephemeral filesystem. Local database metrics and uploads automatically reset when the container goes to sleep or code updates are pushed.)*

### Try It Yourself (Drought Assessment Test Case)
Test the multimodal extraction layer by submitting a field log with a mix of media:
1. Navigate to the **New Field Visit** tab.
2. Enter `Drought Mitigation & Relief Assessment` as the **Program** and `Mandya District` as the **Location**.
3. Copy/paste or say this into the **Field Notes/Audio**: *"Fields in Mandya are completely dry due to stopped canal water from the KRS reservoir. Standing sugarcane is dying. Farmers are anxious and need the pending subsidy immediately."*
4. Upload a photo of dry, cracked ground or a parched farm field.
5. Click **Generate AI Debrief** to see the system visually analyze the cracked soil texture from the image, log the speech bytes, flag the community sentiment as `Negative/Anxious`, and map the metrics into the dynamic dashboard.

---

# Features

## Field Visit Management

- Record field visit details
- Program information
- Visit location
- Visit date
- Stakeholders involved
- Detailed field notes

---

## AI Report Generation

Powered by **Google Gemini 2.5 Flash**

Automatically generates:

- Executive Summary
- Key Findings
- Operational Blockers
- Community Sentiment
- Recommendations
- Suggested Follow-up Actions
- Issues Identified

Every report follows a structured schema using **Pydantic**, ensuring consistent outputs.

---

## Image Analysis

Upload field photos or capture images directly from your device.

The AI analyzes:

- Ground conditions
- Environmental observations
- Infrastructure
- Visible field issues

These visual insights are incorporated into the final report.

---

## Voice Recording

Supports both:

- Uploading audio files
- Live audio recording

Voice notes are stored alongside the visit for future reference.

---

## Live Camera Capture

Capture photos directly inside the application using your device camera.

No need to leave the application to upload evidence.

---

## Dashboard

Real-time operational dashboard showing:

- Total Field Visits
- Programs Covered
- AI Reports Generated
- Most Reported Issue

Also includes:

- Recent field visits
- AI summary previews

---

## Visit History

Browse all historical visits.

Features include:

- Search by program
- Search by location
- Search by stakeholder
- View AI reports
- View uploaded images
- Listen to saved voice notes

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| AI Model | Google Gemini 2.5 Flash |
| Database | SQLite |
| Validation | Pydantic v2 |
| Language | Python 3.11+ |

---

# 📂 Project Structure

```
FieldLens-AI/
│
├── About.py
├── config.py
├── requirements.txt
│
├── core/
│   ├── database.py
│   └── gemini_service.py
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_New_Field_Visit.py
│   └── 3_Visit_History.py
│
├── uploads/
│   ├── images/
│   └── audio/
│
├── data/
│   └── fieldlens.db
│
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/sidhanth01/FieldLens-AI.git
```

Go into the project directory

```bash
cd FieldLens-AI
```

Create a virtual environment

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Gemini API

Create a `.env` file or configure a Streamlit secret.

Example

```
GEMINI_API_KEY=YOUR_API_KEY
```

Or create

```
.streamlit/secrets.toml
```

```
GEMINI_API_KEY="YOUR_API_KEY"
```

---

# Run the Application

```bash
streamlit run About.py
```

The application will automatically

- Create the SQLite database
- Create upload directories
- Initialize tables

---

#  Database Design

## visits

Stores

- Visit metadata
- Notes
- Uploaded image path
- Uploaded audio path

---

## reports

Stores

- AI Summary
- Key Findings
- Blockers
- Community Sentiment
- Recommendations
- Follow-ups
- Issues Identified

Reports are linked to visits using a foreign key.

---

# AI Workflow

```
User Input
      │
      ▼
Field Details
      │
      ▼
Photo / Camera
      │
      ▼
Voice Recording
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Structured JSON Response
      │
      ▼
Pydantic Validation
      │
      ▼
Preview Report
      │
      ▼
SQLite Storage
      │
      ▼
Dashboard Updates
```

---

#  Application Pages

## Home

Overview of the platform, technology stack, workflow, and live metrics.

---

## Dashboard

Displays

- Total visits
- Programs covered
- AI reports generated
- Top reported issue
- Recent visits

---

## New Field Visit

Allows users to

- Enter visit details
- Upload images
- Capture images
- Upload audio
- Record live audio
- Generate AI reports
- Save reports

---

## Visit History

Provides

- Historical search
- AI report review
- Media preview
- Audio playback
- Structured report display

---

# Key Design Decisions

- Lightweight SQLite database
- No ORM dependency
- Structured AI outputs using Pydantic
- Modular architecture
- Mobile-friendly interface
- Multimodal AI support
- Local media storage
- Clean separation between UI, AI, and persistence layers

---

#  AI Safety

The AI is instructed to

- Never hallucinate facts
- Base conclusions only on provided notes and media
- Clearly state when information is missing
- Produce structured JSON responses
- Maintain consistent formatting

---

#  Supported Media

Images

- JPG
- JPEG
- PNG

Audio

- MP3
- WAV
- M4A

Supports

- File upload
- Camera capture
- Live audio recording

---

# Future Improvements

Potential enhancements include:

- PDF report export
- Email sharing
- Multi-user authentication
- Cloud database integration
- Interactive analytics dashboard
- Speech-to-text transcription
- Offline-first synchronization
- Geo-tagged field visits
- Multi-language support
- Report versioning

---

# Assessment Highlights

This project demonstrates:

- AI product thinking
- End-to-end application development
- Prompt engineering
- Multimodal AI integration
- Structured output generation
- Database design
- User experience design
- Mobile-first considerations
- Production-oriented architecture
- Clean code organization

---

# Author

**Sidhanth L**

AI/ML Engineer

---

This project showcases how Generative AI can significantly reduce manual reporting effort while helping NGO teams capture, organize, and analyze field intelligence in a structured and scalable manner.
