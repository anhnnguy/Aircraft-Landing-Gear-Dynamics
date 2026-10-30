# Modélisation et simulation d’un impact à l’atterrissage — Modèle à 1 DDL
## 1. Objectif du projet
L’objectif est de développer un modèle dynamique simplifié afin d’étudier le comportement vertical d’un système d’atterrissage lors du contact avec le sol.

Le modèle représente le système par une masse équivalente, un ressort et un amortisseur visqueux. Il permet de simuler la compression, la vitesse, l’accélération et la force de contact au cours de l’impact.

Ce modèle constitue une première approche numérique simplifiée, développée dans le cadre de ce projet. Les paramètres de raideur, d’amortissement et de vitesse initiale sont repris de l’étude de Kang et al. (2023), intitulée Linear and Nonlinear Models for Drop Simulation of an Aircraft Landing Gear System with MR Dampers. La formulation des équations du mouvement et la loi de contact sont établies pour le présent modèle à un degré de liberté et ne constituent pas une reproduction intégrale du modèle de l’article.amortisseurs MR ».
## 2. Paramètres du modèle
| Paramètre | Symbole | Valeur | Unité |
|---|---|---:|---|
| Masse équivalente | $m$ | 816,5 | kg |
| Raideur | $k_c$ | 46 680 | N/m |
| Coefficient d’amortissement | $c_c$ | 7 337 | N·s/m |
| Vitesse verticale initiale | $v_0$ | 3,05 | m/s |
| Accélération de la pesanteur | $g$ | 9,81 | m/s² |

Les valeurs de la raideur $k_c = 46,680 \mathrm{N/m}$, du coefficient d’amortissement $c_c = 7,337\ \mathrm{N.s/m}$ et de la vitesse verticale initiale $v_0 = 3{,}05\ \mathrm{m/s}$ sont reprises de l’étude de Kang et al. (2023). Les valeurs de raideur et d’amortissement correspondent aux paramètres linéarisés des trains principaux présentés dans le Tableau 3 de l’article.

La masse équivalente $m = 816{,}5\ \mathrm{kg}$ constitue une hypothèse propre au présent modèle simplifié, obtenue en divisant par deux la masse de référence $m_0 = 1,633\ \mathrm{kg}$ indiquée dans le Tableau 3. Cette hypothèse n’est pas une valeur directement validée par les auteurs pour un modèle à un degré de liberté.

## 3. Hypothèses de modélisation

Les hypothèses retenues sont les suivantes :

- Le système possède un seul degré de liberté (1 DDL), correspondant au mouvement vertical.
- La coordonnée $z$ est orientée vers le bas.
- La position $z = 0$ correspond à la position du premier contact avec le sol.
- Lorsque $z > 0$, le système est en compression.
- La vitesse verticale initiale est $v_0 = 3,05$ m/s.
- La pesanteur agit vers le bas.
- La force de contact agit vers le haut et devient nulle lorsque le système n’est plus en contact.
- Le ressort et l’amortisseur sont représentés par un modèle linéaire simplifié.

## 4. Équations du mouvement

### 4.1. Équation dynamique

En appliquant le principe fondamental de la dynamique suivant l’axe vertical :

$$
m\ddot{z} = mg - F_c
$$

avec :

- $m$ : masse équivalente ;
- $\ddot{z}$ : accélération verticale ;
- $mg$ : poids ;
- $F_c$ : force de contact exercée vers le haut.

### 4.2. Loi de contact

La force de contact est définie par :

$$
F_c =
\begin{cases}
0, & z \leq 0,\\
\max(0, k_c z + c_c \dot{z}), & z > 0.
\end{cases}
$$

où $k_c$ représente la raideur et $c_c$ le coefficient d’amortissement.

Cette loi empêche l’apparition d’une force de contact en traction. Elle constitue une approximation du comportement réel du système d’atterrissage.

## 5. Méthode numérique

La simulation est réalisée en Python. Les équations différentielles sont intégrées numériquement à l’aide de `solve_ivp`, fourni par la bibliothèque SciPy.

Les bibliothèques utilisées sont :

