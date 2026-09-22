# =========================================================
# GUJARAT CCTV REGISTRY
# MODEL 01
# Centralised CCTV Registry & GIS Mapping
# =========================================================

import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/api"

def get_dashboard():
    response = requests.get(
        f"{API_URL}/dashboard/summary"
    )
    response.raise_for_status()
    return response.json()


def get_cameras():
    response = requests.get(
        f"{API_URL}/cameras/"
    )
    response.raise_for_status()
    return response.json()


def get_departments():
    response = requests.get(
        f"{API_URL}/departments/"
    )
    response.raise_for_status()
    return response.json()


def get_districts():
    response = requests.get(
        f"{API_URL}/districts/"
    )
    response.raise_for_status()
    return response.json()


def get_camera_locations():
    response = requests.get(
        f"{API_URL}/gis/cameras"
    )
    response.raise_for_status()
    return response.json()

st.set_page_config(
    page_title="Gujarat CCTV Registry",
    page_icon="📹",
    layout="wide"
)

st.title("Gujarat Government Centralised CCTV Registry")
st.caption("CCTV Registry & GIS Mapping System")


try:
    dashboard = get_dashboard()

    total = dashboard["total_cameras"]
    active = dashboard["active_cameras"]
    inactive = dashboard["inactive_cameras"]
    active_percentage = dashboard["active_percentage"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Cameras",
        total
    )

    col2.metric(
        "Active Cameras",
        active
    )

    col3.metric(
        "Inactive Cameras",
        inactive
    )

    col4.metric(
        "Active %",
        f"{active_percentage}%"
    )

except Exception as e:
    st.error(f"API connection error: {e}")

# ---------------------------------------------------------
# API FUNCTIONS
# ---------------------------------------------------------

def get_dashboard():
    response = requests.get(
        f"{API_URL}/dashboard/summary"
    )
    response.raise_for_status()
    return response.json()


def get_cameras():
    response = requests.get(
        f"{API_URL}/cameras/"
    )
    response.raise_for_status()
    return response.json()


def get_departments():
    response = requests.get(
        f"{API_URL}/departments/"
    )
    response.raise_for_status()
    return response.json()


def get_districts():
    response = requests.get(
        f"{API_URL}/districts/"
    )
    response.raise_for_status()
    return response.json()


def get_camera_locations():
    response = requests.get(
        f"{API_URL}/gis/cameras"
    )
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------

st.title("Gujarat CCTV Registry")

from sqlalchemy import func

from config.database import SessionLocal

from database.models import (
    Camera,
    Department,
    District
)

