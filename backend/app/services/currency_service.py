from typing import Dict

# Base rates against 1 INR (scalable currency exchange matrix)
INR_EXCHANGE_RATES: Dict[str, float] = {
    "INR": 1.0,
    "USD": 0.012,       # 1 USD ≈ 83.33 INR
    "EUR": 0.011,       # 1 EUR ≈ 90.90 INR
    "GBP": 0.0095,      # 1 GBP ≈ 105.26 INR
    "AED": 0.044,       # 1 AED ≈ 22.72 INR
    "SGD": 0.016,       # 1 SGD ≈ 62.50 INR
    "THB": 0.43,        # 1 THB ≈ 2.32 INR
    "JPY": 1.85,        # 1 JPY ≈ 0.54 INR
    "CHF": 0.0105,      # 1 CHF ≈ 95.23 INR
    "CAD": 0.0163,      # 1 CAD ≈ 61.34 INR
    "AUD": 0.0182,      # 1 AUD ≈ 54.94 INR
}


class CurrencyService:
    @staticmethod
    def get_supported_currencies() -> Dict[str, str]:
        return {
            "INR": "Indian Rupee (₹)",
            "USD": "US Dollar ($)",
            "EUR": "Euro (€)",
            "GBP": "British Pound (£)",
            "AED": "UAE Dirham (د.إ)",
            "SGD": "Singapore Dollar (S$)",
            "THB": "Thai Baht (฿)",
            "JPY": "Japanese Yen (¥)",
            "CHF": "Swiss Franc (CHF)",
            "CAD": "Canadian Dollar (C$)",
            "AUD": "Australian Dollar (A$)",
        }

    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> float:
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()

        if from_curr == to_curr:
            return round(amount, 2)

        # Convert to INR first
        from_rate = INR_EXCHANGE_RATES.get(from_curr, 1.0)
        to_rate = INR_EXCHANGE_RATES.get(to_curr, 1.0)

        # Amount in INR
        amount_in_inr = amount / from_rate
        # Amount in target currency
        converted = amount_in_inr * to_rate
        return round(converted, 2)

    @staticmethod
    def format_currency(amount: float, currency: str) -> str:
        symbols = {
            "INR": "₹", "USD": "$", "EUR": "€", "GBP": "£",
            "AED": "AED ", "SGD": "S$", "THB": "฿", "JPY": "¥", "CHF": "CHF "
        }
        sym = symbols.get(currency.upper(), f"{currency.upper()} ")
        return f"{sym}{amount:,.2f}"
