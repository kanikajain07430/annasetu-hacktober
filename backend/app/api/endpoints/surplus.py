from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
import datetime
import random
from app.db.session import get_db
from app.schemas.surplus import SurplusDonationCreate, SurplusDonationResponse, SurplusReserveRequest

router = APIRouter(prefix="/surplus", tags=["Surplus Food Redistribution Bridge"])

@router.post("/donations", response_model=SurplusDonationResponse, status_code=status.HTTP_201_CREATED)
def create_surplus_donation(payload: SurplusDonationCreate):
    conn = get_db()
    cursor = conn.cursor()

    surplus_id = f"SUR-{random.randint(100, 999)}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    cursor.execute("""
        INSERT INTO surplus_donations (
            id, donor_name, category, servings, pickup_window,
            location_zone, is_reserved, reserved_by_ngo, estimated_pickup_time, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, 0, NULL, NULL, ?)
    """, (
        surplus_id,
        payload.donorOrg,
        payload.category,
        payload.servings,
        payload.pickupWindowHours,
        payload.locationZone,
        now
    ))
    conn.commit()
    conn.close()

    return SurplusDonationResponse(
        id=surplus_id,
        donor=payload.donorOrg,
        food=payload.category,
        servings=payload.servings,
        window=payload.pickupWindowHours,
        location=payload.locationZone,
        isReserved=False,
        reservedByNGO=None,
        estimatedPickupTime=None,
        createdAt=now
    )

@router.get("/available", response_model=List[SurplusDonationResponse])
def get_available_surplus():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, donor_name, category, servings, pickup_window,
               location_zone, is_reserved, reserved_by_ngo, estimated_pickup_time, created_at
        FROM surplus_donations
        WHERE is_reserved = 0
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        SurplusDonationResponse(
            id=r["id"],
            donor=r["donor_name"],
            food=r["category"],
            servings=r["servings"],
            window=r["pickup_window"],
            location=r["location_zone"],
            isReserved=bool(r["is_reserved"]),
            reservedByNGO=r["reserved_by_ngo"],
            estimatedPickupTime=r["estimated_pickup_time"],
            createdAt=r["created_at"]
        )
        for r in rows
    ]

@router.post("/reserve/{surplus_id}")
def reserve_surplus(surplus_id: str, payload: Optional[SurplusReserveRequest] = None):
    ngo_id = payload.ngoId if payload else "Verified Local NGO Rescue Unit"
    pickup_time = payload.estimatedPickupTime if payload else "Within 45 Minutes"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, is_reserved, donor_name, category, servings FROM surplus_donations WHERE id = ?", (surplus_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Surplus batch '{surplus_id}' not found.")

    if row["is_reserved"]:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Surplus batch '{surplus_id}' is already reserved.")

    cursor.execute("""
        UPDATE surplus_donations
        SET is_reserved = 1, reserved_by_ngo = ?, estimated_pickup_time = ?
        WHERE id = ?
    """, (ngo_id, pickup_time, surplus_id))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "surplusId": surplus_id,
        "donor": row["donor_name"],
        "category": row["category"],
        "servings": row["servings"],
        "reservedBy": ngo_id,
        "estimatedPickupTime": pickup_time,
        "message": f"Pickup slot reserved for batch {surplus_id}. Redistribution pass issued."
    }
