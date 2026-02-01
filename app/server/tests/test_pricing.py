"""
Tests for pricing API endpoints and UWM config validation.
"""
import pytest
import json
import os
from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient
from main import app


# UWM config expected structure based on UWM API requirements
EXPECTED_UWM_CONFIG_FIELDS = {
    "brokerAlias": str,
    "loanAmount": str,
    "loanTypeIds": list,
    "salesPrice": (int, float),
    "appraisedValue": (int, float),
    "purposeTypeId": str,
    "firstTimeHomeBuyer": bool,
    "propertyTypeId": str,
    "occupancyTypeId": str,
    "propertyZipCode": str,
    "creditScore": int,
    "monthlyIncome": (int, float),
    "borrowerName": str,
}


class TestGetUWMConfig:
    """Tests for GET /api/pricing/config endpoint."""

    def test_config_endpoint_returns_200(self):
        """Test that config endpoint returns 200 OK."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        assert response.status_code == 200

    def test_config_returns_valid_json(self):
        """Test that config endpoint returns valid JSON."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()
        assert isinstance(data, dict)

    def test_config_has_required_fields(self):
        """Test that config contains all required UWM fields."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        for field_name, expected_type in EXPECTED_UWM_CONFIG_FIELDS.items():
            assert field_name in data, f"Missing required field: {field_name}"
            assert isinstance(data[field_name], expected_type), \
                f"Field {field_name} has wrong type: expected {expected_type}, got {type(data[field_name])}"

    def test_config_loan_type_ids_format(self):
        """Test that loanTypeIds is an array of strings (UWM format)."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        loan_type_ids = data.get("loanTypeIds", [])
        assert isinstance(loan_type_ids, list), "loanTypeIds must be an array"
        assert len(loan_type_ids) > 0, "loanTypeIds must not be empty"
        for item in loan_type_ids:
            assert isinstance(item, str), f"loanTypeIds items must be strings, got {type(item)}"

    def test_config_loan_amount_is_string(self):
        """Test that loanAmount is a string (UWM format)."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        assert isinstance(data.get("loanAmount"), str), "loanAmount must be a string"

    def test_config_purpose_type_id_is_string(self):
        """Test that purposeTypeId is a string (UWM format)."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        assert isinstance(data.get("purposeTypeId"), str), "purposeTypeId must be a string"

    def test_config_property_type_id_is_string(self):
        """Test that propertyTypeId is a string (UWM format)."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        assert isinstance(data.get("propertyTypeId"), str), "propertyTypeId must be a string"

    def test_config_occupancy_type_id_is_string(self):
        """Test that occupancyTypeId is a string (UWM format)."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        assert isinstance(data.get("occupancyTypeId"), str), "occupancyTypeId must be a string"


class TestUWMConfigFile:
    """Tests for uwm_config.json file integrity."""

    def test_config_file_exists(self):
        """Test that uwm_config.json file exists."""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'uwm_config.json'
        )
        assert os.path.exists(config_path), "uwm_config.json file not found"

    def test_config_file_is_valid_json(self):
        """Test that uwm_config.json contains valid JSON."""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'uwm_config.json'
        )
        with open(config_path, 'r') as f:
            data = json.load(f)
        assert isinstance(data, dict), "Config must be a JSON object"

    def test_config_file_matches_api_response(self):
        """Test that config file matches API response."""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'uwm_config.json'
        )
        with open(config_path, 'r') as f:
            file_data = json.load(f)

        client = TestClient(app)
        response = client.get("/api/pricing/config")
        api_data = response.json()

        assert file_data == api_data, "Config file and API response should match"


