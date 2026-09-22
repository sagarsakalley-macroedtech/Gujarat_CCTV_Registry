import streamlit as st

from streamlit_folium import st_folium

from config.database import SessionLocal

from database.models import (
    Camera,
    Department,
    District
)

from gis.map_layers import create_gujarat_map


def show_map():

    st.title("GIS Camera Map")

    st.caption(
        "Geographical inventory of registered CCTV infrastructure"
    )

    db = SessionLocal()

    try:

        # -------------------------------------------------
        # LOAD DATA
        # -------------------------------------------------

        cameras = (
            db.query(Camera)
            .all()
        )

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

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            department_options = [
                "All Departments"
            ] + [
                department.department_name
                for department in departments
            ]

            selected_department = st.selectbox(
                "Department",
                department_options
            )

        with col2:

            district_options = [
                "All Districts"
            ] + [
                district.district_name
                for district in districts
            ]

            selected_district = st.selectbox(
                "District",
                district_options
            )

        with col3:

            status_options = [
                "All Status",
                "Active",
                "Offline"
            ]

            selected_status = st.selectbox(
                "Operational Status",
                status_options
            )

        # -------------------------------------------------
        # CONVERT FILTERS
        # -------------------------------------------------

        department_filter = None

        if selected_department != "All Departments":
            department_filter = selected_department

        district_filter = None

        if selected_district != "All Districts":
            district_filter = selected_district

        status_filter = None

        if selected_status != "All Status":
            status_filter = selected_status

        # -------------------------------------------------
        # CREATE MAP
        # -------------------------------------------------

        cctv_map = create_gujarat_map(
            cameras=cameras,
            selected_department=department_filter,
            selected_district=district_filter,
            selected_status=status_filter
        )

        # -------------------------------------------------
        # MAP
        # -------------------------------------------------

        map_data = st_folium(
            cctv_map,
            width=None,
            height=650,
            returned_objects=[]
        )

    finally:

        db.close()