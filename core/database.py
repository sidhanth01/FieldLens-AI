import json
import sqlite3
from pathlib import Path
from typing import Any

from config import DB_PATH, IMAGES_DIR, AUDIO_DIR


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection with configuration overrides."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create database tables if they don't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program TEXT NOT NULL,
            location TEXT NOT NULL,
            date TEXT NOT NULL,
            stakeholders TEXT,
            notes TEXT,
            image_path TEXT,
            audio_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visit_id INTEGER NOT NULL,
            summary TEXT,
            key_findings TEXT,
            blockers TEXT,
            community_sentiment TEXT,
            recommendations TEXT,
            follow_ups TEXT,
            issues_identified TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (visit_id) REFERENCES visits(id) ON DELETE CASCADE
        )
        """)
        conn.commit()


def save_visit(
    visit_data: dict,
    image_bytes: bytes | None = None,
    audio_bytes: bytes | None = None,
    image_extension: str = ".jpg",
    audio_extension: str = ".mp3",
) -> int:
    """Save field visit details, write media files, and store portable relative paths."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO visits(program, location, date, stakeholders, notes, image_path, audio_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                visit_data["program"],
                visit_data["location"],
                visit_data["date"],
                visit_data["stakeholders"],
                visit_data["notes"],
                None,
                None,
            ),
        )
        visit_id = cursor.lastrowid

        image_path = None
        audio_path = None

        if image_bytes:
            filename = f"visit_{visit_id}{image_extension}"
            filepath = IMAGES_DIR / filename
            with open(filepath, "wb") as file:
                file.write(image_bytes)
            # Store clean relative paths for frontend accessibility
            image_path = f"uploads/images/{filename}"

        if audio_bytes:
            filename = f"visit_{visit_id}{audio_extension}"
            filepath = AUDIO_DIR / filename
            with open(filepath, "wb") as file:
                file.write(audio_bytes)
            audio_path = f"uploads/audio/{filename}"

        if image_path or audio_path:
            cursor.execute(
                "UPDATE visits SET image_path=?, audio_path=? WHERE id=?",
                (image_path, audio_path, visit_id),
            )
        conn.commit()
        return visit_id


def save_report(visit_id: int, report: dict) -> None:
    """Persist the structured AI report entries consistently using 'follow_ups'."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reports(
                visit_id, summary, key_findings, blockers, 
                community_sentiment, recommendations, follow_ups, issues_identified
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                visit_id,
                report["summary"],
                json.dumps(report["key_findings"], ensure_ascii=False),
                json.dumps(report["blockers"], ensure_ascii=False),
                report["community_sentiment"],
                json.dumps(report["recommendations"], ensure_ascii=False),
                json.dumps(report["follow_ups"], ensure_ascii=False),  # Fixed key matching
                json.dumps(report["issues_identified"], ensure_ascii=False),
            ),
        )
        conn.commit()


def get_dashboard_metrics() -> dict:
    """Calculates summary operational KPIs and extracts recent log structures with normalized issue tracking."""
    with get_connection() as conn:
        cursor = conn.cursor()

        total_visits = cursor.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
        programs = cursor.execute("SELECT COUNT(DISTINCT program) FROM visits").fetchone()[0]
        ai_reports = cursor.execute("SELECT COUNT(*) FROM reports").fetchone()[0]

        cursor.execute("SELECT issues_identified FROM reports")
        issue_counter = {}

        for row in cursor.fetchall():
            if not row["issues_identified"]:
                continue
            try:
                issues = json.loads(row["issues_identified"])
                for issue in issues:
                    issue_lower = issue.lower()
                    
                    # ---- Macro-Issue Normalization Mapping ----
                    if "irrigation" in issue_lower or "crop" in issue_lower:
                        category = "Irrigation problems"
                    elif "toilet" in issue_lower or "sanitation" in issue_lower or "hygiene" in issue_lower:
                        category = "Sanitation & Toilets"
                    elif "electricity" in issue_lower or "power" in issue_lower or "solar" in issue_lower:
                        category = "Power & Electricity Supply"
                    elif "tablet" in issue_lower or "digital" in issue_lower or "device" in issue_lower:
                        category = "Digital Learning Tools"
                    elif "absent" in issue_lower or "attendance" in issue_lower:
                        category = "Student Absenteeism"
                    else:
                        # Fallback to a cleaned capitalization of short sentences if no keyword hits
                        category = issue[:30] + "..." if len(issue) > 30 else issue
                    
                    issue_counter[category] = issue_counter.get(category, 0) + 1
            except json.JSONDecodeError:
                continue

        most_common_issue = max(issue_counter, key=issue_counter.get) if issue_counter else "No Issues Yet"

        cursor.execute('''
            SELECT v.id, v.program, v.location, v.date, r.summary 
            FROM visits v 
            LEFT JOIN reports r ON v.id = r.visit_id 
            ORDER BY v.created_at DESC LIMIT 5
        ''')
        recent_visits = [dict(row) for row in cursor.fetchall()]

        return {
            "total_visits": total_visits,
            "programs_covered": programs,
            "ai_reports": ai_reports,
            "most_common_issue": most_common_issue,
            "recent_visits": recent_visits
        }


def get_visit_history() -> list[dict[str, Any]]:
    """Returns all logs joined with fully decoded Python native list structures."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT v.id, v.program, v.location, v.date, v.stakeholders, v.notes, v.image_path, v.audio_path,
                   r.summary, r.key_findings, r.blockers, r.community_sentiment, r.recommendations, r.follow_ups, r.issues_identified
            FROM visits v
            LEFT JOIN reports r ON v.id = r.visit_id
            ORDER BY v.created_at DESC
            """
        )
        
        visits = [dict(row) for row in cursor.fetchall()]
        
        # Pre-decode JSON strings so UI reads lists directly
        for visit in visits:
            for field in ["key_findings", "blockers", "recommendations", "follow_ups", "issues_identified"]:
                if visit.get(field):
                    try:
                        visit[field] = json.loads(visit[field])
                    except json.JSONDecodeError:
                        visit[field] = []
                else:
                    visit[field] = []
        return visits