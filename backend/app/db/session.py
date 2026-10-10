import sqlite3
import datetime
import hashlib
from app.core.config import settings

def get_db():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('farmer', 'vendor', 'ngo', 'admin')),
        full_name TEXT NOT NULL,
        phone TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Mandi Rates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mandi_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        district TEXT NOT NULL,
        msp REAL NOT NULL,
        market_rate REAL NOT NULL,
        trend TEXT NOT NULL CHECK(trend IN ('up', 'down')),
        updated_at TEXT NOT NULL
    )
    """)

    # Procurement Orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS procurement_orders (
        id TEXT PRIMARY KEY,
        farmer_name TEXT NOT NULL,
        crop_type TEXT NOT NULL,
        quantity_quintals REAL NOT NULL,
        price_per_quintal REAL NOT NULL,
        estimated_value REAL NOT NULL,
        district TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('Pending', 'Matched', 'In-Transit', 'Completed')),
        whatsapp_alerts INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    )
    """)

    # Surplus Donations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS surplus_donations (
        id TEXT PRIMARY KEY,
        donor_name TEXT NOT NULL,
        category TEXT NOT NULL,
        servings INTEGER NOT NULL,
        pickup_window TEXT NOT NULL,
        location_zone TEXT NOT NULL,
        is_reserved INTEGER NOT NULL DEFAULT 0,
        reserved_by_ngo TEXT,
        estimated_pickup_time TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Transit Passes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transit_passes (
        id TEXT PRIMARY KEY,
        order_id TEXT,
        commodity TEXT NOT NULL,
        volume TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        green_corridor_clearance TEXT NOT NULL DEFAULT 'APPROVED (Fast-Track)',
        qr_hash TEXT NOT NULL,
        vehicle_type TEXT NOT NULL DEFAULT 'Electric EV-Truck 4.5T',
        carbon_reduction_kg REAL NOT NULL DEFAULT 142.0,
        created_at TEXT NOT NULL
    )
    """)

    # Grievances
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grievances (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        issue_details TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open', 'In-Review', 'Resolved')),
        resolution_notes TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()

    # Seed Initial Demo Data if empty
    seed_demo_data(cursor, conn)
    conn.close()

def seed_demo_data(cursor, conn):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    cursor.execute("SELECT COUNT(*) FROM mandi_rates")
    if cursor.fetchone()[0] == 0:
        initial_mandi = [
            ("Wheat (Lokwan)", "Karnal, Haryana", 2275.0, 2380.0, "up", now),
            ("Paddy Rice (Basmati)", "Amritsar, Punjab", 2183.0, 3450.0, "up", now),
            ("Red Onion", "Nashik, Maharashtra", 1800.0, 2100.0, "up", now),
            ("Yellow Soybean", "Indore, Madhya Pradesh", 4600.0, 4450.0, "down", now),
            ("Cotton (Long Staple)", "Rajkot, Gujarat", 7020.0, 7250.0, "up", now),
            ("Maize (Hybrid)", "Davanagere, Karnataka", 2090.0, 2150.0, "up", now)
        ]
        cursor.executemany("""
            INSERT INTO mandi_rates (crop, district, msp, market_rate, trend, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, initial_mandi)

    cursor.execute("SELECT COUNT(*) FROM procurement_orders")
    if cursor.fetchone()[0] == 0:
        initial_orders = [
            ("ORD-8821", "Ramesh Kumar", "Wheat (Lokwan)", 120.0, 2380.0, 285600.0, "Karnal, Haryana", "Matched", 1, now),
            ("ORD-8822", "Sukhwinder Singh", "Paddy Rice (Basmati)", 85.0, 3450.0, 293250.0, "Amritsar, Punjab", "Pending", 1, now),
            ("ORD-8823", "Anil Deshmukh", "Soybean (Yellow)", 50.0, 4450.0, 222500.0, "Indore, Madhya Pradesh", "In-Transit", 1, now)
        ]
        cursor.executemany("""
            INSERT INTO procurement_orders (id, farmer_name, crop_type, quantity_quintals, price_per_quintal, estimated_value, district, status, whatsapp_alerts, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_orders)

    cursor.execute("SELECT COUNT(*) FROM surplus_donations")
    if cursor.fetchone()[0] == 0:
        initial_surplus = [
            ("SUR-101", "Royal Palace Banquet", "Cooked Meals (Veg)", 180, "2 Hours Left", "North Sector 4", 0, None, None, now),
            ("SUR-102", "Apex Corporate Canteen", "Packaged / Dry Rations", 75, "4 Hours Left", "Tech Park Hub", 0, None, None, now),
            ("SUR-103", "Metro Fresh Supermarket", "Fresh Produce / Fruits", 200, "5 Hours Left", "Central District", 0, None, None, now)
        ]
        cursor.executemany("""
            INSERT INTO surplus_donations (id, donor_name, category, servings, pickup_window, location_zone, is_reserved, reserved_by_ngo, estimated_pickup_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_surplus)

    cursor.execute("SELECT COUNT(*) FROM transit_passes")
    if cursor.fetchone()[0] == 0:
        initial_pass = (
            "AS-PASS-2026-9042",
            "ORD-8821",
            "Wheat Lokwan (120 Quintals)",
            "120 Qt",
            "Karnal Mandi",
            "Delhi Central Warehouse",
            "APPROVED (Fast-Track)",
            "8f9b2a1c0d3e4f5a",
            "Electric EV-Truck 4.5T",
            142.0,
            now
        )
        cursor.execute("""
            INSERT INTO transit_passes (id, order_id, commodity, volume, origin, destination, green_corridor_clearance, qr_hash, vehicle_type, carbon_reduction_kg, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_pass)

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        initial_users = [
            ("farmer_ramesh", "ramesh@annasetu.in", hash_pw("Farmer@123"), "farmer", "Ramesh Kumar", "+91 98765 43210", now),
            ("vendor_itc", "procurement@itc.in", hash_pw("Vendor@123"), "vendor", "ITC Agri Procurement", "+91 98765 11223", now),
            ("ngo_roti_bank", "contact@rotibank.org", hash_pw("Ngo@123"), "ngo", "Feeding Hope Foundation", "+91 98765 99887", now),
            ("admin_officer", "admin@annasetu.gov.in", hash_pw("Admin@123"), "admin", "District Ag Officer Sharma", "+91 98765 00000", now)
        ]
        cursor.executemany("""
            INSERT INTO users (username, email, password_hash, role, full_name, phone, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, initial_users)

    conn.commit()
