"""
Etude de l'influence de la raideur sur l'impact d'un train
d'atterrissage simplifie a un degre de liberte (1 DOF).

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

m0 = 1633.0       # Masse de reference issue de Kang et al. (2023) (kg)
m = m0 / 2        # Masse equivalente par train (hypothese de partage egal)

v0 = 3.05         # Vitesse initiale (m/s)
c_c = 7337.0      # Coefficient d'amortissement (N.s/m)

k_c_values = np.array([30000, 46680, 60000])  # Valeurs de raideur (N/m)

z0 = 0.0          # Position initiale (m)
g = 9.81          # Acceleration gravitationnelle (m/s2)

tfin = 2.0        # Duree de simulation (s)
n_points = 4001

time = np.linspace(0.0, tfin, n_points)

# ============================================================
# 2. DOSSIER DE SORTIE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "results" / "influence_raideur"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. MODELE PHYSIQUE
# ============================================================

def contact_force(z, vz, k_c):
    """
    Force de contact dirigee vers le haut.
    """

    if z <= 0.0:
        return 0.0

    return max(0.0, k_c * z + c_c * vz)


def equation_state(t, state, k_c):
    """
    Equations d'etat du systeme.
    state = [z, vz]
    """

    z, vz = state

    Fc = contact_force(z, vz, k_c)

    az = g - Fc / m

    return [vz, az]


# ============================================================
# 4. DETECTION DU DECOLLAGE
# ============================================================

def make_leave_contact(k_c):

    def leave_contact_event(t, state, k_c_event):

        z, vz = state

        if z <= 0.0:
            return -1.0

        return k_c_event * z + c_c * vz

    leave_contact_event.terminal = True
    leave_contact_event.direction = -1

    return leave_contact_event

# ============================================================
# 5. SIMULATIONS POUR LES DIFFERENTES RAIDEURS
# ============================================================

results = []
simulation_data = []

for k_c in k_c_values:

    event = make_leave_contact(float(k_c))

    solution = solve_ivp(
        equation_state,
        (0.0, tfin),
        [z0, float(v0)],
        args=(float(k_c),),
        t_eval=time,
        events=event,
        max_step=0.001,
        rtol=1e-8,
        atol=1e-10
    )

    if not solution.success:
        raise RuntimeError(
            f"Echec de la simulation pour k_c = {k_c:.0f} N/m : "
            f"{solution.message}"
        )

    t = solution.t
    z, vz = solution.y

    Fc = np.array([
            contact_force(zi, vi, k_c)
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

# Conservation des resultats

    results.append({
        "k_c": float(k_c),
        "max_compression": max_compression,
        "max_contact_force": max_contact_force,
        "max_abs_acceleration": max_abs_acceleration,
        "t_max_compression": t_max_compression,
        "liftoff": bool(solution.t_events[0].size > 0)
    })

    simulation_data.append({
        "k_c": float(k_c),
        "t": t,
        "z": z,
        "vz": vz,
        "Fc": Fc,
        "az": az
    })


# ============================================================
# 6. AFFICHAGE DES RESULTATS
# ============================================================

print("\n" + "=" * 85)
print("ETUDE DE L'INFLUENCE DE LA RAIDEUR DU SYSTEME")
print("=" * 85)

print(
    f"{'k_c (N/m)':>12} | "
    f"{'Compression (mm)':>18} | "
    f"{'Force max (kN)':>16} | "
    f"{'Acc. max (m/s2)':>17} | "
    f"{'Temps max (s)':>14} | "
    f"{'Decollage':>10}"
)

print("-" * 105)

for r in results:

    print(
        f"{r['k_c']:12.2f} | "
        f"{r['max_compression'] * 1000:18.3f} | "
        f"{r['max_contact_force'] / 1000:16.3f} | "
        f"{r['max_abs_acceleration']:17.3f} | "
        f"{r['t_max_compression']:14.4f} | "
        f"{'Oui' if r['liftoff'] else 'Non':>10}"
    )


# ============================================================
# 7. EXPORT DES RESULTATS EN CSV
# ============================================================

csv_path = OUTPUT_DIR / "resultats_influence_raideur.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:

    fieldnames = [
        "k_c_N_m",
        "compression_max_mm",
        "force_max_kN",
        "acceleration_max_m_s2",
        "temps_compression_max_s",
        "decollage_detecte"
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for r in results:

        writer.writerow({
            "k_c_N_m": r["k_c"],
            "compression_max_mm": r["max_compression"] * 1000,
            "force_max_kN": r["max_contact_force"] / 1000,
            "acceleration_max_m_s2": r["max_abs_acceleration"],
            "temps_compression_max_s": r["t_max_compression"],
            "decollage_detecte": r["liftoff"]
        })

print(f"\nFichier CSV enregistre : {csv_path}")


# ============================================================
# 8. PREPARATION DES DONNEES POUR LES GRAPHIQUES
# ============================================================

k_c = np.array([r["k_c"] for r in results])

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
    k_c,
    compression_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Raideur du système (N/m)")
plt.ylabel("Compression maximale (mm)")
plt.title("Influence de la raideur du système sur la compression maximale")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_raideur_compression.png",
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
    k_c,
    force_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Raideur du système (N/m)")
plt.ylabel("Force de contact maximale (kN)")
plt.title("Influence de la raideur du système sur la force de contact")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_raideur_force.png",
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
    k_c,
    acceleration_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Raideur du système (N/m)")
plt.ylabel("Acceleration maximale absolue (m/s2)")
plt.title("Influence de la raideur du système sur l'acceleration maximale")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_raideur_acceleration.png",
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
print("- resultats_influence_raideur.csv")
print("- influence_raideur_compression.png")
print("- influence_raideur_force.png")
print("- influence_raideur_acceleration.png")

print("\n" + "=" * 85)
