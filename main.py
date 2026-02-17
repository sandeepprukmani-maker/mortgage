import os
import json
import re
import requests
import logging
import uuid
from typing import Any, Dict
from datetime import datetime, timezone, timedelta

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from models import db, Customer

# ============================================================
# Logging
# ============================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# Env
# ============================================================
load_dotenv()

UWM_USERNAME = os.getenv("UWM_USERNAME")
UWM_PASSWORD = os.getenv("UWM_PASSWORD")
UWM_CLIENT_ID = os.getenv("UWM_CLIENT_ID")
UWM_CLIENT_SECRET = os.getenv("UWM_CLIENT_SECRET")
UWM_SCOPE = os.getenv("UWM_SCOPE")
SOCKS_PROXY = os.getenv("SOCKS_PROXY")

# Allow override via env, else fallback to common defaults
TOKEN_URL = os.getenv("TOKEN_URL", "https://sso.uwm.com/adfs/oauth2/token")
PRICEQUOTE_URL = os.getenv("PRICEQUOTE_URL", "https://stg.api.uwm.com/public/instantpricequote/v2/pricequote")

# ============================================================
# Flask
# ============================================================
app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mortgage_analyzer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

with app.app_context():
    db.init_app(app)
    db.create_all()

# ============================================================
# Requests session (SOCKS)
# ============================================================
session = requests.Session()
if SOCKS_PROXY:
    session.proxies = {"http": SOCKS_PROXY, "https": SOCKS_PROXY}
session.headers.update({
    "User-Agent": "uwm-ipq-python/1.0",
    "Accept": "application/json",
})

# ============================================================
# Helpers
# ============================================================
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


def _to_str(x):
    if x is None:
        return None
    return str(x)


def _coerce_list_str(value):
    """
    Ensure value is a list[str]. Handles:
      - [0] -> ["0"]
      - "0" -> ["0"]
      - None -> []
    """
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def normalize_uwm_pricequote_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes payload fields for UWM expectations WITHOUT wrapping in priceQuoteRequest.
    - Fix key casing issues (*ID -> *Id)
    - Force ID-ish fields to strings
    - Force array-of-ids to list[str] (loanTypeIds etc)
    """
    if not isinstance(payload, dict):
        payload = {}

    # If someone accidentally sent wrapped payload, unwrap it
    inner = payload.get("priceQuoteRequest") if "priceQuoteRequest" in payload else payload
    if not isinstance(inner, dict):
        inner = {}

    # Fix common casing variants you used in your builder
    key_map = {
        "purposeTypeID": "purposeTypeId",
        "compensationPayerTypeID": "compensationPayerTypeId",
        "buyDownAliasID": "buyDownAliasId",
    }
    for old_k, new_k in key_map.items():
        if old_k in inner and new_k not in inner:
            inner[new_k] = inner.pop(old_k)

    # Ensure list-of-strings where UWM expects string IDs
    if "loanTypeIds" in inner:
        inner["loanTypeIds"] = _coerce_list_str(inner.get("loanTypeIds"))
    if "loanTermIds" in inner:
        inner["loanTermIds"] = _coerce_list_str(inner.get("loanTermIds"))
    if "waivableFeeTypeIds" in inner:
        inner["waivableFeeTypeIds"] = _coerce_list_str(inner.get("waivableFeeTypeIds"))

    # Force typical ID fields to string (but don't stringify booleans)
    string_id_fields = [
        "monthsOfReservesId",
        "monthsOfBankStatementsId",
        "commitmentPeriodId",
        "occupancyTypeId",
        "propertyTypeId",
        "compensationPayerTypeId",
        "escrowWaiverTypeId",
        "tracTypeId",
        "loanShieldTypeId",
        "paPlusTypeId",
        "exactRateTypeId",
        "purposeTypeId",
        "numberOfBorrowers",
    ]
    for f in string_id_fields:
        if f in inner and inner[f] is not None and not isinstance(inner[f], bool):
            inner[f] = _to_str(inner[f])

    # purposeTypeId in particular often needs to be string
    if "purposeTypeId" in inner and inner["purposeTypeId"] is not None and not isinstance(inner["purposeTypeId"], str):
        inner["purposeTypeId"] = str(inner["purposeTypeId"])

    return inner


# =========================
# Robust JSON parsing
# =========================
def coerce_json_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Ensure obj is a dict.
    Handles:
      - dict
      - list -> wrapped in {"_list": [...]}
      - JSON returned as quoted string (stringified JSON)
      - double-stringified JSON
    """
    if isinstance(obj, dict):
        return obj

    if isinstance(obj, list):
        return {"_list": obj}

    if isinstance(obj, str):
        s = obj.strip()
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
    """Safely parse response to a dict, even if server returns stringified JSON."""
    try:
        data = resp.json()
    except Exception:
        data = resp.text

    data = coerce_json_to_dict(data)

    if not data:
        try:
            data = coerce_json_to_dict(resp.text)
        except Exception:
            return {}

    return data


