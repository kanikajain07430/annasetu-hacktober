from fastapi import APIRouter, HTTPException, status
from typing import List
import datetime
import random
from app.db.session import get_db
from app.schemas.support import GrievanceCreate, GrievanceResponse

router = APIRouter(prefix="/support", tags=["Support & Grievances"])

@router.post("/grievance", response_model=GrievanceResponse, status_code=status.HTTP_201_CREATED)
def submit_grievance(payload: GrievanceCreate):
    conn = get_db()
    cursor = conn.cursor()

    ticket_id = f"GRV-{random.randint(1000, 9999)}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    cursor.execute("""
        INSERT INTO grievances (id, name, category, issue_details, status, resolution_notes, created_at)
        VALUES (?, ?, ?, ?, 'Open', NULL, ?)
    """, (ticket_id, payload.name, payload.category, payload.issueDetails, now))
    conn.commit()
    conn.close()

    return GrievanceResponse(
        ticketId=ticket_id,
        name=payload.name,
        category=payload.category,
        issueDetails=payload.issueDetails,
        status="Open",
        resolutionNotes=None,
        createdAt=now
    )

@router.get("/grievances", response_model=List[GrievanceResponse])
def list_grievances():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, issue_details, status, resolution_notes, created_at FROM grievances ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        GrievanceResponse(
            ticketId=r["id"],
            name=r["name"],
            category=r["category"],
            issueDetails=r["issue_details"],
            status=r["status"],
            resolutionNotes=r["resolution_notes"],
            createdAt=r["created_at"]
        )
        for r in rows
    ]

@router.patch("/grievances/{ticket_id}/resolve")
def resolve_grievance(ticket_id: str, resolution_notes: str = "Resolved by District Agriculture Officer"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM grievances WHERE id = ?", (ticket_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Grievance ticket '{ticket_id}' not found.")

    cursor.execute("UPDATE grievances SET status = 'Resolved', resolution_notes = ? WHERE id = ?", (resolution_notes, ticket_id))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "ticketId": ticket_id,
        "status": "Resolved",
        "notes": resolution_notes
    }
