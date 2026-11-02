
"""
Etude de l'influence de la masse equivalente sur l'impact
d'un train d'atterrissage simplifie a un degre de liberte (1 DOF).

Modele : masse - ressort - amortisseur unilateral.
Convention : z positif vers le bas.
z = 0 : premier contact avec le sol.
z > 0 : compression du ressort.

Parametres de reference inspires de Kang et al. (2023).
"""

from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# ============================================================
# 1. PARAMETRES DU MODELE
# ============================================================

m0 = 1633.0
m_ref = m0 / 2

# Valeurs de masse a etudier (kg)
m_values = m_ref * np.array([0.50, 0.75, 1.00, 1.25, 1.50])

v0 = 3.05
k_c = 46680.0
c_c = 7337.0

z0 = 0.0
g = 9.81

tfin = 2.0
n_points = 4001

time = np.linspace(0.0, tfin, n_points)


# ============================================================
# 2. DOSSIER DE SORTIE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "results" / "influence_masse"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. MODELE PHYSIQUE
# ============================================================

def contact_force(z, vz):
    """
    Force de contact dirigee vers le haut.
    """

    if z <= 0.0:
        return 0.0

    return max(0.0, k_c * z + c_c * vz)


def equation_state(t, state, m):
    """
    Equations d'etat du systeme.
    state = [z, vz]
    """

    z, vz = state

    Fc = contact_force(z, vz)

    az = g - Fc / m

    return [vz, az]


# ============================================================
# 4. DETECTION DU DECOLLAGE
# ============================================================

def make_leave_contact():

    def leave_contact_event(t, state, m_event):

        z, vz = state

        if z <= 0.0:
            return -1.0

        return k_c * z + c_c * vz

    leave_contact_event.terminal = True
    leave_contact_event.direction = -1

    return leave_contact_event


# ============================================================
# 5. SIMULATIONS POUR LES DIFFERENTES VALEURS DE MASSE
# ============================================================

results = []
simulation_data = []

for m in m_values:

    event = make_leave_contact()

    solution = solve_ivp(
        equation_state,
        (0.0, tfin),
        [z0, v0],
        args=(float(m),),
        t_eval=time,
        events=event,
        max_step=0.001,
        rtol=1e-8,
        atol=1e-10
    )

    if not solution.success:
        raise RuntimeError(
            f"Echec de la simulation pour m = {m:.2f} kg : "
            f"{solution.message}"
        )

    t = solution.t
    z, vz = solution.y

    Fc = np.array([
        contact_force(zi, vi)
        for zi, vi in zip(z, vz)
    ])

    az = g - Fc / m

    compression = np.maximum(z, 0.0)

    # Grandeurs maximales

    i_max_compression = int(np.argmax(compression))

    max_compression = float(compression[i_max_compression])
    max_contact_force = float(np.max(Fc))
    max_abs_acceleration = float(np.max(np.abs(az)))

    t_max_compression = float(t[i_max_compression])

    # Parametres dynamiques theoriques

    omega_n = np.sqrt(k_c / m)

    zeta = c_c / (2.0 * np.sqrt(m * k_c))

    omega_d = (
        omega_n * np.sqrt(1.0 - zeta**2)
        if zeta < 1.0 else 0.0
    )

    # Conservation des resultats

    results.append({
        "m": float(m),
        "max_compression": max_compression,
        "max_contact_force": max_contact_force,
        "max_abs_acceleration": max_abs_acceleration,
        "t_max_compression": t_max_compression,
        "omega_n": float(omega_n),
        "zeta": float(zeta),
        "omega_d": float(omega_d),
        "liftoff": bool(solution.t_events[0].size > 0)
    })

    simulation_data.append({
        "m": float(m),
        "t": t,
        "z": z,
        "vz": vz,
        "Fc": Fc,
        "az": az
    })


# ============================================================
# 6. AFFICHAGE DES RESULTATS
# ============================================================

