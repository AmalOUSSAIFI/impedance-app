import streamlit as st
import numpy as np
import joblib

st.title("🔮 Modèle de Prédiction")

# Load model
model = joblib.load("modele_additif_temp.pkl")

st.write("Entrez les paramètres pour prédire l'impédance.")

# Inputs
temp = st.slider("🌡️ Température (°C)", 100, 1000, 400, 10)
additif = st.selectbox("🧪 Additif (%)", [0, 0.025, 0.05, 0.075, 0.1])
champ = st.number_input("⚡ Champ (V/m)", 0.0, 10.0, 5.0, 0.1)

if st.button("🔮 Prédire"):
    X_input = np.array([[temp, additif, champ]])
    pred = model.predict(X_input)[0]
    st.success(f"Impédance prédite : **{pred:.3f}**")