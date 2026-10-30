
"""
Etude de l'influence de la vitesse initiale sur l'impact d'un train
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

k_c = 46680.0     # Raideur du ressort (N/m)
c_c = 7337.0      # Coefficient d'amortissement (N.s/m)

v0_values = np.array([2.0, 2.5, 3.05, 3.5, 4.0])

z0 = 0.0          # Position initiale (m)
g = 9.81          # Acceleration gravitationnelle (m/s2)

tfin = 2.0        # Duree de simulation (s)
n_points = 4001

time = np.linspace(0.0, tfin, n_points)


# ============================================================
# 2. DOSSIER DE SORTIE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "results" / "influence_vitesse"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. MODELE PHYSIQUE
# ============================================================

def contact_force(z, vz):
    """
    Force de contact dirigee vers le haut.

    La force est nulle lorsque z <= 0.
    Elle ne peut pas etre negative (pas de traction).
    """

    if z <= 0.0:
        return 0.0

    return max(0.0, k_c * z + c_c * vz)


def equation_state(t, state):
    """
    Equations d'etat du systeme.

    state = [z, vz]

    m * z'' = m * g - Fc
    """

    z, vz = state

    Fc = contact_force(z, vz)

    az = g - Fc / m

    return [vz, az]


# ============================================================
# 4. DETECTION DU DECOLLAGE
# ============================================================

def leave_contact(t, state):
    """
    Detecte la disparition de la force de contact
    pendant le mouvement ascendant.

    L'evenement correspond a :
    k_c * z + c_c * vz = 0
    """

    z, vz = state

    if z <= 0.0:
        return -1.0

    return k_c * z + c_c * vz


leave_contact.terminal = True
leave_contact.direction = -1


# ============================================================
# 5. SIMULATIONS POUR LES DIFFERENTES VITESSES
# ============================================================

results = []
simulation_data = []

for v0 in v0_values:

    solution = solve_ivp(
        equation_state,
        (0.0, tfin),
        [z0, float(v0)],
        t_eval=time,
        events=leave_contact,
        max_step=0.001,
        rtol=1e-8,
        atol=1e-10
    )

    if not solution.success:
        raise RuntimeError(
            f"Echec de la simulation pour v0 = {v0:.2f} m/s : "
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

    # Conservation des resultats

    results.append({
        "v0": float(v0),
        "max_compression": max_compression,
        "max_contact_force": max_contact_force,
        "max_abs_acceleration": max_abs_acceleration,
        "t_max_compression": t_max_compression,
        "liftoff": bool(solution.t_events[0].size > 0)
    })

    simulation_data.append({
        "v0": float(v0),
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
print("ETUDE DE L'INFLUENCE DE LA VITESSE INITIALE")
print("=" * 85)

print(
    f"{'v0 (m/s)':>10} | "
    f"{'Compression (mm)':>18} | "
    f"{'Force max (kN)':>16} | "
    f"{'Acc. max (m/s2)':>17} | "
    f"{'Temps max (s)':>14} | "
    f"{'Decollage':>10}"
)

print("-" * 105)

for r in results:

    print(
        f"{r['v0']:10.2f} | "
        f"{r['max_compression'] * 1000:18.3f} | "
        f"{r['max_contact_force'] / 1000:16.3f} | "
        f"{r['max_abs_acceleration']:17.3f} | "
        f"{r['t_max_compression']:14.4f} | "
        f"{'Oui' if r['liftoff'] else 'Non':>10}"
    )


# ============================================================
# 7. EXPORT DES RESULTATS EN CSV
# ============================================================

csv_path = OUTPUT_DIR / "resultats_influence_vitesse.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:

    fieldnames = [
        "v0_m_s",
        "compression_max_mm",
        "force_max_kN",
        "acceleration_max_m_s2",
        "temps_compression_max_s",
        "decolage_detecte"
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for r in results:

        writer.writerow({
            "v0_m_s": r["v0"],
            "compression_max_mm": r["max_compression"] * 1000,
            "force_max_kN": r["max_contact_force"] / 1000,
            "acceleration_max_m_s2": r["max_abs_acceleration"],
            "temps_compression_max_s": r["t_max_compression"],
            "decolage_detecte": r["liftoff"]
        })

print(f"\nFichier CSV enregistre : {csv_path}")


# ============================================================
# 8. PREPARATION DES DONNEES POUR LES GRAPHIQUES
# ============================================================

vitesse = np.array([r["v0"] for r in results])

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
    vitesse,
    compression_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Vitesse initiale (m/s)")
plt.ylabel("Compression maximale (mm)")
plt.title("Influence de la vitesse initiale sur la compression maximale")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_vitesse_compression.png",
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
    vitesse,
    force_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Vitesse initiale (m/s)")
plt.ylabel("Force de contact maximale (kN)")
plt.title("Influence de la vitesse initiale sur la force de contact")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_vitesse_force.png",
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
    vitesse,
    acceleration_max,
    "o-",
    linewidth=2,
    markersize=7
)

plt.xlabel("Vitesse initiale (m/s)")
plt.ylabel("Acceleration maximale absolue (m/s2)")
plt.title("Influence de la vitesse initiale sur l'acceleration maximale")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "influence_vitesse_acceleration.png",
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
print("- resultats_influence_vitesse.csv")
print("- influence_vitesse_compression.png")
print("- influence_vitesse_force.png")
print("- influence_vitesse_acceleration.png")

print("\n" + "=" * 85)
