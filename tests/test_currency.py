from unittest.mock import patch, Mock
from app.currency import convert_inr_to_eur, FALLBACK_RATE


def test_convert_returns_positive_float(mock_fx_response):
    mock_resp = Mock()
    mock_resp.json.return_value = mock_fx_response

    with patch("app.currency.requests.get", return_value=mock_resp):
        result = convert_inr_to_eur(10000.0)

    assert isinstance(result, float)
    assert result > 0


def test_convert_uses_live_rate(mock_fx_response):
    mock_resp = Mock()
    mock_resp.json.return_value = mock_fx_response

    with patch("app.currency.requests.get", return_value=mock_resp):
        result = convert_inr_to_eur(10000.0)

    assert result == round(10000.0 * 0.011, 2)


def test_convert_fallback_when_api_down():
    with patch("app.currency.requests.get", side_effect=Exception("API down")):
        result = convert_inr_to_eur(10000.0)

    assert result == round(10000.0 * FALLBACK_RATE, 2)


def test_convert_fallback_is_positive():
    with patch("app.currency.requests.get", side_effect=Exception("timeout")):
        result = convert_inr_to_eur(5000.0)

    assert result > 0
