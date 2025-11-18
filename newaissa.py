import pandas as pd

df = pd.read_excel("total.xlsx")

# Automatically detect columns formatted like "0,025*Temp 400 °C*Z"
cols = [c for c in df.columns if "Temp" in c]

data = []

for col in cols:
    parts = col.split("*")
    
    additif = float(parts[0].replace(",", "."))      # ex: 0.025
    temp_str = parts[1]
    temp_str = temp_str.replace("Temp ", "")
    temp_str = temp_str.replace("°C", "")
    temp_str = temp_str.replace("° C", "")
    temp_str = temp_str.replace("◦C", "")
    temp_str = temp_str.replace("◦ C", "")
    temp_str = temp_str.replace(" C", "")
    temp_str = temp_str.replace("°", "")
    temp_str = temp_str.replace("◦", "")
    temp_str = temp_str.strip()

    temp = int(temp_str) 
    signe = "Positif" if parts[2] == "Z" else "Négatif"
    
    for val in df[col]:
        data.append([additif, temp, signe, val])
        
df_long = pd.DataFrame(data, columns=["Additif", "Température", "Signe", "Impédance"])

# Encode sign
df_long["Signe_enc"] = df_long["Signe"].map({"Positif": 1, "Négatif": -1})

print(df_long.head())


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

X = df_long[["Additif", "Température", "Signe_enc"]]
y = df_long["Impédance"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("R² =", r2_score(y_test, y_pred))
print("MAE =", mean_absolute_error(y_test, y_pred))

joblib.dump(model, "modele.pkl")
print("Modèle sauvegardé !")


import streamlit as st
import numpy as np
import joblib

model = joblib.load("modele.pkl")

st.title("🔬 Prédiction de l'impédance")

temp = st.slider("🌡️ Température (°C)", 100, 1000, 400, 50)
add = st.selectbox("🧪 Additif (%)", [0, 0.025, 0.05, 0.075, 0.1])
signe = st.selectbox("Signe", ["Positif", "Négatif"])

signe_enc = 1 if signe == "Positif" else -1

X_input = np.array([[add, temp, signe_enc]])

pred = model.predict(X_input)[0]

st.success(f"🔮 Impédance prédite : **{pred:.3f}**")