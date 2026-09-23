# =========================================================
# GUJARAT CCTV REGISTRY
# MODEL 01
# Centralised CCTV Registry & GIS Mapping
# =========================================================

import streamlit as st
import pandas as pd

from sqlalchemy import func

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

# IMPORTANT:
# Use the SAME engine/session for both table creation
# and application queries.

from database.database import engine, SessionLocal
from database.models import (
    Base,
    Camera,
    Department,
    District,
)

# ---------------------------------------------------------
# FRONTEND MODULES
# ---------------------------------------------------------

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

# IMPORTANT:
# models.py contains the actual SQLAlchemy Base and models.
# Therefore tables MUST be created from models.Base.

try:
    Base.metadata.create_all(bind=engine)
    from database.seed_data import seed_database

    try:
    db = SessionLocal()

    department_count = db.query(func.count(Department.id)).scalar()
    district_count = db.query(func.count(District.id)).scalar()
    camera_count = db.query(func.count(Camera.id)).scalar()

    db.close()

    if department_count == 0 and district_count == 0 and camera_count == 0:
        seed_database()

except Exception as e:
    st.error(f"Database seeding failed: {e}")
except Exception as e:
    st.error(f"Database initialization failed: {e}")
    st.exception(e)
    st.stop()

# =========================================================
# SEED DATABASE IF EMPTY
# =========================================================

from sqlalchemy import func

def seed_database_if_empty():
    db = SessionLocal()

    try:
        department_count = db.query(func.count(Department.id)).scalar()
        district_count = db.query(func.count(District.id)).scalar()
        camera_count = db.query(func.count(Camera.id)).scalar()

        if department_count == 0 and district_count == 0 and camera_count == 0:

            # Departments
            departments = [
                "Police",
                "Home Department",
                "Health Department",
                "Education Department",
                "Urban Development",
                "Transport Department",
                "Revenue Department",
                "Municipal Corporation",
                "Forest Department",
                "Fire Department",
                "Disaster Management",
                "PWD",
                "Water Resources",
                "Energy Department",
                "Industries Department",
                "Tourism Department",
                "Agriculture Department",
                "Rural Development",
                "Information Technology",
                "Gujarat State Road Transport",
                "Smart City Mission",
                "Airport Authority",
                "Railways",
                "Ports Department",
                "Environment Department",
                "Other"
            ]

            for name in departments:
                db.add(Department(name=name))

            db.commit()

            # Districts
            districts = [
                "Ahmedabad", "Amreli", "Anand", "Aravalli",
                "Banaskantha", "Bharuch", "Bhavnagar", "Botad",
                "Chhota Udaipur", "Dahod", "Dang", "Devbhumi Dwarka",
                "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh",
                "Kheda", "Kutch", "Mahisagar", "Mehsana",
                "Morbi", "Narmada", "Navsari", "Panchmahal",
                "Patan", "Porbandar", "Rajkot", "Sabarkantha",
                "Surat", "Surendranagar", "Vadodara", "Valsad"
            ]

            for name in districts:
                db.add(District(name=name))

            db.commit()

            st.success("Database seeded successfully.")

        # Camera records should be added by your existing
        # camera onboarding / seed logic.

    except Exception as e:
        db.rollback()
        st.error(f"Database seeding failed: {e}")

    finally:
        db.close()


