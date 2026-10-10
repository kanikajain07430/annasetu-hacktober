from fastapi import APIRouter, HTTPException, status, Depends
import datetime
from app.db.session import get_db, hash_pw
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication & User Management"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (payload.username, payload.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email is already registered.")

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, role, full_name, phone, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        payload.username,
        payload.email,
        hash_pw(payload.password),
        payload.role,
        payload.fullName,
        payload.phone,
        now
    ))
    conn.commit()
    conn.close()

    token = create_access_token({"sub": payload.username, "role": payload.role})
    return TokenResponse(
        accessToken=token,
        tokenType="bearer",
        role=payload.role,
        username=payload.username,
        fullName=payload.fullName
    )

@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLogin):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, email, password_hash, role, full_name
        FROM users
        WHERE username = ? OR email = ?
    """, (payload.usernameOrEmail, payload.usernameOrEmail))
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please check your username/email and password."
        )

    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return TokenResponse(
        accessToken=token,
        tokenType="bearer",
        role=user["role"],
        username=user["username"],
        fullName=user["full_name"]
    )

@router.get("/me")
def get_user_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user["role"],
        "fullName": current_user["full_name"],
        "phone": current_user.get("phone")
    }