# ============================================================
# Auth + UWM Call
# ============================================================
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
    """
    Normalize payload (fix casing, list[str], ID strings).
    NOTE: This function sends the UNWRAPPED object. If UWM requires wrapping, do it here.
    """
    normalized = normalize_uwm_pricequote_payload(payload)

    logger.info("Posting payload to UWM (normalized) keys=%s", list(normalized.keys()))
    return session.post(
        PRICEQUOTE_URL,
        json=normalized,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )


# ============================================================
# Payload building
# ============================================================
def build_payload_from_customer(customer: Customer, base_payload: dict) -> dict:
    """Build API payload from customer data and template (UNWRAPPED inner payload)."""
    import copy
    payload = copy.deepcopy(base_payload) if isinstance(base_payload, dict) else {}

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

    # Early coercion for common gotchas
    if "loanTypeIds" in payload:
        payload["loanTypeIds"] = _coerce_list_str(payload.get("loanTypeIds"))
    if "loanTermIds" in payload:
        payload["loanTermIds"] = _coerce_list_str(payload.get("loanTermIds"))

    return payload


# ============================================================
# Buydown helpers
# ============================================================
def calculate_buydown_details(base_rate: float, buydown_type: str, loan_amount: float, term_years: int):
    """
    Lightweight placeholder so your /analysis flow doesn't crash.
    For "accurate" year-by-year, you already use calculate_buydown_details_from_response
    in the legacy detailed endpoint.
    """
    if base_rate is None or buydown_type == "None":
        return None

    if "2-1" in (buydown_type or ""):
        return {
            "year1": {"rate": round(base_rate - 2.0, 3)},
            "year2": {"rate": round(base_rate - 1.0, 3)},
            "actual": {"rate": round(base_rate, 3)},
            "note": "Estimated rates only (use /api/customers/<key>/analyze for accurate lookup)"
        }
    if "1-0" in (buydown_type or ""):
        return {
            "year1": {"rate": round(base_rate - 1.0, 3)},
            "year2": {"rate": round(base_rate, 3)},
            "actual": {"rate": round(base_rate, 3)},
            "note": "Estimated rates only (use /api/customers/<key>/analyze for accurate lookup)"
        }
    return None


def calculate_buydown_details_from_response(base_rate: float, buydown_type: str, all_scenarios: list, term_years: int,
                                            product_name: str):
    """
    Look up actual year-by-year rates from the full API response
    """
    if not base_rate or buydown_type == "None":
        return None

    if "2-1" in buydown_type:
        year1_target = base_rate - 2.0
        year2_target = base_rate - 1.0
    elif "1-0" in buydown_type:
        year1_target = base_rate - 1.0
        year2_target = base_rate
    else:
        return None

    def find_closest_rate(scenarios, target_rate, term, product, tolerance=0.5):
        closest_match = None
        closest_diff = float('inf')

        for scenario in scenarios:
            if not scenario.get("products"):
                continue

            for prod in scenario["products"]:
                if prod.get("term_years") != term or prod.get("product_name") != product:
                    continue

                for rate in prod.get("rates", []):
                    rate_val = rate.get("interest_rate")
                    if rate_val is None:
                        continue

                    diff = abs(rate_val - target_rate)
                    if diff <= tolerance and diff < closest_diff:
                        closest_diff = diff
                        closest_match = {
                            "rate": rate_val,
                            "payment": rate.get("monthly_payment"),
                            "savings": rate.get("monthly_savings"),
                            "credit_cost": rate.get("credit_cost"),
                            "is_exact": diff < 0.01
                        }

        return closest_match

    year1 = find_closest_rate(all_scenarios, year1_target, term_years, product_name)
    year2 = find_closest_rate(all_scenarios, year2_target, term_years, product_name)
    actual = find_closest_rate(all_scenarios, base_rate, term_years, product_name)

    if not year1:
        year1 = {"rate": None, "payment": None, "savings": None, "credit_cost": None, "is_exact": False, "note": "No Year 1 data found"}
    if not year2:
        year2 = {"rate": None, "payment": None, "savings": None, "credit_cost": None, "is_exact": False, "note": "No Year 2 data found"}
    if not actual:
        actual = {"rate": base_rate, "payment": None, "savings": None, "credit_cost": None, "is_exact": True, "note": "Actual rate (future years)"}

    return {"year1": year1, "year2": year2, "actual": actual}


