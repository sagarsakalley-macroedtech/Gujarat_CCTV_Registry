# =========================================================
# GUJARAT CCTV REGISTRY
# MODEL 01
# Centralised CCTV Registry & GIS Mapping
# =========================================================

import streamlit as st
from sqlalchemy import func

# =========================================================
# DATABASE IMPORTS
# =========================================================

from database.database import engine, SessionLocal
from database.models import (
    Base,
    Camera,
    Department,
    District,
)

# =========================================================
# FRONTEND MODULES
# =========================================================

from frontend.map_view import show_map
from frontend.camera_onboarding import show_onboarding


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Gujarat CCTV Registry",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

try:
    # Create tables using the SAME engine as the application
    Base.metadata.create_all(bind=engine)

except Exception as e:
    st.error(f"Database initialization failed: {e}")
    st.stop()


# =========================================================
# DATABASE SEEDING
# =========================================================

try:

    db = SessionLocal()

    department_count = (
        db.query(func.count(Department.id)).scalar() or 0
    )

    district_count = (
        db.query(func.count(District.id)).scalar() or 0
    )

    camera_count = (
        db.query(func.count(Camera.id)).scalar() or 0
    )

    db.close()

    # Seed only when database is completely empty
    if (
        department_count == 0
        and district_count == 0
        and camera_count == 0
    ):

        from database.seed_data import seed_database

        seed_database()

except Exception as e:
    st.error(f"Database seeding failed: {e}")
    st.exception(e)
    st.stop()


# =========================================================
# GET DATABASE COUNTS
# =========================================================

try:

    db = SessionLocal()

    total_cameras = (
        db.query(func.count(Camera.id)).scalar() or 0
    )

    total_departments = (
        db.query(func.count(Department.id)).scalar() or 0
    )

    total_districts = (
        db.query(func.count(District.id)).scalar() or 0
    )

    # Active cameras
    try:
        active_cameras = (
            db.query(func.count(Camera.id))
            .filter(Camera.status == "Active")
            .scalar()
            or 0
        )
    except Exception:
        active_cameras = total_cameras

    offline_cameras = max(
        total_cameras - active_cameras,
        0
    )

    db.close()

except Exception as e:

    st.error(f"Database query failed: {e}")
    st.exception(e)
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Gujarat CCTV Registry")

st.sidebar.caption(
    "Centralised CCTV Asset & GIS Registry"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "CCTV Registry",
        "GIS Map",
        "Camera Onboarding",
        "Camera Details",
    ],
)

st.sidebar.divider()

st.sidebar.info(
    "Model 01\n\n"
    "Centralised CCTV Registry & GIS Mapping"
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("Gujarat CCTV Registry")

    st.subheader(
        "Centralised Government CCTV Asset Management Platform"
    )

    st.divider()

    # -----------------------------------------------------
    # TOP METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Cameras",
            total_cameras
        )

    with col2:
        st.metric(
            "Active Cameras",
            active_cameras
        )

    with col3:
        st.metric(
            "Offline Cameras",
            offline_cameras
        )

    with col4:
        st.metric(
            "Departments",
            total_departments
        )

    st.divider()

    # -----------------------------------------------------
    # INFRASTRUCTURE OVERVIEW
    # -----------------------------------------------------

    st.subheader("Infrastructure Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Districts Covered",
            total_districts
        )

    with col2:
        st.metric(
            "Under Maintenance",
            0
        )

    with col3:

        if total_cameras > 0:
            operational_rate = (
                active_cameras / total_cameras
            ) * 100
        else:
            operational_rate = 0

        st.metric(
            "Operational Rate",
            f"{operational_rate:.1f}%"
        )

    st.divider()

    # -----------------------------------------------------
    # MODEL INFORMATION
    # -----------------------------------------------------

    st.subheader("Model 01")

    st.markdown(
        """
        **Centralised CCTV Registry & GIS Mapping**

        The platform provides a central registry for government
        CCTV assets with department, district, location and
        camera-level information.

        **Core Components**

        - Central CCTV Registry
        - Department Registry
        - District Registry
        - Camera Metadata
        - Camera Health Monitoring
        - GIS Mapping
        - Camera Onboarding
        """
    )


# =========================================================
# CCTV REGISTRY
# =========================================================

elif page == "CCTV Registry":

    st.title("CCTV Registry")

    db = SessionLocal()

    try:

        cameras = db.query(Camera).all()

        if cameras:

            data = []

            for camera in cameras:

                data.append(
                    {
                        "Camera ID": camera.id,
                        "Camera Name": getattr(
                            camera,
                            "name",
                            ""
                        ),
                        "Status": getattr(
                            camera,
                            "status",
                            ""
                        ),
                        "Latitude": getattr(
                            camera,
                            "latitude",
                            None
                        ),
                        "Longitude": getattr(
                            camera,
                            "longitude",
                            None
                        ),
                    }
                )

            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No cameras are currently registered."
            )

    except Exception as e:

        st.error(
            f"Unable to load CCTV registry: {e}"
        )

    finally:

        db.close()


# =========================================================
# GIS MAP
# =========================================================

elif page == "GIS Map":

    st.title("GIS CCTV Map")

    try:

        show_map()

    except Exception as e:

        st.error(
            f"GIS map could not be loaded: {e}"
        )


# =========================================================
# CAMERA ONBOARDING
# =========================================================

elif page == "Camera Onboarding":

    st.title("Camera Onboarding")

    try:

        show_onboarding()

    except Exception as e:

        st.error(
            f"Camera onboarding could not be loaded: {e}"
        )


# =========================================================
# CAMERA DETAILS
# =========================================================

elif page == "Camera Details":

    st.title("Camera Details")

    db = SessionLocal()

    try:

        cameras = db.query(Camera).all()

        if not cameras:

            st.info(
                "No camera records available."
            )

        else:

            camera_options = {
                f"Camera {camera.id}": camera.id
                for camera in cameras
            }

            selected = st.selectbox(
                "Select Camera",
                list(camera_options.keys())
            )

            camera_id = camera_options[selected]

            camera = (
                db.query(Camera)
                .filter(Camera.id == camera_id)
                .first()
            )

            if camera:

                st.subheader(
                    f"Camera {camera.id}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Camera ID:**",
                        camera.id
                    )

                    st.write(
                        "**Name:**",
                        getattr(
                            camera,
                            "name",
                            "N/A"
                        )
                    )

                    st.write(
                        "**Status:**",
                        getattr(
                            camera,
                            "status",
                            "N/A"
                        )
                    )

                with col2:

                    st.write(
                        "**Latitude:**",
                        getattr(
                            camera,
                            "latitude",
                            "N/A"
                        )
                    )

                    st.write(
                        "**Longitude:**",
                        getattr(
                            camera,
                            "longitude",
                            "N/A"
                        )
                    )

    except Exception as e:

        st.error(
            f"Unable to load camera details: {e}"
        )

    finally:

        db.close()