- **NumPy** : manipulation des données numériques ;
- **SciPy** : résolution des équations différentielles ;
- **Matplotlib** : génération des graphiques ;
- **Pathlib** : gestion des chemins et des dossiers de résultats.

Le programme prévoit également la détection d’un événement correspondant à la perte de contact, lorsque la force calculée du ressort-amortisseur atteint zéro pendant le mouvement de remontée.

## 6. Résultats de la simulation

Le programme génère les courbes suivantes :

1. Déplacement vertical en fonction du temps ;
2. Vitesse verticale en fonction du temps ;
3. Accélération verticale en fonction du temps ;
4. Force de contact en fonction du temps.

Les résultats numériques comprennent également :

- la compression maximale ;
- l’instant correspondant à cette compression maximale ;
- la force de contact maximale ;
- la valeur maximale de l’accélération en valeur absolue.

Les résultats doivent être analysés afin de vérifier la cohérence physique du modèle et d’identifier les limites des hypothèses retenues.

## 7. Organisation des fichiers

```text
Landing_Impact_Model/
├── landing_impact.py
├── README.md
└── results/
    ├── landing_impact_deplacement.png
    ├── landing_impact_vitesse.png
    ├── landing_impact_acceleration.png
    ├── landing_impact_contact_force.png
    └── landing_impact_data.csv
```

## 8. Exécution du programme

Installer les bibliothèques nécessaires si elles ne sont pas déjà disponibles :

```bash
python3 -m pip install numpy scipy matplotlib
```

Lancer ensuite le programme depuis le dossier `Landing_Impact_Model` :

```bash
python3 landing_impact.py
```

Les graphiques et les données numériques sont enregistrés automatiquement dans le dossier `results`.

## 9. Limites du modèle

Ce modèle est une première approximation du phénomène d’impact à l’atterrissage. Il ne prend pas explicitement en compte :

- la dynamique complète du fuselage et des autres trains ;
- les non-linéarités réelles du pneu et de l’amortisseur ;
- les variations de géométrie et les phénomènes de frottement ;
- la validation expérimentale des résultats.

Le modèle pourra être amélioré ultérieurement en intégrant des lois de contact plus réalistes et en comparant les résultats à des données de référence.

## 10. Vérification et validation numérique

La cohérence numérique du modèle a été vérifiée à l'aide de deux méthodes complémentaires.

### 10.1 Comparaison avec la solution analytique

La solution numérique obtenue avec `solve_ivp` a été comparée à la solution analytique de l'équation différentielle linéaire.

Les erreurs maximales obtenues sont :

| Grandeur | Erreur maximale |
|---|---:|
| Déplacement | 2,03 × 10⁻⁷ m |
| Vitesse | 3,04 × 10⁻⁶ m/s |
| Accélération | 2,75 × 10⁻⁵ m/s² |

Ces erreurs très faibles confirment la précision numérique de la résolution.

### 10.2 Vérification du bilan énergétique

Le bilan énergétique a également été vérifié à partir de l'équation :

$$\Delta E_c + \Delta E_e = E_p - E_d$$

avec :

- $E_c$ : énergie cinétique ;
- $E_e$ : énergie élastique stockée dans le ressort ;
- $E_p$ : énergie potentielle ;
- $E_d$ : énergie dissipée par l'amortisseur.

Le résidu énergétique maximal obtenu est de **0,02434 J**, pour une énergie cinétique initiale de **3797,75 J**.

Ce résultat confirme la cohérence énergétique de la simulation, dans les limites des erreurs d'intégration numérique.

### 10.3 Conclusion

Les deux vérifications montrent que l'implémentation numérique est cohérente avec les équations mathématiques du modèle à un degré de liberté.

Cette validation concerne uniquement la cohérence mathématique et numérique du modèle. Elle ne constitue pas une validation expérimentale du comportement réel de l’étude de Kang et al. (2023).

## 11. Référence bibliographique

Kang, B.-H., Jo, B.-H., Kim, B.-G., Hwang, J.-H. et Choi, S.-B. (2023). Linear and Nonlinear Models for Drop Simulation of an Aircraft Landing Gear System with MR Dampers. Actuators, 12(7), 287.

https://doi.org/10.3390/act12070287