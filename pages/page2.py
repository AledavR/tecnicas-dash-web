import dash_mantine_components as dmc
import dash
from dash import dcc, html, Input, Output, callback
from utils import modelo_depredador_presa
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(
    __name__,
    path='/page2',
    name='Edo-2'
)

layout = html.Div(className='envoltura-derecha', children=[
     html.Div(className="header-top", children=[
        html.H2('Modelo Depredador-Presa', className="titulo-principal"),
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
        
        
        html.Div(className="col-5", children=[
            html.Div(className="grafica-principal card-shadow", children=[
                dcc.Loading(
                    type='default',
                    children=dcc.Graph(id='figura_2')
                )
            ]),
            
           
        ]),

         html.Div(className="col-3", children=[
            html.Div(className="grafica-circular card-shadow", children=[
                        dcc.Loading(
                            type='default',
                            children=dcc.Graph(id='grafica-circular')
                        )
                    ]),

             html.Div(className="graficas-secundarias card-shadow", children=[
                   
                    html.Div(className="grafica-barras", children=[
                        dcc.Loading(
                            type='default',
                            children=dcc.Graph(id='grafica-barras')
                        )])
            ])

        ]),

        html.Div(className='col-2 card-shadow', children=[

            html.Div(className='', children=[
                    html.H3("Parametros", className="titulo-parametros"),

                    html.Div(className="w-input", children=[
                        dmc.NumberInput(label="Población Inicial de Presas", value=40, id='prey_init'),
                    ]),
                    html.Div(className="w-input", children=[
                        dmc.NumberInput(label="Población Inicial de Depredadores", value=9, id='predator_init'),
                    ]),

                    html.Div(className="w-input", children=[
                        dmc.NumberInput(label="Tasa de Crecimiento de Presas (alpha)", value=0.1, id='alpha' ),
                    ]),

                    html.Div(className="w-input", children=[
                        dmc.NumberInput(label="Tasa de Depredación (beta)", value=0.02, id='beta'),
                    ]),

                    html.Div(className="w-input", children=[
                        dmc.NumberInput(label="Tasa de Crecimiento de Depredadores (delta)", value=0.01, id='delta'),
                    ]),

                    html.Div(className="w-input", children=[
                        dmc.NumberInput(label="Tasa de Mortalidad de Depredadores (gamma)", value=0.1, id='gamma'),  
                    ]),

                    html.Div(className="w-input", children=[
                    dmc.NumberInput(label="Tiempo Total", value=100, id='tiempo'), 
                    ]),
                    
                    html.Div(className="w-input", children=[
                    dmc.Slider(min=10, max=1000, step=1, value=100,  id='cant', label="Particiones del Tiempo")
                    ]),
                    
                ]),
            ])


    ])



])

@callback(
    [Output('figura_2', 'figure'),
     Output('grafica-circular', 'figure'),
     Output('grafica-barras', 'figure')],
    [Input('prey_init', 'value'),
     Input('predator_init', 'value'),
     Input('alpha', 'value'),
     Input('beta', 'value'),
     Input('delta', 'value'),
     Input('gamma', 'value'),
     Input('tiempo', 'value'),
     Input('cant', 'value')]
)
def actualizar_graficas(prey_init, predator_init, alpha, beta, delta, gamma, tiempo, cant):
    fig_principal = modelo_depredador_presa(prey_init, predator_init, alpha, beta, delta, gamma, tiempo, cant)
    
    fig_principal.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    fig_circular = go.Figure(data=[go.Pie(
        labels=['Presas', 'Depredadores'],
        values=[prey_init, predator_init],
        hole=.7,
        marker=dict(colors=['#98DED9', '#161D6F'])
    )])

    fig_circular.update_layout(
        title={
            'text': "Distribución Inicial de Población",
            'font': {
                'size': 20,    
                'color': 'black',
                'family': 'Roboto, sans-serif',
                'weight': 'bold'
            },
            'x': 0.05, 
            'y': 0.9,
            'xanchor': 'left', 
            'yanchor': 'top'  
        },
        height=350,  # Aumentado para dar más espacio vertical total
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(
            t=80,    # Aumentado significativamente el margen superior
            b=80,    # Margen inferior para la leyenda
            l=20,
            r=20,
            pad=20
        ),
        paper_bgcolor='rgba(0,0,0,0)'  # Fondo transparente para mejor integración
    )
    
    fig_barras = go.Figure(data=[
        go.Bar(name='Presas', x=['Población Inicial'], y=[prey_init],  marker=dict(color='#98DED9')),
        go.Bar(name='Depredadores', x=['Población Inicial'], y=[predator_init], marker=dict(color='#161D6F'))
    ])
    fig_barras.update_layout(
        barmode='group',
        title={
            'text': "Comparación de Poblaciones Iniciales",
            'font': {
                'size': 20,    
                'color': 'black',
                'family': 'Roboto, sans-serif',
                'weight': 'bold'
            },
            'x': 0.05, 
            'y': 0.9,
            'xanchor': 'left', 
            'yanchor': 'top'  
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(
            t=80,    # Aumentado significativamente el margen superior
            b=80,    # Margen inferior para la leyenda
            l=20,
            r=20,
            pad=20
        ),
        height=300
    )
    
    return fig_principal, fig_circular, fig_barras
external_stylesheets = [
    {
        'selector': '.graficas-container',
        'rule': '''
            display: flex;
            flex-direction: column;
            gap: 10px;
        '''
    },
    {
        'selector': '.graficas-secundarias',
        'rule': '''
            display: flex;
            gap: 10px;
        '''
    },
    {
        'selector': '.grafica-circular, .grafica-barras',
        'rule': '''
            flex: 1;
            min-width: 0;
        '''
    }
]