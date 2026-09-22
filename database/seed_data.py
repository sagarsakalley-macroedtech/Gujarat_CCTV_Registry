from config.database import (
    engine,
    SessionLocal
)

from database.models import (
    Base,
    Department,
    District,
    Camera
)

from datetime import date


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

Base.metadata.create_all(
    bind=engine
)


db = SessionLocal()


# ---------------------------------------------------------
# DEPARTMENTS
# ---------------------------------------------------------

departments = [

    ("POL", "Police Department"),
    ("RTO", "Regional Transport Office"),
    ("MC-AHM", "Ahmedabad Municipal Corporation"),
    ("MC-SRT", "Surat Municipal Corporation"),
    ("MC-VAD", "Vadodara Municipal Corporation"),
    ("MC-RAJ", "Rajkot Municipal Corporation"),
    ("FCS", "Food and Civil Supplies Department"),
    ("HEALTH", "Health Department"),
    ("EDU", "Education Department"),
    ("PWD", "Public Works Department"),
    ("FOREST", "Forest Department"),
    ("REVENUE", "Revenue Department"),
    ("TRANSPORT", "Transport Department"),
    ("HOME", "Home Department"),
    ("ENERGY", "Energy Department"),
    ("WATER", "Water Resources Department"),
    ("URBAN", "Urban Development Department"),
    ("RURAL", "Rural Development Department"),
    ("TOURISM", "Tourism Department"),
    ("PORT", "Ports Department"),
    ("INDUSTRY", "Industries Department"),
    ("LABOUR", "Labour Department"),
    ("AGRI", "Agriculture Department"),
    ("ANIMAL", "Animal Husbandry Department"),
    ("DISASTER", "Disaster Management Department"),
    ("OTHER", "Other Government Institutions")
]


for code, name in departments:

    existing = db.query(
        Department
    ).filter(
        Department.department_code == code
    ).first()

    if not existing:

        db.add(
            Department(
                department_code=code,
                department_name=name
            )
        )


db.commit()


# ---------------------------------------------------------
# DISTRICTS
# ---------------------------------------------------------

district_names = [

    "Ahmedabad",
    "Amreli",
    "Anand",
    "Aravalli",
    "Banaskantha",
    "Bharuch",
    "Bhavnagar",
    "Botad",
    "Chhota Udepur",
    "Dahod",
    "Dang",
    "Devbhoomi Dwarka",
    "Gandhinagar",
    "Gir Somnath",
    "Jamnagar",
    "Junagadh",
    "Kheda",
    "Kutch",
    "Mahisagar",
    "Mehsana",
    "Morbi",
    "Narmada",
    "Navsari",
    "Panchmahal",
    "Patan",
    "Porbandar",
    "Rajkot",
    "Sabarkantha",
    "Surat",
    "Surendranagar",
    "Vadodara",
    "Valsad"
]


for name in district_names:

    existing = db.query(
        District
    ).filter(
        District.district_name == name
    ).first()

    if not existing:

        db.add(
            District(
                district_name=name
            )
        )


db.commit()


# ---------------------------------------------------------
# SAMPLE CAMERAS
# ---------------------------------------------------------

