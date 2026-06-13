import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import streamlit as st
from app.api_client import predict_price
from app.currency import convert_inr_to_eur
from monitoring.logger import log_request

st.set_page_config(page_title="Smart Flight Pricer", page_icon="✈️")
st.title("✈️ Smart Flight Pricer")
st.caption("Estimation du prix d'un billet basée sur l'IA")

airline = st.selectbox(
    "Compagnie aérienne",
    ["Air_India", "Vistara", "Indigo", "GO_FIRST", "AirAsia", "SpiceJet"],
)
source_city = st.selectbox(
    "Ville de départ",
    ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"],
)
destination_city = st.selectbox(
    "Ville d'arrivée",
    ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"],
)
stops = st.selectbox("Nombre d'escales", ["zero", "one", "two_or_more"])
flight_class = st.selectbox("Classe", ["Economy", "Business"])
duration = st.number_input(
    "Durée du vol (heures)", min_value=0.5, max_value=50.0, value=2.0, step=0.5
)
days_left = st.slider("Jours avant le départ", 1, 365, 30)

if st.button("Estimer le prix", type="primary"):
    if source_city == destination_city:
        st.warning("La ville de départ et la ville d'arrivée doivent être différentes.")
        st.stop()

    inputs = {
        "airline": airline,
        "source_city": source_city,
        "destination_city": destination_city,
        "stops": stops,
        "class": flight_class,
        "duration": duration,
        "days_left": days_left,
    }

    start = time.time()
    result = predict_price(
        airline, source_city, destination_city, stops, flight_class, duration, days_left
    )
    latency_ms = (time.time() - start) * 1000

    if result:
        prix_inr = result["predicted_price"]
        prix_eur = convert_inr_to_eur(prix_inr)
        st.success(
            f"Prix estimé : **{prix_inr:,.0f} INR** — soit **~{prix_eur:.2f} €**"
        )
        log_request(inputs, result, latency_ms, error=None)
    else:
        st.error(
            "Le service de prédiction est actuellement indisponible. "
            "Veuillez réessayer dans quelques instants."
        )
        log_request(inputs, None, latency_ms, error="API indisponible")
