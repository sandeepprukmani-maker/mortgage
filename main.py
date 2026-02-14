import os
import json
import re
import requests
import logging
from typing import Any, Dict, List, Optional, Union
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

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

def customer_to_payload(customer: Dict[str, Any]) -> Dict[str, Any]:
    monthly_income = customer.get("monthlyIncome", 20000)
    mi = safe_float(monthly_income)
    if mi is None or mi < 1:
        monthly_income = 20000

    return {
        "brokerAlias": customer.get("brokerAlias", "TEST"),
        "loanOfficer": customer.get("loanOfficer", customer.get("email", "lofficer@email.com")),
        "borrowerName": customer.get("borrowerName", customer.get("name", "Unknown")),
        "purposeTypeID": customer.get("purposeTypeID", "3"),
        "loanTypeIds": customer.get("loanTypeIds", ["0"]),
        "refinancePurposeId": customer.get("refinancePurposeId", "Rate And Term Reduction-CONV"),
        "salesPrice": customer.get("salesPrice", 0),
        "appraisedValue": customer.get("appraisedValue", customer.get("propertyValue", 0)),
        "loanAmount": customer.get("loanAmount", customer.get("remainingBalance", 0)),
        "secondLoanAmount": customer.get("secondLoanAmount", 0),
        "occupancyTypeId": str(customer.get("occupancyTypeId", "1")),
        "propertyTypeId": str(customer.get("propertyTypeId", "22")),
        "propertyZipCode": str(customer.get("propertyZipCode", customer.get("propertyZip", ""))),
        "propertyCounty": customer.get("propertyCounty", ""),
        "propertyState": customer.get("propertyState", ""),
        "creditScore": int(customer.get("creditScore", 0)),
        "commitmentPeriodId": str(customer.get("commitmentPeriodId", "13")),
        "isCorrespondent": bool(customer.get("isCorrespondent", False)),
        "isDTIOver45Percent": bool(customer.get("isDTIOver45Percent", False)),
        "monthlyDebt": customer.get("monthlyDebt", 0),
        "annualTaxes": customer.get("annualTaxes", 0),
        "annualHomeownersInsurance": customer.get("annualHomeownersInsurance", customer.get("annualInsurance", 0)),
        "annualPercentageRateFees": customer.get("annualPercentageRateFees", 0),
        "selfEmployed": bool(customer.get("selfEmployed", False)),
        "monthsOfBankStatementsId": str(customer.get("monthsOfBankStatementsId", "0")),
        "monthsOfReservesId": str(customer.get("monthsOfReservesId", "0")),
        "numberOfBorrowers": int(customer.get("numberOfBorrowers", 1)),
        "compensationPayerTypeID": str(customer.get("compensationPayerTypeID", "1")),
        "escrowWaiverTypeId": str(customer.get("escrowWaiverTypeId", "1")),
        "includeFlexTerms": bool(customer.get("includeFlexTerms", False)),
        "tracTypeId": str(customer.get("tracTypeId", "0")),
        "waivableFeeTypeIds": customer.get("waivableFeeTypeIds", ["0"]),
        "loanShieldTypeId": str(customer.get("loanShieldTypeId", "0")),
        "paPlusTypeId": str(customer.get("paPlusTypeId", "0")),
        "exactRateTypeId": str(customer.get("exactRateTypeId", "2")),
        "targetPriceValue": customer.get("targetPriceValue", 0),
        "targetCashValue": customer.get("targetCashValue", 0),
        "waiveUnderwritingFee": bool(customer.get("waiveUnderwritingFee", False)),
        "monthlyIncome": monthly_income,
        "buyDownAliasID": customer.get("buyDownAliasID", "None"),
        "firstTimeHomeBuyer": bool(customer.get("firstTimeHomeBuyer", False)),
        "loanTermIds": customer.get("loanTermIds", ["4", "3", "1", "2", "0"]),
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
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400

        min_savings = float(request.form.get('min_savings', 200))
        target_amount = float(request.form.get('target_amount', -2000))
        tolerance_str = request.form.get('tolerance')
        tolerance = float(tolerance_str) if (tolerance_str and tolerance_str.strip()) else None

        try:
            content = json.load(file)
            if isinstance(content, dict):
                content = [content]
            elif not isinstance(content, list):
                return jsonify({"message": "JSON must be a list or object"}), 400
        except json.JSONDecodeError:
            return jsonify({"message": "Invalid JSON file"}), 400

        access_token = get_access_token()

        results = []
        for customer in content:
            current_mp = safe_float(customer.get("currentMonthlyPayment"))
            if current_mp is None:
                continue

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
