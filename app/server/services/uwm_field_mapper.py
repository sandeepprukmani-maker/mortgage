"""
UWM API field mapper for translating between internal and UWM formats.

Maps internal string-based field values to UWM's numeric ID system and vice versa.
"""
import logging
from typing import Any

logger = logging.getLogger(__name__)


# Loan Type ID mappings (UWM API uses string IDs in array)
# 0=Conventional, 1=Conventional ARM, 2=FHA, 3=FHA ARM, 4=VA, 5=VA ARM, 6=USDA
LOAN_TYPE_TO_UWM: dict[str, str] = {
    "conventional": "0",
    "conventional-arm": "1",
    "fha": "2",
    "fha-arm": "3",
    "va": "4",
    "va-arm": "5",
    "usda": "6",
    # Legacy mappings
    "non-qm": "0",
    "bank-statement": "0",
    "jumbo": "0",
}

UWM_TO_LOAN_TYPE: dict[str, str] = {v: k for k, v in LOAN_TYPE_TO_UWM.items()}


# Purpose Type ID mappings
PURPOSE_TYPE_TO_UWM: dict[str, int] = {
    "purchase": 1,
    "refinance": 3,
    "rate-term-refinance": 3,
    "cash-out": 6,
    "cash-out-refinance": 6,
    "streamline": 12,
    "streamline-refinance": 12,
}

UWM_TO_PURPOSE_TYPE: dict[int, str] = {
    1: "purchase",
    3: "refinance",
    6: "cash-out",
    12: "streamline",
}


# Property Type ID mappings
PROPERTY_TYPE_TO_UWM: dict[str, int] = {
    "single-family": 22,
    "sfr": 22,
    "condo": 25,
    "condominium": 25,
    "townhouse": 30,
    "cooperative": 32,
    "co-op": 32,
    "manufactured": 34,
    "manufactured-home": 34,
    "pud": 38,
    "planned-unit-development": 38,
    "2-unit": 48,
    "duplex": 48,
    "3-unit": 52,
    "triplex": 52,
    "4-unit": 53,
    "fourplex": 53,
    "modular": 54,
    "high-rise-condo": 55,
    "detached-condo": 56,
    "low-rise-condo": 57,
}

UWM_TO_PROPERTY_TYPE: dict[int, str] = {
    22: "single-family",
    25: "condo",
    30: "townhouse",
    32: "cooperative",
    34: "manufactured",
    38: "pud",
    48: "2-unit",
    52: "3-unit",
    53: "4-unit",
    54: "modular",
    55: "high-rise-condo",
    56: "detached-condo",
    57: "low-rise-condo",
}


# Occupancy Type ID mappings
OCCUPANCY_TYPE_TO_UWM: dict[str, int] = {
    "primary": 1,
    "primary-residence": 1,
    "owner-occupied": 1,
    "secondary": 2,
    "vacation": 2,
    "second-home": 2,
    "investment": 3,
    "rental": 3,
    "non-owner-occupied": 3,
}

UWM_TO_OCCUPANCY_TYPE: dict[int, str] = {
    1: "primary",
    2: "secondary",
    3: "investment",
}


# Commitment Period ID mappings (lock period in days)
COMMITMENT_PERIOD_TO_UWM: dict[int, int] = {
    15: 12,
    30: 13,
    45: 14,
    60: 15,
}

UWM_TO_COMMITMENT_PERIOD: dict[int, int] = {v: k for k, v in COMMITMENT_PERIOD_TO_UWM.items()}


# Mortgage Insurance Type ID mappings
MI_TYPE_TO_UWM: dict[str, int] = {
    "borrower-paid-monthly": 1,
    "bpmi": 1,
    "borrower-paid-single": 2,
    "single-premium": 2,
    "lender-paid-single": 3,
    "lpmi": 3,
    "split-premium": 4,
    "no-mi": 5,
    "none": 5,
}

UWM_TO_MI_TYPE: dict[int, str] = {
    1: "borrower-paid-monthly",
    2: "borrower-paid-single",
    3: "lender-paid-single",
    4: "split-premium",
    5: "no-mi",
}


