from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.mandi import router as mandi_router
from app.api.endpoints.procurement import router as procurement_router
from app.api.endpoints.surplus import router as surplus_router
from app.api.endpoints.logistics import router as logistics_router
from app.api.endpoints.support import router as support_router
from app.api.endpoints.analytics import router as analytics_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(mandi_router)
api_router.include_router(procurement_router)
api_router.include_router(surplus_router)
api_router.include_router(logistics_router)
api_router.include_router(support_router)
api_router.include_router(analytics_router)
