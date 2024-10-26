from dash import Dash, html, dcc, _dash_renderer, callback, Input, Output
import dash_mantine_components as dmc
import dash
_dash_renderer._set_react_version("18.2.0")

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=dmc.styles.ALL
)

app.layout = dmc.MantineProvider(
    children=[
        html.Div(children=[
            dcc.Location(id='url', refresh=False),

            html.Div(className='header', children=[
                html.Img(className='sm_logo', src='assets/imgs/UNMSM-white.png'),

                html.Ul(className='menu', children=[
                    html.Li(  
                        children=[
                            html.Img(src='assets/imgs/icono-capas.png', className='menu-icon', style={'width': '25px',}),
                            dcc.Link('Modelo Logístico', href='/', className='link')
                        ],
                        id='li-edo1'
                    ),
                    
                     html.Li( 
                        children=[
                            html.Img(src='assets/imgs/icono-cohete.png', className='menu-icon', style={'width': '25px',}),
                            dcc.Link('Modelo Voltaren', href='/page2', className='link')
                        ],
                        id='li-page2'
                    ),
                     html.Li( 
                        children=[
                            html.Img(src='assets/imgs/destellos.png', className='menu-icon', style={'width': '25px', }),  # icono ejemplo
                            dcc.Link('Modelo SIR', href='/page3', className='link')
                        ],
                        id='li-page3'
                    ),
                     html.Li( 
                        children=[
                            html.Img(src='assets/imgs/destellos.png', className='menu-icon', style={'width': '25px', }),  # icono ejemplo
                            dcc.Link('Modelo SIS', href='/page4', className='link')
                        ],
                        id='li-page4'
                    ),
                     html.Li( 
                        children=[
                            html.Img(src='assets/imgs/destellos.png', className='menu-icon', style={'width': '25px', }),  # icono ejemplo
                            dcc.Link('Analisis Puntos', href='/page5', className='link')
                        ],
                        id='li-page5'
                    ),
                    html.Li( 
                        children=[
                            html.Img(src='assets/imgs/icono-enfermero2.png', className='menu-icon', style={'width': '25px', }),  # icono ejemplo
                            dcc.Link('Covid API', href='/page6', className='link')
                        ],
                        id='li-page6'
                    ),
                   
                ])

            ]),

            html.Div(className='page-container', children=[
                dash.page_container
            ])
        ], className="contenedor-principal")
    ]
)


# Para poder darle unas class de CSS activo cuando este en la pagina que corresponde.
@app.callback(
    [Output('li-edo1', 'className'),
    Output('li-page2', 'className'),
    Output('li-page3', 'className'), 
    Output('li-page4', 'className'), 
    Output('li-page5', 'className'),
    Output('li-page6', 'className'), 
    ],  
    [Input('url', 'pathname')]
)

def update_active_link(pathname):
    li_edo1_class = 'active' if pathname == '/' else ''
    li_page2_class = 'active' if pathname == '/page2' else '' 
    li_page3_class = 'active' if pathname == '/page3' else '' 
    li_page4_class = 'active' if pathname == '/page4' else '' 
    li_page5_class = 'active' if pathname == '/page5' else '' 
    li_page6_class = 'active' if pathname == '/page6' else '' 
    
    return li_edo1_class, li_page2_class, li_page3_class, li_page4_class,  li_page5_class,li_page6_class

if __name__ == '__main__':
    app.run(debug=True, port='1254')
