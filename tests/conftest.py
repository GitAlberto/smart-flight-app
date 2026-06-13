import pytest


@pytest.fixture
def mock_predict_response():
    return {"predicted_price": 7838.42, "currency": "INR", "model_version": "1.0.0"}


@pytest.fixture
def mock_fx_response():
    return {"rates": {"EUR": 0.011}}
