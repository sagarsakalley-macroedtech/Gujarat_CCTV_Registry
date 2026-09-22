import folium


def create_gujarat_map(
    cameras,
    selected_department=None,
    selected_district=None,
    selected_status=None
):
    """
    Create an interactive Gujarat CCTV map.

    Parameters
    ----------
    cameras : list
        List of Camera ORM objects.

    selected_department : str, optional
        Department filter.

    selected_district : str, optional
        District filter.

    selected_status : str, optional
        Operational status filter.

    Returns
    -------
    folium.Map
        Interactive CCTV map.
    """

    # -----------------------------------------------------
    # GUJARAT MAP CENTER
    # -----------------------------------------------------

    gujarat_center = [
        22.2587,
        71.1924
    ]

    m = folium.Map(
        location=gujarat_center,
        zoom_start=7,
        control_scale=True
    )

    # -----------------------------------------------------
    # FILTER CAMERAS
    # -----------------------------------------------------

    filtered_cameras = []

    for camera in cameras:

        if selected_department:
            if (
                camera.department
                and camera.department.department_name
                != selected_department
            ):
                continue

        if selected_district:
            if (
                camera.district
                and camera.district.district_name
                != selected_district
            ):
                continue

        if selected_status:
            if (
                camera.operational_status
                != selected_status
            ):
                continue

        if (
            camera.latitude is None
            or camera.longitude is None
        ):
            continue

        filtered_cameras.append(camera)

    # -----------------------------------------------------
    # MARKERS
    # -----------------------------------------------------

    for camera in filtered_cameras:

        # Determine marker colour
        if camera.operational_status == "Active":
            marker_color = "green"

        elif camera.operational_status == "Offline":
            marker_color = "red"

        else:
            marker_color = "orange"

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
        # POPUP
        # -------------------------------------------------

        popup_html = f"""
        <div style="width: 300px;">

            <h4>
                CCTV Camera
            </h4>

            <hr>

            <b>Camera ID:</b>
            {camera.camera_id}
            <br><br>

            <b>Department:</b>
            {department_name}
            <br><br>

            <b>District:</b>
            {district_name}
            <br><br>

            <b>Location:</b>
            {camera.location_name or "N/A"}
            <br><br>

            <b>Camera Type:</b>
            {camera.camera_type or "N/A"}
            <br><br>

            <b>Manufacturer:</b>
            {camera.manufacturer or "N/A"}
            <br><br>

            <b>Connectivity:</b>
            {camera.connectivity_type or "N/A"}
            <br><br>

            <b>Storage:</b>
            {camera.storage_type or "N/A"}
            <br><br>

            <b>Retention:</b>
            {camera.retention_days or "N/A"} days
            <br><br>

            <b>Status:</b>
            {camera.operational_status or "N/A"}

        </div>
        """

        popup = folium.Popup(
            popup_html,
            max_width=350
        )

        # -------------------------------------------------
        # MARKER
        # -------------------------------------------------

        folium.Marker(
            location=[
                camera.latitude,
                camera.longitude
            ],
            popup=popup,
            tooltip=(
                f"{camera.camera_id} | "
                f"{camera.operational_status}"
            ),
            icon=folium.Icon(
                color=marker_color,
                icon="video-camera",
                prefix="fa"
            )
        ).add_to(m)

    # -----------------------------------------------------
    # LEGEND
    # -----------------------------------------------------

    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        width: 180px;
        z-index: 9999;
        background-color: white;
        border: 2px solid #777;
        border-radius: 6px;
        padding: 10px;
        font-size: 13px;
    ">

        <b>CCTV Status</b>
        <br><br>

        <span style="color:green;">
            ●
        </span>
        Active
        <br>

        <span style="color:red;">
            ●
        </span>
        Offline
        <br>

        <span style="color:orange;">
            ●
        </span>
        Other

    </div>
    """

    m.get_root().html.add_child(
        folium.Element(legend_html)
    )

    return m