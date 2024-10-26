import dash_mantine_components as dmc
import dash
from dash import dcc, html, Input, Output, callback
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

dash.register_page(
    __name__,
    path='/page5',
    name='Edo-5'
)

layout = html.Div(className='envoltura-derecha', children=[
    html.Div(className="header-top", children=[
        html.H2('Análisis Puntos Críticos', className="titulo-principal"),
        html.Div(className='header-usuario', children=[
            html.Img(className='header-usuario-img', src='assets/imgs/usuario.jpg'),
            html.P('Erick Garcia', className="header-usuario-text"),
        ])
    ]),
    html.Div(className="wrapper-contenido", children=[
        html.Div([
            dmc.TextInput(
                id='ingresar-primera-ecuacion',
                label='Ingresa tu ecuación',
                placeholder='Por ejemplo: 5 - y',
            ),
            dmc.TextInput(
                id='ingresar-segunda-ecuacion',
                label='Ingresa tu ecuación',
                placeholder='Por ejemplo: 5 - x',
            ),
            html.Button('Calcular puntos de equilibrio', id='boton-calcular', n_clicks=0),
            html.Div(id='resultado-equilibrio'),
            dcc.Markdown(id='resultado-jacobiano', mathjax=True),
            dcc.Markdown(id='resultado-autovalores', mathjax=True),
            html.Img(id='campo-vectores-img')  # Mostrar la imagen del campo de vectores aquí
        ]),
    ])
])

@callback(
    [Output('resultado-equilibrio', 'children'),
     Output('resultado-jacobiano', 'children'),
     Output('resultado-autovalores', 'children'),
     Output('campo-vectores-img', 'src')],
    [Input('ingresar-primera-ecuacion', 'value'),
     Input('ingresar-segunda-ecuacion', 'value'),
     Input('boton-calcular', 'n_clicks')]
)
def calcular_puntos_equilibrio_y_jacobiano(ecuacion1, ecuacion2, n_clicks):
    if n_clicks > 0 and ecuacion1 and ecuacion2:
        try:
      
            x, y = sp.symbols('x y')
            
            x_prima = sp.sympify(ecuacion1)
            y_prima = sp.sympify(ecuacion2)
            
            puntos_equilibrio = sp.solve([x_prima, y_prima], (x, y))
            
            # Calculamos la matriz Jacobiana
            Jacobiano = sp.Matrix([
                [sp.diff(x_prima, x), sp.diff(x_prima, y)],
                [sp.diff(y_prima, x), sp.diff(y_prima, y)]
            ])
            
            # Crear una representación más limpia de la matriz Jacobiana
            matriz_latex = "\\begin{bmatrix}\n"
            for i in range(Jacobiano.rows):
                fila = " & ".join([sp.latex(elem) for elem in Jacobiano.row(i)])
                matriz_latex += fila
                if i < Jacobiano.rows - 1:
                    matriz_latex += " \\\\\n"
                else:
                    matriz_latex += "\n"
            matriz_latex += "\\end{bmatrix}"
            
            resultado_equilibrio = f'Los puntos de equilibrio son: {puntos_equilibrio}'
            
            # Calcular autovalores
            autovalores_resultado = []
            for punto in puntos_equilibrio:
                Evaluar_Jacobiano = Jacobiano.subs({x: punto[0], y: punto[1]})
                autovalores = Evaluar_Jacobiano.eigenvals()
                autovalores_str = ', '.join([f'λ = {val} (multiplicidad: {multip})' for val, multip in autovalores.items()])
                autovalores_resultado.append(f'En el punto {punto}: Autovalores = {autovalores_str}')

            # Unir los resultados en formato Markdown
            resultado_autovalores = " \n\n ".join(autovalores_resultado)

            x_vals = np.linspace(-1, 10, 10) 
            y_vals = np.linspace(-1, 10, 10) 
            X, Y = np.mgrid[-1:10:20j, -1:10:20j] 

            # Evaluar las ecuaciones para obtener los vectores
            U = np.array([[float(x_prima.subs({x: xi, y: yi})) for xi, yi in zip(X[i], Y[i])] for i in range(len(X))])
            V = np.array([[float(y_prima.subs({x: xi, y: yi})) for xi, yi in zip(X[i], Y[i])] for i in range(len(Y))])

            # Crear el gráfico
            plt.figure(figsize=(6, 6))
            plt.quiver(X, Y, U, V, color='blue', angles='xy', scale_units='xy', scale=10)  
            plt.xlim([-1, 10])
            plt.ylim([-1, 10])
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Campo de Vectores')
            plt.grid()

            #Marcar los puntos críticos en rojo
            for punto in puntos_equilibrio:
                plt.plot(float(punto[0]), float(punto[1]), 'ro')  # 'ro' indica puntos en rojo
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close()

     
            image_src = f'data:image/png;base64,{encoded_image}'

            return resultado_equilibrio, f"$$ \\text{{Matriz Jacobiana}} = {matriz_latex} $$", f"$$ {resultado_autovalores} $$", image_src
            
        except Exception as e:
            return f'Error al procesar las ecuaciones: {str(e)}', '', '', ''  
    
    return 'Ingresa ambas ecuaciones y presiona "Calcular" para obtener los puntos de equilibrio.', '', '', ''
