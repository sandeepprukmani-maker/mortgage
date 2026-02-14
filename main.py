import os
import json
import re
import requests
import logging
from typing import Any, Dict, List, Optional, Union
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from models import db, Customer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load variables from .env
load_dotenv()

# ===== Environment variables =====
UWM_USERNAME = os.getenv("UWM_USERNAME")
UWM_PASSWORD = os.getenv("UWM_PASSWORD")
UWM_CLIENT_ID = os.getenv("UWM_CLIENT_ID")
UWM_CLIENT_SECRET = os.getenv("UWM_CLIENT_SECRET")
UWM_SCOPE = os.getenv("UWM_SCOPE")
SOCKS_PROXY = os.getenv("SOCKS_PROXY")

# ===== Endpoints =====
TOKEN_URL = "https://sso.uwm.com/adfs/oauth2/token"
PRICEQUOTE_URL = "https://stg.api.uwm.com/public/instantpricequote/v2/pricequote"

app = Flask(__name__, static_folder="static", static_url_path="/")
app.secret_key = os.environ.get("SESSION_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

with app.app_context():
    db.init_app(app)
    db.create_all()
    current_count = Customer.query.count()
    if current_count < 500:
        import random

        needed = 500 - current_count
        for i in range(needed):
            cust = Customer(
                name=f"Customer {current_count + i + 1}",
                current_monthly_payment=random.uniform(1000, 5000),
                remaining_balance=random.uniform(100000, 500000),
                property_value=random.uniform(150000, 700000),
                property_zip=str(random.randint(10000, 99999)),
                property_county="County",
                property_state="ST",
                credit_score=random.randint(600, 850),
                monthly_income=random.uniform(3000, 15000),
            )
            db.session.add(cust)
        db.session.commit()


# ===== Customer CRUD Endpoints =====
@app.route("/api/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify(
        [
            {
                "id": c.id,
                "name": c.name,
                "current_monthly_payment": c.current_monthly_payment,
                "remaining_balance": c.remaining_balance,
                "property_value": c.property_value,
                "property_zip": c.property_zip,
                "property_county": c.property_county,
                "property_state": c.property_state,
                "credit_score": c.credit_score,
                "monthly_income": c.monthly_income,
            }
            for c in customers
        ]
    )


@app.route("/api/customers", methods=["POST"])
def add_customer():
    data = request.json
    new_customer = Customer(
        name=data.get("name"),
        current_monthly_payment=safe_float(data.get("current_monthly_payment")),
        remaining_balance=safe_float(data.get("remaining_balance")),
        property_value=safe_float(data.get("property_value")),
        property_zip=data.get("property_zip"),
        property_county=data.get("property_county"),
        property_state=data.get("property_state"),
        credit_score=int(data.get("credit_score", 0)),
        monthly_income=safe_float(data.get("monthly_income")),
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer added", "id": new_customer.id})


@app.route("/api/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    customer.name = data.get("name", customer.name)
    customer.current_monthly_payment = safe_float(
        data.get("current_monthly_payment", customer.current_monthly_payment)
    )
    customer.remaining_balance = safe_float(
        data.get("remaining_balance", customer.remaining_balance)
    )
    customer.property_value = safe_float(data.get("property_value", customer.property_value))
    customer.property_zip = data.get("property_zip", customer.property_zip)
    customer.property_county = data.get("property_county", customer.property_county)
    customer.property_state = data.get("property_state", customer.property_state)
    customer.credit_score = int(data.get("credit_score", customer.credit_score))
    customer.monthly_income = safe_float(data.get("monthly_income", customer.monthly_income))
    db.session.commit()
    return jsonify({"message": "Customer updated"})


@app.route("/api/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"})


# ===== Requests session with SOCKS5 =====
session = requests.Session()
if SOCKS_PROXY:
    session.proxies = {"http": SOCKS_PROXY, "https": SOCKS_PROXY}
session.headers.update(
    {
        "User-Agent": "uwm-ipq-python/1.0",
        "Accept": "application/json",
    }
)


def normalize_text(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def safe_float(x):
    try:
        if x is None:
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def interest_rate_value(ir):
    """Extract numeric interest rate value.

    The API may return either:
      - a number (e.g., 4.625)
      - an object like { "label": "...", "value": 4.625, "display": true }
    """
    if isinstance(ir, dict):
        return safe_float(ir.get("value"))
    return safe_float(ir)


def to_str_list(v, default: Optional[List[str]] = None) -> List[str]:
    """
    Normalize a value into List[str].

    Accepts:
      - None -> default or []
      - "0, 2,4" -> ["0","2","4"]
      - ["0"] -> ["0"]
      - ["0, 2, 4"] -> ["0","2","4"]
      - [0, 2] -> ["0","2"]
    """
    if v is None:
        return default if default is not None else []

    if isinstance(v, (int, float, bool)):
        return [str(v)]

    if isinstance(v, str):
        parts = [p.strip() for p in v.split(",") if p.strip()]
        return parts if parts else (default if default is not None else [])

    if isinstance(v, list):
        out: List[str] = []
        for item in v:
            if item is None:
                continue
            if isinstance(item, str):
                parts = [p.strip() for p in item.split(",") if p.strip()]
                out.extend(parts)
            else:
                out.append(str(item))
        return out if out else (default if default is not None else [])

    return default if default is not None else []


def parse_api_json(resp: requests.Response) -> Union[Dict[str, Any], List[Any]]:
    try:
        body = resp.json()
    except Exception:
        return {}

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            pass
    return body


def strip_invalid_quote_items(full_body: Any) -> Any:
    if isinstance(full_body, dict):
        cleaned = dict(full_body)
        cleaned.pop("invalidQuoteItems", None)
        return cleaned
    return full_body


def get_access_token() -> str:
    missing = [
        k
        for k, v in {
            "UWM_USERNAME": UWM_USERNAME,
            "UWM_PASSWORD": UWM_PASSWORD,
            "UWM_CLIENT_ID": UWM_CLIENT_ID,
            "UWM_CLIENT_SECRET": UWM_CLIENT_SECRET,
            "UWM_SCOPE": UWM_SCOPE,
        }.items()
        if not v
    ]
    if missing:
        raise RuntimeError(f"Missing required UWM env vars: {', '.join(missing)}")

    data = {
        "grant_type": "password",
        "username": UWM_USERNAME,
        "password": UWM_PASSWORD,
        "client_id": UWM_CLIENT_ID,
        "client_secret": UWM_CLIENT_SECRET,
        "scope": UWM_SCOPE,
    }

    resp = session.post(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"Token request failed ({resp.status_code}): {resp.text}")

    token_json = resp.json()
    access_token = token_json.get("access_token")
    if not access_token:
        raise RuntimeError(f"No access_token in response: {resp.text}")

    return access_token


# -------------------------
# ✅ NEW: strict filter helpers
# -------------------------
def extract_ui_payload_and_allowed_keys(base_payload: Any) -> (Dict[str, Any], set):
    """
    Your UI can send:
      - { "payload": {...}, "excludedFields": [...] }
      - or just {...}

    Returns: (ui_payload_dict, allowed_keys_set)
    The allowed_keys should ONLY include fields that are:
      1. Present in the payload
      2. NOT in excludedFields
    """
    if not isinstance(base_payload, dict):
        return {}, set()

    if "payload" in base_payload and isinstance(base_payload.get("payload"), dict):
        ui_payload = base_payload["payload"]
        excluded_fields = base_payload.get("excludedFields", [])
    else:
        ui_payload = base_payload
        excluded_fields = []

    # Allowed keys = payload keys MINUS excluded fields
    all_keys = set(ui_payload.keys())
    excluded_set = set(excluded_fields)
    allowed_keys = all_keys - excluded_set

    return ui_payload, allowed_keys


def filter_payload_to_allowed_keys(final_payload: Dict[str, Any], allowed_keys: set) -> Dict[str, Any]:
    """
    Keep ONLY keys that were present in the UI payload.
    If allowed_keys is empty, do NOT filter (prevents accidentally sending {}).
    """
    if not allowed_keys:
        return final_payload

    filtered = {}
    for key in allowed_keys:
        if key in final_payload:
            filtered[key] = final_payload[key]

    return filtered


# -------------------------
# existing quote helpers
# -------------------------
def closest_pricepoint_for_item(item: dict, target_amount: float):
    best_pp = None
    best_diff = None

    for pp in (item.get("quotePricePoints") or []):
        fpa = pp.get("finalPriceAfterOriginationFee") or {}
        amt = safe_float(fpa.get("amount"))
        if amt is None:
            continue

        diff = abs(amt - target_amount)
        if best_pp is None or diff < best_diff:
            best_pp = pp
            best_diff = diff

    if not best_pp:
        return None, None

    details = {
        "mortgageProductId": item.get("mortgageProductId"),
        "mortgageProductName": item.get("mortgageProductName"),
        "mortgageProductAlias": item.get("mortgageProductAlias"),
        "interestRate": best_pp.get("interestRate"),
        "finalPriceAfterOriginationFee": best_pp.get("finalPriceAfterOriginationFee"),
        "finalPrice": best_pp.get("finalPrice"),
        "originationFee": best_pp.get("originationFee"),
        "principalAndInterest": best_pp.get("principalAndInterest"),
        "monthlyPayment": best_pp.get("monthlyPayment"),
        "isBestQuotePricePoint": best_pp.get("isBestQuotePricePoint", False),
    }
    return details, best_diff


def customer_to_payload(customer_obj: Any, base_payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Merge customer data into payload.

    If base_payload is provided, it should be the CLEAN payload dict (already extracted).
    This function will preserve all UI values and ONLY override customer-specific fields.
    """
    # If we have a base_payload from the UI, use it as the source-of-truth structure
    if base_payload:
        # Start with a DEEP COPY of the UI-selected payload to preserve all UI values
        import copy
        merged = copy.deepcopy(base_payload)

        # ONLY override customer-specific fields that exist in base_payload
        if hasattr(customer_obj, "name"):
            # Customer is a database object
            if "borrowerName" in merged:
                merged["borrowerName"] = customer_obj.name
            if "creditScore" in merged:
                merged["creditScore"] = customer_obj.credit_score
            if "monthlyIncome" in merged:
                merged["monthlyIncome"] = customer_obj.monthly_income
            if "loanAmount" in merged:
                merged["loanAmount"] = customer_obj.remaining_balance
            if "appraisedValue" in merged:
                merged["appraisedValue"] = customer_obj.property_value
            if "propertyZipCode" in merged:
                merged["propertyZipCode"] = customer_obj.property_zip
            if "propertyCounty" in merged:
                merged["propertyCounty"] = customer_obj.property_county
            if "propertyState" in merged:
                merged["propertyState"] = customer_obj.property_state
        else:
            # Customer is a dict
            if "borrowerName" in merged:
                merged["borrowerName"] = customer_obj.get("borrowerName") or customer_obj.get("name")
            if "creditScore" in merged:
                merged["creditScore"] = customer_obj.get("creditScore") or customer_obj.get("credit_score")
            if "monthlyIncome" in merged:
                merged["monthlyIncome"] = customer_obj.get("monthlyIncome") or customer_obj.get("monthly_income")
            if "loanAmount" in merged:
                merged["loanAmount"] = customer_obj.get("loanAmount") or customer_obj.get("remaining_balance")
            if "appraisedValue" in merged:
                merged["appraisedValue"] = customer_obj.get("appraisedValue") or customer_obj.get("property_value")
            if "propertyZipCode" in merged:
                merged["propertyZipCode"] = customer_obj.get("propertyZipCode") or customer_obj.get("property_zip")
            if "propertyCounty" in merged:
                merged["propertyCounty"] = customer_obj.get("propertyCounty") or customer_obj.get("property_county")
            if "propertyState" in merged:
                merged["propertyState"] = customer_obj.get("propertyState") or customer_obj.get("property_state")

        # ✅ CRITICAL: Normalize all ID fields to strings
        # The UWM API requires these to be strings, not numbers
        string_fields = [
            'monthsOfReservesId', 'monthsOfBankStatementsId', 'commitmentPeriodId',
            'occupancyTypeId', 'propertyTypeId', 'compensationPayerTypeID',
            'escrowWaiverTypeId', 'tracTypeId', 'loanShieldTypeId', 'paPlusTypeId',
            'exactRateTypeId', 'purposeTypeID', 'numberOfBorrowers'
        ]
        for field in string_fields:
            if field in merged and merged[field] is not None:
                merged[field] = str(merged[field])

        # ✅ RETURN HERE - do NOT run the fallback code that adds defaults!
        return merged

    # Fallback: If no base_payload, build from customer data
    # This happens when using /api/analyze/direct WITHOUT a template
    merged = {}
    if hasattr(customer_obj, "name"):
        merged["borrowerName"] = customer_obj.name
        merged["creditScore"] = customer_obj.credit_score
        merged["monthlyIncome"] = customer_obj.monthly_income
        merged["loanAmount"] = customer_obj.remaining_balance
        merged["appraisedValue"] = customer_obj.property_value
        merged["propertyZipCode"] = customer_obj.property_zip
        merged["propertyCounty"] = customer_obj.property_county
        merged["propertyState"] = customer_obj.property_state
    else:
        # Customer is a dict - extract what they provided
        merged["borrowerName"] = customer_obj.get("borrowerName") or customer_obj.get("name")
        merged["creditScore"] = customer_obj.get("creditScore") or customer_obj.get("credit_score")
        merged["monthlyIncome"] = customer_obj.get("monthlyIncome") or customer_obj.get("monthly_income")
        merged["loanAmount"] = customer_obj.get("loanAmount") or customer_obj.get("remaining_balance")
        merged["appraisedValue"] = customer_obj.get("appraisedValue") or customer_obj.get("property_value")
        merged["propertyZipCode"] = customer_obj.get("propertyZipCode") or customer_obj.get("property_zip")
        merged["propertyCounty"] = customer_obj.get("propertyCounty") or customer_obj.get("property_county")
        merged["propertyState"] = customer_obj.get("propertyState") or customer_obj.get("property_state")

        # Also copy all other fields they provided
        for key, value in customer_obj.items():
            if key not in merged:
                merged[key] = value

    # Ensure monthlyIncome is valid
    monthly_income = merged.get("monthlyIncome", 20000)
    mi = safe_float(monthly_income)
    if mi is None or mi < 1:
        monthly_income = 20000

    # Normalize loanTypeIds
    lt_ids = to_str_list(merged.get("loanTypeIds"), default=["0"])

    # Correct casing for purposeTypeId
    purpose_type_id = str(merged.get("purposeTypeId") or merged.get("purposeTypeID", "3"))
    if purpose_type_id == "3" and len(lt_ids) > 1:
        lt_ids = [lt_ids[0]]

    # Never send these
    merged.pop("chatId", None)
    merged.pop("closingType", None)

    # Build your canonical payload (may include defaults)
    # ✅ BUT we will strict-filter it before sending to UWM (see /api/analyze and /api/analyze/direct)
    return {
        "brokerAlias": merged.get("brokerAlias", "TEST"),
        "loanOfficer": merged.get("loanOfficer", "lofficer@email.com"),
        "borrowerName": merged.get("borrowerName"),
        "purposeTypeID": purpose_type_id,
        "loanTypeIds": lt_ids,
        "refinancePurposeId": merged.get("refinancePurposeId", "Rate And Term Reduction-CONV"),
        "salesPrice": merged.get("salesPrice", 0),
        "appraisedValue": merged.get("appraisedValue"),
        "loanAmount": merged.get("loanAmount"),
        "secondLoanAmount": merged.get("secondLoanAmount", 0),
        "occupancyTypeId": str(merged.get("occupancyTypeId", "1")),
        "propertyTypeId": str(merged.get("propertyTypeId", "22")),
        "propertyZipCode": str(merged.get("propertyZipCode")),
        "propertyCounty": merged.get("propertyCounty", ""),
        "propertyState": merged.get("propertyState", ""),
        "creditScore": int(merged.get("creditScore", 0)),
        "commitmentPeriodId": str(merged.get("commitmentPeriodId", "13")),
        "isCorrespondent": bool(merged.get("isCorrespondent", False)),
        "isDTIOver45Percent": bool(merged.get("isDTIOver45Percent", False)),
        "monthlyDebt": merged.get("monthlyDebt", 0),
        "annualTaxes": merged.get("annualTaxes", 0),
        "annualHomeownersInsurance": merged.get("annualHomeownersInsurance", 0),
        "annualPercentageRateFees": merged.get("annualPercentageRateFees", 0),
        "selfEmployed": bool(merged.get("selfEmployed", False)),
        "monthsOfBankStatementsId": str(merged.get("monthsOfBankStatementsId", "0")),
        "monthsOfReservesId": str(merged.get("monthsOfReservesId", "0")),
        "numberOfBorrowers": int(merged.get("numberOfBorrowers", 1)),
        "compensationPayerTypeID": str(merged.get("compensationPayerTypeID", "1")),
        "escrowWaiverTypeId": str(merged.get("escrowWaiverTypeId", "1")),
        "includeFlexTerms": bool(merged.get("includeFlexTerms", False)),
        "tracTypeId": str(merged.get("tracTypeId", "0")),
        "waivableFeeTypeIds": to_str_list(merged.get("waivableFeeTypeIds"), default=["0"]),
        "loanShieldTypeId": str(merged.get("loanShieldTypeId", "0")),
        "paPlusTypeId": str(merged.get("paPlusTypeId", "0")),
        "exactRateTypeId": str(merged.get("exactRateTypeId", "2")),
        "targetPriceValue": merged.get("targetPriceValue", 0),
        "targetCashValue": merged.get("targetCashValue", 0),
        "waiveUnderwritingFee": bool(merged.get("waiveUnderwritingFee", False)),
        "monthlyIncome": monthly_income,
        "buyDownAliasID": merged.get("buyDownAliasID", "2-1 LLPA"),
        "firstTimeHomeBuyer": bool(merged.get("firstTimeHomeBuyer", False)),
        "loanTermIds": to_str_list(merged.get("loanTermIds"), default=["4", "3", "1", "2", "0"]),
        "numberOfUnits": int(merged.get("numberOfUnits", 1)),
        "attachmentTypeId": merged.get("attachmentTypeId"),
        "prepaymentPenaltyId": merged.get("prepaymentPenaltyId"),
        "numberOfFinancedProperties": merged.get("numberOfFinancedProperties"),
        "leaseTypeId": merged.get("leaseTypeId"),
        "isFirstTimeInvestor": merged.get("isFirstTimeInvestor"),
        "debtServiceCoverageRatio": merged.get("debtServiceCoverageRatio"),
        "mortgageInsuranceType": merged.get("mortgageInsuranceType"),
        "controlYourPrice": merged.get("controlYourPrice", 0),
        "targetRateValue": merged.get("targetRateValue", 0),
        "financedMortgageInsuranceTypeId": merged.get("financedMortgageInsuranceTypeId"),
        "useMortgageInsuranceTypeIds": to_str_list(merged.get("useMortgageInsuranceTypeIds"), default=None),
        "federalHousingAdministrationSecondarySourceTypeId": merged.get(
            "federalHousingAdministrationSecondarySourceTypeId"
        ),
        "tracIncentiveID": merged.get("tracIncentiveID"),
    }


def post_price_quote(access_token: str, payload: dict) -> requests.Response:
    # Wrap payload in the required priceQuoteRequest object

    return session.post(
        PRICEQUOTE_URL,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )


def is_texas_zip(zip_code):
    try:
        z = int(str(zip_code).strip())
        return 73301 <= z <= 88595
    except (ValueError, TypeError):
        return False


def qualifying_products_for_customer(
        quote_body: Dict[str, Any],
        current_monthly_payment: float,
        target_amount: float,
        customer_zip: str = "",
        min_savings: float = 200.0,
        tolerance: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Find qualifying products for a customer, grouped by loan term.
    Returns a list where each item represents one loan term's products.
    """
    # Group products by loan term (actualTermYears)
    products_by_term = {}

    is_tx_zip = is_texas_zip(customer_zip)

    for item in (quote_body.get("validQuoteItems") or []):
        actual_term = item.get("actualTermYears")
        product_name = item.get("mortgageProductName", "")
        product_id = item.get("mortgageProductId")

        # Texas Zip filtering: ignore QuoteItems with "Texas" in name if not a Texas zip
        if not is_tx_zip and "Texas" in product_name:
            continue

        # Create a key for grouping: (term, product_name, product_id)
        term_key = (actual_term, product_name, product_id)

        if term_key not in products_by_term:
            products_by_term[term_key] = {
                "actualTermYears": actual_term,
                "mortgageProductName": product_name,
                "mortgageProductId": product_id,
                "mortgageProductAlias": item.get("mortgageProductAlias"),
                "products": []
            }

        for pp in (item.get("quotePricePoints") or []):
            fpa = pp.get("finalPriceAfterOriginationFee") or {}
            amount = safe_float(fpa.get("amount"))
            if amount is None:
                continue

            if tolerance is not None and abs(amount - target_amount) > tolerance:
                continue

            mp_val = safe_float((pp.get("monthlyPayment") or {}).get("value"))
            if mp_val is None:
                continue

            savings = current_monthly_payment - mp_val
            if savings < min_savings:
                continue

            ir_obj = pp.get("interestRate")
            rate_val = interest_rate_value(ir_obj)

            products_by_term[term_key]["products"].append({
                "closestAmount": amount,
                "amountDiff": abs(amount - target_amount),
                "matchedMonthlyPayment": mp_val,
                "currentMonthlyPayment": current_monthly_payment,
                "monthlySavings": round(savings, 2),
                "interestRate": ir_obj,
                "rateValue": rate_val,
                "finalPriceAfterOriginationFee": pp.get("finalPriceAfterOriginationFee"),
                "originationFee": pp.get("originationFee"),
                "finalPrice": pp.get("finalPrice"),
                "isClosest": False # Will be set later
            })

    # Process each term group
    result = []
    for term_key, term_data in products_by_term.items():
        all_products = term_data["products"]

        if not all_products:
            continue

        # Find the closest to target_amount for this term
        all_products.sort(key=lambda x: x["amountDiff"])
        all_products[0]["isClosest"] = True
        closest = all_products[0]

        target_rate = closest.get("rateValue")
        if target_rate is None:
            selected = [closest]
        else:
            higher = [p for p in all_products if p.get("rateValue") is not None and p["rateValue"] > target_rate]
            lower = [p for p in all_products if p.get("rateValue") is not None and p["rateValue"] < target_rate]

            # 2 higher (nearest above target) + 3 lower (nearest below target)
            higher.sort(key=lambda x: x["rateValue"])
            lower.sort(key=lambda x: x["rateValue"], reverse=True)

            selected = [closest]
            selected.extend(higher[:2])
            selected.extend(lower[:3])

        # Sort by interest rate for display (lowest rate first)
        selected.sort(key=lambda x: (x.get("rateValue") is None, x.get("rateValue")))

        # Add term information to the result
        result.append({
            "actualTermYears": term_data["actualTermYears"],
            "mortgageProductName": term_data["mortgageProductName"],
            "mortgageProductId": term_data["mortgageProductId"],
            "mortgageProductAlias": term_data["mortgageProductAlias"],
            "products": selected
        })

    # Sort by term length (shortest first)
    result.sort(key=lambda x: (x["actualTermYears"] is None, x["actualTermYears"]))

    return result


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    static_folder = str(app.static_folder) if app.static_folder else "static"
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    return send_from_directory(static_folder, "index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        min_savings = float(request.form.get("min_savings", 200))
        target_amount = float(request.form.get("target_amount", -2000))
        tolerance_str = request.form.get("tolerance")
        tolerance = float(tolerance_str) if (tolerance_str and tolerance_str.strip()) else None

        base_payload_str = request.form.get("base_payload")
        base_payload_raw = json.loads(base_payload_str) if base_payload_str else {}

        logger.info("=" * 80)
        logger.info("RECEIVED base_payload_raw:\n%s", json.dumps(base_payload_raw, indent=2))

        # ✅ Extract UI payload and allowed keys ONCE here
        ui_payload, allowed_keys = extract_ui_payload_and_allowed_keys(base_payload_raw)

        logger.info("-" * 80)
        logger.info("EXTRACTED ui_payload:\n%s", json.dumps(ui_payload, indent=2))
        logger.info("ALLOWED KEYS: %s", sorted(allowed_keys))
        logger.info("=" * 80)

        customers = Customer.query.all()
        access_token = get_access_token()

        # Three buydown scenarios to test
        buydown_scenarios = [
            {"label": "No Buydown", "value": "None"},
            {"label": "1-0 LLPA Buydown", "value": "1-0 LLPA"},
            {"label": "2-1 LLPA Buydown", "value": "2-1 LLPA"},
        ]

        results = []
        for customer in customers:
            # Add a small delay between customers if not the first one
            if results:
                import time
                time.sleep(1.0)  # 1 second delay between customers

            current_mp = customer.current_monthly_payment

            logger.info("=" * 80)
            logger.info("Analyzing customer: %s", customer.name)

            # Run analysis for each buydown scenario
            scenario_results = []
            for scenario in buydown_scenarios:
                logger.info("-" * 80)
                logger.info("Testing buydown scenario: %s", scenario["label"])

                # Create a copy of ui_payload with this buydown value
                import copy
                scenario_payload = copy.deepcopy(ui_payload) if ui_payload else {}
                scenario_payload["buyDownAliasID"] = scenario["value"]

                # Build payload with customer data merged into UI payload
                payload = customer_to_payload(customer, scenario_payload)

                # STRICT FILTER: remove any field not present in UI payload
                payload = filter_payload_to_allowed_keys(payload, allowed_keys)

                logger.info("FINAL PAYLOAD TO UWM for %s (buydown=%s):\n%s",
                            customer.name,
                            scenario["value"],
                            json.dumps(payload, indent=2))
                logger.info("-" * 80)

                resp = post_price_quote(access_token, payload)

                if resp.status_code != 200:
                    logger.error(
                        f"Quote failed for {payload.get('borrowerName')} with buydown {scenario['value']}: {resp.text}")
                    scenario_results.append({
                        "scenario": scenario["label"],
                        "buyDownAliasID": scenario["value"],
                        "error": resp.text,
                        "termGroups": []
                    })
                    continue

                quote_body = parse_api_json(resp)
                if not isinstance(quote_body, dict):
                    logger.error(
                        f"Unexpected response type for {payload.get('borrowerName')}: {type(quote_body)}"
                    )
                    scenario_results.append({
                        "scenario": scenario["label"],
                        "buyDownAliasID": scenario["value"],
                        "error": "Invalid response format",
                        "termGroups": []
                    })
                    continue

                customer_zip = customer.property_zip if hasattr(customer, 'property_zip') else customer.get('property_zip', '')
                qualifying = qualifying_products_for_customer(
                    quote_body, current_mp, target_amount, customer_zip, min_savings, tolerance
                )

                scenario_results.append({
                    "scenario": scenario["label"],
                    "buyDownAliasID": scenario["value"],
                    "termGroups": qualifying,
                    "fullResponse": strip_invalid_quote_items(quote_body),
                })

            # Add customer result with all scenarios
            if scenario_results:
                results.append({
                    "name": customer.name,
                    "currentMonthlyPayment": current_mp,
                    "scenarios": scenario_results,
                })

        return jsonify(results)

    except Exception as e:
        logger.error(f"Error in analyze: {e}", exc_info=True)
        return jsonify({"message": str(e)}), 500


@app.route("/api/analyze/direct", methods=["POST"])
def analyze_direct():
    """
    Direct mode runs 3 analyses with different buyDownAliasID values:
    - None
    - 1-0 LLPA
    - 2-1 LLPA
    """
    try:
        content = request.json
        if not content:
            return jsonify({"message": "No data provided"}), 400

        if isinstance(content, dict):
            content = [content]
        elif not isinstance(content, list):
            return jsonify({"message": "JSON must be a list or object"}), 400

        min_savings = float(request.args.get("min_savings", 200))
        target_amount = float(request.args.get("target_amount", -2000))
        tolerance_str = request.args.get("tolerance")
        tolerance = float(tolerance_str) if (tolerance_str and tolerance_str.strip()) else None

        access_token = get_access_token()

        # Three buydown scenarios to test
        buydown_scenarios = [
            {"label": "No Buydown", "value": "None"},
            {"label": "1-0 LLPA Buydown", "value": "1-0 LLPA"},
            {"label": "2-1 LLPA Buydown", "value": "2-1 LLPA"},
        ]

        results = []
        for idx, customer in enumerate(content):
            if not isinstance(customer, dict):
                continue

            # Add a small delay between customers if not the first one
            if idx > 0:
                import time
                time.sleep(1.0)  # 1 second delay between customers

            current_mp = safe_float(customer.get("currentMonthlyPayment"))
            if current_mp is None:
                current_mp = 2000.0

            logger.info("=" * 80)
            logger.info("DIRECT MODE - Customer %d: %s", idx + 1, customer.get("borrowerName", "Unknown"))

            # Run analysis for each buydown scenario
            scenario_results = []
            for scenario in buydown_scenarios:
                logger.info("-" * 80)
                logger.info("Testing buydown scenario: %s", scenario["label"])

                # Create a copy of customer with this buydown value
                customer_copy = customer.copy()
                customer_copy["buyDownAliasID"] = scenario["value"]

                # Allowed keys are exactly what caller provided
                allowed_keys = set(customer_copy.keys())

                # Pass customer as BOTH the data source AND base_payload
                payload = customer_to_payload(customer_copy, base_payload=customer_copy)

                # STRICT FILTER: only caller-provided keys survive
                payload = filter_payload_to_allowed_keys(payload, allowed_keys)

                logger.info("FINAL PAYLOAD TO UWM (buydown=%s):\n%s",
                            scenario["value"],
                            json.dumps(payload, indent=2))

                resp = post_price_quote(access_token, payload)
                if resp.status_code != 200:
                    logger.error(
                        f"Quote failed for {payload.get('borrowerName')} with buydown {scenario['value']}: {resp.text}")
                    scenario_results.append({
                        "scenario": scenario["label"],
                        "buyDownAliasID": scenario["value"],
                        "error": resp.text,
                        "termGroups": []
                    })
                    continue

                quote_body = parse_api_json(resp)
                if not isinstance(quote_body, dict):
                    logger.error(
                        f"Unexpected response type for {payload.get('borrowerName')}: {type(quote_body)}"
                    )
                    scenario_results.append({
                        "scenario": scenario["label"],
                        "buyDownAliasID": scenario["value"],
                        "error": "Invalid response format",
                        "termGroups": []
                    })
                    continue

                customer_zip = customer.property_zip if hasattr(customer, 'property_zip') else customer.get('property_zip', '')
                qualifying = qualifying_products_for_customer(
                    quote_body, current_mp, target_amount, customer_zip, min_savings, tolerance
                )

                scenario_results.append({
                    "scenario": scenario["label"],
                    "buyDownAliasID": scenario["value"],
                    "termGroups": qualifying,
                    "fullResponse": strip_invalid_quote_items(quote_body),
                })

            # Add customer result with all scenarios
            if scenario_results:
                results.append({
                    "name": customer.get("borrowerName") or customer.get("name") or "Unknown",
                    "currentMonthlyPayment": current_mp,
                    "scenarios": scenario_results,
                })

        return jsonify(results)

    except Exception as e:
        logger.error(f"Error in analyze_direct: {e}", exc_info=True)
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)