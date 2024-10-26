import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
from utils import cargar_datos_covid, generar_modelo_sir, obtener_datos_vacunacion

import requests
import pandas as pd
import io

usuarios = [
    {'nombre': 'Erick Garcia', 'img': 'assets/imgs/usuario1.jpg', 'color': 'lightblue'},
    {'nombre': 'Alejandro Ramirez', 'img': 'assets/imgs/usuario2.jpg', 'color': 'lightgreen'},
    {'nombre': 'Rocio Guiterrez', 'img': 'assets/imgs/usuario3.jpg', 'color': 'lightcoral'}
]


dash.register_page(
    __name__,
    path='/page6',
    name='Edo-6'
)

# Obtener datos iniciales
df = obtener_datos_vacunacion()
datos_iniciales = cargar_datos_covid('usa')

fig = px.choropleth(
    df,
    locations='country',
    locationmode='country names',
    color='vaccination',
    hover_name='country',
    title='Vacunación por País',
    color_continuous_scale=px.colors.sequential.Blues,
    labels={'vaccination': 'Número de Vacunaciones'},
)

fig.update_layout(
    width=None,
    height=None,
    margin=dict(l=20, r=20, t=40, b=80),
    title={
        'text': 'Vacunación por País',
        'font': {
            'family': 'Roboto, sans-serif', 
            'size': 20,                     
            'color': 'black',               
            'weight': 'bold'                 
        },
        'y': 0.95,                          
        'x': 0.5,                       
        'xanchor': 'center',               
        'yanchor': 'top'                   
    },
    coloraxis_colorbar=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5,
        len=0.6,
        title=dict(
            text='Número de Vacunaciones',
            side='bottom'
        )
    )
)


figura_inicial = generar_modelo_sir(datos_iniciales) if datos_iniciales else {}

# Layout de la página
layout = html.Div(className='envoltura-derecha', children=[
    html.Div(className="header-top", children=[
        html.H2('Análisis COVID-19 con Modelo SIR', className="titulo-principal"),
        html.Div(className="grupo-container", children=[
            html.H4('Grupo', className='grupo-titulo', ),
            html.Div(className='integrantes card-shadow', children=[
                html.Div([
                    html.Img(className='header-usuario-img', src='assets/imgs/usuario.jpg'),
                    html.P('Erick Garcia', className="header-usuario-text header-grupo-item"),
                ], className="header-usuario"),
                 html.Div([
                    html.Img(className='header-usuario-img', src='assets/imgs/usuario-alejandro.jpeg'),
                    html.P('Alejandro Ramirez', className="header-usuario-text header-grupo-item"),
                ], className="header-usuario"),
                 html.Div([
                    html.Img(className='header-usuario-img', src='assets/imgs/usuario-rocio.jpg'),
                    html.P('Rocio Guiterrez', className="header-usuario-text header-grupo-item"),
                ], className="header-usuario"),
            ]),
        ]),
    ]),
    html.Div(className="wrapper-contenido", children=[
        html.Div([
            html.Div([
                html.H4(id='titulo-datos-covid', className="titulo-size-20"), 
                html.Div([
                    html.Label('Seleccionar País', className='mb-2 f-light'),
                    dcc.Dropdown(
                        id='selector-pais',
                        options=[
                            {'label': 'Estados Unidos', 'value': 'usa'},
                            {'label': 'Perú', 'value': 'peru'},
                            {'label': 'Italia', 'value': 'italy'},
                            {'label': 'España', 'value': 'spain'}
                        ],
                        value='usa',
                        className='mb-4'
                    ),
                    html.Div([
                        html.Button(
                            'Actualizar Datos',
                            id='boton-calcular',
                            className='btn btn-primary mb-4'
                        ),
                        html.Button(
                            'Exportar datos',
                            id='boton-exportar-datos',
                            className='btn btn-primary mb-4'
                        ),
                        dcc.Download(id='descargar-datos')
                    ], className="wrapper-botones-covid")
                ], className="subwrapper-filtrador-selector")
            ], className="cabecera-covid-filtro"),
            
            # Resultado COVID con estructura unificada
            html.Div(id='resultado-covid', className='mb-4', children=[
                html.Div([
                    html.Div(className='caja-datos-paises', children=[
                        html.Div(className='card mt-20 w-25 card-shadow', children=[
                            html.P('Confirmados', className="card_subtitulo"),
                            html.H3(f'{datos_iniciales["confirmados"]:,}', className="card_titulo_dato"),
                            html.Div([
                                html.P('Población total', className="card_subdatos_titulo"),
                                html.P(f'{datos_iniciales["poblacion"]:,}', className="card_subdatos_dato boton-data-success"),
                            ], className="card_subdatos")
                        ]),
                        html.Div(className='card card-shadow w-25 mt-20', children=[
                            html.P('Activos', className="card_subtitulo"),
                            html.H3(f'{datos_iniciales["activos"]:,}', className="card_titulo_dato"),
                            html.Div([
                                html.P('Pruebas covid', className="card_subdatos_titulo"),
                                html.P(f'{datos_iniciales["pruebas"]:,}', className="card_subdatos_dato boton-data-danger"),
                            ], className="card_subdatos")
                        ]),
                        html.Div(className='card card-shadow w-25 mt-20', children=[
                            html.P('Recuperados', className="card_subtitulo"),
                            html.H3(f'{datos_iniciales["recuperados"]:,}', className="card_titulo_dato"),
                            html.Div([
                                html.P('Pacientes críticos', className="card_subdatos_titulo"),
                                html.P(f'{datos_iniciales["criticos"]:,}', className="card_subdatos_dato boton-data-danger"),
                            ], className="card_subdatos")
                        ]),
                        html.Div(className='card card-shadow w-25 mt-20', children=[
                            html.P('Fallecidos', className="card_subtitulo"),
                            html.H3(f'{datos_iniciales["fallecidos"]:,}', className="card_titulo_dato"),
                            html.Div([
                                html.P('Muerte por persona', className="card_subdatos_titulo"),
                                html.P(f'{datos_iniciales["muerte_por_persona"]:,}', className="card_subdatos_dato boton-data-danger"),
                            ], className="card_subdatos")
                        ])
                    ])
                ])
            ] if datos_iniciales else dcc.Loading(
                type="circle",
                children=html.Div(className='caja-datos-paises')
            )),
     
            html.Div([
                html.Div([
                    dcc.Graph(id='grafico-sir', figure=figura_inicial),
                ], className="w-60 card-shadow mt-20"),
                html.Div([
                    dcc.Graph(
                        id='vacunacion-map',
                        figure=fig
                    )
                ], className="w-35 card-shadow mt-20")
            ], className="wrapper-grafico-sir"),
            
            html.Div([
                html.H4("Información del Modelo SIR:", className='mb-3'),
                html.P([
                    "β (beta): Tasa de transmisión - La velocidad a la que se propaga la enfermedad",
                    html.Br(),
                    "γ (gamma): Tasa de recuperación - La velocidad a la que se recuperan los infectados",
                    html.Br(),
                    "R₀: Número básico de reproducción - Número promedio de nuevos casos por cada infectado"
                ])
            ], className='modelo-info mt-4'),
        ], className="full-width"),
    ])
])

