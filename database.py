"""SQLite database with JSON storage for sections."""
import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from models import SEOOutput, SectionedContent, PackageInput

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo_pipeline.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seo_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_name TEXT NOT NULL,
            package_data TEXT NOT NULL,
            primary_keyword TEXT,
            title_tag TEXT,
            meta_description TEXT,
            sections TEXT NOT NULL,
            qa_score INTEGER DEFAULT 0,
            qa_flags TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_status ON seo_outputs(status)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_package_name ON seo_outputs(package_name)
    """)
    conn.commit()
    conn.close()


def _sections_to_dict(sections: SectionedContent) -> dict:
    return sections.model_dump()


def _dict_to_sections(data: dict) -> SectionedContent:
    return SectionedContent(**data)


def save_output(output: SEOOutput) -> int:
    conn = get_conn()
    now = output.created_at or output.updated_at or __import__("datetime").datetime.now().isoformat()
    cursor = conn.execute(
        """INSERT INTO seo_outputs 
           (package_name, package_data, primary_keyword, title_tag, meta_description, 
            sections, qa_score, qa_flags, status, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            output.package_input.name,
            json.dumps(output.package_input.model_dump()),
            output.primary_keyword,
            output.title_tag,
            output.meta_description,
            json.dumps(_sections_to_dict(output.sections)),
            output.qa_score,
            json.dumps(output.qa_flags),
            output.status,
            now,
            now,
        ),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def update_output(output_id: int, output: SEOOutput) -> bool:
    conn = get_conn()
    now = __import__("datetime").datetime.now().isoformat()
    conn.execute(
        """UPDATE seo_outputs SET
            package_name = ?,
            package_data = ?,
            primary_keyword = ?,
            title_tag = ?,
            meta_description = ?,
            sections = ?,
            qa_score = ?,
            qa_flags = ?,
            status = ?,
            updated_at = ?
           WHERE id = ?""",
        (
            output.package_input.name,
            json.dumps(output.package_input.model_dump()),
            output.primary_keyword,
            output.title_tag,
            output.meta_description,
            json.dumps(_sections_to_dict(output.sections)),
            output.qa_score,
            json.dumps(output.qa_flags),
            output.status,
            now,
            output_id,
        ),
    )
    conn.commit()
    updated = conn.total_changes > 0
    conn.close()
    return updated


def get_output(output_id: int) -> Optional[SEOOutput]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM seo_outputs WHERE id = ?", (output_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_output(row)


def list_outputs(status: Optional[str] = None, search: Optional[str] = None) -> List[SEOOutput]:
    conn = get_conn()
    query = "SELECT * FROM seo_outputs WHERE 1=1"
    params = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if search:
        query += " AND (package_name LIKE ? OR primary_keyword LIKE ? OR title_tag LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    query += " ORDER BY created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [_row_to_output(row) for row in rows]


def bulk_update_status(ids: List[int], status: str) -> int:
    if not ids:
        return 0
    conn = get_conn()
    placeholders = ",".join("?" * len(ids))
    conn.execute(f"UPDATE seo_outputs SET status = ? WHERE id IN ({placeholders})", (status, *ids))
    conn.commit()
    count = conn.total_changes
    conn.close()
    return count


def delete_output(output_id: int) -> bool:
    conn = get_conn()
    conn.execute("DELETE FROM seo_outputs WHERE id = ?", (output_id,))
    conn.commit()
    deleted = conn.total_changes > 0
    conn.close()
    return deleted


def clear_all_outputs() -> int:
    conn = get_conn()
    conn.execute("DELETE FROM seo_outputs")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='seo_outputs'")
    conn.commit()
    count = conn.total_changes
    conn.close()
    return count


def get_stats() -> Dict[str, Any]:
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM seo_outputs").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status = 'pending'").fetchone()[0]
    approved = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status = 'approved'").fetchone()[0]
    rejected = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status = 'rejected'").fetchone()[0]
    avg_score = conn.execute("SELECT AVG(qa_score) FROM seo_outputs").fetchone()[0] or 0
    conn.close()
    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "average_qa_score": round(avg_score, 1),
    }


def _row_to_output(row: sqlite3.Row) -> SEOOutput:
    return SEOOutput(
        id=row["id"],
        package_input=PackageInput(**json.loads(row["package_data"])),
        primary_keyword=row["primary_keyword"] or "",
        title_tag=row["title_tag"] or "",
        meta_description=row["meta_description"] or "",
        sections=_dict_to_sections(json.loads(row["sections"])),
        qa_score=row["qa_score"] or 0,
        qa_flags=json.loads(row["qa_flags"]) if row["qa_flags"] else [],
        status=row["status"] or "pending",
        created_at=row["created_at"] or "",
        updated_at=row["updated_at"] or "",
    )
