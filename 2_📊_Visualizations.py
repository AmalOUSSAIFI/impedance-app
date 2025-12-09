import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title("📊 Interactive Visualizations")

# Load Excel
df = pd.read_excel("total.xlsx")

st.subheader("📁 Aperçu des données")
st.write(df.head())

# ----- 1️⃣ CORRELATION HEATMAP -----

st.subheader("🔥 Heatmap de corrélation")
corr = df.corr(numeric_only=True)

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Matrice de corrélation"
)
st.plotly_chart(fig_corr, use_container_width=True)

# ----- 2️⃣ IMPEDANCE VS TEMPERATURE (interactive line plot) -----

st.subheader("🌡️ Évolution Impédance vs Température")

# Extract temperature columns
temp_cols = [c for c in df.columns if "Temp" in c]

temp_values = [int(c.split("Temp ")[1].split(" ")[0]) for c in temp_cols]

fig_line = go.Figure()

for col in temp_cols:
    fig_line.add_trace(go.Scatter(
        x=temp_values,
        y=df[col],
        mode="lines+markers",
        name=col
    ))

fig_line.update_layout(
    xaxis_title="Température (°C)",
    yaxis_title="Impédance",
    title="Impédance en fonction de la température"
)

st.plotly_chart(fig_line, use_container_width=True)

# ----- 3️⃣ 3D SCATTER (Temperature vs Additif vs Impedance) -----

st.subheader("🧪 3D Scatter : Additif - Température - Impédance")

# Detect additif columns (ex: 0,025*Temp 400 °C*Z)
impedance_cols = [c for c in df.columns if "*" in c]

data_points = []

for col in impedance_cols:
    try:
        additif = col.split("*Temp")[0].replace(",", ".")
        additif = float(additif)

        temp = int(col.split("Temp ")[1].split(" ")[0])

        for val in df[col]:
            data_points.append([additif, temp, float(val)])

    except:
        pass

df3d = pd.DataFrame(data_points, columns=["Additif", "Température", "Impédance"])

fig3d = px.scatter_3d(
    df3d,
    x="Additif", y="Température", z="Impédance",
    color="Température",
    title="Visualisation 3D des Impédances"
)

st.plotly_chart(fig3d, use_container_width=True)

# ----- 4️⃣ 3D SURFACE (ALL IMPEDANCE VALUES) -----

st.subheader("🌈 3D Surface : Impédance = f(Additif, Température)")

# Prepare grid for surface
try:
    df_surface = df3d.pivot_table(
        index="Additif",
        columns="Température",
        values="Impédance",
        aggfunc="mean"
    )

    X = df_surface.columns.values      # Températures
    Y = df_surface.index.values        # Additifs
    Z = df_surface.values              # Impédance

    fig_surface = go.Figure(data=[go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale="Viridis"
    )])

    fig_surface.update_layout(
        title="Surface 3D des Impédances",
        scene=dict(
            xaxis_title="Température (°C)",
            yaxis_title="Additif (%)",
            zaxis_title="Impédance"
        ),
        width=900,
        height=700
    )

    st.plotly_chart(fig_surface, use_container_width=True)

except Exception as e:
    st.error("Impossible de générer la surface 3D (données irrégulières).")
    st.write("Erreur :", e)