seed_database_if_empty()
# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .sidebar-title {
        font-size: 25px;
        font-weight: 700;
    }

    .sidebar-subtitle {
        font-size: 14px;
        color: #6b7280;
    }

    .model-card {
        background-color: #e8f0fe;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
    }

    .model-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .model-text {
        font-size: 15px;
        color: #374151;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        Gujarat CCTV Registry
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="sidebar-subtitle">
        Centralised CCTV Asset & GIS Registry
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.divider()


# =========================================================
# NAVIGATION
# =========================================================

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


# =========================================================
# MODEL INFORMATION
# =========================================================

st.sidebar.markdown(
    """
    <div class="model-card">

        <div class="model-title">
            Model 01
        </div>

        <div class="model-text">
            Centralised CCTV Registry &amp; GIS Mapping
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATABASE HELPER
# =========================================================

def get_database():
    return SessionLocal()


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    st.markdown(
        '<div class="main-title">Gujarat CCTV Registry</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sub-title">
            Centralised Government CCTV Asset Management Platform
        </div>
        """,
        unsafe_allow_html=True,
    )

    db = get_database()

    try:

        # -------------------------------------------------
        # BASIC COUNTS
        # -------------------------------------------------

        total_cameras = (
            db.query(Camera)
            .count()
        )

        active_cameras = (
            db.query(Camera)
            .filter(
                Camera.operational_status == "Active"
            )
            .count()
        )

        offline_cameras = (
            db.query(Camera)
            .filter(
                Camera.operational_status == "Offline"
            )
            .count()
        )

        total_departments = (
            db.query(Department)
            .count()
        )

        total_districts = (
            db.query(District)
            .count()
        )

        maintenance_cameras = (
            db.query(Camera)
            .filter(
                Camera.maintenance_status == "Under Maintenance"
            )
            .count()
        )

        # -------------------------------------------------
        # OPERATIONAL RATE
        # -------------------------------------------------

        if total_cameras > 0:
            operational_rate = (
                active_cameras / total_cameras
            ) * 100
        else:
            operational_rate = 0

        # -------------------------------------------------
        # TOP METRICS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # INFRASTRUCTURE OVERVIEW
        # -------------------------------------------------

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
                maintenance_cameras
            )

        with col3:
            st.metric(
                "Operational Rate",
                f"{operational_rate:.1f}%"
            )

        st.divider()

        # -------------------------------------------------
        # DEPARTMENT DISTRIBUTION
        # -------------------------------------------------

        st.subheader(
            "Camera Distribution by Department"
        )

        department_data = (
            db.query(
                Department.department_name,
                func.count(Camera.id)
            )
            .outerjoin(
                Camera,
                Department.id == Camera.department_id
            )
            .group_by(
                Department.department_name
            )
            .order_by(
                func.count(Camera.id).desc()
            )
            .all()
        )

        if department_data:

            df_department = pd.DataFrame(
                department_data,
                columns=[
                    "Department",
                    "Cameras",
                ],
            )

            st.bar_chart(
                df_department.set_index(
                    "Department"
                )
            )

        else:
            st.info(
                "No department camera data available."
            )

        # -------------------------------------------------
        # STATUS DISTRIBUTION
        # -------------------------------------------------

        st.subheader(
            "Camera Operational Status"
        )

        status_data = (
            db.query(
                Camera.operational_status,
                func.count(Camera.id)
            )
            .group_by(
                Camera.operational_status
            )
            .all()
        )

        if status_data:

            df_status = pd.DataFrame(
                status_data,
                columns=[
                    "Status",
                    "Cameras",
                ],
            )

            col1, col2 = st.columns(2)

            with col1:
                st.bar_chart(
                    df_status.set_index("Status")
                )

            with col2:
                st.dataframe(
                    df_status,
                    use_container_width=True,
                    hide_index=True,
                )

        # -------------------------------------------------
        # RECENT CAMERAS
        # -------------------------------------------------

        st.subheader(
            "Registered CCTV Assets"
        )

        recent_cameras = (
            db.query(Camera)
            .order_by(Camera.id.desc())
            .limit(10)
            .all()
        )

        if recent_cameras:

            rows = []

            for camera in recent_cameras:

                department_name = (
                    camera.department.department_name
                    if camera.department
                    else "Unknown"
                )

                district_name = (
                    camera.district.district_name
                    if camera.district
                    else "Unknown"
                )

                rows.append(
                    {
                        "Camera ID":
                            camera.camera_id,

                        "Department":
                            department_name,

                        "District":
                            district_name,

                        "Location":
                            camera.location_name,

                        "Status":
                            camera.operational_status,

                        "Maintenance":
                            camera.maintenance_status,
                    }
                )

            df_recent = pd.DataFrame(rows)

            st.dataframe(
                df_recent,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No CCTV cameras registered yet."
            )

    except Exception as e:

        st.error(
            "Dashboard error."
        )

        st.exception(e)

    finally:

        db.close()


