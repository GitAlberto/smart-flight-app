from unittest.mock import patch, Mock
import requests as req_lib
from app.api_client import predict_price


def test_predict_price_success(mock_predict_response):
    mock_resp = Mock()
    mock_resp.json.return_value = mock_predict_response
    mock_resp.raise_for_status.return_value = None

    with patch("app.api_client.requests.post", return_value=mock_resp):
        result = predict_price("Vistara", "Delhi", "Mumbai", "zero", "Economy", 2.0, 30)

    assert result is not None
    assert result["predicted_price"] == 7838.42
    assert result["currency"] == "INR"


def test_predict_price_returns_none_when_api_down():
    with patch("app.api_client.requests.post", side_effect=Exception("Connection refused")):
        result = predict_price("Vistara", "Delhi", "Mumbai", "zero", "Economy", 2.0, 30)

    assert result is None


def test_predict_price_returns_none_on_timeout():
    with patch("app.api_client.requests.post", side_effect=req_lib.exceptions.Timeout):
        result = predict_price("Vistara", "Delhi", "Mumbai", "zero", "Economy", 2.0, 30)

    assert result is None


def test_predict_price_returns_none_on_http_error():
    mock_resp = Mock()
    mock_resp.raise_for_status.side_effect = req_lib.exceptions.HTTPError("403")

    with patch("app.api_client.requests.post", return_value=mock_resp):
        result = predict_price("Vistara", "Delhi", "Mumbai", "zero", "Economy", 2.0, 30)

    assert result is None
