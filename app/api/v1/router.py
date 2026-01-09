from fastapi import APIRouter
from app.api.v1.endpoints import auth, patients, visites, risques, csu, admin
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(visites.router, prefix="/visites", tags=["visites"])
api_router.include_router(risques.router, prefix="/risques", tags=["risques"])
api_router.include_router(csu.router, prefix="/csu", tags=["csu"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
