import numpy as np
from scipy.integrate import odeint

def SIR_model2(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

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
        k1 = np.array(f(y[i - 1], t[i - 1], N, beta, gamma)) * dt
        k2 = np.array(f(y[i - 1] + k1/2, t[i - 1] + dt/2, N, beta, gamma)) * dt
        k3 = np.array(f(y[i - 1] + k2/2, t[i - 1] + dt/2, N, beta, gamma)) * dt
        k4 = np.array(f(y[i - 1] + k3, t[i - 1] + dt, N, beta, gamma)) * dt
        y[i] = y[i - 1] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return y.T


def modelo_sir2(N, I0, R0, beta, gamma, tiempo_total, particiones, metodo='odeint'):
    S0 = N - I0 - R0
    y0 = S0, I0, R0
    #particiones = 20
    t = np.linspace(0, tiempo_total, particiones)
    
    if metodo == 'odeint':
        ret = odeint(SIR_model2, y0, t, args=(N, beta, gamma))
        S, I, R = ret.T 
    elif metodo == 'euler':
        ret = metodo_euler(SIR_model2, y0, t, N, beta, gamma)
        S, I, R = ret  
    elif metodo == 'rk4':
        ret = metodo_rk4(SIR_model2, y0, t, N, beta, gamma)
        S, I, R = ret  

    return t, S, I, R


