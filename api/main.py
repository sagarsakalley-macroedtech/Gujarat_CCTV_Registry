from fastapi import FastAPI
from api.routes import gis

from api.routes import (
    cameras,
    departments,
    districts,
    dashboard,
    health
)


app = FastAPI(
    title="Gujarat CCTV Registry API",
    description=(
        "REST API for Gujarat Government "
        "Centralised CCTV Registry & GIS Mapping"
    ),
    version="1.0.0"
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    health.router,
    prefix="/api/health",
    tags=["Health"]
)

app.include_router(
    cameras.router,
    prefix="/api/cameras",
    tags=["Cameras"]
)

app.include_router(
    departments.router,
    prefix="/api/departments",
    tags=["Departments"]
)

app.include_router(
    districts.router,
    prefix="/api/districts",
    tags=["Districts"]
)

app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


app.include_router(
    gis.router,
    prefix="/api"
)

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "application": "Gujarat CCTV Registry",
        "model": "Model 01",
        "status": "running",
        "version": "1.0.0"
    }