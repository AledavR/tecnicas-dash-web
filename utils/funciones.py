# Librerías
import numpy as np 
import plotly.graph_objects as go  # Gráfica
import plotly.figure_factory as ff  # Mallado de vectores

# Funciones

# Función Logística
def ecuacion_logistica(K: float, P0: float, r: float, t0: float, t: float, cant: float, scale: float, show_vectors: bool):
    """
    Retorna una gráfica de la ecuación logística con su campo vectorial.

    Parámetros:
    -------
    - K: Capacidad de carga.
    - P0: Población Inicial.
    - r: Tasa de crecimiento poblacional.
    - t0: Tiempo inicial.
    - t: Tiempo final.
    - cant: Las particiones para el eje temporal y espacial.
    - scale: Tamaño del vector del campo vectorial.
    """

    # Rango de P y t
    P_values = np.linspace(0, K + 5, cant)
    t_values = np.linspace(0, t, cant)

    # Crear una malla de puntos (P, t)
    T, P = np.meshgrid(t_values, P_values)

    # Definir la EDO
    dP_dt = r * P * (1 - P / K)

    # Solución exacta de la Ecuación Logística
    funcion = K * P0 * np.exp(r * t_values) / (P0 * np.exp(r * t_values) + (K - P0) * np.exp(r * t0))

    # Campo vectorial: dP/dt (componente vertical)
    U = np.ones_like(T)  # Componente en t (horizontal)
    V = dP_dt            # Componente en P (vertical)

    # Crear el campo de vectores con Plotly
    if show_vectors:
        fig = ff.create_quiver(
            T, P, U, V,
            scale=scale,
            line=dict(color='blue', width=1),
            showlegend=False
        )
    else:
        fig = go.Figure()   

    fig.add_trace(
        go.Scatter(
            x=t_values,
            y=funcion,
            mode='markers+lines',
            line=dict(color='#3eb9f6'),
            name='Ecuación Logística',
            marker=dict(
                color='white',  
                line=dict(color='#3eb9f6', width=2), 
                size=8  
            ),
            fill='tozeroy', 
            fillcolor='rgba(62, 185, 246, 0.2)'
        )
    )

    # Agregar línea de capacidad de carga solo una vez
    fig.add_trace(
        go.Scatter(
            x=[0, t],
            y=[K, K],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Capacidad de carga'
        )
    )

    # Etiquetas para la gráfica
    fig.update_layout(
        title={
            'text': 'Campo de vectores de dP/dt = rP(1 - P/K)',
            'x': 0.5,
            'y': 0.98,
            'xanchor': 'center'
        },
        xaxis_title='Tiempo (t)',
        xaxis_title_font=dict(size=14, color='black', family='Roboto'), 
        yaxis_title='Población (P)',
        yaxis_title_font=dict(size=14, color='black', family='Roboto'), 
        #width=800,
        template='plotly_white',
        margin=dict(
            l=0,
            r=10,
            t=20,
            b=0
        ),
        legend=dict(orientation='h', y=1.1),

        # Espaciado entre la gráfica y los ejes
        xaxis=dict(
            title='',  # 'Tiempo (t)'
            showline=False,
            linewidth=2,
            linecolor='black',
            mirror=True,
            ticks='outside',
            tickwidth=5,
            ticklen=8,
            tickcolor='white',
            tickfont=dict(
                color='#d1d5db'  # Cambia 'red' por el color que desees
            )
        ),
        yaxis=dict(
            title='',  # 'Población (P)'
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            ticks='outside',
            tickwidth=2,
            ticklen=8,
            tickcolor='white',
            tickfont=dict(
                color='#d1d5db'  # Cambia 'red' por el color que desees
            )
        )
    )

    # Contorno a la gráfica
    fig.update_xaxes(
        mirror=True,
        showline=True,  # true
        linecolor='white',
        gridcolor='gray',
        zeroline=False, 
        showgrid=False
    )
    fig.update_yaxes(
        mirror=True,
        showline=True,
        linecolor='white',
        gridcolor='#d5d9df',
        showgrid=False
    )

    return fig
