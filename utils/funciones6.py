import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests

#para pintar
import pandas as pd


def cargar_datos_covid(pais):
    # Carga los datos del pais,  q va entre parentesis es la variable del select que se pone en el select
    url = f"https://disease.sh/v3/covid-19/countries/{pais}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # es un objeto asignadolo para posteriormente llamarlo en los recuadros
        datos_procesados = {
            'confirmados': data['cases'],
            'recuperados': data['recovered'] if data['recovered'] is not None else 0,
            'fallecidos': data['deaths'] if data['deaths'] is not None else 0,
            'poblacion': data['population'],
            'activos': data['active'] if data['active'] is not None else 0,
            'casos_por_millon': data['casesPerOneMillion'],
            'fecha_actualizacion': data['updated'],
            'pais': data['country'],
            'criticos': data['critical'] if data['critical'] is not None else 0,
            #subdatos
            'muerte_por_persona': data['oneDeathPerPeople'],
            'pruebas': data['tests']
        }
        

        if datos_procesados['recuperados'] == 0:
            casos_no_activos = datos_procesados['confirmados'] - datos_procesados['activos']
            datos_procesados['recuperados'] = int(casos_no_activos * 0.8)
        
        if datos_procesados['activos'] == 0:
            datos_procesados['activos'] = ( datos_procesados['confirmados'] - datos_procesados['recuperados']  - datos_procesados['fallecidos']  )
        
        if datos_procesados['confirmados'] < (datos_procesados['recuperados'] + datos_procesados['fallecidos']):
            datos_procesados['recuperados'] = ( datos_procesados['confirmados'] - datos_procesados['fallecidos'] - datos_procesados['activos'] )
        
        # Me retorna los datos dependiendo del if
        return datos_procesados
    
    except Exception as e:
        print(f"Error al obtener datos de {pais}: {str(e)}")
        return None

def modelo_sir(state, t, beta, gamma, N):
    """
    Modelo SIR básico
    """
    S, I, R = state
    
    S = max(0, S)
    I = max(0, I)
    R = max(0, R)
    
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    
    return [dSdt, dIdt, dRdt]

def estimar_parametros_sir(datos):
    """
    Estima los parámetros beta y gamma basados en los datos reales
    """
    confirmados = datos['confirmados']
    recuperados = datos['recuperados']
    fallecidos = datos['fallecidos']
    N = datos['poblacion']
    
    if N == 0:
        raise ValueError("La población total no puede ser cero.")

    gamma = 1/14 
    R0 = 2.5 
    beta = R0 * gamma
    
    proporcion_casos = confirmados / N
    beta = beta * (1 + proporcion_casos)
    
    return beta, gamma

def generar_modelo_sir(datos):
    """
    Genera el modelo SIR y su visualización
    """
    # Parámetros iniciales
    N = datos['poblacion']
    I0 = datos['activos']
    R0 = datos['recuperados'] + datos['fallecidos']
    S0 = N - I0 - R0
    
    beta, gamma = estimar_parametros_sir(datos)
    
    # Período de simulación
    dias = 100
    t = np.linspace(0, dias, dias)
    
    solution = odeint(
        modelo_sir,
        [S0, I0, R0],
        t,
        args=(beta, gamma, N)
    )
    
    S, I, R = solution.T
    
    # El modelo se tiene que Normalizar a porcentajes
    S_norm = [s / N * 100 for s in S]
    I_norm = [i / N * 100 for i in I]
    R_norm = [r / N * 100 for r in R]

    S0_norm = (S0 / N) * 100
    I0_norm = (I0 / N) * 100
    R0_norm = (R0 / N) * 100
    
    fechas = [(datetime.now() + timedelta(days=i)) for i in range(dias)]
    
    # Crear figura
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=fechas, y=S_norm,
        mode='lines', name='Susceptibles (%)',
        line=dict(color='blue', dash='solid')
    ))
    
    fig.add_trace(go.Scatter(
        x=fechas, y=I_norm,
        mode='lines', name='Infectados (%)',
        line=dict(color='red', dash='solid')
    ))
    
    fig.add_trace(go.Scatter(
        x=fechas, y=R_norm,
        mode='lines', name='Recuperados (%)',
        line=dict(color='green', dash='solid')
    ))
    
    fig.add_trace(go.Scatter(
        x=[fechas[0]], y=[S0_norm],
        mode='markers', name='Susceptibles Actuales (%)',
        marker=dict(color='blue', size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=[fechas[0]], y=[I0_norm],
        mode='markers', name='Infectados Actuales (%)',
        marker=dict(color='red', size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=[fechas[0]], y=[R0_norm],
        mode='markers', name='Recuperados Actuales (%)',
        marker=dict(color='green', size=10)
    ))
    
    fig.update_layout(
        title={
            'text': f'Modelo SIR COVID-19 - {datos["pais"]}',
            'y':0.95,
            'x':0.02,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {
                'family': 'Roboto, sans-serif',  
                'size': 20,                
                'color': 'black',            
                'weight': 'bold'                 
            }
        },
        xaxis_title='Fecha',
        yaxis_title='Porcentaje de la población',
        yaxis=dict(
            range=[0, 100],
            tickformat='.1f',
            ticksuffix='%'
        ),
        hovermode='x unified',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        annotations=[
            dict(
                text=f'R₀ = {beta/gamma:.2f}',
                xref="paper", yref="paper",
                x=0.988, y=1.00,
                showarrow=False
            ),
            dict(
                text=f'β = {beta:.4f}',
                xref="paper", yref="paper",
                x=1.00, y=0.95,
                showarrow=False
            ),
            dict(
                text=f'γ = {gamma:.4f}',
                xref="paper", yref="paper",
                x=1.00, y=0.90,
                showarrow=False
            )
        ]
    )
    
    return fig


def obtener_datos_vacunacion():
    url = "https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=1"

    try:
     
        respuesta = requests.get(url)
        respuesta.raise_for_status() 

        data = respuesta.json()

        rows = []
        for item in data:
            country = item['country']
            vaccination_count = list(item['timeline'].values())[0]  # Obtener el valor del primer (y único) día en 'timeline'
            rows.append({'country': country, 'vaccination': vaccination_count})

        df = pd.DataFrame(rows)
        return df

    except Exception as e:
        print(f"Error al obtener datos de vacunación: {str(e)}")
        return pd.DataFrame(columns=['country', 'vaccination']) 


obtener_datos_vacunacion()
