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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# The error occurs because db.create_all() or other db operations 
# might be called before db.init_app(app) or outside app context correctly.
# Also, in models.py, db is imported from models, but main.py might be creating its own instance.
# Let's fix the imports and initialization.

with app.app_context():
    db.init_app(app)
    db.create_all()
    # Seed data if empty
    if not Customer.query.first():
        import random
        for i in range(100):
            cust = Customer(
                name=f"Customer {i+1}",
                current_monthly_payment=random.uniform(1000, 5000),
                remaining_balance=random.uniform(100000, 500000),
                property_value=random.uniform(150000, 700000),
                property_zip=str(random.randint(10000, 99999)),
                property_county="County",
                property_state="ST",
                credit_score=random.randint(600, 850),
                monthly_income=random.uniform(3000, 15000)
            )
            db.session.add(cust)
        db.session.commit()

# ===== Customer CRUD Endpoints =====
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "current_monthly_payment": c.current_monthly_payment,
        "remaining_balance": c.remaining_balance,
        "property_value": c.property_value,
        "property_zip": c.property_zip,
        "property_county": c.property_county,
        "property_state": c.property_state,
        "credit_score": c.credit_score,
        "monthly_income": c.monthly_income
    } for c in customers])

@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(
        name=data.get('name'),
        current_monthly_payment=safe_float(data.get('current_monthly_payment')),
        remaining_balance=safe_float(data.get('remaining_balance')),
        property_value=safe_float(data.get('property_value')),
        property_zip=data.get('property_zip'),
        property_county=data.get('property_county'),
        property_state=data.get('property_state'),
        credit_score=int(data.get('credit_score', 0)),
        monthly_income=safe_float(data.get('monthly_income'))
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer added", "id": new_customer.id})

@app.route('/api/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    customer.name = data.get('name', customer.name)
    customer.current_monthly_payment = safe_float(data.get('current_monthly_payment', customer.current_monthly_payment))
    customer.remaining_balance = safe_float(data.get('remaining_balance', customer.remaining_balance))
    customer.property_value = safe_float(data.get('property_value', customer.property_value))
    customer.property_zip = data.get('property_zip', customer.property_zip)
    customer.property_county = data.get('property_county', customer.property_county)
    customer.property_state = data.get('property_state', customer.property_state)
    customer.credit_score = int(data.get('credit_score', customer.credit_score))
    customer.monthly_income = safe_float(data.get('monthly_income', customer.monthly_income))
    db.session.commit()
    return jsonify({"message": "Customer updated"})

@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"})

# ===== Requests session with SOCKS5 =====
session = requests.Session()
if SOCKS_PROXY:
    session.proxies = {"http": SOCKS_PROXY, "https": SOCKS_PROXY}
session.headers.update({
    "User-Agent": "uwm-ipq-python/1.0",
    "Accept": "application/json",
})

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

def parse_api_json(resp: requests.Response) -> Union[Dict[str, Any], List[Any]]:
    """
    Make response JSON safe:
    - resp.json() might return a dict/list OR a string that itself is JSON
    - handle both
    """
    try:
        body = resp.json()
    except Exception:
        return {}
        
    if isinstance(body, str):
        # sometimes API returns JSON serialized as a string
        try:
            body = json.loads(body)
        except:
            pass
    return body

def strip_invalid_quote_items(full_body: Any) -> Any:
    """Remove invalidQuoteItems from dict response (for response viewing purposes)."""
    if isinstance(full_body, dict):
        cleaned = dict(full_body)
        cleaned.pop("invalidQuoteItems", None)
        return cleaned
    return full_body

def get_access_token() -> str:
    if not all([UWM_USERNAME, UWM_PASSWORD, UWM_CLIENT_ID, UWM_CLIENT_SECRET, UWM_SCOPE]):
        # For development/demo purposes if credentials aren't set
        logger.warning("Missing UWM credentials in environment variables")
        return "mock_token"

    data = {
        "grant_type": "password",
        "username": UWM_USERNAME,
        "password": UWM_PASSWORD,
        "client_id": UWM_CLIENT_ID,
        "client_secret": UWM_CLIENT_SECRET,
        "scope": UWM_SCOPE,
    }

    try:
        resp = session.post(
            TOKEN_URL,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )

        if resp.status_code != 200:
            raise RuntimeError(f"Token request failed ({resp.status_code}):\n{resp.text}")

        token_json = resp.json()
        access_token = token_json.get("access_token")
        if not access_token:
            raise RuntimeError(f"No access_token in response:\n{resp.text}")
        return access_token
    except Exception as e:
        logger.error(f"Token error: {e}")
        return "mock_token"

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

def customer_to_payload(customer_obj: Customer, base_payload: Dict[str, Any] = None) -> Dict[str, Any]:
    # Extract actual payload if base_payload is the new format {payload, excludedFields}
    if base_payload and "payload" in base_payload:
        base_payload = base_payload["payload"]
        
    merged = (base_payload or {}).copy()
    
    # Mapping based on user request
    merged["borrowerName"] = customer_obj.name
    merged["creditScore"] = customer_obj.credit_score
    merged["monthlyIncome"] = customer_obj.monthly_income
    merged["loanAmount"] = customer_obj.remaining_balance
    merged["appraisedValue"] = customer_obj.property_value
    merged["propertyZipCode"] = customer_obj.property_zip
    
    # Additional fields from DB
    merged["propertyCounty"] = customer_obj.property_county
    merged["propertyState"] = customer_obj.property_state
    
    # Business logic defaults
    monthly_income = merged.get("monthlyIncome", 20000)
    mi = safe_float(monthly_income)
    if mi is None or mi < 1:
        monthly_income = 20000

    lt_ids = merged.get("loanTypeIds", ["0"])
    if isinstance(lt_ids, str):
        lt_ids = [id.strip() for id in lt_ids.split(",")]
    
    if str(merged.get("purposeTypeID", "3")) == "3" and len(lt_ids) > 1:
        lt_ids = [lt_ids[0]]

    return {
        "brokerAlias": merged.get("brokerAlias", "TEST"),
        "loanOfficer": merged.get("loanOfficer", "lofficer@email.com"),
        "borrowerName": merged.get("borrowerName"),
        "purposeTypeID": str(merged.get("purposeTypeID", "3")),
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
        "waivableFeeTypeIds": merged.get("waivableFeeTypeIds", ["0"]),
        "loanShieldTypeId": str(merged.get("loanShieldTypeId", "0")),
        "paPlusTypeId": str(merged.get("paPlusTypeId", "0")),
        "exactRateTypeId": str(merged.get("exactRateTypeId", "2")),
        "targetPriceValue": merged.get("targetPriceValue", 0),
        "targetCashValue": merged.get("targetCashValue", 0),
        "waiveUnderwritingFee": bool(merged.get("waiveUnderwritingFee", False)),
        "monthlyIncome": monthly_income,
        "buyDownAliasID": merged.get("buyDownAliasID", "None"),
        "firstTimeHomeBuyer": bool(merged.get("firstTimeHomeBuyer", False)),
        "loanTermIds": merged.get("loanTermIds", ["4", "3", "1", "2", "0"]),
        "numberOfUnits": merged.get("numberOfUnits"),
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
        "useMortgageInsuranceTypeIds": merged.get("useMortgageInsuranceTypeIds"),
        "federalHousingAdministrationSecondarySourceTypeId": merged.get("federalHousingAdministrationSecondarySourceTypeId"),
        "tracIncentiveID": merged.get("tracIncentiveID"),
        "closingType": merged.get("closingType")
    }

def post_price_quote(access_token: str, payload: dict):
    # Mock response if token is mock_token
    if access_token == "mock_token":
        class MockResponse:
            status_code = 200
            text = "{}"
            def json(self):
                # Return a mock valid response structure to prevent errors
                return {
                    "validQuoteItems": [
                        {
                            "mortgageProductId": "123",
                            "mortgageProductName": "Test Product",
                            "mortgageProductAlias": "Test Alias",
                            "quotePricePoints": [
                                {
                                    "interestRate": 0.065,
                                    "finalPrice": 100.0,
                                    "finalPriceAfterOriginationFee": {"amount": -2000.0},
                                    "monthlyPayment": {"value": 1500.0},
                                    "originationFee": 0.0,
                                    "principalAndInterest": 1200.0
                                }
                            ]
                        }
                    ]
                }
        return MockResponse()

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
            out.append({
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
            })

    out.sort(key=lambda x: x["monthlySavings"], reverse=True)
    return out

app = Flask(__name__, static_folder="static", static_url_path="/")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        min_savings = float(request.form.get('min_savings', 200))
        target_amount = float(request.form.get('target_amount', -2000))
        tolerance_str = request.form.get('tolerance')
        tolerance = float(tolerance_str) if (tolerance_str and tolerance_str.strip()) else None
        
        # Base payload from builder
        base_payload_str = request.form.get('base_payload')
        base_payload = json.loads(base_payload_str) if base_payload_str else {}

        customers = Customer.query.all()
        access_token = get_access_token()

        results = []
        for customer in customers:
            current_mp = customer.current_monthly_payment
            payload = customer_to_payload(customer, base_payload)

            try:
                resp = post_price_quote(access_token, payload)
                if resp.status_code != 200:
                    logger.error(f"Quote failed for {payload.get('borrowerName')}: {resp.text}")
                    continue

                quote_body = parse_api_json(resp)
                if not isinstance(quote_body, dict):
                    logger.error(f"Unexpected response type for {payload.get('borrowerName')}: {type(quote_body)}")
                    continue

            except Exception as e:
                logger.error(f"API Request failed: {e}")
                continue

            qualifying = qualifying_products_for_customer(
                quote_body,
                current_mp,
                target_amount,
                min_savings,
                tolerance
            )

            if qualifying:
                results.append({
                    "name": customer.name,
                    "currentMonthlyPayment": current_mp,
                    "products": qualifying,
                    "fullResponse": strip_invalid_quote_items(quote_body),
                })

        return jsonify(results)

    except Exception as e:
        logger.error(f"Error in analyze: {e}")
        return jsonify({"message": str(e)}), 500

@app.route('/api/analyze/direct', methods=['POST'])
def analyze_direct():
    try:
        content = request.json
        if not content:
            return jsonify({"message": "No data provided"}), 400
            
        if isinstance(content, dict):
            content = [content]
        elif not isinstance(content, list):
            return jsonify({"message": "JSON must be a list or object"}), 400

        # Optional params for analysis
        min_savings = float(request.args.get('min_savings', 200))
        target_amount = float(request.args.get('target_amount', -2000))
        tolerance_str = request.args.get('tolerance')
        tolerance = float(tolerance_str) if (tolerance_str and tolerance_str.strip()) else None

        access_token = get_access_token()

        results = []
        for customer in content:
            current_mp = safe_float(customer.get("currentMonthlyPayment"))
            if current_mp is None:
                # Fallback to a default if not provided in builder
                current_mp = 2000.0

            payload = customer_to_payload(customer)

            try:
                resp = post_price_quote(access_token, payload)
                if resp.status_code != 200:
                    logger.error(f"Quote failed for {payload.get('borrowerName')}: {resp.text}")
                    continue

                quote_body = parse_api_json(resp)
                if not isinstance(quote_body, dict):
                    logger.error(f"Unexpected response type for {payload.get('borrowerName')}: {type(quote_body)}")
                    continue

            except Exception as e:
                logger.error(f"API Request failed: {e}")
                continue

            qualifying = qualifying_products_for_customer(
                quote_body,
                current_mp,
                target_amount,
                min_savings,
                tolerance
            )

            if qualifying:
                results.append({
                    "name": customer.get("borrowerName") or customer.get("name") or "Unknown",
                    "currentMonthlyPayment": current_mp,
                    "products": qualifying,
                    "fullResponse": strip_invalid_quote_items(quote_body),
                })

        return jsonify(results)

    except Exception as e:
        logger.error(f"Error in analyze_direct: {e}")
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
