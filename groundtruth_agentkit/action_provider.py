import requests
from typing import Optional, Dict, Any

DEFAULT_NODE_URL = "https://unlisted-cabbage-swaddling.ngrok-free.dev"

class GroundTruthActionProvider:
    """
    Coinbase AgentKit-compatible Action Provider for GroundTruth Autonomous Oracle.
    Executes real-world due diligence gated by automated x402 Base USDC micro-settlements.
    """
    def __init__(self, node_base_url: str = DEFAULT_NODE_URL):
        self.node_base_url = node_base_url.rstrip("/")

    def _execute_x402_call(self, url: str, wallet_signer=None) -> Dict[str, Any]:
        headers = {"ngrok-skip-browser-warning": "true"}
        res = requests.get(url, headers=headers, timeout=12)

        if res.status_code == 200:
            return res.json()

        if res.status_code == 402:
            challenge = res.json()
            terms = challenge.get("accepts", [{}])[0]
            payee = terms.get("payee")
            amount_micro = terms.get("amount", 5000000)
            amount_usdc = amount_micro / 1_000_000

            if not wallet_signer:
                raise PermissionError(
                    f"HTTP 402 Payment Required: Endpoint requires {amount_usdc} USDC transfer to {payee} on Base Mainnet."
                )

            tx_hash = wallet_signer.transfer(to=payee, amount=amount_usdc, asset_id="usdc")
            fulfillment_headers = {
                "PAYMENT-SIGNATURE": str(tx_hash),
                "ngrok-skip-browser-warning": "true"
            }
            fulfilled_res = requests.get(url, headers=fulfillment_headers, timeout=15)
            
            if fulfilled_res.status_code == 200:
                return fulfilled_res.json()
            else:
                raise RuntimeError(f"Fulfillment failed: HTTP {fulfilled_res.status_code} - {fulfilled_res.text}")

        raise RuntimeError(f"Unexpected response: HTTP {res.status_code} - {res.text}")

    def check_rural_risk(self, apn: str, wallet_signer=None) -> Dict[str, Any]:
        url = f"{self.node_base_url}/api/v1/rural-risk?apn={apn}"
        return self._execute_x402_call(url, wallet_signer)

    def check_flood_zone(self, lat: float, lon: float, wallet_signer=None) -> Dict[str, Any]:
        url = f"{self.node_base_url}/v1/environmental/flood-zone?lat={lat}&lon={lon}"
        return self._execute_x402_call(url, wallet_signer)

    def triage_tax_auction_lot(self, apn: str, county: str = None, wallet_signer=None) -> Dict[str, Any]:
        url = f"{self.node_base_url}/v1/sniper/triage?apn={apn}"
        if county:
            url += f"&county={county}"
        return self._execute_x402_call(url, wallet_signer)

    def get_municipal_permits(self, city: str, query: str = "commercial", limit: int = 5) -> Dict[str, Any]:
        url = f"{self.node_base_url}/v1/civic/permits/{city}/{query}?limit={limit}"
        return self._execute_x402_call(url)
