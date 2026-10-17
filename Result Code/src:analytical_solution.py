import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#parameters
m = 100.0
k = 20_000.0
c = 1500.0
F0 = 1_000.0

alpha = c/(2*m)
omega_d = k/m - alpha**2

t = np.linspace(0, 2, 2000)

x_analytical = (F0/k)*(1-np.exp(-alpha*t)*(np.cos(omega_d*t) + (alpha/omega_d)*np.sin(omega_d*t)))

def model(t, y):
    x, v = y
    return [v, -(k/m)*x - (c/m)*v + F0/m]

sol = solve_ivp(model, [0, 2], [0, 0], t_eval=t, tol=1e-9, atol=1e-11)

x_numerical = sol.y[0]

error = np.abs(x_analytical - x_numerical)

plt.plot(t, x_analytical, label="Solution analytique")
plt.plot(t, x_numerical, "--", label="Solution numerique")
plt.xlabel("Temps (s)")
plt.ylabel("Deplacement x (m)")
plt.title("Verification du modele")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print(f"Erreur maximale : {error:.3e} m")
print(f"Deplacement statique : {F0/k:.4f} m")
