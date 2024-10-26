import dash_mantine_components as dmc
import dash
from dash import dcc, html, Input, Output, callback
from utils import ecuacion_logistica
from dash import dash_table
import numpy as np
import dash_daq as daq

dash.register_page(
    __name__,
    path='/',
    name='Edo-1'
)

###################################################################################
#
# Funciones de Estilos
#
###################################################################################
def obtener_slider_estilos(mostrar_vector):
    activar_estilos_verde = {
        "track": {"backgroundColor": "#34cd99"},
        "thumb": {"backgroundColor": "#34cd99", "border": "2px solid #2bb586"},
        "bar": {"backgroundColor": "#34cd99"}
    }
    
    activar_estilos_azul = {
        "track": {"backgroundColor": "#3B82F6"},
        "thumb": {"backgroundColor": "#3B82F6", "border": "2px solid #2563EB"},
        "bar": {"backgroundColor": "#3B82F6"}
    }
    
    desactivar_estilos = {
        "track": {"backgroundColor": "#E9ECEF"},
        "thumb": {"backgroundColor": "#ADB5BD", "border": "2px solid #6C757D"},
        "bar": {"backgroundColor": "#ADB5BD"}
    }
    
    current_styles_mallado = activar_estilos_verde if mostrar_vector else desactivar_estilos
    current_styles_size_vec = activar_estilos_azul if mostrar_vector else desactivar_estilos
    
    return current_styles_mallado, current_styles_size_vec

# Layout HTML
layout = html.Div(className='envoltura-derecha', children=[

    html.Div(className="header-top", children=[
        html.H2('Ecuación Logistica', className="titulo-principal"),
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
        html.Div(className='div_parametros', children=[
            html.H2('PARÁMETROS'),
            html.Div(className='div_flex', children=[
                html.Div([
                    dmc.NumberInput(label="Población Inicial", value=10, id='pob_ini',step=5),
                ]),
                html.Div([
                    dmc.NumberInput(label="Tiempo Inicial", value=0, id='time_ini'),
                ]),
                html.Div([
                    dmc.NumberInput(label="Tiempo Final", value=60, id='time_fin'),
                ]),
                html.Div([
                    dmc.NumberInput(label="Tasa de Crecimiento", value=0.15, id='r',step = 0.1),
                ]),
                html.Div([
                    dmc.NumberInput(label="Capacidad de Carga", value=150, id='K',step = 5),
                ]),
            ]),
        ]),

        html.Div(className='div_grafica', children=[
            html.Div(className="div_grafica_sub", children=[
                dcc.Loading(
                    type='default',
                    children=dcc.Graph(
                        id='figura_1',
                        style={
                            'width': '100%',
                            'height': '600px',
                            'margin': '0px',
                            'background': 'white'
                        },
                        config={
                            'modeBarButtonsToRemove': ['toImage', 'toggleSpikelines'],
                            'displayModeBar': False
                        }
                    )
                ),
            ]),

            html.Div(className="column3", children=[
                html.Div(className="card w-33", children=[
                    html.H3('Malla para el Campo de Vectores'),
                    dmc.Slider(
                        min=0.1,
                        max=40.0,
                        step=1.0,
                        value=15,
                        id='mallado',
                        disabled=True,
                        styles={
                            "track": {"backgroundColor": "#E9ECEF"},
                            "thumb": {"backgroundColor": "#ADB5BD", "border": "2px solid #6C757D"},
                            "bar": {"backgroundColor": "#ADB5BD"}
                        }
                    ),
                ]),
                html.Div(className="card w-33", children=[
                    html.H3('Tamaño del Vector'),
                    dmc.Slider(
                        min=0.1,
                        max=2,
                        step=0.1,
                        value=1,
                        id='size_vec',
                        disabled=True,
                        styles={
                            "track": {"backgroundColor": "#E9ECEF"},
                            "thumb": {"backgroundColor": "#ADB5BD", "border": "2px solid #6C757D"},
                            "bar": {"backgroundColor": "#ADB5BD"}
                        }
                    ),
                ]),
                html.Div(className="card w-33", children=[
                    html.P('Mostrar Campos Vectoriales'),
                    dmc.Switch(
                        id="toggle-vector-switch",
                        size="md",
                        checked=False
                    ),
                ]),
            ]),

            html.Div(className="wrapper-tabla", children=[
                html.Div(id='tabla-contenido', children=[
                    dash_table.DataTable(
                        id='tabla-datos',
                        columns=[
                            {"name": "Tiempo (t)", "id": "tiempo"},
                            {"name": "Población (P)", "id": "poblacion"}
                        ],
                        data=[],
                        style_table={'overflowX': 'auto', 'maxHeight': '650px'},
                        page_size=20,
                        style_cell={
                            'textAlign': 'left',
                            'backgroundColor': '#f9f9f9',
                            'color': '#333',
                            'fontSize': '14px',
                            'padding': '10px',
                            'border': '1px solid #ddd'
                        },
                        style_header={
                            'backgroundColor': '#3B82F6',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'border': '1px solid #ddd'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#f2f2f2'
                            },
                        ]
                    )
                ])
            ]),
        ]),
    ])
])


# Callback
@callback(
    [Output('figura_1', 'figure'),
     Output('tabla-datos', 'data'),
     Output('mallado', 'disabled'),
     Output('mallado', 'styles'),
     Output('size_vec', 'disabled'),
     Output('size_vec', 'styles')],
    [Input('pob_ini', 'value'),
     Input('time_ini', 'value'),
     Input('time_fin', 'value'),
     Input('r', 'value'),
     Input('K', 'value'),
     Input('mallado', 'value'),
     Input('size_vec', 'value'),
     Input('toggle-vector-switch', 'checked')]
)

#### Funciones EDO ########
def grafica_edo1(P0, t_i, t_f, r, k, mallado, size_vec, mostrar_vectores):
    t_values = np.linspace(t_i, t_f, int(mallado))
    
    poblacion_values = k * P0 * np.exp(r * t_values) / (P0 * np.exp(r * t_values) + (k - P0) * np.exp(r * t_i))

    fig = ecuacion_logistica(k, P0, r, t_i, t_f, int(mallado), size_vec, mostrar_vectores)

    fig.update_layout(
        title={
            'text': 'GRÁFICA DE LA EDO DE 1ER ORDEN',
            'x': 0.18,
            'y': 0.97,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(size=18, family='Roboto', color='#293058', weight='bold'),
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Roboto", size=16, color="black"),
        xaxis=dict(showgrid=False, gridcolor='lightgrey', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#f5f5f5'),
        legend=dict(
            x=1,
            y=1.2,
            xanchor='right',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='black',
            borderwidth=0
        ),
        template='plotly_white'
    )

    tabla_data = [{"tiempo": t, "poblacion": p} for t, p in zip(t_values, poblacion_values)]

    # Obtener los estilos de los sliders
    styles_mallado, styles_size_vec = obtener_slider_estilos(mostrar_vectores)

    return fig, tabla_data, not mostrar_vectores, styles_mallado, not mostrar_vectores, styles_size_vec
