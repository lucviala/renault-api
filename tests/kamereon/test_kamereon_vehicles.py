"""Tests for Kamereon models."""
import os

import pytest
from tests import fixtures

from renault_api.kamereon import models
from renault_api.kamereon import schemas

EXPECTED_SPECS = {
    "captur_ii.1.json": {
        "get_brand_label": "RENAULT",
        "get_energy_code": "ESS",
        "get_model_code": "XJB1SU",
        "get_model_label": "CAPTUR II",
        "reports_charging_power_in_watts": False,
        "uses_electricity": False,
        "uses_fuel": True,
        "supports-hvac-status": False,
        "supports-location": True,
        "charge-uses-kcm": False,
    },
    "captur_ii.2.json": {
        "get_brand_label": "RENAULT",
        "get_energy_code": "ESS",
        "get_model_code": "XJB1SU",
        "get_model_label": "CAPTUR II",
        "reports_charging_power_in_watts": False,
        "uses_electricity": True,
        "uses_fuel": True,
        "supports-hvac-status": False,
        "supports-location": True,
        "charge-uses-kcm": False,
    },
    "duster.1.json": {
        "get_brand_label": "RENAULT",
        "get_energy_code": "ESS",
        "get_model_code": "XJD1SU",
        "get_model_label": "NEW DUSTER",
        "reports_charging_power_in_watts": False,
        "uses_electricity": False,
        "uses_fuel": True,
        "supports-hvac-status": True,
        "supports-location": True,
        "charge-uses-kcm": False,
    },
    "twingo_ze.1.json": {
        "get_brand_label": "RENAULT",
        "get_energy_code": "ELEC",
        "get_model_code": "X071VE",
        "get_model_label": "TWINGO III",
        "reports_charging_power_in_watts": False,
        "uses_electricity": True,
        "uses_fuel": False,
        "supports-hvac-status": True,
        "supports-location": True,
        "charge-uses-kcm": False,
    },
    "zoe_40.1.json": {
        "get_brand_label": "RENAULT",
        "get_energy_code": "ELEC",
        "get_model_code": "X101VE",
        "get_model_label": "ZOE",
        "reports_charging_power_in_watts": True,
        "uses_electricity": True,
        "uses_fuel": False,
        "supports-hvac-status": True,
        "supports-location": False,
        "charge-uses-kcm": False,
    },
    "zoe_40.2.json": {
        "get_brand_label": "RENAULT",
        "get_energy_code": "ELEC",
        "get_model_code": "X101VE",
        "get_model_label": "ZOE",
        "reports_charging_power_in_watts": True,
        "uses_electricity": True,
        "uses_fuel": False,
        "supports-hvac-status": True,
        "supports-location": False,
        "charge-uses-kcm": False,
    },
    "zoe_50.1.json": {
        "get_brand_label": "RENAULT",
        "get_energy_code": "ELEC",
        "get_model_code": "X102VE",
        "get_model_label": "ZOE",
        "reports_charging_power_in_watts": False,
        "uses_electricity": True,
        "uses_fuel": False,
        "supports-hvac-status": True,
        "supports-location": True,
        "charge-uses-kcm": False,
    },
    "spring.1.json": {
        "get_brand_label": "DACIA",
        "get_energy_code": "ELEC",
        "get_model_code": "XBG1VE",
        "get_model_label": "SPRING",
        "reports_charging_power_in_watts": False,
        "uses_electricity": True,
        "uses_fuel": False,
        "supports-hvac-status": True,
        "supports-location": True,
        "charge-uses-kcm": True,
    },
}


@pytest.mark.parametrize(
    "filename", fixtures.get_json_files(f"{fixtures.KAMEREON_FIXTURE_PATH}/vehicles")
)
def test_vehicles_response(filename: str) -> None:
    """Test vehicles list response."""
    response: models.KamereonVehiclesResponse = fixtures.get_file_content_as_schema(
        filename, schemas.KamereonVehiclesResponseSchema
    )
    response.raise_for_error_code()
    fixtures.ensure_redacted(response.raw_data)

    assert response.vehicleLinks is not None
    for vehicle_link in response.vehicleLinks:
        fixtures.ensure_redacted(vehicle_link.raw_data)

        vehicle_details = vehicle_link.vehicleDetails
        assert vehicle_details
        fixtures.ensure_redacted(vehicle_details.raw_data)

        if os.path.basename(filename) in EXPECTED_SPECS:
            power_in_watts = vehicle_details.reports_charging_power_in_watts()
            generated_specs = {
                "get_brand_label": vehicle_details.get_brand_label(),
                "get_energy_code": vehicle_details.get_energy_code(),
                "get_model_code": vehicle_details.get_model_code(),
                "get_model_label": vehicle_details.get_model_label(),
                "reports_charging_power_in_watts": power_in_watts,
                "uses_electricity": vehicle_details.uses_electricity(),
                "uses_fuel": vehicle_details.uses_fuel(),
                "supports-hvac-status": vehicle_details.supports_endpoint(
                    "hvac-status"
                ),
                "supports-location": vehicle_details.supports_endpoint("location"),
                "charge-uses-kcm": vehicle_details.controls_action_via_kcm("charge"),
            }
            assert EXPECTED_SPECS[os.path.basename(filename)] == generated_specs