class TestPricingQuoteRequest:
    """Tests for POST /api/pricing/quote endpoint request validation."""

    def test_quote_requires_authentication(self):
        """Test that quote endpoint requires authentication."""
        client = TestClient(app)
        response = client.post(
            "/api/pricing/quote",
            json={"customer_id": 1}
        )
        assert response.status_code == 401

    def test_quote_requires_customer_id(self):
        """Test that quote endpoint requires customer_id."""
        client = TestClient(app)
        # Send UWM config without customer_id - should fail
        response = client.post(
            "/api/pricing/quote",
            json={
                "brokerAlias": "TestB01",
                "loanAmount": "320000"
            }
        )
        assert response.status_code in [401, 422]  # Either auth or validation error

    def test_quote_accepts_uwm_camelcase_format(self):
        """Test that quote endpoint accepts UWM camelCase format."""
        from schemas.pricing_quote import PricingQuoteRequest

        # This is what the client sends (UWM format)
        data = {
            "customer_id": 1,
            "brokerAlias": "TestB01",
            "loanAmount": "320000",
            "loanTypeIds": ["5"],
            "salesPrice": 0,
            "appraisedValue": 450000,
            "purposeTypeId": "3",
            "firstTimeHomeBuyer": False,
            "propertyTypeId": "22",
            "occupancyTypeId": "1",
            "propertyZipCode": "48374",
            "creditScore": 820,
            "monthlyIncome": 6000,
            "borrowerName": "Ed"
        }

        # Schema should accept this without validation errors
        request = PricingQuoteRequest(**data)
        assert request.customer_id == 1
        assert request.brokerAlias == "TestB01"
        assert request.loanAmount == "320000"
        assert request.creditScore == 820

    def test_quote_only_requires_customer_id(self):
        """Test that quote endpoint only requires customer_id."""
        from schemas.pricing_quote import PricingQuoteRequest

        # Minimal request - only customer_id required
        request = PricingQuoteRequest(customer_id=1)
        assert request.customer_id == 1
        assert request.loan_type is None  # Optional fields are None


class TestUWMRequestPayloadFormat:
    """Tests to validate UWM API request payload format."""

    def test_uwm_payload_uses_camel_case(self):
        """Test that UWM payload uses camelCase field names."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        # These should be camelCase (UWM format), not snake_case
        camel_case_fields = [
            "brokerAlias",
            "loanAmount",
            "loanTypeIds",
            "salesPrice",
            "appraisedValue",
            "purposeTypeId",
            "firstTimeHomeBuyer",
            "propertyTypeId",
            "occupancyTypeId",
            "propertyZipCode",
            "creditScore",
            "monthlyIncome",
            "borrowerName",
        ]

        for field in camel_case_fields:
            assert field in data, f"Missing camelCase field: {field}"

    def test_uwm_payload_no_snake_case(self):
        """Test that UWM payload doesn't contain snake_case fields."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        # These should NOT be present (old snake_case format)
        snake_case_fields = [
            "broker_alias",
            "loan_amount",
            "loan_type_ids",
            "sales_price",
            "appraised_value",
            "purpose_type_id",
            "first_time_home_buyer",
            "property_type_id",
            "occupancy_type_id",
            "property_zip_code",
            "credit_score",
            "monthly_income",
            "borrower_name",
        ]

        for field in snake_case_fields:
            assert field not in data, f"Found unexpected snake_case field: {field}"


class TestUWMSampleRequest:
    """Tests to validate against UWM sample request format."""

    SAMPLE_REQUEST = {
        "brokerAlias": "TestB01",
        "loanAmount": "320000",
        "loanTypeIds": ["5"],
        "salesPrice": 0,
        "appraisedValue": 450000,
        "purposeTypeId": "3",
        "firstTimeHomeBuyer": False,
        "propertyTypeId": "22",
        "occupancyTypeId": "1",
        "propertyZipCode": "48374",
        "creditScore": 820,
        "monthlyIncome": 6000,
        "borrowerName": "Ed"
    }

    def test_config_structure_matches_sample(self):
        """Test that config has same structure as UWM sample request."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        sample_keys = set(self.SAMPLE_REQUEST.keys())
        config_keys = set(data.keys())

        assert sample_keys == config_keys, \
            f"Config keys don't match sample. Missing: {sample_keys - config_keys}, Extra: {config_keys - sample_keys}"

    def test_config_field_types_match_sample(self):
        """Test that config field types match UWM sample request types."""
        client = TestClient(app)
        response = client.get("/api/pricing/config")
        data = response.json()

        for field, sample_value in self.SAMPLE_REQUEST.items():
            config_value = data.get(field)
            assert type(config_value) == type(sample_value), \
                f"Field '{field}' type mismatch: expected {type(sample_value).__name__}, got {type(config_value).__name__}"
