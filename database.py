"""SQLite database with JSON storage for sections."""
import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from models import SEOOutput, SectionedContent, PackageInput

import time
import random

def get_db_path() -> str:
    env_path = os.environ.get("SQLITE_DB_PATH") or os.environ.get("DATABASE_PATH")
    if env_path:
        return env_path
    if os.path.exists("/data") and os.access("/data", os.W_OK):
        return "/data/seo_pipeline.db"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo_pipeline.db")

DB_PATH = get_db_path()


def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn



def _execute_with_retry(func, max_attempts=5):
    """Execute a database operation with exponential backoff on lock contention."""
    last_err = None
    for attempt in range(max_attempts):
        try:
            return func()
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() or "busy" in str(e).lower():
                last_err = e
                time.sleep(0.05 * (2 ** attempt) + random.uniform(0.01, 0.05))
            else:
                raise e
    raise last_err or sqlite3.OperationalError("Database busy timeout after retries")


def init_db():
    def _op():
        conn = get_conn()
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                row_id INTEGER,
                event_type TEXT NOT NULL,
                actor TEXT DEFAULT 'system',
                model_used TEXT,
                details TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_audit_row_id ON audit_trail(row_id)
        """)
        conn.commit()
        conn.close()
    _execute_with_retry(_op)



def _sections_to_dict(sections: SectionedContent) -> dict:
    return sections.model_dump()


def _dict_to_sections(data: dict) -> SectionedContent:
    return SectionedContent(**data)


def save_output(output: SEOOutput) -> int:
    def _op():
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
    return _execute_with_retry(_op)


def update_output(output_id: int, output: SEOOutput) -> bool:
    def _op():
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
    return _execute_with_retry(_op)


def get_output(output_id: int) -> Optional[SEOOutput]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM seo_outputs WHERE id = ?", (output_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_output(row)


def list_outputs(
    status: Optional[str] = None, 
    search: Optional[str] = None, 
    limit: Optional[int] = None, 
    offset: Optional[int] = None
) -> List[SEOOutput]:
    conn = get_conn()
    query = "SELECT * FROM seo_outputs WHERE 1=1"
    params = []
    if status and str(status).strip().lower() != "all":
        query += " AND status = ?"
        params.append(status)
    if search:
        query += " AND (package_name LIKE ? OR primary_keyword LIKE ? OR title_tag LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    query += " ORDER BY id DESC"
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)
        if offset is not None:
            query += " OFFSET ?"
            params.append(offset)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [_row_to_output(row) for row in rows]



def bulk_update_status(ids: List[int], status: str) -> int:
    if not ids:
        return 0
    def _op():
        conn = get_conn()
        placeholders = ",".join("?" * len(ids))
        conn.execute(f"UPDATE seo_outputs SET status = ? WHERE id IN ({placeholders})", (status, *ids))
        conn.commit()
        count = conn.total_changes
        conn.close()
        return count
    return _execute_with_retry(_op)


def delete_output(output_id: int) -> bool:
    def _op():
        conn = get_conn()
        conn.execute("DELETE FROM seo_outputs WHERE id = ?", (output_id,))
        conn.commit()
        deleted = conn.total_changes > 0
        conn.close()
        return deleted
    return _execute_with_retry(_op)


def clear_all_outputs() -> int:
    def _op():
        conn = get_conn()
        conn.execute("DELETE FROM seo_outputs")
        conn.execute("DELETE FROM sqlite_sequence WHERE name='seo_outputs'")
        conn.commit()
        count = conn.total_changes
        conn.close()
        return count
    return _execute_with_retry(_op)


def get_stats() -> Dict[str, Any]:
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM seo_outputs").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status = 'pending'").fetchone()[0]
    approved = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status IN ('approved', 'approved_candidate')").fetchone()[0]
    rejected = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status = 'rejected'").fetchone()[0]
    flagged = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status = 'flagged_review'").fetchone()[0]
    approved_candidates = conn.execute("SELECT COUNT(*) FROM seo_outputs WHERE status = 'approved_candidate'").fetchone()[0]
    avg_score = conn.execute("SELECT AVG(qa_score) FROM seo_outputs").fetchone()[0] or 0
    conn.close()
    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "flagged_review": flagged,
        "approved_candidate": approved_candidates,
        "average_qa_score": round(avg_score, 1),
    }


def log_audit_event(row_id: int, event_type: str, actor: str = "system", model_used: Optional[str] = None, details: Optional[str] = None) -> int:
    """Log an audit event for enterprise traceability and compliance."""
    def _op():
        conn = get_conn()
        now = __import__("datetime").datetime.now().isoformat()
        cur = conn.execute(
            """INSERT INTO audit_trail (row_id, event_type, actor, model_used, details, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (row_id, event_type, actor, model_used, details, now)
        )
        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id
    return _execute_with_retry(_op)


def get_audit_trail(row_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve audit history for a package or global pipeline activity."""
    conn = get_conn()
    if row_id is not None:
        rows = conn.execute("SELECT * FROM audit_trail WHERE row_id = ? ORDER BY id DESC LIMIT ?", (row_id, limit)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM audit_trail ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]




def _row_to_output(row: sqlite3.Row) -> SEOOutput:
    pkg_input = PackageInput(**json.loads(row["package_data"]))
    sections = _dict_to_sections(json.loads(row["sections"]))
    title_tag = row["title_tag"] or ""
    meta_desc = row["meta_description"] or ""
    
    # Ground-truth fact verification & schema metrics
    from fact_checker import verify_ground_truth
    from schema_generator import generate_json_ld
    from linter import run_seo_linter
    
    gt = verify_ground_truth(pkg_input.model_dump(), sections.model_dump(), title_tag, meta_desc)
    
    prelim = {
        "package_input": pkg_input.model_dump(),
        "title_tag": title_tag,
        "meta_description": meta_desc,
        "sections": sections.model_dump()
    }
    json_ld = generate_json_ld(prelim)
    linter_metrics = run_seo_linter(title_tag, meta_desc, row["primary_keyword"] or "", sections.model_dump(), json_ld_present=True)
    
    return SEOOutput(
        id=row["id"],
        package_input=pkg_input,
        primary_keyword=row["primary_keyword"] or "",
        title_tag=title_tag,
        meta_description=meta_desc,
        sections=sections,
        qa_score=row["qa_score"] or 0,
        qa_flags=json.loads(row["qa_flags"]) if row["qa_flags"] else [],
        factual_integrity_score=gt.get("factual_integrity_score", 100),
        ground_truth_report=gt,
        json_ld_schema=json_ld,
        linter_metrics=linter_metrics,
        status=row["status"] or "pending",
        created_at=row["created_at"] or "",
        updated_at=row["updated_at"] or "",
    )

