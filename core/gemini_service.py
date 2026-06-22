import io
import json
from typing import Any, List, Optional
from PIL import Image

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from config import GEMINI_API_KEY

# ============================================================
# Constants & Initialization
# ============================================================

MODEL_NAME = "gemini-2.5-flash"

if not GEMINI_API_KEY:
    raise ValueError(
        "Gemini API key not found. Please add GEMINI_API_KEY to your .env file."
    )

# Reusing a single client instance is the standard production pattern
client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# AI Response Schema
# ============================================================

class DebriefReport(BaseModel):
    """
    Structured AI response returned by Gemini.
    """
    summary: str = Field(
        description="A concise summary of the field visit."
    )
    key_findings: List[str] = Field(
        description="Important observations from the visit."
    )
    blockers: List[str] = Field(
        description="Challenges or blockers identified."
    )
    community_sentiment: str = Field(
        description="Overall community sentiment formatted strictly as specified in system instructions."
    )
    recommendations: List[str] = Field(
        description="Suggested recommendations."
    )
    follow_ups: List[str] = Field(
        description="Suggested follow-up actions."
    )
    issues_identified: List[str] = Field(
        description="Recurring issues or themes."
    )


# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are an experienced NGO Field Program Manager working for The Nudge Institute.

Analyze the provided field visit information and generate a structured report.

Instructions:
1. Write a concise summary.
2. Extract the important findings.
3. Identify blockers or challenges.
4. Determine the overall community sentiment. 
   Always start with exactly one of: 'Positive', 'Neutral', or 'Negative', followed by a colon and a brief one-sentence explanation.
   Example: 'Positive: Community members appreciated the training but requested additional irrigation support.'
5. Provide practical recommendations.
6. Suggest realistic follow-up actions.
7. Identify recurring issues discussed.

Multimodal Guidelines:
- If an image is provided: Analyze visible ground conditions, extract relevant visual observations, and incorporate them into the findings or blockers. Do not describe objects unrelated to the field visit.
- If audio is provided: Process and transcribe speech segments from field personnel, mapping out stated core concerns directly into structural sections.

Guardrails:
- Do not invent facts.
- Base every conclusion only on the provided text notes and uploaded media.
- If information is missing, explicitly say so instead of guessing or hallucinating.

Return structured data matching the schema only.
"""


# ============================================================
# AI Service Layer
# ============================================================

def generate_report(
    program: str,
    location: str,
    stakeholders: str,
    notes: str,
    image: Optional[Image.Image] = None,
    audio_bytes: Optional[bytes] = None, # 👈 Added argument to receive incoming audio content safely
) -> dict[str, Any]:
    """
    Generate a structured AI debrief report by orchestrating multimodal inputs.
    """
    prompt = f"""
Program:
{program}

Location:
{location}

Stakeholders:
{stakeholders}

Field Notes:
{notes}
"""

    contents = [prompt]

    # Handle the incoming PIL Image object directly
    if image is not None:
        contents.append(image)

    # Handle the incoming audio binary data securely via native SDK type helper
    if audio_bytes is not None:
        contents.append(
            types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/mp3"
            )
        )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
                response_mime_type="application/json",
                response_schema=DebriefReport,
            ),
        )

        # Utilize native SDK Pydantic parsing mechanism
        report: DebriefReport = response.parsed
        return report.model_dump()

    except Exception as e:
        raise RuntimeError(
            f"Gemini report generation failed: {str(e)}"
        )