print("\n" + "=" * 110)
print("ETUDE DE L'INFLUENCE DE LA MASSE EQUIVALENTE")
print("=" * 110)

print(
    f"{'m (kg)':>12} | "
    f"{'Compression (mm)':>18} | "
    f"{'Force max (kN)':>16} | "
    f"{'Acc. max (m/s2)':>17} | "
    f"{'Temps max (s)':>14} | "
    f"{'omega_n (rad/s)':>17} | "
    f"{'zeta':>8} | "
    f"{'Decollage':>10}"
)

print("-" * 130)

for r in results:

    print(
        f"{r['m']:12.2f} | "
        f"{r['max_compression'] * 1000:18.3f} | "
        f"{r['max_contact_force'] / 1000:16.3f} | "
        f"{r['max_abs_acceleration']:17.3f} | "
        f"{r['t_max_compression']:14.4f} | "
        f"{r['omega_n']:17.4f} | "
        f"{r['zeta']:8.4f} | "
        f"{'Oui' if r['liftoff'] else 'Non':>10}"
    )


# ============================================================
# 7. EXPORT DES RESULTATS EN CSV
# ============================================================

csv_path = OUTPUT_DIR / "resultats_influence_masse.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:

    fieldnames = [
        "masse_kg",
        "compression_max_mm",
        "force_max_kN",
        "acceleration_max_m_s2",
        "temps_compression_max_s",
        "omega_n_rad_s",
        "zeta",
        "omega_d_rad_s",
        "decollage_detecte"
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for r in results:

        writer.writerow({
            "masse_kg": r["m"],
            "compression_max_mm": r["max_compression"] * 1000,
            "force_max_kN": r["max_contact_force"] / 1000,
            "acceleration_max_m_s2": r["max_abs_acceleration"],
            "temps_compression_max_s": r["t_max_compression"],
            "omega_n_rad_s": r["omega_n"],
            "zeta": r["zeta"],
            "omega_d_rad_s": r["omega_d"],
            "decollage_detecte": r["liftoff"]
        })

print(f"\nFichier CSV enregistre : {csv_path}")


# ============================================================
# 8. PREPARATION DES DONNEES POUR LES GRAPHIQUES
# ============================================================

masses = np.array([r["m"] for r in results])

compression_max = np.array([
    r["max_compression"] * 1000 for r in results
])

force_max = np.array([
    r["max_contact_force"] / 1000 for r in results
])

acceleration_max = np.array([
    r["max_abs_acceleration"] for r in results
])


# ============================================================
# 9. GRAPHIQUE 1 : COMPRESSION MAXIMALE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    masses,
    compression_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Masse equivalente (kg)")
plt.ylabel("Compression maximale (mm)")
plt.title("Influence de la masse sur la compression maximale")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_masse_compression.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# 10. GRAPHIQUE 2 : FORCE DE CONTACT MAXIMALE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    masses,
    force_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Masse equivalente (kg)")
plt.ylabel("Force de contact maximale (kN)")
plt.title("Influence de la masse sur la force de contact")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_masse_force.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# 11. GRAPHIQUE 3 : ACCELERATION MAXIMALE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    masses,
    acceleration_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Masse equivalente (kg)")
plt.ylabel("Acceleration maximale absolue (m/s2)")
plt.title("Influence de la masse sur l'acceleration maximale")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_masse_acceleration.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# 12. BILAN FINAL
# ============================================================

print("\n" + "=" * 85)
print("SIMULATION TERMINEE")
print("=" * 85)

print(f"Nombre de simulations : {len(results)}")
print(f"Dossier des resultats : {OUTPUT_DIR}")

print("\nFichiers generes :")
print("- resultats_influence_masse.csv")
print("- influence_masse_compression.png")
print("- influence_masse_force.png")
print("- influence_masse_acceleration.png")

print("\n" + "=" * 85)
