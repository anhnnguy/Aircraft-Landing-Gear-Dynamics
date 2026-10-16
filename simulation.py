import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

m = 100 #masse(kg)
k = 2e4 #raideur(N/m)
c = 1500 #amortissement visqueux(N.s/m)
x0 = 0 #position initiale(m)
v0 = 0 #vitesse initiale(m/s)
tfin = 2 #temps final(s)
F0 = 1000 #force appliquée(N)

# equations différentielles du système masse-ressort-amortisseur
def modele(t,y):
    x, v = y
    dxdt = v
    dvdt = -(k/m)*x - (c/m)*v + F0/m
    return [dxdt, dvdt]

#  resolution numérique de l'équation différentielle

tini = 0
t_eval = np.linspace(tini, tfin, 1000)
solution = integrate.solve_ivp(modele, [tini, tfin], [x0, v0], t_eval=t_eval, method='RK45', rtol=1e-9, atol=1e-11)

t = solution.t
x = solution.y[0]
v = solution.y[1]

a = -(k/m)*x - (c/m)*v + F0/m # acceleration

fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

axs[0].plot(t, x)
axs[0].set_ylabel("Deplacement x (m)")
axs[0].grid(True)

axs[1].plot(t, v)
axs[1].set_ylabel("Vitesse v (m/s)")
axs[1].grid(True)

axs[2].plot(t, a)
axs[2].set_ylabel("Acceleration a (m/s²)")
axs[2].set_xlabel("Temps (s)")
axs[2].grid(True)

fig.suptitle("Reponse du systeme masse-ressort-amortisseur")
plt.tight_layout()
plt.show()

# 7. Verification de l'etat final
print(f"Deplacement final : {x[-1]:.6f} m")
print(f"Deplacement statique theorique : {F0/k:.6f} m")