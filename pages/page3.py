import dash_mantine_components as dmc
import dash
from dash import dcc, html, Input, Output, callback
from utils import modelo_sir2
import plotly.graph_objects as go

dash.register_page(
    __name__,
    path='/page3', 
    name='Edo-3'   
)

layout = html.Div(className='envoltura-derecha', children=[
    html.Div(className="header-top", children=[
        html.H2('Modelo SIR', className="titulo-principal animate__animated animate__fadeInLeft  "),
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
                    children=dcc.Graph(id='figura_sir')  
                )
            ])
        ]),

        html.Div(className="col-3  animate__animated   animate__fadeInUp animate__delay-0.6s", children=[
            html.Div(className="grafica-circular  card-shadow", children=[
                dcc.Loading(
                    type='default',
                    children=dcc.Graph(id='grafica_circular')  
                )
            ]),

            html.Div(className="graficas-secundarias ", children=[
                html.Div(className="grafica-barras  card-shadow", children=[
                    dcc.Loading(
                        type='default',
                        children=dcc.Graph(id='grafica_barras') 
                    )
                ])
            ])
        ]),

        html.Div(className='col-2  card-shadow animate__animated   animate__fadeInUp animate__delay-0.9s', children=[

            html.H3("Parámetros", className="titulo-parametros"),

            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Población Total (N)", value=1000, id='poblacion_total'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Infectados Iniciales", value=1, id='infectados_init'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Recuperados Iniciales", value=0, id='recuperados_init'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Tasa de Transmisión (beta)", value=0.3, id='beta'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Tasa de Recuperación (gamma)", value=0.1, id='gamma'),
            ]),
            html.Div(className="w-input", children=[
                dmc.NumberInput(label="Tiempo Total", value=160, id='tiempo'),
            ]),
            html.Div(className="w-input ocultar-slider", children=[
                dmc.Slider(min=10, max=1000, step=1, value=160, id='cant', label="Particiones del Tiempo")
            ]),

            html.Div(className="w-input", children=[
                html.Label('Método Numérico', className="title-metodo-numerico"), 
                dcc.Dropdown(
                    id='metodo_numerico',
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
                    id='input-particiones',
                    min=1,
                    max=10000,
                    value=5000,  
                    label='Número de particiones',
                    step=1
                )  
            ]),
            html.Div(className="w-input", children=[
                html.Button('Reiniciar Valores', id='reiniciar',  n_clicks=0, style={'width': '100%'},  className='btn_reiniciar',)
            ])

        ])
    ])
])



@callback(
    [Output('poblacion_total', 'value'),
     Output('infectados_init', 'value'),
     Output('recuperados_init', 'value'),
     Output('beta', 'value'),
     Output('gamma', 'value'),
     Output('tiempo', 'value'),
     Output('cant', 'value'),
     Output('metodo_numerico', 'value'),
     Output('input-particiones', 'value')],
    Input('reiniciar', 'n_clicks'),
    prevent_initial_call=True
)
def reiniciar_valores(n_clicks):
    return 1000, 1, 0, 0.3, 0.1, 160, 160, 'odeint', 5000

@callback(
    [Output('figura_sir', 'figure'),
     Output('grafica_circular', 'figure'),
     Output('grafica_barras', 'figure')],
    [Input('poblacion_total', 'value'),
     Input('infectados_init', 'value'),
     Input('recuperados_init', 'value'),
     Input('beta', 'value'),
     Input('gamma', 'value'),
     Input('tiempo', 'value'),
     Input('cant', 'value'),
     Input('metodo_numerico', 'value'),
     Input('input-particiones', 'value'),
     Input('reiniciar', 'n_clicks')]  
)
def actualizar_graficas(N, infectados_init, recuperados_init, beta, gamma, tiempo, cant, metodo_numerico, particiones, n_clicks):
    particiones = int(particiones) if particiones else 5000

    t, S, I, R = modelo_sir2(N, infectados_init, recuperados_init, beta, gamma, tiempo, particiones, metodo_numerico)
    
    
    fig_sir2 = go.Figure()
    fig_sir2.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles', line=dict(color='blue')))
    fig_sir2.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados', line=dict(color='red')))
    fig_sir2.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados', line=dict(color='green')))
    fig_sir2.update_layout(title="Simulación del Modelo SIR", xaxis_title="Tiempo (días)", yaxis_title="Número de personas")
    
    fig_circular2 = go.Figure(data=[go.Pie(
        labels=['Susceptibles', 'Infectados', 'Recuperados'],
        values=[S[-1], I[-1], R[-1]],
        hole=.7,
        marker=dict(colors=['#98DED9', '#161D6F', '#A1D99B'])  
    )])
    fig_circular2.update_layout(title="Distribución Final de Población", height=300)

    fig_barras2 = go.Figure(data=[
        go.Bar(name='Susceptibles', x=['Población Final'], y=[S[-1]], marker=dict(color='#98DED9')),
        go.Bar(name='Infectados', x=['Población Final'], y=[I[-1]], marker=dict(color='#161D6F')),
        go.Bar(name='Recuperados', x=['Población Final'], y=[R[-1]], marker=dict(color='#A1D99B'))
    ])
    fig_barras2.update_layout(barmode='group', title="Comparación de Poblaciones Finales", height=300)

    return fig_sir2, fig_circular2, fig_barras2
