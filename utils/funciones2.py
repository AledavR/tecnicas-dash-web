import numpy as np
import plotly.graph_objects as go

def modelo_depredador_presa(presa_init: float, depredador_init: float, alpha: float, beta: float, delta: float, gamma: float, tiempo: float, cant: int):
    """
    Retorna una gráfica del modelo depredador-presa (Lotka-Volterra).

    Parámetros:
    -------
    - prey_init: Población inicial de presas.
    - predator_init: Población inicial de depredadores.
    - alpha: Tasa de crecimiento de las presas.
    - beta: Tasa de depredación.
    - delta: Tasa de crecimiento de depredadores por consumo.
    - gamma: Tasa de mortalidad de depredadores.
    - tiempo: Tiempo total de simulación.
    - cant: Cantidad de particiones en el tiempo.
    """
    # Crear una malla de tiempo
    t = np.linspace(0, tiempo, cant)
    
    # Inicializar las poblaciones
    prey = np.zeros(cant)
    depredador = np.zeros(cant)
    prey[0] = presa_init
    depredador[0] = depredador_init

    for i in range(1, cant):
        prey[i] = prey[i - 1] + (alpha * prey[i - 1] - beta * prey[i - 1] * depredador[i - 1])
        depredador[i] = depredador[i - 1] + (delta * prey[i - 1] * depredador[i - 1] - gamma * depredador[i - 1])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=t, y=prey, mode='lines', name='Presas', line=dict(color='#161D6F')))
    fig.add_trace(go.Scatter(x=t, y=depredador, mode='lines', name='Depredadores', line=dict(color='#48CFCB')))
    
    # Personalizar el layout
    fig.update_layout(
        title={
        'text': 'Modelo Depredador-Presa (Lotka-Volterra)',
        'font': {
            'size': 20,         
            'color': 'black', 
            'family': 'Roboto, sans-serif', 
            'weight': 'bold' 
        },
            'x': 0.05, 
            'y': 0.93, 
            'xanchor': 'left',  
            'yanchor': 'top' 
        },
        xaxis_title='Tiempo',
        yaxis_title='Población',
        legend=dict(x=0, y=1),
        template='plotly_white'
    )
    
    return fig
