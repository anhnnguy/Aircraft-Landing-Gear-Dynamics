"""
Landing Impact Model — 1 DOF
Simplified vertical impact with a unilateral spring-damper.
z is positive downward; z=0 is first contact; z>0 is compression.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#tous les parametres sont dépensées à le modèle simplifié basé sur les paramètres de recherche Kang et al. (2023)
m0 = 1633 # masse totale de 2 trains d'atterrissage d'avion (kg)
m = m0/2 # masse d'un train d'atterrissage (kg) on suppose que les deux trains d'atterrissage sont identiques
k_c = 46680 # raideur de la suspension (N/m)
c_c = 7337 # coefficient d'amortissement (N.s/m)
v0 = 3.05 # vitesse initiale (m/s)
z0 = 0 # position initiale (m)
g = 9.81 # acceleration due to gravity (m/s²)
tfin = 2 # temps final (s)
n_points = 4001

OUTPUT_DIR = Path(__file__).resolve().parent / "results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def contact_force(z,vz):
    """Force de contact dirigée vers le haut ; nulle en l'absence de contact et jamais de nature tractionnelle"""
    if z <= 0.0:
        Fc = 0.0
    else:
        Fc = max(0.0, k_c * z + c_c * vz)  # force de contact (N)
    return Fc

def equation_state(t,state):
    """Équations d'état du système masse-ressort-amortisseur unilatéral"""
    z, vz = state
    Fc = contact_force(z, vz)
    az = g - Fc / m  # acceleration due to contact force and gravity
    return [vz, az]

# il y a 3 phases dans le modèle d'impact d'atterrissage :
# 1. phase de compression : l'objet est vers le bas, le raideur est compressé et on a la force de l'amortissement z >0, v> 0
# 2. phase de monter: l'objet se déplace vers le haut, la compression diminue progressivement et la force de contact s'atténue
# 3. phase de décollage: La force d'amortissement du ressort s'annule alors que l'objet est encore en mouvement ascendant. C'est ce point que la fonction leave_contact cherche à détecter.

def leave_contact(t, state):
    """Arrêt au décollage: la force brute ressort-amortisseur atteint zéro tandis que 
       la masse monte. Cela évite de simuler un sans contact 
       phase avec la même équation de contact."""
    z, vz = state
    if z <= 0.0: # L'objet se trouve soit hors de la zone de compression
        return -1.0  # la sign moins aide resoudre le cas de quitter de contact
    return k_c * z + c_c * vz

leave_contact.terminal = True
leave_contact.direction = -1

time = np.linspace(0.0, tfin, n_points)
solution = solve_ivp(
    equation_state, (time[0], time[-1]), [z0, v0],
    t_eval=time, events=leave_contact, max_step=0.001,
    rtol=1e-8, atol=1e-10
)

t = solution.t
z, vz = solution.y
Fc = np.array([contact_force(zi, vi) for zi, vi in zip(z, vz)])
az = g - Fc / m
compression = np.maximum(z, 0.0)
max_compression = float(np.max(compression))
max_contact_force = float(np.max(Fc))
max_abs_acceleration = float(np.max(np.abs(az)))
i_max = int(np.argmax(compression))
t_max_compression = float(t[i_max])

# Verification: solution numerical vs solution analytique
# Valider quand le train d'atterrisage contacte avec le sol et Fc = k_c*z + c_c*vz.

omega_n = np.sqrt(k_c / m)
zeta = c_c / (2 * np.sqrt(m * k_c))
omega_d = omega_n * np.sqrt(1 - zeta**2)
alpha = zeta * omega_n

z_eq = g / omega_n**2
A = z0 - z_eq
B = (v0 + alpha * A) / omega_d

exp_term = np.exp(-alpha * t)
cos_term = np.cos(omega_d * t)
sin_term = np.sin(omega_d * t)

z_analytical = z_eq + exp_term * (
    A * cos_term + B * sin_term
)

vz_analytical = exp_term * (
    (-alpha * A + omega_d * B) * cos_term
    + (-alpha * B - omega_d * A) * sin_term
)

az_analytical = g - (
    k_c * z_analytical + c_c * vz_analytical
) / m

# Skip the first millisecond to avoid the contact-switching point at t = 0.
mask = t >= 0.001

error_z = np.max(np.abs(z[mask] - z_analytical[mask]))
error_v = np.max(np.abs(vz[mask] - vz_analytical[mask]))
error_a = np.max(np.abs(az[mask] - az_analytical[mask]))

print("\n=== NUMERICAL VALIDATION ===")
print(f"Natural frequency          : {omega_n:.4f} rad/s")
print(f"Damping ratio              : {zeta:.4f}")
print(f"Damped frequency           : {omega_d:.4f} rad/s")
print(f"Static equilibrium         : {z_eq * 1000:.3f} mm")
print(f"Analytical max compression : {np.max(z_analytical) * 1000:.3f} mm")
print(f"Max displacement error     : {error_z:.6e} m")
print(f"Max velocity error         : {error_v:.6e} m/s")
print(f"Max acceleration error     : {error_a:.6e} m/s²")


plots = [
    (z * 1000, "déplacement vertical z", "déplacement [mm]", "landing_impact_deplacement.png"),
    (vz, "vitesse verticale", "vitesse [m/s]", "landing_impact_vitesse.png"),
    (az, "acceleration verticale", "Acceleration [m/s²]", "landing_impact_acceleration.png"),
    (Fc / 1000, "force de contact", "Contact force [kN]", "landing_impact_contact_force.png"),
]
for values, title, ylabel, filename in plots:
    plt.figure(figsize=(9, 5))
    plt.plot(t, values, linewidth=1.8)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.35)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=200)
    plt.close()

data = np.column_stack((t, z, vz, az, Fc))
np.savetxt(
    OUTPUT_DIR / "landing_impact_data.csv", data, delimiter=",",
    header="time_s,z_m,vitesse_m_s,acceleration_m_s2,contact_force_N",
    comments=""
)

print("\n=== LANDING IMPACT MODEL — 1 DOF ===")
print(f"Equivalent mass             : {m:.2f} kg")
print(f"Stiffness                   : {k_c:.2f} N/m")
print(f"Damping coefficient         : {c_c:.2f} N.s/m")
print(f"Initial downward velocity   : {v0:.2f} m/s")
print(f"Simulation end time reached : {t[-1]:.4f} s")
print(f"Maximum compression         : {max_compression * 1000:.3f} mm")
print(f"Time at maximum compression : {t_max_compression:.4f} s")
print(f"Maximum contact force       : {max_contact_force / 1000:.3f} kN")
print(f"Maximum |acceleration|      : {max_abs_acceleration:.3f} m/s^2")
print(f"Outputs saved in            : {OUTPUT_DIR}")