# =========================================================
# CCTV REGISTRY
# =========================================================

def show_registry():

    st.title("CCTV Registry")

    st.caption(
        "Centralised inventory of registered CCTV assets"
    )

    db = get_database()

    try:

        # -------------------------------------------------
        # LOAD DEPARTMENTS
        # -------------------------------------------------

        departments = (
            db.query(Department)
            .order_by(
                Department.department_name
            )
            .all()
        )

        # -------------------------------------------------
        # LOAD DISTRICTS
        # -------------------------------------------------

        districts = (
            db.query(District)
            .order_by(
                District.district_name
            )
            .all()
        )

        department_options = [
            "All Departments"
        ]

        department_options += [
            d.department_name
            for d in departments
        ]

        district_options = [
            "All Districts"
        ]

        district_options += [
            d.district_name
            for d in districts
        ]

        # -------------------------------------------------
        # STATUS OPTIONS
        # -------------------------------------------------

        status_options = [
            "All Status",
            "Active",
            "Offline",
            "Unknown",
        ]

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            selected_department = st.selectbox(
                "Department",
                department_options,
            )

        with col2:

            selected_district = st.selectbox(
                "District",
                district_options,
            )

        with col3:

            selected_status = st.selectbox(
                "Operational Status",
                status_options,
            )

        # -------------------------------------------------
        # CAMERA QUERY
        # -------------------------------------------------

        query = db.query(Camera)

        if selected_department != "All Departments":

            department = next(
                (
                    d
                    for d in departments
                    if d.department_name
                    == selected_department
                ),
                None,
            )

            if department:

                query = query.filter(
                    Camera.department_id
                    == department.id
                )

        if selected_district != "All Districts":

            district = next(
                (
                    d
                    for d in districts
                    if d.district_name
                    == selected_district
                ),
                None,
            )

            if district:

                query = query.filter(
                    Camera.district_id
                    == district.id
                )

        if selected_status != "All Status":

            query = query.filter(
                Camera.operational_status
                == selected_status
            )

        cameras = (
            query
            .order_by(Camera.id)
            .all()
        )

        st.write(
            f"**{len(cameras)} camera(s) found**"
        )

        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        rows = []

        for camera in cameras:

            department_name = (
                camera.department.department_name
                if camera.department
                else "Unknown"
            )

            district_name = (
                camera.district.district_name
                if camera.district
                else "Unknown"
            )

            rows.append(
                {
                    "Camera ID":
                        camera.camera_id,

                    "Department":
                        department_name,

                    "District":
                        district_name,

                    "Location":
                        camera.location_name,

                    "Camera Type":
                        camera.camera_type,

                    "Connectivity":
                        camera.connectivity_type,

                    "Storage":
                        camera.storage_type,

                    "Status":
                        camera.operational_status,

                    "Maintenance":
                        camera.maintenance_status,
                }
            )

        if rows:

            df = pd.DataFrame(rows)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No cameras match the selected filters."
            )

    except Exception as e:

        st.error(
            "CCTV Registry error."
        )

        st.exception(e)

    finally:

        db.close()


# =========================================================
# CAMERA DETAILS
# =========================================================

