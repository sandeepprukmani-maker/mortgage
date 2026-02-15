import os
import json
import re
import requests
import logging
import uuid
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
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

# Zipcode database (subset - in production use a complete database or API)
ZIPCODE_DATA = {}


def load_zipcode_database():
    """Load zipcode to state/county mapping"""
    # This is a simplified version. In production, use:
    # - A complete zipcode database
    # - An external API (e.g., Zippopotam.us, Google Maps API)
    # - A database table with all US zipcodes
    # For now, we'll use a public API
    pass


app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mortgage_analyzer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

with app.app_context():
    db.init_app(app)
    db.create_all()


# ===== ZIPCODE LOOKUP =====
@app.route("/api/zipcode/<zipcode>", methods=["GET"])
def lookup_zipcode(zipcode):
    try:
        if not re.match(r"^\d{5}$", zipcode):
            return jsonify({"error": "Invalid zipcode format", "success": False}), 400

        # 1) Zippopotam: city/state + lat/lon
        zp = requests.get(
            f"https://api.zippopotam.us/us/{zipcode}",
            timeout=5,
            headers={"User-Agent": "zipcode-lookup/1.0"},
        )

        if zp.status_code == 404:
            return jsonify({"error": "Zipcode not found", "success": False}), 404
        if zp.status_code != 200:
            return jsonify({"error": "Lookup service unavailable", "success": False}), 503

        data = zp.json()
        place = (data.get("places") or [{}])[0]

        city = place.get("place name", "") or ""
        state = place.get("state abbreviation", "") or ""

        # lat/lon are strings in this API
        lat = place.get("latitude")
        lon = place.get("longitude")

        county_name = ""
        county_fips = ""

        # 2) Census Geocoder: county from coordinates (if we have lat/lon)
        if lat and lon:
            cg = requests.get(
                "https://geocoding.geo.census.gov/geocoder/geographies/coordinates",
                params={
                    "x": lon,
                    "y": lat,
                    "benchmark": "Public_AR_Current",
                    "vintage": "Current_Current",
                    "format": "json",
                },
                timeout=5,
                headers={"User-Agent": "zipcode-lookup/1.0"},
            )

            if cg.status_code == 200:
                gj = cg.json()
                # structure: result -> geographies -> "Counties" -> [ { NAME, GEOID, ... } ]
                counties = (
                    (gj.get("result") or {})
                    .get("geographies", {})
                    .get("Counties", [])
                )
                if counties:
                    county_name = counties[0].get("NAME", "") or ""
                    county_fips = counties[0].get("GEOID", "") or ""

        return jsonify({
            "zipcode": zipcode,
            "state": state,
            "city": city,
            "county": county_name,        # real county name (best-effort)
            "countyFips": county_fips,    # optional but useful
            "latitude": lat,
            "longitude": lon,
            "success": True,
        }), 200

    except requests.Timeout:
        return jsonify({"error": "Lookup service timeout", "success": False}), 504
    except requests.RequestException as e:
        logger.error(f"Zipcode lookup request error: {e}")
        return jsonify({"error": "Lookup failed", "success": False}), 502
    except Exception as e:
        logger.exception(f"Zipcode lookup error: {e}")
        return jsonify({"error": "Lookup failed", "success": False}), 500


# ===== Requests session with SOCKS5 =====
session = requests.Session()
if SOCKS_PROXY:
    session.proxies = {"http": SOCKS_PROXY, "https": SOCKS_PROXY}
session.headers.update({
    "User-Agent": "uwm-ipq-python/1.0",
    "Accept": "application/json",
})


def safe_float(x):
    try:
        if x is None:
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def interest_rate_value(ir):
    """Extract numeric interest rate value."""
    if isinstance(ir, dict):
        return safe_float(ir.get("value"))
    return safe_float(ir)


