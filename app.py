import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="El clima en mi negocio - GJA",
    page_icon="logo.jpeg",
    layout="wide",
)

# ---------- Estilos ----------
st.markdown(
    """
    <style>
    .banner {
        background: linear-gradient(90deg, #E8590C, #F59F00);
        padding: 28px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(232, 89, 12, 0.35);
    }
    .banner h1 { color: white; margin: 0; font-size: 2.2rem; }
    .banner p { margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.95; }

    div[data-testid="stMetric"] {
        background-color: white;
        border-left: 6px solid #E8590C;
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 18px rgba(232, 89, 12, 0.25);
    }
    div[data-testid="stMetricValue"] { font-size: 1.9rem; }

    h2, h3 { color: #E8590C; }
    h3 {
        border-bottom: 3px solid #F59F00;
        padding-bottom: 6px;
        display: inline-block;
    }

    .conclusion {
        background: linear-gradient(90deg, #FFF3E0, #FFE8D1);
        border-left: 8px solid #E8590C;
        border-radius: 12px;
        padding: 18px 22px;
        font-size: 1.15rem;
        color: #3B2A20;
        margin: 12px 0;
    }
    .pie {
        text-align: center;
        color: #8A6F5C;
        font-size: 0.9rem;
        padding: 24px 0 8px 0;
        border-top: 2px dashed #F59F00;
        margin-top: 32px;
    }
    button[data-baseweb="tab"] { font-size: 1.05rem; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="banner">
        <h1>👟 El clima en mi negocio - GJA</h1>
        <p>☀️ 🌧️ Cómo la lluvia y la temperatura influyen en mis ventas</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Cargar datos ----------
df = pd.read_excel("Proyecto_GJA_ el clima en mi negocio.xlsx")
df["Fecha"] = pd.to_datetime(df["Fecha"])

# ---------- Filtros ----------
st.sidebar.image("logo.jpeg", use_container_width=True)
st.sidebar.header("🔎 Filtros")

fecha_min = df["Fecha"].min().date()
fecha_max = df["Fecha"].max().date()
rango = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
)

orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
dias_disponibles = [d for d in orden_dias if d in df["Dia_semana"].unique()]
dias = st.sidebar.multiselect("Día de la semana", dias_disponibles, default=dias_disponibles)

umbral = st.sidebar.slider(
    "Un día cuenta como 'con lluvia' si llovió más de (mm):",
    min_value=0.0, max_value=10.0, value=1.0, step=0.5,
)

st.sidebar.markdown("---")
st.sidebar.caption("👟 Proyecto GJA · Análisis de ventas y clima")

if isinstance(rango, tuple) and len(rango) == 2:
    inicio, fin = rango
else:
    inicio, fin = fecha_min, fecha_max

dff = df[
    (df["Fecha"].dt.date >= inicio)
    & (df["Fecha"].dt.date <= fin)
    & (df["Dia_semana"].isin(dias))
].copy()

if dff.empty:
    st.warning("No hay datos con esos filtros. Cambia el rango de fechas o los días.")
    st.stop()

dff["Condicion"] = dff["Precipitacion_mm"].apply(
    lambda x: "Con lluvia" if x > umbral else "Sin lluvia"
)

# ---------- Métricas ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("👟 Pares vendidos", int(dff["Pares_vendidos"].sum()))
c2.metric("💰 Ingresos totales (COP)", f"{dff['Ingresos_COP'].sum():,.0f}")
c3.metric("📅 Días analizados", len(dff))
c4.metric("🌧️ Lluvia total", f"{dff['Precipitacion_mm'].sum():,.1f} mm")

st.write("")

# ---------- Pestañas ----------
tab1, tab2, tab3 = st.tabs(["📈 Resumen", "☔ Lluvia y ventas", "📋 Datos"])

# ----- Pestaña 1: Resumen -----
with tab1:
    st.subheader("💰 Ingresos por día")
    st.line_chart(dff.set_index("Fecha")["Ingresos_COP"], color="#E8590C")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🌧️ Lluvia por día (mm)")
        st.bar_chart(dff.set_index("Fecha")["Precipitacion_mm"], color="#1C7ED6")
    with col_b:
        st.subheader("🌡️ Temperatura media (°C)")
        st.line_chart(dff.set_index("Fecha")["Temperatura_media_C"], color="#F59F00")

# ----- Pestaña 2: Lluvia y ventas -----
with tab2:
    st.subheader("📊 Relación entre lluvia y ventas")

    resumen = (
        dff.groupby("Condicion")
        .agg(
            Dias=("Fecha", "count"),
            Promedio_pares=("Pares_vendidos", "mean"),
            Promedio_ingresos=("Ingresos_COP", "mean"),
        )
        .round(1)
    )

    if len(resumen) == 2:
        con = resumen.loc["Con lluvia", "Promedio_pares"]
        sin = resumen.loc["Sin lluvia", "Promedio_pares"]
        if sin > 0:
            dif = (con - sin) / sin * 100
            if dif < 0:
                texto = f"☔ En días con lluvia se venden en promedio <b>{abs(dif):.1f}% menos</b> pares que en días sin lluvia ({con:.1f} frente a {sin:.1f})."
            else:
                texto = f"☔ En días con lluvia se venden en promedio <b>{dif:.1f}% más</b> pares que en días sin lluvia ({con:.1f} frente a {sin:.1f})."
            st.markdown(f'<div class="conclusion">{texto}</div>', unsafe_allow_html=True)
    else:
        st.info("Con estos filtros solo hay un tipo de día (con lluvia o sin lluvia), así que no se puede comparar. Ajusta el filtro.")

    col_s, col_d = st.columns(2)
    with col_s:
        st.write("**Lluvia (mm) frente a pares vendidos**")
        st.scatter_chart(
            dff, x="Precipitacion_mm", y="Pares_vendidos",
            x_label="Lluvia (mm)", y_label="Pares vendidos",
            color="#E8590C",
        )
    with col_d:
        st.write("**Pares vendidos en promedio por día**")
        datos_barras = resumen.reset_index()[["Condicion", "Promedio_pares"]]
        base = alt.Chart(datos_barras).encode(
            x=alt.X("Condicion:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y(
                "Promedio_pares:Q",
                title="Pares por día",
                scale=alt.Scale(domain=[0, float(datos_barras["Promedio_pares"].max()) * 1.25]),
            ),
        )
        barras = base.mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=70).encode(
            color=alt.Color(
                "Condicion:N",
                scale=alt.Scale(domain=["Con lluvia", "Sin lluvia"], range=["#1C7ED6", "#E8590C"]),
                legend=None,
            )
        )
        etiquetas = base.mark_text(dy=-10, fontSize=16, fontWeight="bold", color="#3B2A20").encode(
            text=alt.Text("Promedio_pares:Q", format=".1f")
        )
        st.altair_chart(barras + etiquetas, use_container_width=True)

    st.write("**Promedio por tipo de día**")
    st.dataframe(resumen, use_container_width=True)

    corr = dff["Precipitacion_mm"].corr(dff["Pares_vendidos"])
    st.caption(f"Correlación entre lluvia y pares vendidos: {corr:.2f} (cerca de 0 = casi no hay relación; negativa = a más lluvia, menos ventas).")

# ----- Pestaña 3: Datos -----
with tab3:
    st.subheader("📋 Tabla de datos")
    st.dataframe(dff, use_container_width=True)

    with st.expander("🖼️ Ver gráficos originales del análisis"):
        st.image("grafico_ventas.png")
        st.image("grafico_lluvia.png")
        st.image("grafico_temperatura.png")

# ---------- Pie de página ----------
st.markdown(
    '<div class="pie">👟 GJA · El clima en mi negocio · Hecho con Streamlit y mucho café ☕</div>',
    unsafe_allow_html=True,
)