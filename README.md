# vehicles_env

# Dashboard Analítico: Mercado de Vehículos Usados en EE.UU. 🚗

Este proyecto es una aplicación web interactiva desarrollada con **Streamlit** y **Plotly** para realizar un Análisis Exploratorio de Datos (EDA) sobre un conjunto de datos que contiene más de 50,000 anuncios de venta de coches en los EE.UU.

La plataforma permite a los usuarios interactuar de forma dinámica con los datos mediante filtros personalizados en tiempo real para analizar la distribución de precios, la relación entre kilometraje y costo, y la condición física de los vehículos.

---

## 🚀 Características del Dashboard

*   **KPIs en tiempo real:** Resumen dinámico de anuncios totales, precio promedio, millaje promedio y cantidad de marcas tras aplicar filtros.
*   **Filtros Interactivos (Sidebar):** Segmentación por rango de precio, tipo de vehículo, tipo de combustible y tipo de transmisión.
*   **Visualizaciones con Plotly:**
    *   **Histograma interactivo:** Distribución de precios categorizada por tipo de vehículo (activado mediante un botón).
    *   **Gráfico de dispersión (Scatter Plot):** Relación de Odómetro vs. Precio según la condición del auto (controlado mediante una casilla de verificación).
*   **Explorador de datos crudos:** Tabla interactiva para inspeccionar los datos filtrados directamente desde la aplicación.

---

## 🛠️ Tecnologías Utilizadas

*   **Python** (versión 3.14.6)
*   **Streamlit** (para la interfaz web interactiva)
*   **Pandas** (para la manipulación y limpieza de los datos)
*   **Plotly Express** (para la creación de gráficos interactivos)

---

## 🔧 Instalación y Ejecución Local

Sigue estos pasos para clonar el repositorio, configurar tu entorno y correr la aplicación en tu computadora:

### 1. Clonar el repositorio
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd vehicles_env