# =========================
# FIX: Robust JSON parsing
# =========================
def coerce_json_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Ensure obj is a dict.
    Handles:
      - already-a-dict
      - JSON returned as a quoted string (stringified JSON)
      - double-stringified JSON
      - top-level list -> wrapped in {"_list": [...]}
    """
    if isinstance(obj, dict):
        return obj

    if isinstance(obj, list):
        return {"_list": obj}

    if isinstance(obj, str):
        s = obj.strip()
        # Try up to 2 rounds (common for nested/double-encoded)
        for _ in range(2):
            try:
                parsed = json.loads(s)
            except Exception:
                break

            if isinstance(parsed, dict):
                return parsed
            if isinstance(parsed, list):
                return {"_list": parsed}
            if isinstance(parsed, str):
                s = parsed.strip()
                continue
            break

    return {}


def parse_response_json(resp: requests.Response) -> Dict[str, Any]:
    """
    Safely parse response to a dict, even if server returns stringified JSON.
    """
    try:
        data = resp.json()
    except Exception:
        data = resp.text

    data = coerce_json_to_dict(data)

    # If still empty, try parsing resp.text explicitly
    if not data:
        try:
            data = coerce_json_to_dict(resp.text)
        except Exception:
            return {}

    return data


def get_access_token() -> str:
    missing = [
        k for k, v in {
            "UWM_USERNAME": UWM_USERNAME,
            "UWM_PASSWORD": UWM_PASSWORD,
            "UWM_CLIENT_ID": UWM_CLIENT_ID,
            "UWM_CLIENT_SECRET": UWM_CLIENT_SECRET,
            "UWM_SCOPE": UWM_SCOPE,
        }.items() if not v
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
        timeout=30
    )

    if resp.status_code != 200:
        raise RuntimeError(f"Token request failed ({resp.status_code}): {resp.text}")

    token_json = resp.json()
    access_token = token_json.get("access_token")
    if not access_token:
        raise RuntimeError(f"No access_token in response: {resp.text}")

    return access_token


def post_price_quote(access_token: str, payload: dict) -> requests.Response:
    return session.post(
        PRICEQUOTE_URL,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )


def build_payload_from_customer(customer: Customer, base_payload: dict) -> dict:
    """Build API payload from customer data and template"""
    import copy
    payload = copy.deepcopy(base_payload)

    # Override customer-specific fields
    if "borrowerName" in payload:
        payload["borrowerName"] = customer.name
    if "creditScore" in payload:
        payload["creditScore"] = customer.credit_score
    if "monthlyIncome" in payload:
        payload["monthlyIncome"] = customer.monthly_income
    if "loanAmount" in payload:
        payload["loanAmount"] = customer.remaining_balance
    if "appraisedValue" in payload:
        payload["appraisedValue"] = customer.property_value
    if "propertyZipCode" in payload:
        payload["propertyZipCode"] = customer.property_zip
    if "propertyState" in payload:
        payload["propertyState"] = customer.property_state
    if "propertyCounty" in payload:
        payload["propertyCounty"] = customer.property_county or ""

    # Normalize ID fields to strings
    string_fields = [
        "monthsOfReservesId", "monthsOfBankStatementsId", "commitmentPeriodId",
        "occupancyTypeId", "propertyTypeId", "compensationPayerTypeID",
        "escrowWaiverTypeId", "tracTypeId", "loanShieldTypeId", "paPlusTypeId",
        "exactRateTypeId", "purposeTypeID", "numberOfBorrowers"
    ]
    for field in string_fields:
        if field in payload and payload[field] is not None:
            payload[field] = str(payload[field])

    return payload


def calculate_buydown_details(base_rate: float, buydown_type: str, loan_amount: float, term_years: int):
    """Calculate year-by-year savings for buydown products"""
    if buydown_type == "None":
        return None

    # Parse buydown type (e.g., "2-1 LLPA" means -2% year 1, -1% year 2)
    if "2-1" in buydown_type:
        year1_reduction = 2.0
        year2_reduction = 1.0
    elif "1-0" in buydown_type:
        year1_reduction = 1.0
        year2_reduction = 0.0
    else:
        return None

    total_months = term_years * 12

    year1_rate = base_rate - year1_reduction
    year2_rate = base_rate - year2_reduction if year2_reduction > 0 else base_rate
    year3_rate = base_rate

    # Monthly payment calculation: M = P[r(1+r)^n]/[(1+r)^n – 1]
    def monthly_payment(principal, annual_rate, months):
        if annual_rate == 0:
            return principal / months
        monthly_rate = annual_rate / 100 / 12
        return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

    year1_payment = monthly_payment(loan_amount, year1_rate, total_months)
    year2_payment = monthly_payment(loan_amount, year2_rate, total_months)
    year3_payment = monthly_payment(loan_amount, year3_rate, total_months)

    return {
        "year1": {"rate": year1_rate, "monthlyPayment": round(year1_payment, 2)},
        "year2": {"rate": year2_rate, "monthlyPayment": round(year2_payment, 2)},
        "year3": {"rate": year3_rate, "monthlyPayment": round(year3_payment, 2)},
    }


# ===== SCREEN 1: Lead Generation =====
@app.route("/api/screen1/analyze", methods=["POST"])
def screen1_analyze():
    """
    Screen 1: Lead Generation
    Returns list of customers who can save minimum amount with contact details
    """
    try:
        data = request.json
        min_savings = float(data.get("min_savings", 200))
        target_amount = float(data.get("target_amount", -2000))
        base_payload = data.get("payload", {})

        logger.info("Screen 1 Analysis - Min Savings: $%.2f", min_savings)

        # Get all current customers
        customers = Customer.get_current_customers()
        access_token = get_access_token()

        # Buydown scenarios
        buydown_scenarios = ["None", "1-0 LLPA", "2-1 LLPA"]

        qualifying_leads = []

        for customer in customers:
            logger.info(f"Analyzing customer: {customer.name}")
            current_payment = customer.current_monthly_payment

            # Try all buydown scenarios
            for buydown in buydown_scenarios:
                payload = build_payload_from_customer(customer, base_payload)
                payload["buyDownAliasID"] = buydown

                # Try all loan terms if multiple specified
                loan_terms = payload.get("loanTermIds", ["4"])
                for term in loan_terms:
                    payload_copy = payload.copy()
                    payload_copy["loanTermIds"] = [term]

                    resp = post_price_quote(access_token, payload_copy)
                    if resp.status_code != 200:
                        continue

                    quote_body = parse_response_json(resp)
                    if not isinstance(quote_body, dict) or not quote_body:
                        logger.warning(
                            "Screen1: Could not parse quote response as dict. status=%s body_snip=%r",
                            resp.status_code, (resp.text or "")[:300]
                        )
                        continue

                    # Check each product
                    for item in quote_body.get("validQuoteItems", []):
                        for pp in item.get("quotePricePoints", []):
                            mp_val = safe_float((pp.get("monthlyPayment") or {}).get("value"))
                            if mp_val is None:
                                continue

                            savings = current_payment - mp_val
                            if savings >= min_savings:
                                # Found a qualifying product!
                                rate_val = interest_rate_value(pp.get("interestRate"))
                                fpa = pp.get("finalPriceAfterOriginationFee") or {}

                                qualifying_leads.append({
                                    "customer_key": customer.customer_key,
                                    "name": customer.name,
                                    "phone": customer.phone,
                                    "email": customer.email,
                                    "current_payment": current_payment,
                                    "new_payment": mp_val,
                                    "monthly_savings": round(savings, 2),
                                    "annual_savings": round(savings * 12, 2),
                                    "product_name": item.get("mortgageProductName"),
                                    "product_alias": item.get("mortgageProductAlias"),
                                    "term_years": item.get("actualTermYears"),
                                    "interest_rate": rate_val,
                                    "buydown_type": buydown,
                                    "credit_cost": safe_float(fpa.get("amount")),
                                })
                                break  # Found one, move to next customer
                        if qualifying_leads and qualifying_leads[-1]["name"] == customer.name:
                            break
                    if qualifying_leads and qualifying_leads[-1]["name"] == customer.name:
                        break
                if qualifying_leads and qualifying_leads[-1]["name"] == customer.name:
                    break

        return jsonify({
            "total_leads": len(qualifying_leads),
            "leads": qualifying_leads
        })

    except Exception as e:
        logger.error(f"Error in screen1_analyze: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# ===== SCREEN 2: Payload Builder (already exists in your code) =====
# No changes needed - reuse existing payload builder


# ===== SCREEN 3: Customer Management with SCD Type 2 =====
@app.route("/api/customers", methods=["GET"])
def get_customers():
    """Get all current customers"""
    customers = Customer.get_current_customers()
    return jsonify([c.to_dict() for c in customers])


@app.route("/api/customers/<customer_key>/history", methods=["GET"])
def get_customer_history(customer_key):
    """Get all versions of a customer"""
    history = Customer.get_customer_history(customer_key)
    return jsonify([c.to_dict() for c in history])


@app.route("/api/customers", methods=["POST"])
def add_customer():
    """Add a new customer"""
    data = request.json

    customer_key = str(uuid.uuid4())
    new_customer = Customer(
        customer_key=customer_key,
        version=1,
        name=data.get("name"),
        phone=data.get("phone"),
        email=data.get("email"),
        current_monthly_payment=safe_float(data.get("current_monthly_payment")),
        remaining_balance=safe_float(data.get("remaining_balance")),
        property_value=safe_float(data.get("property_value")),
        property_zip=data.get("property_zip"),
        property_county=data.get("property_county"),
        property_state=data.get("property_state"),
        credit_score=int(data.get("credit_score", 0)),
        monthly_income=safe_float(data.get("monthly_income")),
        is_current=True,
        effective_date=datetime.now(timezone.utc),
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer added", "customer_key": customer_key})


@app.route("/api/customers/<customer_key>", methods=["PUT"])
def update_customer(customer_key):
    """Update customer - implements SCD Type 2"""
    data = request.json

    # Get current version
    current = Customer.get_current_by_key(customer_key)
    if not current:
        return jsonify({"error": "Customer not found"}), 404

    # Close current record
    current.is_current = False
    current.end_date = datetime.now(timezone.utc)

    # Create new version
    new_version = Customer(
        customer_key=customer_key,
        version=current.version + 1,
        name=data.get("name", current.name),
        phone=data.get("phone", current.phone),
        email=data.get("email", current.email),
        current_monthly_payment=safe_float(data.get("current_monthly_payment", current.current_monthly_payment)),
        remaining_balance=safe_float(data.get("remaining_balance", current.remaining_balance)),
        property_value=safe_float(data.get("property_value", current.property_value)),
        property_zip=data.get("property_zip", current.property_zip),
        property_county=data.get("property_county", current.property_county),
        property_state=data.get("property_state", current.property_state),
        credit_score=int(data.get("credit_score", current.credit_score)),
        monthly_income=safe_float(data.get("monthly_income", current.monthly_income)),
        is_current=True,
        effective_date=datetime.now(timezone.utc),
    )

    db.session.add(new_version)
    db.session.commit()

    return jsonify({"message": "Customer updated", "version": new_version.version})


@app.route("/api/customers/<customer_key>", methods=["DELETE"])
def delete_customer(customer_key):
    """Soft delete - mark as inactive"""
    current = Customer.get_current_by_key(customer_key)
    if not current:
        return jsonify({"error": "Customer not found"}), 404

    current.is_current = False
    current.end_date = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"message": "Customer deactivated"})


# ===== SCREEN 3: Detailed Analysis for Single Customer =====
@app.route("/api/customers/<customer_key>/analyze", methods=["POST"])
def analyze_customer_detailed(customer_key):
    """
    Detailed analysis for a single customer with buydown comparison
    Shows year-by-year breakdown
    ✅ UPDATED: Checks if customer qualifies based on min_savings & target_amount
    """
    try:
        data = request.json
        base_payload = data.get("payload", {})
        min_savings = float(data.get("min_savings", 200))
        target_amount = float(data.get("target_amount", -2000))

        customer = Customer.get_current_by_key(customer_key)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        access_token = get_access_token()
        buydown_scenarios = ["None", "1-0 LLPA", "2-1 LLPA"]

        results = []
        has_qualifying_product = False  # ✅ Track if ANY product qualifies

        for buydown in buydown_scenarios:
            payload = build_payload_from_customer(customer, base_payload)
            payload["buyDownAliasID"] = buydown

            resp = post_price_quote(access_token, payload)
            logger.info(f"Price quote response for {customer.name} ({buydown}): {resp.status_code}")

            if resp.status_code != 200:
                results.append({
                    "buydown_type": buydown,
                    "error": resp.text,
                    "products": []
                })
                continue

            quote_body = parse_response_json(resp)
            if not isinstance(quote_body, dict) or not quote_body:
                results.append({
                    "buydown_type": buydown,
                    "error": f"Could not parse response as JSON object. status={resp.status_code}",
                    "raw": (resp.text[:2000] if resp.text else ""),
                    "products": []
                })
                continue

            products_by_term = {}

            # Group by term
            for item in quote_body.get("validQuoteItems", []):
                term = item.get("actualTermYears")
                product_name = item.get("mortgageProductName")

                key = (term, product_name)
                if key not in products_by_term:
                    products_by_term[key] = {
                        "term_years": term,
                        "product_name": product_name,
                        "product_alias": item.get("mortgageProductAlias"),
                        "rates": []
                    }

                for pp in item.get("quotePricePoints", []):
                    mp_val = safe_float((pp.get("monthlyPayment") or {}).get("value"))
                    if mp_val is None:
                        continue

                    savings = customer.current_monthly_payment - mp_val

                    # ✅ Check if this product qualifies
                    qualifies = savings >= min_savings
                    if qualifies:
                        has_qualifying_product = True

                    rate_val = interest_rate_value(pp.get("interestRate"))
                    fpa = pp.get("finalPriceAfterOriginationFee") or {}

                    # Calculate buydown details
                    buydown_details = calculate_buydown_details(
                        rate_val, buydown, customer.remaining_balance, term
                    )

                    products_by_term[key]["rates"].append({
                        "interest_rate": rate_val,
                        "monthly_payment": mp_val,
                        "monthly_savings": round(savings, 2),
                        "credit_cost": safe_float(fpa.get("amount")),
                        "buydown_breakdown": buydown_details,
                        "qualifying": qualifies  # ✅ Mark if qualifies
                    })

            # Sort rates by interest rate (lowest first)
            for product in products_by_term.values():
                product["rates"].sort(key=lambda x: x.get("interest_rate") if x.get("interest_rate") is not None else 999)

            results.append({
                "buydown_type": buydown,
                "products": list(products_by_term.values())
            })

        return jsonify({
            "customer": customer.to_dict(),
            "scenarios": results,
            "target_amount": target_amount,
            "min_savings": min_savings,
            "has_qualifying_product": has_qualifying_product,  # ✅ Return qualification status
            "results": results  # ✅ For frontend compatibility
        })

    except Exception as e:
        logger.error(f"Error in analyze_customer_detailed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
