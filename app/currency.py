import requests

FALLBACK_RATE = 0.011


def convert_inr_to_eur(amount_inr: float) -> float:
    try:
        response = requests.get(
            "https://api.frankfurter.app/latest?from=INR&to=EUR",
            timeout=3,
        )
        taux = response.json()["rates"]["EUR"]
        return round(amount_inr * taux, 2)
    except Exception:
        return round(amount_inr * FALLBACK_RATE, 2)
