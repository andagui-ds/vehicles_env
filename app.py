import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA (Debe ser el primer comando de Streamlit)
# ==============================================================================
st.set_page_config(
    page_title="Dashboard de Vehículos Usados EE.UU.",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para mejorar la tipografía y los contenedores
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# CARGAR Y LIMPIAR DATOS
# ==============================================================================


@st.cache_data  # Para que cargue los datos en memoria y la app sea súper rápida al filtrar
def load_data():
    df = pd.read_csv('notebooks/vehicles_us.csv')

    # Tratamiento rápido de nulos para no romper los gráficos
    df['paint_color'] = df['paint_color'].fillna('Desconocido')
    df['is_4wd'] = df['is_4wd'].fillna(0).astype(int)
    df['model_year'] = df['model_year'].fillna(df['model_year'].median())
    df['odometer'] = df['odometer'].fillna(df['odometer'].median())

    # Extraer la marca del vehículo del modelo (ej: "bmw x5" -> "bmw")
    df['brand'] = df['model'].apply(lambda x: str(x).split()[0].upper())
    return df


df = load_data()

# ==============================================================================
# BARRA LATERAL - FILTROS DINÁMICOS
# ==============================================================================
st.sidebar.header("🎯 Panel de Filtros")
st.sidebar.write("Segmenta los datos para actualizar el análisis:")

# 1. Filtro de Precio (Rango)
min_price, max_price = int(df['price'].min()), int(df['price'].max())
price_range = st.sidebar.slider(
    "Rango de Precio ($)",
    min_value=min_price,
    max_value=max_price,
    # Límite por defecto en 100k para filtrar valores atípicos extremos
    value=(min_price, 100000)
)

# 2. Filtro Multiselección de Tipo de Vehículo
types_available = sorted(df['type'].dropna().unique())
selected_types = st.sidebar.multiselect(
    "Tipo de Vehículo",
    options=types_available,
    default=types_available[:5]  # Preselecciona los primeros 5 por defecto
)

# 3. Filtro Multiselección de Combustible
fuels_available = sorted(df['fuel'].dropna().unique())
selected_fuels = st.sidebar.multiselect(
    "Tipo de Combustible",
    options=fuels_available,
    default=fuels_available
)

# 4. Filtro por Transmisión
trans_available = sorted(df['transmission'].dropna().unique())
selected_trans = st.sidebar.multiselect(
    "Transmisión",
    options=trans_available,
    default=trans_available
)

# Aplicar filtros al DataFrame original de manera dinámica
df_filtered = df[
    (df['price'] >= price_range[0]) &
    (df['price'] <= price_range[1]) &
    (df['type'].isin(selected_types if selected_types else types_available)) &
    (df['fuel'].isin(selected_fuels if selected_fuels else fuels_available)) &
    (df['transmission'].isin(selected_trans if selected_trans else trans_available))
]

# ==============================================================================
# CUERPO PRINCIPAL - DASHBOARD
# ==============================================================================

# Encabezado con Texto (Requisito 1)
st.title("🚗 Dashboard Analítico: Mercado de Vehículos Usados")
st.markdown("""
Esta plataforma interactiva analiza un conjunto de datos de **51,526 anuncios de venta de coches** en los EE.UU. 
Utiliza los controles laterales para explorar cómo interactúan variables como el precio, millaje, año del modelo, tipo de combustible y transmisión.
""")

st.markdown("---")

# MÓDULO DE MÉTRICAS CLAVE (KPIs)
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
with col_kpi1:
    st.metric("Total Anuncios Filtrados", f"{df_filtered.shape[0]:,}")
with col_kpi2:
    st.metric("Precio Promedio", f"${df_filtered['price'].mean():,.2f}")
with col_kpi3:
    st.metric("Odómetro Promedio", f"{df_filtered['odometer'].mean():,.0f} mi")
with col_kpi4:
    st.metric("Marcas Distintas", f"{df_filtered['brand'].nunique()}")

st.markdown("---")

# SECCIÓN DE GRÁFICOS
col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("📊 Distribución de Precios y Tipos de Vehículo")

    # Histograma Interactivo con Botón (Requisito 2)
    st.write("Presiona el botón para construir el histograma de distribución de precios para los datos filtrados:")
    hist_button = st.button("Construir Histograma de Precios")

    if hist_button:
        with st.spinner("Generando Histograma..."):
            fig_hist = px.histogram(
                df_filtered,
                x='price',
                color='type',
                marginal='box',  # Agrega un boxplot arriba para ver la mediana y cuartiles
                title="Distribución de Precios por Categoría de Vehículo",
                color_discrete_sequence=px.colors.qualitative.Safe,
                labels={'price': 'Precio ($)',
                        'count': 'Frecuencia de Anuncios'}
            )
            fig_hist.update_layout(
                template="plotly_white",
                legend_title_text="Tipo de Vehículo",
                height=450
            )
            st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info(
            "💡 Haz clic en 'Construir Histograma de Precios' para visualizar esta distribución.")

with col_graph2:
    st.subheader("📈 Análisis de Kilometraje vs Precio")

    # Gráfico de Disperción con Casilla de Verificación (Requisito 3)
    # "value=True" para que inicie activado por diseño pro
    build_scatter = st.checkbox("Activar Gráfico de Dispersión", value=True)

    if build_scatter:
        with st.spinner("Generando Gráfico de Dispersión..."):
            fig_scatter = px.scatter(
                df_filtered,
                x='odometer',
                y='price',
                # Colorear por condición de auto (excellent, good, fair...)
                color='condition',
                # Mostrar detalles al pasar el cursor
                hover_data=['model_year', 'model'],
                title="Relación entre Odómetro y Precio por Condición",
                labels={
                    'odometer': 'Odómetro (Millas)', 'price': 'Precio ($)', 'condition': 'Condición'},
                color_discrete_sequence=px.colors.qualitative.Bold,
                opacity=0.6
            )
            fig_scatter.update_layout(
                template="plotly_white",
                height=450
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("⚠️ Gráfico de dispersión desactivado por el usuario.")

st.markdown("---")

# SECCIÓN EXTRA SÚPER PRO: ANÁLISIS DE DATOS TABULAR
st.subheader("📁 Explorador de Datos Crudos")
with st.expander("Ver tabla de datos filtrados"):
    st.write("Mostrando las primeras 100 filas del conjunto de datos filtrado:")
    st.dataframe(
        df_filtered[['brand', 'model', 'model_year', 'price',
                     'odometer', 'condition', 'fuel', 'transmission']].head(100),
        use_container_width=True
    )