def show_camera_details():

    st.title("Camera Details")

    st.caption(
        "Detailed CCTV asset information"
    )

    db = get_database()

    try:

        cameras = (
            db.query(Camera)
            .order_by(Camera.camera_id)
            .all()
        )

        if not cameras:

            st.warning(
                "No cameras are currently registered."
            )

            return

        camera_ids = [
            camera.camera_id
            for camera in cameras
        ]

        selected_camera_id = st.selectbox(
            "Select Camera",
            camera_ids,
        )

        camera = next(
            (
                c
                for c in cameras
                if c.camera_id
                == selected_camera_id
            ),
            None,
        )

        if not camera:

            st.error(
                "Camera not found."
            )

            return

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        st.subheader(
            f"Camera: {camera.camera_id}"
        )

        department_name = (
            camera.department.department_name
            if camera.department
            else "Unknown"
        )

        district_name = (
            camera.district.district_name
            if camera.district
            else "Unknown"
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Operational Status",
                camera.operational_status
                or "Unknown",
            )

        with col2:

            st.metric(
                "Maintenance",
                camera.maintenance_status
                or "Unknown",
            )

        with col3:

            retention = (
                camera.retention_days
                if camera.retention_days is not None
                else 0
            )

            st.metric(
                "Retention",
                f"{retention} days",
            )

        st.divider()

        # -------------------------------------------------
        # BASIC INFORMATION
        # -------------------------------------------------

        st.subheader(
            "Camera Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Camera ID:** {camera.camera_id}"
            )

            st.write(
                f"**Department:** {department_name}"
            )

            st.write(
                f"**District:** {district_name}"
            )

            st.write(
                f"**Location:** "
                f"{camera.location_name or 'N/A'}"
            )

            st.write(
                f"**Taluka:** "
                f"{camera.taluka or 'N/A'}"
            )

            st.write(
                f"**Village / Area:** "
                f"{camera.village or 'N/A'}"
            )

        with col2:

            st.write(
                f"**Camera Type:** "
                f"{camera.camera_type or 'N/A'}"
            )

            st.write(
                f"**Manufacturer:** "
                f"{camera.manufacturer or 'N/A'}"
            )

            st.write(
                f"**Model:** "
                f"{camera.model or 'N/A'}"
            )

            st.write(
                f"**Ownership:** "
                f"{camera.ownership or 'N/A'}"
            )

        # -------------------------------------------------
        # GEOGRAPHICAL INFORMATION
        # -------------------------------------------------

        st.subheader(
            "Geographical Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Latitude:** "
                f"{camera.latitude if camera.latitude is not None else 'N/A'}"
            )

        with col2:

            st.write(
                f"**Longitude:** "
                f"{camera.longitude if camera.longitude is not None else 'N/A'}"
            )

        # -------------------------------------------------
        # CONNECTIVITY & STORAGE
        # -------------------------------------------------

        st.subheader(
            "Connectivity & Storage"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Connectivity:** "
                f"{camera.connectivity_type or 'N/A'}"
            )

            st.write(
                f"**VMS Vendor:** "
                f"{camera.vms_vendor or 'N/A'}"
            )

        with col2:

            st.write(
                f"**Storage:** "
                f"{camera.storage_type or 'N/A'}"
            )

            st.write(
                f"**Retention:** "
                f"{camera.retention_days if camera.retention_days is not None else 'N/A'} days"
            )

        # -------------------------------------------------
        # DATES
        # -------------------------------------------------

        st.subheader(
            "Installation & AMC"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Installation Date:** "
                f"{camera.installation_date or 'N/A'}"
            )

            st.write(
                f"**AMC Start:** "
                f"{camera.amc_start_date or 'N/A'}"
            )

        with col2:

            st.write(
                f"**AMC End:** "
                f"{camera.amc_end_date or 'N/A'}"
            )

        # -------------------------------------------------
        # DESCRIPTION
        # -------------------------------------------------

        if camera.description:

            st.subheader(
                "Description"
            )

            st.write(
                camera.description
            )

    except Exception as e:

        st.error(
            "Camera Details error."
        )

        st.exception(e)

    finally:

        db.close()


# =========================================================
# PAGE ROUTING
# =========================================================

if page == "Dashboard":

    show_dashboard()

elif page == "CCTV Registry":

    show_registry()

elif page == "GIS Map":

    try:
        show_map()
    except Exception as e:
        st.error("GIS Map error.")
        st.exception(e)

elif page == "Camera Onboarding":

    try:
        show_onboarding()
    except Exception as e:
        st.error("Camera Onboarding error.")
        st.exception(e)

elif page == "Camera Details":

    show_camera_details()