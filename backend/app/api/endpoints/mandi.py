from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Optional
import datetime
from app.db.session import get_db
from app.schemas.mandi import MandiRateResponse, MandiRateCreate

router = APIRouter(prefix="/mandi", tags=["Mandi & Market Prices"])

@router.get("/rates", response_model=List[MandiRateResponse])
def get_mandi_rates(
    crop: Optional[str] = Query(None, description="Filter by crop name"),
    district: Optional[str] = Query(None, description="Filter by district/mandi name")
):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT id, crop, district, msp, market_rate, trend, updated_at FROM mandi_rates WHERE 1=1"
    params = []

    if crop:
        query += " AND LOWER(crop) LIKE ?"
        params.append(f"%{crop.lower()}%")
    if district:
        query += " AND LOWER(district) LIKE ?"
        params.append(f"%{district.lower()}%")

    query += " ORDER BY id ASC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        MandiRateResponse(
            id=r["id"],
            crop=r["crop"],
            district=r["district"],
            msp=r["msp"],
            marketRate=r["market_rate"],
            trend=r["trend"],
            updated_at=r["updated_at"]
        )
        for r in rows
    ]

@router.post("/rates", response_model=MandiRateResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_rate(payload: MandiRateCreate):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM mandi_rates WHERE LOWER(crop) = LOWER(?) AND LOWER(district) = LOWER(?)",
        (payload.crop, payload.district)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE mandi_rates
            SET msp = ?, market_rate = ?, trend = ?, updated_at = ?
            WHERE id = ?
        """, (payload.msp, payload.marketRate, payload.trend, now, existing["id"]))
        rate_id = existing["id"]
    else:
        cursor.execute("""
            INSERT INTO mandi_rates (crop, district, msp, market_rate, trend, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (payload.crop, payload.district, payload.msp, payload.marketRate, payload.trend, now))
        rate_id = cursor.lastrowid

    conn.commit()
    cursor.execute("SELECT id, crop, district, msp, market_rate, trend, updated_at FROM mandi_rates WHERE id = ?", (rate_id,))
    row = cursor.fetchone()
    conn.close()

    return MandiRateResponse(
        id=row["id"],
        crop=row["crop"],
        district=row["district"],
        msp=row["msp"],
        marketRate=row["market_rate"],
        trend=row["trend"],
        updated_at=row["updated_at"]
    )

@router.get("/benchmark/{crop}")
def get_crop_benchmark(crop: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT crop, AVG(msp) as avg_msp, AVG(market_rate) as avg_market_rate, COUNT(*) as mandis_reporting
        FROM mandi_rates
        WHERE LOWER(crop) LIKE ?
        GROUP BY crop
    """, (f"%{crop.lower()}%",))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"No mandi rate benchmarks found for crop '{crop}'.")

    avg_msp = row["avg_msp"]
    avg_market = row["avg_market_rate"]
    diff_percent = round(((avg_market - avg_msp) / avg_msp) * 100, 2)

    return {
        "crop": row["crop"],
        "mandisReporting": row["mandis_reporting"],
        "averageMSP": round(avg_msp, 2),
        "averageMarketRate": round(avg_market, 2),
        "marginAboveMSPPercent": diff_percent,
        "isFairPriced": diff_percent >= 0
    }
