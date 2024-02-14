import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def dashboard(results_fol,top_n):

  data = pd.read_excel(ua.ultimo_archivo(results_fol, '.xlsx'))

  # Mapa de Energía Acumulada
  fig_map = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="Energia_acum",
                              size="Energia_acum", color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                              mapbox_style="carto-positron", title="Ubicación y Energía Acumulada")
  fig_map.show()

  top = data.nlargest(10, 'Energia_anual')
  fig_table = go.Figure(data=[go.Table(
      header=dict(values=['Índice', 'Energia_anual'],
                  fill_color='paleturquoise',
                  align='left'),
      cells=dict(values=[top.index, top['Energia_anual']],
                fill_color='lavender',
                align='left'))
  ])
  fig_table.update_layout(title="Top 10 Propiedades por Energía Anual")
  fig_table.show()

  # Crear subplots
  fig = make_subplots(
      rows=2, cols=2,
      subplot_titles=("Distribución de la Energía Anual", "Comparación Energía Diaria y Anual",
                      "Horas Acumuladas de Sol", "Energía Acumulada por Número de Paneles"))

  # Histograma de la energía anual
  fig.add_trace(go.Histogram(x=data["Energia_anual"], name="Energía Anual"), row=1, col=1)

  # Gráfico de barras comparando energía diaria y anual
  # Asumiendo que se desea comparar estas dos métricas para las primeras 10 propiedades
  fig.add_trace(go.Bar(x=data.head(10).index, y=data.head(10)["Energia_diaria"], name="Energía Diaria"), row=1, col=2)
  fig.add_trace(go.Bar(x=data.head(10).index, y=data.head(10)["Energia_anual"], name="Energía Anual"), row=1, col=2)

  # Gráfico de caja para las horas acumuladas de sol
  fig.add_trace(go.Box(y=data["horas_acum"], name="Horas Acumuladas de Sol"), row=2, col=1)

  # Gráfico de líneas variación de la energía acumulada con el número de paneles
  fig.add_trace(go.Scatter(x=data["n_paneles"], y=data["Energia_acum"], mode='lines', name="Energía Acumulada"), row=2, col=2)

  # Actualizar layout para ajustar
  fig.update_layout(height=800, showlegend=True, title_text="Gráficos Interactivos")

  fig.show()
