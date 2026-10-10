from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Optional
import datetime
import random
from app.db.session import get_db
from app.schemas.procurement import FarmerListingCreate, ProcurementOrderResponse, OrderStatusUpdate

router = APIRouter(prefix="/procurement", tags=["Farmer Harvest Listings & Procurement"])

def format_currency_inr(amount: float) -> str:
    s = f"{int(amount)}"
    if len(s) <= 3:
        return f"₹{s}"
    last_three = s[-3:]
    remaining = s[:-3]
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
    parts.append(last_three)
    return "₹" + ",".join(parts)

@router.post("/listings", response_model=ProcurementOrderResponse, status_code=status.HTTP_201_CREATED)
def create_harvest_listing(payload: FarmerListingCreate):
    conn = get_db()
    cursor = conn.cursor()

    order_id = f"ORD-{random.randint(1000, 9999)}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    estimated_val = round(payload.quantityQuintals * payload.pricePerQuintal, 2)

    cursor.execute("""
        INSERT INTO procurement_orders (
            id, farmer_name, crop_type, quantity_quintals, price_per_quintal,
            estimated_value, district, status, whatsapp_alerts, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?, ?)
    """, (
        order_id,
        payload.farmerName,
        payload.cropType,
        payload.quantityQuintals,
        payload.pricePerQuintal,
        estimated_val,
        payload.location,
        1 if payload.whatsappAlerts else 0,
        now
    ))
    conn.commit()
    conn.close()

    return ProcurementOrderResponse(
        id=order_id,
        farmer=payload.farmerName,
        crop=payload.cropType,
        qty=f"{int(payload.quantityQuintals) if payload.quantityQuintals.is_integer() else payload.quantityQuintals} Qt",
        quantityQuintals=payload.quantityQuintals,
        pricePerQuintal=payload.pricePerQuintal,
        location=payload.location,
        value=format_currency_inr(estimated_val),
        numericValue=estimated_val,
        status="Pending",
        whatsappAlerts=payload.whatsappAlerts,
        createdAt=now
    )

@router.get("/orders", response_model=List[ProcurementOrderResponse])
def get_procurement_orders(
    status: Optional[str] = Query(None, description="Filter by status: Pending, Matched, In-Transit, Completed")
):
    conn = get_db()
    cursor = conn.cursor()
    query = """
        SELECT id, farmer_name, crop_type, quantity_quintals, price_per_quintal,
               estimated_value, district, status, whatsapp_alerts, created_at
        FROM procurement_orders
    """
    params = []
    if status and status.lower() != "all":
        query += " WHERE status = ?"
        params.append(status)

    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        qty_num = r["quantity_quintals"]
        qty_str = f"{int(qty_num) if qty_num.is_integer() else qty_num} Qt"
        result.append(ProcurementOrderResponse(
            id=r["id"],
            farmer=r["farmer_name"],
            crop=r["crop_type"],
            qty=qty_str,
            quantityQuintals=r["quantity_quintals"],
            pricePerQuintal=r["price_per_quintal"],
            location=r["district"],
            value=format_currency_inr(r["estimated_value"]),
            numericValue=r["estimated_value"],
            status=r["status"],
            whatsappAlerts=bool(r["whatsapp_alerts"]),
            createdAt=r["created_at"]
        ))
    return result

@router.get("/orders/{order_id}", response_model=ProcurementOrderResponse)
def get_order_by_id(order_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, farmer_name, crop_type, quantity_quintals, price_per_quintal,
               estimated_value, district, status, whatsapp_alerts, created_at
        FROM procurement_orders WHERE id = ?
    """, (order_id,))
    r = cursor.fetchone()
    conn.close()

    if not r:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")

    qty_num = r["quantity_quintals"]
    return ProcurementOrderResponse(
        id=r["id"],
        farmer=r["farmer_name"],
        crop=r["crop_type"],
        qty=f"{int(qty_num) if qty_num.is_integer() else qty_num} Qt",
        quantityQuintals=r["quantity_quintals"],
        pricePerQuintal=r["price_per_quintal"],
        location=r["district"],
        value=format_currency_inr(r["estimated_value"]),
        numericValue=r["estimated_value"],
        status=r["status"],
        whatsappAlerts=bool(r["whatsapp_alerts"]),
        createdAt=r["created_at"]
    )

@router.patch("/orders/{order_id}/status")
def update_order_status(order_id: str, payload: OrderStatusUpdate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM procurement_orders WHERE id = ?", (order_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")

    cursor.execute("UPDATE procurement_orders SET status = ? WHERE id = ?", (payload.status, order_id))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "orderId": order_id,
        "newStatus": payload.status,
        "message": f"Order {order_id} status updated to {payload.status}."
    }
