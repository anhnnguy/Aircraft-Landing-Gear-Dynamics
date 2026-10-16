# Aircraft-Landing-Gear-Dynamics
Modélisation et simulation dynamique d’un amortisseur de train d’atterrissage d’avion

---

## 1. Context and Background
During landing, the contact between the wheels and the runway causes rapid mechanical force variations transmitted to the landing gear. The damping system must absorb a significant portion of the impact energy to limit oscillations and reduce the load transferred to the aircraft structure.

The performance of this damping system depends primarily on the supported mass, equivalent stiffness, and damping coefficient.

In this project, we analyze the dynamic behavior of a simplified 1-DOF landing gear model using **Python**. The main objective is to evaluate how mechanical parameters influence the system's dynamic response and to identify tradeoffs between limiting displacement, acceleration, and transmitted forces.

---

## 2. Problem Statement
When an aircraft lands, the landing gear shock absorber compresses to absorb impact energy. **How do the equivalent stiffness and damping coefficient influence displacement, acceleration, and forces transmitted to the aircraft structure?**

---

## 3. Modeling Assumptions
To simplify the physical study, the following assumptions are adopted:
- **1-DOF Model:** The system is represented as a single-degree-of-freedom mechanical oscillator.
- **Lumped Mass:** The supported mass is treated as a point mass $m$.
- **Linear Spring:** Characterized by a constant stiffness $k$.
- **Viscous Damping:** Characterized by a constant damping coefficient $c$.
- **Small Displacements:** Motion is studied around the static equilibrium position.
- **Vertical Motion:** Aerodynamic effects, wheel rotation, and oleo-pneumatic non-linearities are neglected.
- **Free Response:** The initial analysis focuses on the free response following an initial impact velocity $v_0$.

> *Note: This model is a pedagogical approximation and does not fully represent real oleo-pneumatic landing gear systems or complex tire-piste contact dynamics.*

---

## 4. Governing Equations
The motion of the mass $m$ is governed by the second-order linear differential equation:

$$m \ddot{x}(t) + c \dot{x}(t) + k x(t) = 0$$

Where:
- $x(t)$: Vertical displacement from static equilibrium (m)
- $\dot{x}(t)$: Vertical velocity (m/s)
- $\ddot{x}(t)$: Vertical acceleration (m/s²)
- $F_{\text{transmitted}}(t) = c \dot{x}(t) + k x(t)$: Transmitted force to the structure (N)

---

## 5. Numerical Parameters
| Parameter | Symbol | Reference Value | Unit |
| :--- | :---: | :---: | :---: |
| Equivalent Mass | $m$ | $100$ | $\text{kg}$ |
| Spring Stiffness | $k$ | $20\ 000$ | $\text{N/m}$ |
| Damping Coefficient | $c$ | $1\ 500$ | $\text{N}\cdot\text{s/m}$ |
| Initial Displacement | $x(0)$ | $0$ | $\text{m}$ |
| Initial Velocity | $\dot{x}(0)$ | $1.0$ | $\text{m/s}$ |
| Simulation Duration | $T$ | $2.0$ | $\text{s}$ |

---

## 6. Project Structure & Usage
```text
.
├── main.py            # Main simulation script (SciPy ODE solver)
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
