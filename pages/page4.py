import dash_mantine_components as dmc
import dash
from dash import dcc, html, Input, Output, callback
from utils import modelo_sis  # Cambiado de modelo_sir2 a modelo_sis
import plotly.graph_objects as go

dash.register_page(
    __name__,
    path='/page4', 
    name='Edo-4'   
)

layout = html.Div(className='envoltura-derecha', children=[
    html.Div(className="header-top", children=[
        html.H2('Modelo SIS', className="titulo-principal animate__animated animate__fadeInLeft  "),
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

    html.Div(className="wrapper-contenido ", children=[
        html.Div(className="col-5 ", children=[
            html.Div(className="grafica-principal  card-shadow  animate__animated   animate__fadeInUp animate__delay-0.2s", children=[
                dcc.Loading(
                    type='default',
                    children=dcc.Graph(id='figura_sis')  
                )
            ])
        ]),

        html.Div(className="col-3  animate__animated   animate__fadeInUp animate__delay-0.6s", children=[
            html.Div(className="grafica-circular  card-shadow", children=[
                dcc.Loading(
                    type='default',
                    children=dcc.Graph(id='grafica_circular_sis')  
                )
            ]),

            html.Div(className="graficas-secundarias ", children=[
                html.Div(className="grafica-barras  card-shadow", children=[
                    dcc.Loading(
                        type='default',
                        children=dcc.Graph(id='grafica_barras_sis') 
                    )
                ])
            ])
        ]),

        html.Div(className='col-2  card-shadow animate__animated   animate__fadeInUp animate__delay-0.9s', children=[
            html.H3("Parámetros", className="titulo-parametros"),

            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Población Total (N)", value=1000, id='poblacion_total_sis'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Infectados Iniciales", value=1, id='infectados_init_sis'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Recuperados Iniciales", value=0, id='recuperados_init_sis'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Tasa de Transmisión (beta)", value=0.3, id='beta_sis'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Tasa de Recuperación (gamma)", value=0.1, id='gamma_sis'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Tiempo Total", value=160, id='tiempo_sis'),
            ]),
            html.Div(className="w-input ocultar-slider", children=[
                dmc.Slider(min=10, max=1000, step=1, value=160, id='cant_sis', label="Particiones del Tiempo")
            ]),

            html.Div(className="w-input", children=[
                html.Label('Método Numérico', className="title-metodo-numerico"), 
                dcc.Dropdown(
                    id='metodo_numerico_sis',
                    options=[
                        {'label': 'Euler', 'value': 'euler'},
                        {'label': 'Runge-Kutta 4', 'value': 'rk4'},
                        {'label': 'ODEINT', 'value': 'odeint'}
                    ],
                    value='odeint',  
                    clearable=False,
                    style={"width": "100%"}
                ),
             ]),
             html.Div(className="w-input", children=[
                dmc.NumberInput(
                    id='input-particiones_sis',
                    min=1,
                    max=10000,
                    value=5000,  
                    label='Número de particiones',
                    step=1
                )  
            ]),
            html.Div(className="w-input", children=[
                html.Button('Reiniciar Valores', id='reiniciar_sis',  n_clicks=0, style={'width': '100%'},  className='btn_reiniciar',)
            ])

        ])
    ])
])

@callback(
    [Output('poblacion_total_sis', 'value'),
     Output('infectados_init_sis', 'value'),
     Output('recuperados_init_sis', 'value'),
     Output('beta_sis', 'value'),
     Output('gamma_sis', 'value'),
     Output('tiempo_sis', 'value'),
     Output('cant_sis', 'value'),
     Output('metodo_numerico_sis', 'value'),
     Output('input-particiones_sis', 'value')],
    Input('reiniciar_sis', 'n_clicks'),
    prevent_initial_call=True
)
def reiniciar_valores_sis(n_clicks):
    return 1000, 1, 0, 0.3, 0.1, 160, 160, 'odeint', 5000

@callback(
    [Output('figura_sis', 'figure'),
     Output('grafica_circular_sis', 'figure'),
     Output('grafica_barras_sis', 'figure')],
    [Input('poblacion_total_sis', 'value'),
     Input('infectados_init_sis', 'value'),
     Input('recuperados_init_sis', 'value'),
     Input('beta_sis', 'value'),
     Input('gamma_sis', 'value'),
     Input('tiempo_sis', 'value'),
     Input('cant_sis', 'value'),
     Input('metodo_numerico_sis', 'value'),
     Input('input-particiones_sis', 'value'),
     Input('reiniciar_sis', 'n_clicks')]  
)
def actualizar_graficas_sis(N, infectados_init, recuperados_init, beta, gamma, tiempo, cant, metodo_numerico, particiones, n_clicks):
    particiones = int(particiones) if particiones else 5000

    t, S, I = modelo_sis(N, infectados_init, recuperados_init, beta, gamma, tiempo, particiones, metodo_numerico)
    
    fig_sis = go.Figure()
    fig_sis.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles', line=dict(color='blue')))
    fig_sis.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados', line=dict(color='red')))
    fig_sis.update_layout(title="Simulación del Modelo SIS", xaxis_title="Tiempo (días)", yaxis_title="Número de personas")
    
    fig_circular = go.Figure(data=[go.Pie(
        labels=['Susceptibles', 'Infectados'],
        values=[S[-1], I[-1]],
        hole=.7,
        marker=dict(colors=['#98DED9', '#161D6F'])  
    )])
    fig_circular.update_layout(title="Distribución Final de Población", height=300)

    fig_barras = go.Figure(data=[
        go.Bar(name='Susceptibles', x=['Población Final'], y=[S[-1]], marker=dict(color='#98DED9')),
        go.Bar(name='Infectados', x=['Población Final'], y=[I[-1]], marker=dict(color='#161D6F')),
    ])
    fig_barras.update_layout(barmode='group', title="Comparación de Poblaciones Finales", height=300)

    return fig_sis, fig_circular, fig_barras
