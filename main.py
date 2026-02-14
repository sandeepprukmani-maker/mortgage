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
    """
    if not isinstance(base_payload, dict):
        return {}, set()

    if "payload" in base_payload and isinstance(base_payload.get("payload"), dict):
        ui_payload = base_payload["payload"]
    else:
        ui_payload = base_payload

    return ui_payload, set(ui_payload.keys())

def filter_payload_to_allowed_keys(final_payload: Dict[str, Any], allowed_keys: set) -> Dict[str, Any]:
    """
    Keep ONLY keys that were present in the UI payload.
    If allowed_keys is empty, do NOT filter (prevents accidentally sending {}).
    """
    if not allowed_keys:
        return final_payload
    return {k: v for k, v in final_payload.items() if k in allowed_keys}

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
    # Extract actual payload if base_payload is the new format {payload, excludedFields}
    if base_payload and isinstance(base_payload, dict) and "payload" in base_payload:
        base_payload = base_payload["payload"]

    merged = (base_payload or {}).copy()

    # Merge customer-specific values (overwrite existing merged keys or add keys)
    # NOTE: strict filtering later will remove any keys the UI didn't define.
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
        merged["borrowerName"] = customer_obj.get("borrowerName") or customer_obj.get("name")
        merged["creditScore"] = customer_obj.get("creditScore") or customer_obj.get("credit_score")
        merged["monthlyIncome"] = customer_obj.get("monthlyIncome") or customer_obj.get("monthly_income")
        merged["loanAmount"] = customer_obj.get("loanAmount") or customer_obj.get("remaining_balance")
        merged["appraisedValue"] = customer_obj.get("appraisedValue") or customer_obj.get("property_value")
        merged["propertyZipCode"] = customer_obj.get("propertyZipCode") or customer_obj.get("property_zip")
        merged["propertyCounty"] = customer_obj.get("propertyCounty") or customer_obj.get("property_county")
        merged["propertyState"] = customer_obj.get("propertyState") or customer_obj.get("property_state")

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
    return session.post(
        PRICEQUOTE_URL,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )

def qualifying_products_for_customer(
    quote_body: Dict[str, Any],
    current_monthly_payment: float,
    target_amount: float,
    min_savings: float = 200.0,
    tolerance: Optional[float] = None,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    for item in (quote_body.get("validQuoteItems") or []):
        match, diff = closest_pricepoint_for_item(item, target_amount=target_amount)
        if not match:
            continue

        amount = safe_float((match.get("finalPriceAfterOriginationFee") or {}).get("amount"))
        if tolerance is not None and amount is not None and abs(amount - target_amount) > tolerance:
            continue

        mp_val = safe_float((match.get("monthlyPayment") or {}).get("value"))
        if mp_val is None:
            continue

        savings = current_monthly_payment - mp_val
        if savings >= min_savings:
            out.append(
                {
                    "mortgageProductId": match.get("mortgageProductId"),
                    "mortgageProductName": match.get("mortgageProductName"),
                    "mortgageProductAlias": match.get("mortgageProductAlias"),
                    "closestAmount": amount,
                    "amountDiff": diff,
                    "matchedMonthlyPayment": mp_val,
                    "currentMonthlyPayment": current_monthly_payment,
                    "monthlySavings": round(savings, 2),
                    "interestRate": match.get("interestRate"),
                    "finalPriceAfterOriginationFee": match.get("finalPriceAfterOriginationFee"),
                    "originationFee": match.get("originationFee"),
                    "finalPrice": match.get("finalPrice"),
                }
            )

    out.sort(key=lambda x: x["monthlySavings"], reverse=True)
    return out

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        min_savings = float(request.form.get("min_savings", 200))
        target_amount = float(request.form.get("target_amount", -2000))
        tolerance_str = request.form.get("tolerance")
        tolerance = float(tolerance_str) if (tolerance_str and tolerance_str.strip()) else None

        base_payload_str = request.form.get("base_payload")
        base_payload_raw = json.loads(base_payload_str) if base_payload_str else {}

        # ✅ UI source-of-truth keys (ONLY these keys will be sent to UWM)
        ui_payload, allowed_keys = extract_ui_payload_and_allowed_keys(base_payload_raw)

        customers = Customer.query.all()
        access_token = get_access_token()

        results = []
        for customer in customers:
            current_mp = customer.current_monthly_payment

            # Build canonical payload (may include defaults)
            payload = customer_to_payload(customer, ui_payload)

            # ✅ STRICT FILTER: remove any field not present in UI payload
            payload = filter_payload_to_allowed_keys(payload, allowed_keys)

            # Optional: log exactly what you're sending
            # logger.info("UWM REQUEST PAYLOAD:\n%s", json.dumps({"priceQuoteRequest": payload}, indent=2))

            resp = post_price_quote(access_token, payload)
            if resp.status_code != 200:
                logger.error(f"Quote failed for {payload.get('borrowerName')}: {resp.text}")
                continue

            quote_body = parse_api_json(resp)
            if not isinstance(quote_body, dict):
                logger.error(
                    f"Unexpected response type for {payload.get('borrowerName')}: {type(quote_body)}"
                )
                continue

            qualifying = qualifying_products_for_customer(
                quote_body, current_mp, target_amount, min_savings, tolerance
            )

            if qualifying:
                results.append(
                    {
                        "name": customer.name,
                        "currentMonthlyPayment": current_mp,
                        "products": qualifying,
                        "fullResponse": strip_invalid_quote_items(quote_body),
                    }
                )

        return jsonify(results)

    except Exception as e:
        logger.error(f"Error in analyze: {e}")
        return jsonify({"message": str(e)}), 500

@app.route("/api/analyze/direct", methods=["POST"])
def analyze_direct():
    """
    Direct mode now also defaults to strict behavior:
    - UWM gets ONLY the keys present in each input customer JSON object.
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

        results = []
        for customer in content:
            if not isinstance(customer, dict):
                continue

            current_mp = safe_float(customer.get("currentMonthlyPayment"))
            if current_mp is None:
                current_mp = 2000.0

            # Allowed keys are exactly what caller provided
            allowed_keys = set(customer.keys())

            payload = customer_to_payload(customer)

            # ✅ STRICT FILTER: only caller-provided keys survive
            payload = filter_payload_to_allowed_keys(payload, allowed_keys)

            print(payload)

            resp = post_price_quote(access_token, payload)
            if resp.status_code != 200:
                logger.error(f"Quote failed for {payload.get('borrowerName')}: {resp.text}")
                continue

            quote_body = parse_api_json(resp)
            if not isinstance(quote_body, dict):
                logger.error(
                    f"Unexpected response type for {payload.get('borrowerName')}: {type(quote_body)}"
                )
                continue

            qualifying = qualifying_products_for_customer(
                quote_body, current_mp, target_amount, min_savings, tolerance
            )

            if qualifying:
                results.append(
                    {
                        "name": customer.get("borrowerName") or customer.get("name") or "Unknown",
                        "currentMonthlyPayment": current_mp,
                        "products": qualifying,
                        "fullResponse": strip_invalid_quote_items(quote_body),
                    }
                )

        return jsonify(results)

    except Exception as e:
        logger.error(f"Error in analyze_direct: {e}")
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