sample_cameras = [

    {
        "camera_id": "CAM-AHM-0001",
        "department_id": 1,
        "district_id": 1,
        "location_name": "Ahmedabad City Police Control Point",
        "taluka": "Ahmedabad City",
        "latitude": 23.0225,
        "longitude": 72.5714,
        "camera_type": "IP PTZ",
        "manufacturer": "Axis",
        "model": "PTZ-01",
        "ownership": "Government",
        "connectivity_type": "Fiber",
        "storage_type": "Local",
        "retention_days": 15,
        "vms_vendor": "Generic VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2024, 1, 15)
    },

    {
        "camera_id": "CAM-SRT-0001",
        "department_id": 4,
        "district_id": 29,
        "location_name": "Surat Municipal Zone",
        "taluka": "Surat",
        "latitude": 21.1702,
        "longitude": 72.8311,
        "camera_type": "IP Dome",
        "manufacturer": "Hikvision",
        "model": "DS-2CD",
        "ownership": "Government",
        "connectivity_type": "Fiber",
        "storage_type": "Cloud",
        "retention_days": 30,
        "vms_vendor": "Hikvision VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2023, 8, 20)
    },

    {
        "camera_id": "CAM-VLS-0001",
        "department_id": 1,
        "district_id": 32,
        "location_name": "Valsad Highway Checkpoint",
        "taluka": "Valsad",
        "latitude": 20.5992,
        "longitude": 72.9342,
        "camera_type": "IP Fixed",
        "manufacturer": "Dahua",
        "model": "IPC-01",
        "ownership": "Government",
        "connectivity_type": "4G",
        "storage_type": "Local",
        "retention_days": 7,
        "vms_vendor": "Dahua VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2024, 5, 10)
    },

    {
        "camera_id": "CAM-DHD-0001",
        "department_id": 1,
        "district_id": 10,
        "location_name": "Dahod Public Area",
        "taluka": "Dahod",
        "latitude": 22.8390,
        "longitude": 74.2550,
        "camera_type": "IP Dome",
        "manufacturer": "Hikvision",
        "model": "DS-2CD",
        "ownership": "Government",
        "connectivity_type": "Wireless",
        "storage_type": "Local",
        "retention_days": 15,
        "vms_vendor": "Generic VMS",
        "operational_status": "Offline",
        "maintenance_status": "Under Maintenance",
        "installation_date": date(2022, 11, 12)
    },

    {
        "camera_id": "CAM-DWK-0001",
        "department_id": 20,
        "district_id": 12,
        "location_name": "Dwarka Tourism Zone",
        "taluka": "Dwarka",
        "latitude": 22.2442,
        "longitude": 68.9685,
        "camera_type": "IP PTZ",
        "manufacturer": "Axis",
        "model": "PTZ-02",
        "ownership": "Government",
        "connectivity_type": "Fiber",
        "storage_type": "Cloud",
        "retention_days": 15,
        "vms_vendor": "Axis VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2024, 2, 18)
    },

    {
        "camera_id": "CAM-JMN-0001",
        "department_id": 1,
        "district_id": 15,
        "location_name": "Jamnagar Public Road",
        "taluka": "Jamnagar",
        "latitude": 22.4707,
        "longitude": 70.0577,
        "camera_type": "IP Fixed",
        "manufacturer": "CP Plus",
        "model": "CP-01",
        "ownership": "Government",
        "connectivity_type": "Fiber",
        "storage_type": "Local",
        "retention_days": 15,
        "vms_vendor": "CP Plus VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2023, 3, 10)
    },

    {
        "camera_id": "CAM-SMN-0001",
        "department_id": 20,
        "district_id": 14,
        "location_name": "Somnath Temple Zone",
        "taluka": "Veraval",
        "latitude": 20.8880,
        "longitude": 70.4010,
        "camera_type": "IP PTZ",
        "manufacturer": "Axis",
        "model": "PTZ-03",
        "ownership": "Government",
        "connectivity_type": "Fiber",
        "storage_type": "Cloud",
        "retention_days": 30,
        "vms_vendor": "Axis VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2024, 7, 1)
    },

    {
        "camera_id": "CAM-RJT-0001",
        "department_id": 2,
        "district_id": 27,
        "location_name": "Rajkot RTO Testing Track",
        "taluka": "Rajkot",
        "latitude": 22.3039,
        "longitude": 70.8022,
        "camera_type": "IP Fixed",
        "manufacturer": "Hikvision",
        "model": "DS-2CD",
        "ownership": "Government",
        "connectivity_type": "Fiber",
        "storage_type": "Local",
        "retention_days": 15,
        "vms_vendor": "Hikvision VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2023, 9, 5)
    },

    {
        "camera_id": "CAM-VAD-0001",
        "department_id": 5,
        "district_id": 31,
        "location_name": "Vadodara Municipal Area",
        "taluka": "Vadodara",
        "latitude": 22.3072,
        "longitude": 73.1812,
        "camera_type": "IP Dome",
        "manufacturer": "Dahua",
        "model": "IPC-02",
        "ownership": "Government",
        "connectivity_type": "Fiber",
        "storage_type": "Local",
        "retention_days": 7,
        "vms_vendor": "Dahua VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2024, 4, 22)
    },

    {
        "camera_id": "CAM-KUT-0001",
        "department_id": 1,
        "district_id": 18,
        "location_name": "Kutch Border Monitoring Area",
        "taluka": "Bhuj",
        "latitude": 23.2420,
        "longitude": 69.6669,
        "camera_type": "IP PTZ",
        "manufacturer": "Axis",
        "model": "PTZ-04",
        "ownership": "Government",
        "connectivity_type": "Wireless",
        "storage_type": "Local",
        "retention_days": 15,
        "vms_vendor": "Generic VMS",
        "operational_status": "Active",
        "maintenance_status": "Normal",
        "installation_date": date(2022, 12, 15)
    }
]


# ---------------------------------------------------------
# INSERT CAMERAS
# ---------------------------------------------------------

for data in sample_cameras:

    existing = db.query(
        Camera
    ).filter(
        Camera.camera_id == data["camera_id"]
    ).first()

    if not existing:

        db.add(
            Camera(**data)
        )


db.commit()

db.close()


print("Database initialized successfully.")
print("Departments added:", len(departments))
print("Districts added:", len(district_names))
print("Sample cameras added:", len(sample_cameras))