def filter_rates_by_target(rates_list, target_amount):
    """
    Filter rates to show rows around the closest match to target_amount.

    1. Find row where credit_cost closest to target_amount
    2. Sort by interest_rate asc
    3. Select: 3 lower + closest + 2 higher
    """
    if not rates_list:
        return []

    valid_rates = [r for r in rates_list if r.get('credit_cost') is not None and r.get('interest_rate') is not None]
    if not valid_rates:
        return rates_list

    closest_match = min(valid_rates, key=lambda x: abs(x['credit_cost'] - target_amount))
    sorted_rates = sorted(valid_rates, key=lambda x: x['interest_rate'])
    closest_index = sorted_rates.index(closest_match)

    start_index = max(0, closest_index - 3)
    end_index = min(len(sorted_rates), closest_index + 3)

    selected_rates = sorted_rates[start_index:end_index]
    for rate in selected_rates:
        rate['is_closest_to_target'] = (rate is closest_match)

    return selected_rates


# ============================================================
# ZIPCODE LOOKUP
# ============================================================
@app.route("/api/zipcode/<zipcode>", methods=["GET"])
def lookup_zipcode(zipcode):
    try:
        if not re.match(r"^\d{5}$", zipcode):
            return jsonify({"error": "Invalid zipcode format", "success": False}), 400

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

        lat = place.get("latitude")
        lon = place.get("longitude")

        county_name = ""
        county_fips = ""

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
                counties = ((gj.get("result") or {}).get("geographies", {}).get("Counties", []))
                if counties:
                    county_name = counties[0].get("NAME", "") or ""
                    county_fips = counties[0].get("GEOID", "") or ""

        return jsonify({
            "zipcode": zipcode,
            "state": state,
            "city": city,
            "county": county_name,
            "countyFips": county_fips,
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


# ============================================================
# SCREEN 1: Lead Generation
# ============================================================
@app.route("/api/screen1/analyze", methods=["POST"])
def screen1_analyze():
    try:
        data = request.json or {}
        min_savings = float(data.get("min_savings", 200))
        target_amount = float(data.get("target_amount", -2000))
        base_payload = data.get("payload", {}) or {}

        logger.info("Screen 1 Analysis - Min Savings: $%.2f", min_savings)

        customers = Customer.get_current_customers()
        access_token = get_access_token()

        buydown_scenarios = ["None", "1-0 LLPA", "2-1 LLPA"]
        qualifying_leads = []

        for customer in customers:
            logger.info("Analyzing customer: %s", customer.name)
            current_payment = customer.current_monthly_payment

            for buydown in buydown_scenarios:
                payload = build_payload_from_customer(customer, base_payload)
                payload["buyDownAliasId"] = buydown  # consistent casing

                loan_terms = payload.get("loanTermIds", ["4"])
                loan_terms = _coerce_list_str(loan_terms)

                for term in loan_terms:
                    payload_copy = payload.copy()
                    payload_copy["loanTermIds"] = [str(term)]

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

                    for item in quote_body.get("validQuoteItems", []):
                        for pp in item.get("quotePricePoints", []):
                            mp_val = safe_float((pp.get("monthlyPayment") or {}).get("value"))
                            if mp_val is None:
                                continue

                            savings = current_payment - mp_val
                            if savings >= min_savings:
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
                                break
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
        logger.error("Error in screen1_analyze: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500


# ============================================================
# Customers CRUD
# ============================================================
@app.route("/api/customers", methods=["GET"])
def get_customers():
    customers = Customer.get_current_customers()
    return jsonify([c.to_dict() for c in customers])


@app.route("/api/customers/<customer_key>/history", methods=["GET"])
def get_customer_history(customer_key):
    history = Customer.get_customer_history(customer_key)
    return jsonify([c.to_dict() for c in history])


@app.route("/api/customers", methods=["POST"])
def add_customer():
    data = request.json or {}

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
    data = request.json or {}

    current = Customer.get_current_by_key(customer_key)
    if not current:
        return jsonify({"error": "Customer not found"}), 404

    current.is_current = False
    current.end_date = datetime.now(timezone.utc)

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
    current = Customer.get_current_by_key(customer_key)
    if not current:
        return jsonify({"error": "Customer not found"}), 404

    current.is_current = False
    current.end_date = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"message": "Customer deactivated"})


# ============================================================
# Analysis cache
# ============================================================
analysis_cache = {}  # {cache_key: {...}}


@app.route("/api/analysis/start", methods=["POST"])
def start_batch_analysis():
    data = request.json or {}
    base_payload = data.get("payload", {}) or {}
    min_savings = float(data.get("min_savings", 200))
    target_amount = float(data.get("target_amount", -2000))
    ttl_hours = float(data.get("ttl_hours", 2))

    cache_key = str(uuid.uuid4())

    analysis_cache[cache_key] = {
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(hours=ttl_hours),
        "payload": base_payload,
        "min_savings": min_savings,
        "target_amount": target_amount,
        "results": {},
        "total_customers": 0,
        "analyzed_count": 0,
        "qualified_count": 0
    }

    return jsonify({"cache_key": cache_key, "message": "Analysis started"})


@app.route("/api/analysis/<cache_key>/analyze-next", methods=["POST"])
def analyze_next_customer(cache_key):
    try:
        if cache_key not in analysis_cache:
            return jsonify({"error": "Cache key not found"}), 404

        cache_entry = analysis_cache[cache_key]

        if datetime.now(timezone.utc) > cache_entry["expires_at"]:
            del analysis_cache[cache_key]
            return jsonify({"error": "Cache expired"}), 410

        data = request.json or {}
        customer_key = data.get("customer_key")
        if not customer_key:
            return jsonify({"error": "customer_key required"}), 400

        customer = Customer.get_current_by_key(customer_key)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        base_payload = cache_entry["payload"]
        min_savings = cache_entry["min_savings"]
        target_amount = cache_entry["target_amount"]

        access_token = get_access_token()
        buydown_scenarios = ["None", "1-0 LLPA", "2-1 LLPA"]

        results = []
        best_option = None
        best_savings = 0.0

        for buydown in buydown_scenarios:
            payload = build_payload_from_customer(customer, base_payload)
            payload["buyDownAliasId"] = buydown

            resp = post_price_quote(access_token, payload)
            logger.info("UWM response status=%s body_snip=%s", resp.status_code, (resp.text or "")[:2000])

            if resp.status_code != 200:
                results.append({"buydown_type": buydown, "error": resp.text, "products": []})
                continue

            quote_body = parse_response_json(resp)
            if not isinstance(quote_body, dict) or not quote_body:
                results.append({"buydown_type": buydown, "error": "Could not parse response", "products": []})
                continue

            products_by_term = {}

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
                    if savings < min_savings:
                        continue

                    rate_val = interest_rate_value(pp.get("interestRate"))
                    fpa = pp.get("finalPriceAfterOriginationFee") or {}
                    credit_cost = safe_float(fpa.get("amount"))

                    # Avoid NameError; this is only an estimated breakdown
                    buydown_details = calculate_buydown_details(
                        rate_val, buydown, customer.remaining_balance, int(term) if term else 0
                    )

                    rate_data = {
                        "interest_rate": rate_val,
                        "monthly_payment": mp_val,
                        "monthly_savings": round(savings, 2),
                        "credit_cost": credit_cost,
                        "buydown_breakdown": buydown_details
                    }

                    products_by_term[key]["rates"].append(rate_data)

                    if savings > best_savings:
                        best_savings = float(savings)
                        best_option = {
                            "buydown": buydown,
                            "product": product_name,
                            "term": term,
                            **rate_data
                        }

            # Mark closest to target on each product
            for product in products_by_term.values():
                product["rates"].sort(
                    key=lambda x: x.get("interest_rate") if x.get("interest_rate") is not None else 999
                )

                if product["rates"]:
                    closest_rate = min(
                        product["rates"],
                        key=lambda x: abs(x.get("credit_cost", 0) - target_amount)
                        if x.get("credit_cost") is not None else float('inf')
                    )
                    closest_rate["is_closest_to_target"] = True

            results.append({"buydown_type": buydown, "products": list(products_by_term.values())})

        analysis_result = {
            "customer": customer.to_dict(),
            "scenarios": results,
            "target_amount": target_amount,
            "best_option": best_option,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "viewed": False
        }

        cache_entry["results"][customer_key] = analysis_result
        cache_entry["analyzed_count"] += 1

        qualified = bool(best_option and best_savings >= min_savings)
        if qualified:
            cache_entry["qualified_count"] += 1

        return jsonify({
            "qualified": qualified,
            "customer_key": customer_key,
            "customer_name": customer.name,
            "best_savings": best_savings if best_option else 0,
            "analysis": analysis_result if qualified else None
        })

    except Exception as e:
        logger.error("Error in analyze_next_customer: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/analysis/<cache_key>/results", methods=["GET"])
def get_cached_results(cache_key):
    if cache_key not in analysis_cache:
        return jsonify({"error": "Cache key not found"}), 404

    cache_entry = analysis_cache[cache_key]

    if datetime.now(timezone.utc) > cache_entry["expires_at"]:
        del analysis_cache[cache_key]
        return jsonify({"error": "Cache expired"}), 410

    return jsonify({
        "cache_key": cache_key,
        "created_at": cache_entry["created_at"].isoformat(),
        "expires_at": cache_entry["expires_at"].isoformat(),
        "analyzed_count": cache_entry["analyzed_count"],
        "qualified_count": cache_entry["qualified_count"],
        "results": cache_entry["results"]
    })


@app.route("/api/analysis/<cache_key>/result/<customer_key>", methods=["GET"])
def get_customer_analysis(cache_key, customer_key):
    if cache_key not in analysis_cache:
        return jsonify({"error": "Cache key not found"}), 404

    cache_entry = analysis_cache[cache_key]

    if customer_key not in cache_entry["results"]:
        return jsonify({"error": "Customer analysis not found"}), 404

    return jsonify(cache_entry["results"][customer_key])


@app.route("/api/analysis/<cache_key>/mark-viewed/<customer_key>", methods=["POST"])
def mark_analysis_viewed(cache_key, customer_key):
    if cache_key not in analysis_cache:
        return jsonify({"error": "Cache key not found"}), 404

    cache_entry = analysis_cache[cache_key]
    if customer_key in cache_entry["results"]:
        cache_entry["results"][customer_key]["viewed"] = True
        return jsonify({"success": True})

    return jsonify({"error": "Customer analysis not found"}), 404


# ============================================================
# Legacy detailed analysis (accurate buydown lookup)
# ============================================================
@app.route("/api/customers/<customer_key>/analyze", methods=["POST"])
def analyze_customer_detailed(customer_key):
    try:
        data = request.json or {}
        base_payload = data.get("payload", {}) or {}
        min_savings = float(data.get("min_savings", 200))
        target_amount = float(data.get("target_amount", -2000))

        customer = Customer.get_current_by_key(customer_key)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        access_token = get_access_token()
        buydown_scenarios = ["None", "1-0 LLPA", "2-1 LLPA"]

        # FIRST PASS: Collect ALL rates from ALL scenarios (no filtering)
        all_scenarios_data = []

        for buydown in buydown_scenarios:
            payload = build_payload_from_customer(customer, base_payload)
            payload["buyDownAliasId"] = buydown

            resp = post_price_quote(access_token, payload)
            logger.info("UWM response status=%s body_snip=%s", resp.status_code, (resp.text or "")[:2000])

            if resp.status_code != 200:
                all_scenarios_data.append({"buydown_type": buydown, "error": resp.text, "products": []})
                continue

            quote_body = parse_response_json(resp)
            if not isinstance(quote_body, dict) or not quote_body:
                all_scenarios_data.append({
                    "buydown_type": buydown,
                    "error": f"Could not parse response as JSON object. status={resp.status_code}",
                    "products": []
                })
                continue

            products_by_term = {}

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

                    rate_val = interest_rate_value(pp.get("interestRate"))
                    fpa = pp.get("finalPriceAfterOriginationFee") or {}
                    savings = customer.current_monthly_payment - mp_val

                    products_by_term[key]["rates"].append({
                        "interest_rate": rate_val,
                        "monthly_payment": mp_val,
                        "monthly_savings": round(savings, 2),
                        "credit_cost": safe_float(fpa.get("amount")),
                    })

            all_scenarios_data.append({
                "buydown_type": buydown,
                "products": list(products_by_term.values())
            })

        # SECOND PASS: Build filtered results with buydown details
        results = []

        for scenario in all_scenarios_data:
            buydown_type = scenario["buydown_type"]
            filtered_products = []

            if "error" in scenario:
                results.append(scenario)
                continue

            for product in scenario.get("products", []):
                filtered_rates = [r for r in product["rates"] if r["monthly_savings"] >= min_savings]
                if not filtered_rates:
                    continue

                filtered_rates.sort(key=lambda x: x.get("interest_rate", 999))

                for rate in filtered_rates:
                    if buydown_type != "None":
                        buydown_details = calculate_buydown_details_from_response(
                            rate["interest_rate"],
                            buydown_type,
                            all_scenarios_data,
                            product["term_years"],
                            product["product_name"]
                        )
                        rate["buydown_breakdown"] = buydown_details
                    else:
                        rate["buydown_breakdown"] = None

                if filtered_rates:
                    closest_rate = min(
                        filtered_rates,
                        key=lambda x: abs(x.get("credit_cost", 0) - target_amount)
                        if x.get("credit_cost") is not None else float('inf')
                    )
                    closest_rate["is_closest_to_target"] = True

                filtered_products.append({
                    "term_years": product["term_years"],
                    "product_name": product["product_name"],
                    "product_alias": product["product_alias"],
                    "rates": filtered_rates
                })

            results.append({
                "buydown_type": buydown_type,
                "products": filtered_products
            })

        return jsonify({
            "customer": customer.to_dict(),
            "scenarios": results,
            "target_amount": target_amount,
        })

    except Exception as e:
        logger.error("Error in analyze_customer_detailed: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500


# ============================================================
# Debug: payload build
# ============================================================
@app.route("/api/debug/payload/<customer_key>", methods=["POST"])
def debug_build_payload(customer_key):
    try:
        data = request.json or {}
        base_payload = data.get("payload", {}) or {}
        buydown = data.get("buydown")
        loan_term = data.get("loan_term")

        customer = Customer.get_current_by_key(customer_key)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        payload = build_payload_from_customer(customer, base_payload)
        if buydown:
            payload["buyDownAliasId"] = buydown
        if loan_term:
            payload["loanTermIds"] = [str(loan_term)]

        logger.info("Built debug payload for customer %s:\n%s",
                    customer_key, json.dumps(payload, indent=2, default=str))

        return jsonify({
            "payload_unwrapped": payload,
            "payload_sent_to_uwm": normalize_uwm_pricequote_payload(payload)
        })
    except Exception as e:
        logger.exception("Error building debug payload: %s", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# FIXED: Accurate buydown endpoint (MUST be above catch-all + above app.run)
# ============================================================
@app.route("/api/buydown/accurate", methods=["POST"])
def get_accurate_buydown():
    try:
        data = request.json or {}
        customer_key = data.get("customer_key")
        product_name = data.get("product_name")
        term_years = int(data.get("term_years", 0))
        buydown_type = data.get("buydown_type")
        target_rate = float(data.get("target_rate"))
        buydown_percent = float(data.get("buydown_percent", 0))
        base_payload = data.get("payload", {}) or {}

        customer = Customer.get_current_by_key(customer_key)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        payload = build_payload_from_customer(customer, base_payload)
        payload["buyDownAliasId"] = buydown_type
        payload["targetRateValue"] = target_rate
        payload["buydownPercent"] = buydown_percent

        access_token = get_access_token()
        resp = post_price_quote(access_token, payload)
        if resp.status_code != 200:
            return jsonify({"error": resp.text}), resp.status_code

        quote_body = parse_response_json(resp)
        if not isinstance(quote_body, dict) or not quote_body:
            return jsonify({"error": "Could not parse response"}), 500

        for item in quote_body.get("validQuoteItems", []):
            if item.get("actualTermYears") != term_years or item.get("mortgageProductName") != product_name:
                continue
            for pp in item.get("quotePricePoints", []):
                rate_val = interest_rate_value(pp.get("interestRate"))
                if rate_val is None:
                    continue
                if abs(rate_val - target_rate) < 0.01:
                    mp = safe_float((pp.get("monthlyPayment") or {}).get("value"))
                    return jsonify({
                        "rate": rate_val,
                        "payment": mp,
                        "savings": (customer.current_monthly_payment - mp) if mp is not None else None,
                        "credit_cost": safe_float((pp.get("finalPriceAfterOriginationFee") or {}).get("amount")),
                        "is_exact": True
                    })

        return jsonify({"error": "No accurate match found"}), 404

    except Exception as e:
        logger.error("Error in get_accurate_buydown: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500


# ============================================================
# Static serving (KEEP THIS LAST among routes)
# This is what caused your 405 earlier when placed above /api routes.
# ============================================================
@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


# ============================================================
# Run (KEEP THIS LAST in file)
# ============================================================
if __name__ == "__main__":
    # Optional: print routes once to verify registration
    # print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
