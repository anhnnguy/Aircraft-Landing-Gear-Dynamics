import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

c_list = np.array([750,1500,2250]) # paramètres d'amortissement 750 est le plus faible et 2250 le plus fort
m = 100 # masse (kg)
k = 20000 # raideur (N/m)
x0 = 0 #position initiale(m)
v0 = 1 #vitesse initiale(m/s), apes la vibration libre, et la vibration plus constance par l'amortissement, la vitesse initiale est de 1 m/s
tfin = 2 #temps final(s)

def simuler_systeme(m,c,k,x0,v0,tfin):
    """simule la reponse dynamique du systeme masse-ressort -amortisseur"""

    def equations(t,y):
        x, v = y
        a = -(c*v + k*x)/m
        return [v, a]

    temps = np.linspace(0, tfin, 2000)

    solution = solve_ivp(equations, [0, tfin], [x0, v0], t_eval=temps, method='RK45', rtol=1e-9, atol=1e-11)
    x = solution.y[0]
    v = solution.y[1]
    a = -(c*v + k*x)/m 

    return temps, x, v, a
#resultats de la simulation pour chaque raideur
resultats = {}

for c in c_list:
    temps,x,v,a = simuler_systeme(m,c,k,x0,v0,tfin)
    resultats[c] = (temps,x,v,a)

plt.figure(figsize = (10,5))

#graphique 1: deplacement en fonction du temps pour chaque amortissement
plt.figure(figsize=(10,5))

for c in c_list:
    temps, x, v, a = resultats[c]
    plt.plot(temps, x, label=f"Amortissement c={c:.0f} N.s/m")

plt.xlabel("Temps (s)")
plt.ylabel("Deplacement x (m)")
plt.title("Deplacement en fonction du temps pour différentes raideurs")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("influence_amortissement_deplacement.png", dpi = 300)
plt.show()

#graphique 2: vitesse en fonction du temps pour chaque amortissement
plt.figure(figsize=(10,5))

for c in c_list:
    temps, x, v, a = resultats[c]
    plt.plot(temps, v, label=f"Amortissement c={c:.0f} N.s/m")

plt.xlabel("Temps (s)")
plt.ylabel("Vitesse v (m/s)")
plt.title("Vitesse en fonction du temps pour différentes raideurs")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("influence_amortissement_vitesse.png", dpi = 300)
plt.show()

#graphique 3: acceleration en fonction du temps pour chaque amortissement
plt.figure(figsize=(10,5))

for c in c_list:
    temps, x, v, a = resultats[c]
    plt.plot(temps, a, label=f"Amortissement c={c:.0f} N.s/m")

plt.xlabel("Temps (s)")
plt.ylabel("Acceleration a (m/s²)")
plt.title("Acceleration en fonction du temps pour différentes raideurs")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("influence_amortissement_acceleration.png", dpi = 300)
plt.show()


#tableau des resultats finaux pour chaque amortissement
print("\nComparaison des resultats finaux pour chaque amortissement:")
print("-" *75)
print(f"{'c (N.s/m)':>12}{'x_max (m)':>15}{'|a|_max (m/s²)':>18}{'zeta':>12}")

for c in c_list:
    temps, x, v, a = resultats[c]
    x_max = np.max(np.abs(x))
    a_max = np.max(np.abs(a))
    zeta = c/(2*np.sqrt(k*m)) #coefficient d'amortissement critique
    print(f"{c:>12.0f}{x_max:>15.6f}{a_max:>18.6f}{zeta:>12.4f}")

