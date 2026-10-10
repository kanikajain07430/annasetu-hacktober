from fastapi import APIRouter, HTTPException, status
import hashlib
import datetime
import random
from app.db.session import get_db
from app.schemas.logistics import SmartMatchRequest, SmartMatchResponse, TransitPassResponse

router = APIRouter(prefix="/logistics", tags=["Logistics & Smart Route Engine"])

WAREHOUSE_HUBS = [
    {"name": "Delhi Central Warehouse Depot", "district_match": ["karnal", "haryana", "punjab", "delhi"], "distance_base": 42.0},
    {"name": "Mumbai Vashi Agricultural APMC Hub", "district_match": ["nashik", "maharashtra", "pune"], "distance_base": 158.0},
    {"name": "Central Indore Food Logistics Terminal", "district_match": ["indore", "madhya pradesh", "bhopal"], "distance_base": 35.0},
    {"name": "Bengaluru Rural Ag-Logistics Node", "district_match": ["davanagere", "karnataka", "bengaluru"], "distance_base": 240.0}
]

def choose_destination_hub(origin_district: str):
    origin_lower = origin_district.lower()
    for hub in WAREHOUSE_HUBS:
        if any(match in origin_lower for match in hub["district_match"]):
            return hub["name"], hub["distance_base"]
    return "Delhi Central Warehouse Depot", 65.0

@router.post("/smart-match", response_model=SmartMatchResponse)
def execute_smart_match(payload: SmartMatchRequest):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db()
    cursor = conn.cursor()

    order_id = f"ORD-{random.randint(8000, 8999)}"
    pass_id = f"AS-PASS-2026-{random.randint(9000, 9999)}"
    route_code = f"AG-{random.randint(9000, 9999)}"

    destination_hub, base_distance = choose_destination_hub(payload.originDistrict)
    distance_km = round(base_distance + random.uniform(2.0, 15.0), 1)

    hours = int(distance_km / 45)
    minutes = int((distance_km % 45) * 1.3)
    duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

    if payload.quantity > 80:
        vehicle_type = "Heavy EV-Freight Carrier 10T"
        carbon_saved = round(distance_km * 3.4, 1)
    else:
        vehicle_type = "Electric EV-Truck 4.5T"
        carbon_saved = round(distance_km * 2.1, 1)

    hash_payload = f"{pass_id}:{payload.cropType}:{payload.quantity}:{payload.originDistrict}:{destination_hub}:{now}"
    qr_hash = hashlib.sha256(hash_payload.encode()).hexdigest()[:16]

    commodity_str = f"{payload.cropType} ({payload.quantity} Quintals)"
    cursor.execute("""
        INSERT INTO transit_passes (
            id, order_id, commodity, volume, origin, destination,
            green_corridor_clearance, qr_hash, vehicle_type, carbon_reduction_kg, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, 'APPROVED (Fast-Track)', ?, ?, ?, ?)
    """, (
        pass_id,
        order_id,
        commodity_str,
        f"{payload.quantity} Qt",
        f"{payload.originDistrict} Mandi",
        destination_hub,
        qr_hash,
        vehicle_type,
        carbon_saved,
        now
    ))
    conn.commit()
    conn.close()

    logs = [
        "[SYS] Engine Execution Started...",
        f"[1/3] Scanning cluster harvest ledgers in {payload.originDistrict}...",
        f"[2/3] Matched {payload.quantity} Quintals {payload.cropType} to {destination_hub}.",
        f"[3/3] Route optimized via Green EV Corridor ({route_code}) - {distance_km} km ({duration_str}).",
        f"✓ Match Finalized: Order #{order_id} | Pass #{pass_id}"
    ]

    return SmartMatchResponse(
        orderId=order_id,
        matchFound=True,
        clusterOrigin=payload.originDistrict,
        destinationHub=destination_hub,
        distanceKm=distance_km,
        estimatedDuration=duration_str,
        optimizedVehicle=vehicle_type,
        carbonReductionKg=carbon_saved,
        transitPassId=pass_id,
        routeCode=route_code,
        qrHash=qr_hash,
        logs=logs
    )

@router.get("/pass/{order_or_pass_id}", response_model=TransitPassResponse)
def get_transit_pass(order_or_pass_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, order_id, commodity, volume, origin, destination,
               green_corridor_clearance, qr_hash, vehicle_type, carbon_reduction_kg, created_at
        FROM transit_passes
        WHERE id = ? OR order_id = ?
        LIMIT 1
    """, (order_or_pass_id, order_or_pass_id))
    row = cursor.fetchone()

    if not row:
        cursor.execute("SELECT id, farmer_name, crop_type, quantity_quintals, district FROM procurement_orders WHERE id = ?", (order_or_pass_id,))
        order = cursor.fetchone()
        if order:
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            pass_id = f"AS-PASS-2026-{random.randint(9000, 9999)}"
            commodity_str = f"{order['crop_type']} ({order['quantity_quintals']} Quintals)"
            origin_str = f"{order['district']} Mandi"
            dest_str = "Delhi Central Warehouse"
            hash_payload = f"{pass_id}:{order['id']}:{now}"
            qr_hash = hashlib.sha256(hash_payload.encode()).hexdigest()[:16]

            cursor.execute("""
                INSERT INTO transit_passes (
                    id, order_id, commodity, volume, origin, destination,
                    green_corridor_clearance, qr_hash, vehicle_type, carbon_reduction_kg, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'APPROVED (Fast-Track)', ?, 'Electric EV-Truck 4.5T', 142.0, ?)
            """, (pass_id, order["id"], commodity_str, f"{order['quantity_quintals']} Qt", origin_str, dest_str, qr_hash, now))
            conn.commit()

            cursor.execute("SELECT * FROM transit_passes WHERE id = ?", (pass_id,))
            row = cursor.fetchone()
        else:
            conn.close()
            raise HTTPException(status_code=404, detail=f"No transit pass found for '{order_or_pass_id}'.")

    conn.close()

    return TransitPassResponse(
        passId=row["id"],
        orderId=row["order_id"],
        commodity=row["commodity"],
        volume=row["volume"],
        origin=row["origin"],
        destination=row["destination"],
        greenCorridorClearance=row["green_corridor_clearance"],
        qrHash=row["qr_hash"],
        vehicleType=row["vehicle_type"],
        carbonReductionKg=row["carbon_reduction_kg"],
        createdAt=row["created_at"]
    )