class UWMFieldMapper:
    """Mapper for translating between internal and UWM API field formats."""

    @staticmethod
    def to_loan_type_ids(loan_type: str) -> list[str]:
        """Convert internal loan type string to UWM loan type IDs array."""
        normalized = loan_type.lower().strip()
        if normalized not in LOAN_TYPE_TO_UWM:
            logger.warning(f"Unknown loan type: {loan_type}, defaulting to conventional (0)")
            return ["0"]
        return [LOAN_TYPE_TO_UWM[normalized]]

    @staticmethod
    def from_loan_type_id(loan_type_id: str) -> str:
        """Convert UWM loan type ID to internal string."""
        return UWM_TO_LOAN_TYPE.get(str(loan_type_id), "conventional")

    @staticmethod
    def to_purpose_type_id(purpose: str) -> int:
        """Convert internal purpose string to UWM purpose type ID."""
        normalized = purpose.lower().strip()
        if normalized not in PURPOSE_TYPE_TO_UWM:
            logger.warning(f"Unknown purpose type: {purpose}, defaulting to purchase (1)")
            return 1
        return PURPOSE_TYPE_TO_UWM[normalized]

    @staticmethod
    def from_purpose_type_id(purpose_type_id: int) -> str:
        """Convert UWM purpose type ID to internal string."""
        return UWM_TO_PURPOSE_TYPE.get(purpose_type_id, "purchase")

    @staticmethod
    def to_property_type_id(property_type: str) -> int:
        """Convert internal property type string to UWM property type ID."""
        normalized = property_type.lower().strip()
        if normalized not in PROPERTY_TYPE_TO_UWM:
            logger.warning(f"Unknown property type: {property_type}, defaulting to single-family (22)")
            return 22
        return PROPERTY_TYPE_TO_UWM[normalized]

    @staticmethod
    def from_property_type_id(property_type_id: int) -> str:
        """Convert UWM property type ID to internal string."""
        return UWM_TO_PROPERTY_TYPE.get(property_type_id, "single-family")

    @staticmethod
    def to_occupancy_type_id(occupancy: str) -> int:
        """Convert internal occupancy string to UWM occupancy type ID."""
        normalized = occupancy.lower().strip()
        if normalized not in OCCUPANCY_TYPE_TO_UWM:
            logger.warning(f"Unknown occupancy type: {occupancy}, defaulting to primary (1)")
            return 1
        return OCCUPANCY_TYPE_TO_UWM[normalized]

    @staticmethod
    def from_occupancy_type_id(occupancy_type_id: int) -> str:
        """Convert UWM occupancy type ID to internal string."""
        return UWM_TO_OCCUPANCY_TYPE.get(occupancy_type_id, "primary")

    @staticmethod
    def to_commitment_period_id(lock_days: int) -> int:
        """Convert lock period in days to UWM commitment period ID."""
        if lock_days not in COMMITMENT_PERIOD_TO_UWM:
            # Find closest valid lock period
            valid_periods = sorted(COMMITMENT_PERIOD_TO_UWM.keys())
            closest = min(valid_periods, key=lambda x: abs(x - lock_days))
            logger.warning(f"Invalid lock period: {lock_days}, using closest: {closest}")
            return COMMITMENT_PERIOD_TO_UWM[closest]
        return COMMITMENT_PERIOD_TO_UWM[lock_days]

    @staticmethod
    def from_commitment_period_id(commitment_period_id: int) -> int:
        """Convert UWM commitment period ID to lock days."""
        return UWM_TO_COMMITMENT_PERIOD.get(commitment_period_id, 30)

    @classmethod
    def to_uwm_request(
        cls,
        loan_type: str,
        loan_amount: float,
        property_value: float,
        credit_score: int,
        loan_purpose: str,
        property_type: str,
        occupancy: str,
        state: str,
        county: str | None = None,
        zip_code: str | None = None,
        lock_days: int = 30,
        dti_ratio: float | None = None,
        first_time_buyer: bool = False,
        number_of_units: int = 1,
        broker_alias: str = "TestB01",
        borrower_name: str = "",
        monthly_income: float | None = None,
        sales_price: float = 0,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Convert internal request parameters to UWM API request format.

        Args:
            loan_type: Internal loan type string
            loan_amount: Loan amount in dollars
            property_value: Property value (appraised value) in dollars
            credit_score: Borrower credit score
            loan_purpose: Internal purpose string
            property_type: Internal property type string
            occupancy: Internal occupancy string
            state: Two-letter state code
            county: County name (optional)
            zip_code: ZIP code (optional)
            lock_days: Rate lock period in days
            dti_ratio: Debt-to-income ratio (optional)
            first_time_buyer: First-time homebuyer flag
            number_of_units: Number of units (1-4)
            broker_alias: UWM broker alias
            borrower_name: Borrower name
            monthly_income: Monthly income in dollars
            sales_price: Sales price (0 for refinance)
            **kwargs: Additional parameters to pass through

        Returns:
            Dictionary formatted for UWM API request
        """
        # UWM expects specific field format with string IDs
        uwm_request: dict[str, Any] = {
            "brokerAlias": broker_alias,
            "loanAmount": str(int(loan_amount)),  # UWM expects string
            "loanTypeIds": cls.to_loan_type_ids(loan_type),  # Array of strings
            "salesPrice": sales_price,
            "appraisedValue": property_value,
            "purposeTypeId": str(cls.to_purpose_type_id(loan_purpose)),  # String
            "firstTimeHomeBuyer": first_time_buyer,
            "propertyTypeId": str(cls.to_property_type_id(property_type)),  # String
            "occupancyTypeId": str(cls.to_occupancy_type_id(occupancy)),  # String
            "creditScore": credit_score,
        }

        # Add ZIP code (required field)
        if zip_code:
            uwm_request["propertyZipCode"] = zip_code

        # Add borrower name if provided
        if borrower_name:
            uwm_request["borrowerName"] = borrower_name

        # Add monthly income if provided
        if monthly_income is not None:
            uwm_request["monthlyIncome"] = monthly_income

        # Add optional fields
        if county:
            uwm_request["county"] = county
        if dti_ratio is not None:
            uwm_request["dti"] = dti_ratio
        if number_of_units > 1:
            uwm_request["numberOfUnits"] = number_of_units

        # Pass through any additional UWM-specific parameters
        for key, value in kwargs.items():
            if key not in uwm_request and value is not None:
                uwm_request[key] = value

        return uwm_request

    @classmethod
    def from_uwm_response(cls, uwm_response: dict[str, Any]) -> dict[str, Any]:
        """
        Convert UWM API response to internal format.

        Args:
            uwm_response: Raw response from UWM API

        Returns:
            Dictionary in internal format
        """
        # Extract the best quote from valid items
        valid_quotes = uwm_response.get("validQuoteItems", [])
        invalid_quotes = uwm_response.get("invalidQuoteItems", [])

        # Find best quote (lowest rate with best terms)
        best_quote = None
        if valid_quotes:
            # Sort by rate, then by price (higher price = more lender credit)
            sorted_quotes = sorted(
                valid_quotes,
                key=lambda q: (q.get("rate", float("inf")), -q.get("price", 0))
            )
            best_quote = sorted_quotes[0] if sorted_quotes else None

        internal_response: dict[str, Any] = {
            "uwm_scenario_id": uwm_response.get("scenarioId"),
            "valid_quote_count": len(valid_quotes),
            "invalid_quote_count": len(invalid_quotes),
            "valid_quotes": valid_quotes,
            "invalid_quotes": invalid_quotes,
        }

        if best_quote:
            internal_response.update({
                "best_price": f"${best_quote.get('monthlyPayment', 0):,.2f}/mo",
                "rate": best_quote.get("rate"),
                "apr": best_quote.get("apr"),
                "monthly_payment": best_quote.get("monthlyPayment"),
                "points": best_quote.get("points"),
                "lender_credit": best_quote.get("lenderCredit"),
                "closing_costs": best_quote.get("closingCosts"),
                "total_cash_to_close": best_quote.get("totalCashToClose"),
                "lock_period": best_quote.get("lockPeriod"),
                "product_name": best_quote.get("productName"),
            })
        else:
            internal_response["best_price"] = "No valid quotes"
            internal_response["ineligibility_reasons"] = [
                item.get("ineligibilityReasons", [])
                for item in invalid_quotes
            ]

        # Include error messages if present
        if "errorMessages" in uwm_response and uwm_response["errorMessages"]:
            internal_response["error_messages"] = uwm_response["errorMessages"]
            internal_response["best_price"] = "Error: " + uwm_response["errorMessages"][0]

        # Include brokerage and loan officer info if present
        if "brokerage" in uwm_response:
            internal_response["brokerage"] = uwm_response["brokerage"]
        if "loanOfficer" in uwm_response:
            internal_response["loan_officer"] = uwm_response["loanOfficer"]

        return internal_response


# Singleton instance for convenience
uwm_field_mapper = UWMFieldMapper()