@callback(
    Output('resultado-covid', 'children'),
    Output('grafico-sir', 'figure'),
    Output('titulo-datos-covid', 'children'), 
    [Input('boton-calcular', 'n_clicks'),
     Input('selector-pais', 'value')],
)
def actualizar_datos_covid(n_clicks, pais_seleccionado):
    try:
        datos = cargar_datos_covid(pais_seleccionado)
        
        if not datos:
            return html.Div('No se encontraron datos para este país.'), {}, 'Datos de COVID-19:'
        
        # Generar el modelo SIR
        fig_modelo_sir = generar_modelo_sir(datos)
        
        titulo = f'Datos de COVID-19 en {datos["pais"]}:'
        resumen = html.Div([
            html.Div(className='caja-datos-paises', children=[
                html.Div(className='card mt-20 w-25 card-shadow', children=[
                    html.P('Confirmados', className="card_subtitulo"),
                    html.H3(f'{datos["confirmados"]:,}', className="card_titulo_dato"),
                    html.Div([
                        html.P('Población total', className="card_subdatos_titulo"),
                        html.P(f'{datos["poblacion"]:,}', className="card_subdatos_dato boton-data-verde"),
                    ], className="card_subdatos")
                ]),
                html.Div(className='card card-shadow w-25 mt-20', children=[
                    html.P('Activos', className="card_subtitulo"),
                    html.H3(f'{datos["activos"]:,}', className="card_titulo_dato"),
                    html.Div([
                        html.P('Pruebas covid', className="card_subdatos_titulo"),
                        html.P(f'{datos["pruebas"]:,}', className="card_subdatos_dato boton-data-success"),
                    ], className="card_subdatos")
                ]),
                html.Div(className='card card-shadow w-25 mt-20', children=[
                    html.P('Recuperados', className="card_subtitulo"),
                    html.H3(f'{datos["recuperados"]:,}', className="card_titulo_dato"),
                    html.Div([
                        html.P('Pacientes críticos', className="card_subdatos_titulo"),
                        html.P(f'{datos["criticos"]:,}', className="card_subdatos_dato boton-data-danger"),
                    ], className="card_subdatos")
                ]),
                html.Div(className='card card-shadow w-25 mt-20', children=[
                    html.P('Fallecidos', className="card_subtitulo"),
                    html.H3(f'{datos["fallecidos"]:,}', className="card_titulo_dato"),
                    html.Div([
                        html.P('Muerte por persona', className="card_subdatos_titulo"),
                        html.P(f'{datos["muerte_por_persona"]:,}', className="card_subdatos_dato boton-data-warning"),
                    ], className="card_subdatos")
                ])
            ])
        ])
        
        return resumen, fig_modelo_sir, titulo

    except Exception as e:
        return html.Div(f'Error al obtener datos: {str(e)}'), {}, 'Datos de COVID-19:'

@callback(
    Output('descargar-datos', 'data'),
    Input('boton-exportar-datos', 'n_clicks'),
    Input('selector-pais', 'value'),  # Este input solo se usa para acceder al país seleccionado
    prevent_initial_call=True
)
def exportar_datos(n_clicks, pais_seleccionado):
  
    if n_clicks is None:
        return dash.no_update

    datos = cargar_datos_covid(pais_seleccionado)

    if not datos:
        return None 

    datos_exportar = {
        'Indicador': ['confirmados', 'activos', 'recuperados', 'fallecidos', 
                      'poblacion', 'casos_por_millon', 'criticos', 
                      'muerte_por_persona', 'pruebas'],
        'Valor': [
            datos['confirmados'],
            datos['activos'],
            datos['recuperados'],
            datos['fallecidos'],
            datos['poblacion'],
            datos['casos_por_millon'],
            datos['criticos'],
            datos['muerte_por_persona'],
            datos['pruebas']
        ]
    }

    df = pd.DataFrame(datos_exportar)
    
    return dcc.send_data_frame(df.to_csv, f'datos_covid_{pais_seleccionado}.csv', index=False)