from frontend.map_view import show_map
from frontend.camera_onboarding import show_onboarding


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Gujarat CCTV Registry",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main title */

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

    /* Sidebar */

    .sidebar-title {
        font-size: 25px;
        font-weight: 700;
    }

    .sidebar-subtitle {
        font-size: 14px;
        color: #6b7280;
    }

    /* Model card */

    .model-card {
        background-color: #e8f0fe;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
    }

    .model-title {
        font-size: 20px;
        font-weight: 700;
    }

    .model-text {
        font-size: 15px;
        color: #374151;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR HEADER
# =========================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        Gujarat CCTV Registry
    </div>

    <div class="sidebar-subtitle">
        Centralised CCTV Asset & GIS Registry
    </div>
    """,
    unsafe_allow_html=True
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
        "Camera Details"
    ]
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

        <br>

        <div class="model-text">
            Centralised CCTV Registry & GIS Mapping
        </div>

    </div>
    """,
    unsafe_allow_html=True
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
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Centralised Government CCTV Asset Management Platform'
        '</div>',
        unsafe_allow_html=True
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
                Camera.maintenance_status
                == "Under Maintenance"
            )
            .count()
        )

        # -------------------------------------------------
        # OPERATIONAL RATE
        # -------------------------------------------------

        if total_cameras > 0:

            operational_rate = (
                active_cameras /
                total_cameras
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

        st.subheader(
            "Infrastructure Overview"
        )

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
                Department.id
                == Camera.department_id
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
                    "Cameras"
                ]
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
                    "Cameras"
                ]
            )

            col1, col2 = st.columns(2)

            with col1:

                st.bar_chart(
                    df_status.set_index(
                        "Status"
                    )
                )

            with col2:

                st.dataframe(
                    df_status,
                    use_container_width=True,
                    hide_index=True
                )

        # -------------------------------------------------
        # RECENT CAMERAS
        # -------------------------------------------------

        st.subheader(
            "Registered CCTV Assets"
        )

        recent_cameras = (
            db.query(Camera)
            .order_by(
                Camera.id.desc()
            )
            .limit(10)
            .all()
        )

        if recent_cameras:

            rows = []

            for camera in recent_cameras:

                department_name = "Unknown"

                district_name = "Unknown"

                if camera.department:

                    department_name = (
                        camera.department.department_name
                    )

                if camera.district:

                    district_name = (
                        camera.district.district_name
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
                            getattr(
                                camera,
                                "location_name",
                                None
                            ),

                        "Status":
                            getattr(
                                camera,
                                "operational_status",
                                None
                            ),

                        "Maintenance":
                            getattr(
                                camera,
                                "maintenance_status",
                                None
                            )
                    }
                )

            df_recent = pd.DataFrame(
                rows
            )

            st.dataframe(
                df_recent,
                use_container_width=True,
                hide_index=True
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

    st.title(
        "CCTV Registry"
    )

    st.caption(
        "Centralised inventory of registered CCTV assets"
    )

    db = get_database()

    try:

        # -------------------------------------------------
        # LOAD FILTER DATA
        # -------------------------------------------------

        departments = (
            db.query(Department)
            .order_by(
                Department.department_name
            )
            .all()
        )

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

        status_options = [
            "All Status",
            "Active",
            "Offline",
            "Unknown"
        ]

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            selected_department = st.selectbox(
                "Department",
                department_options
            )

        with col2:

            selected_district = st.selectbox(
                "District",
                district_options
            )

        with col3:

            selected_status = st.selectbox(
                "Operational Status",
                status_options
            )

        # -------------------------------------------------
        # QUERY
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
                None
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
                None
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

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

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
                        getattr(
                            camera,
                            "location_name",
                            None
                        ),

                    "Camera Type":
                        getattr(
                            camera,
                            "camera_type",
                            None
                        ),

                    "Connectivity":
                        getattr(
                            camera,
                            "connectivity_type",
                            None
                        ),

                    "Storage":
                        getattr(
                            camera,
                            "storage_type",
                            None
                        ),

                    "Status":
                        getattr(
                            camera,
                            "operational_status",
                            None
                        ),

                    "Maintenance":
                        getattr(
                            camera,
                            "maintenance_status",
                            None
                        )
                }
            )

        if rows:

            df = pd.DataFrame(
                rows
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
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

    st.title(
        "Camera Details"
    )

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
            camera_ids
        )

        camera = next(
            (
                c
                for c in cameras
                if c.camera_id
                == selected_camera_id
            ),
            None
        )

        if not camera:

            st.error(
                "Camera not found."
            )

            return

        # -------------------------------------------------
        # CAMERA HEADER
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
                getattr(
                    camera,
                    "operational_status",
                    "Unknown"
                )
            )

        with col2:

            st.metric(
                "Maintenance",
                getattr(
                    camera,
                    "maintenance_status",
                    "Unknown"
                )
            )

        with col3:

            retention = getattr(
                camera,
                "retention_days",
                0
            )

            st.metric(
                "Retention",
                f"{retention} days"
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
                f"**Camera ID:** "
                f"{camera.camera_id}"
            )

            st.write(
                f"**Department:** "
                f"{department_name}"
            )

            st.write(
                f"**District:** "
                f"{district_name}"
            )

            st.write(
                f"**Location:** "
                f"{getattr(camera, 'location_name', 'N/A')}"
            )

            st.write(
                f"**Taluka:** "
                f"{getattr(camera, 'taluka', 'N/A')}"
            )

            st.write(
                f"**Village / Area:** "
                f"{getattr(camera, 'village', 'N/A')}"
            )

        with col2:

            st.write(
                f"**Camera Type:** "
                f"{getattr(camera, 'camera_type', 'N/A')}"
            )

            st.write(
                f"**Manufacturer:** "
                f"{getattr(camera, 'manufacturer', 'N/A')}"
            )

            st.write(
                f"**Model:** "
                f"{getattr(camera, 'model', 'N/A')}"
            )

            st.write(
                f"**Ownership:** "
                f"{getattr(camera, 'ownership', 'N/A')}"
            )

        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------

        st.subheader(
            "Geographical Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Latitude:** "
                f"{getattr(camera, 'latitude', 'N/A')}"
            )

        with col2:

            st.write(
                f"**Longitude:** "
                f"{getattr(camera, 'longitude', 'N/A')}"
            )

        # -------------------------------------------------
        # CONNECTIVITY
        # -------------------------------------------------

        st.subheader(
            "Connectivity & Storage"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Connectivity:** "
                f"{getattr(camera, 'connectivity_type', 'N/A')}"
            )

            st.write(
                f"**VMS Vendor:** "
                f"{getattr(camera, 'vms_vendor', 'N/A')}"
            )

        with col2:

            st.write(
                f"**Storage:** "
                f"{getattr(camera, 'storage_type', 'N/A')}"
            )

            st.write(
                f"**Retention:** "
                f"{getattr(camera, 'retention_days', 'N/A')} days"
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

    show_map()


elif page == "Camera Onboarding":

    show_onboarding()


elif page == "Camera Details":

    show_camera_details()