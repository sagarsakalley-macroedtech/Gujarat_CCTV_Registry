import streamlit as st
import pandas as pd

from config.database import SessionLocal
from database.models import Camera, Department, District


def show_onboarding():

    st.title("Camera Onboarding")

    st.write(
        "Register and onboard CCTV cameras into the "
        "Centralised CCTV Registry."
    )

    st.divider()

    tab1, tab2 = st.tabs(
        [
            "Manual Registration",
            "Bulk CSV Upload"
        ]
    )

    # =====================================================
    # MANUAL REGISTRATION
    # =====================================================

    with tab1:

        st.subheader("Manual Camera Registration")

        db = SessionLocal()

        try:

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

            if not departments:

                st.warning(
                    "No departments found in database."
                )

                return

            if not districts:

                st.warning(
                    "No districts found in database."
                )

                return

            department_names = [
                d.department_name
                for d in departments
            ]

            district_names = [
                d.district_name
                for d in districts
            ]

            # -------------------------------------------------
            # FORM
            # -------------------------------------------------

            with st.form(
                "manual_camera_registration"
            ):

                st.markdown(
                    "### Camera Identification"
                )

                camera_id = st.text_input(
                    "Camera ID *",
                    placeholder="CAM-AHM-0002"
                )

                department_name = st.selectbox(
                    "Department *",
                    department_names
                )

                district_name = st.selectbox(
                    "District *",
                    district_names
                )

                location_name = st.text_input(
                    "Location Name *",
                    placeholder="SG Highway Junction"
                )

                st.markdown(
                    "### Geographic Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    latitude = st.number_input(
                        "Latitude",
                        value=23.0225,
                        format="%.6f"
                    )

                with col2:

                    longitude = st.number_input(
                        "Longitude",
                        value=72.5714,
                        format="%.6f"
                    )

                st.markdown(
                    "### Camera Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    camera_type = st.selectbox(
                        "Camera Type",
                        [
                            "IP Fixed",
                            "IP Dome",
                            "IP PTZ",
                            "Analog",
                            "ANPR",
                            "Thermal",
                            "Other"
                        ]
                    )

                with col2:

                    manufacturer = st.text_input(
                        "Manufacturer"
                    )

                model = st.text_input(
                    "Model"
                )

                ownership = st.selectbox(
                    "Ownership",
                    [
                        "Government",
                        "Private",
                        "Society",
                        "Commercial",
                        "Other"
                    ]
                )

                st.markdown(
                    "### Connectivity & Storage"
                )

                col1, col2 = st.columns(2)

                with col1:

                    connectivity_type = st.selectbox(
                        "Connectivity",
                        [
                            "Fiber",
                            "4G",
                            "5G",
                            "Wireless",
                            "LAN",
                            "Other"
                        ]
                    )

                with col2:

                    storage_type = st.selectbox(
                        "Storage",
                        [
                            "Local",
                            "Cloud",
                            "Hybrid",
                            "Unknown"
                        ]
                    )

                retention_days = st.number_input(
                    "Retention Period (Days)",
                    min_value=0,
                    max_value=3650,
                    value=15
                )

                vms_vendor = st.text_input(
                    "VMS Vendor"
                )

                st.markdown(
                    "### Operational Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    operational_status = st.selectbox(
                        "Operational Status",
                        [
                            "Active",
                            "Offline",
                            "Unknown"
                        ]
                    )

                with col2:

                    maintenance_status = st.selectbox(
                        "Maintenance Status",
                        [
                            "Normal",
                            "Under Maintenance",
                            "AMC Expired",
                            "Unknown"
                        ]
                    )

                submitted = st.form_submit_button(
                    "Register Camera",
                    type="primary",
                    use_container_width=True
                )

            # -------------------------------------------------
            # SAVE CAMERA
            # -------------------------------------------------

            if submitted:

                if not camera_id.strip():

                    st.error(
                        "Camera ID is required."
                    )

                elif not location_name.strip():

                    st.error(
                        "Location Name is required."
                    )

                else:

                    existing_camera = (
                        db.query(Camera)
                        .filter(
                            Camera.camera_id
                            == camera_id.strip()
                        )
                        .first()
                    )

                    if existing_camera:

                        st.error(
                            f"Camera ID "
                            f"'{camera_id}' already exists."
                        )

                    else:

                        department = next(
                            d for d in departments
                            if d.department_name
                            == department_name
                        )

                        district = next(
                            d for d in districts
                            if d.district_name
                            == district_name
                        )

                        camera = Camera(

                            camera_id=
                                camera_id.strip(),

                            department_id=
                                department.id,

                            district_id=
                                district.id,

                            location_name=
                                location_name.strip(),

                            latitude=
                                latitude,

                            longitude=
                                longitude,

                            camera_type=
                                camera_type,

                            manufacturer=
                                manufacturer.strip(),

                            model=
                                model.strip(),

                            ownership=
                                ownership,

                            connectivity_type=
                                connectivity_type,

                            storage_type=
                                storage_type,

                            retention_days=
                                retention_days,

                            vms_vendor=
                                vms_vendor.strip(),

                            operational_status=
                                operational_status,

                            maintenance_status=
                                maintenance_status
                        )

                        db.add(camera)

                        db.commit()

                        st.success(
                            f"Camera {camera_id} "
                            "registered successfully."
                        )

                        st.balloons()

        except Exception as e:

            db.rollback()

            st.error(
                "Camera onboarding error:"
            )

            st.exception(e)

        finally:

            db.close()

    # =====================================================
    # BULK CSV
    # =====================================================

    with tab2:

        st.subheader(
            "Bulk Camera Onboarding"
        )

        st.write(
            "Upload a CSV file containing CCTV "
            "camera metadata."
        )

        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=["csv"]
        )

        if uploaded_file:

            try:

                df = pd.read_csv(
                    uploaded_file
                )

                st.success(
                    f"{len(df)} records loaded."
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                if st.button(
                    "Validate CSV",
                    type="primary"
                ):

                    required_columns = [
                        "camera_id",
                        "department_name",
                        "district_name",
                        "latitude",
                        "longitude"
                    ]

                    missing = [
                        col
                        for col in required_columns
                        if col not in df.columns
                    ]

                    if missing:

                        st.error(
                            "Missing columns:"
                        )

                        st.write(
                            missing
                        )

                    else:

                        st.success(
                            "CSV structure is valid."
                        )

            except Exception as e:

                st.error(
                    "Unable to read CSV."
                )

                st.exception(e)

        else:

            st.info(
                "Upload a CSV file to begin "
                "bulk onboarding."
            )