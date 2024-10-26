import numpy as np
from scipy.integrate import odeint

def SIS_model(y, t, N, beta, gamma):
    S, I = y
    dSdt = -beta * S * I / N + gamma * I
    dIdt = beta * S * I / N - gamma * I
    return dSdt, dIdt

def metodo_euler(f, y0, t, N, beta, gamma):
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        y[i] = y[i - 1] + np.array(f(y[i - 1], t[i - 1], N, beta, gamma)) * dt
    return y.T

def metodo_rk4(f, y0, t, N, beta, gamma):
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        k1 = np.array(f(y[i - 1], t[i - 1], N, beta, gamma))
        k2 = np.array(f(y[i - 1] + k1 * dt / 2, t[i - 1] + dt / 2, N, beta, gamma))
        k3 = np.array(f(y[i - 1] + k2 * dt / 2, t[i - 1] + dt / 2, N, beta, gamma))
        k4 = np.array(f(y[i - 1] + k3 * dt, t[i - 1] + dt, N, beta, gamma))
        y[i] = y[i - 1] + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6
    return y.T

def modelo_sis(N, I0, R0, beta, gamma, tiempo, particiones, metodo):
    S0 = N - I0 - R0
    y0 = S0, I0
    t = np.linspace(0, tiempo, particiones)
    
    if metodo == 'euler':
        S, I = metodo_euler(SIS_model, y0, t, N, beta, gamma)
    elif metodo == 'rk4':
        S, I = metodo_rk4(SIS_model, y0, t, N, beta, gamma)
    else:  
        result = odeint(SIS_model, y0, t, args=(N, beta, gamma))
        S, I = result.T

    return t, S, I
