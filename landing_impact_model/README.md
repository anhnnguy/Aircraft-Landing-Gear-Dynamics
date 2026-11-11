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

Les valeurs de la raideur $k_c = 46 680 \mathrm{N/m}$, du coefficient d’amortissement $c_c = 7 337\ \mathrm{N.s/m}$ et de la vitesse verticale initiale $v_0 = 3{,}05\ \mathrm{m/s}$ sont reprises de l’étude de Kang et al. (2023). Les valeurs de raideur et d’amortissement correspondent aux paramètres linéarisés des trains principaux présentés dans le Tableau 3 de l’article.

La masse équivalente $m = 816{,}5\ \mathrm{kg}$ constitue une hypothèse propre au présent modèle simplifié, obtenue en divisant par deux la masse de référence $m_0 = 1 633\ \mathrm{kg}$ indiquée dans le Tableau 3. Cette hypothèse n’est pas une valeur directement validée par les auteurs pour un modèle à un degré de liberté.

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
├── etude_influence_vitesse.py
├── etude_influence_raideur.py
├── etude_influence_amortissement.py
├── etude_influence_masse.py
├── landing_impact.py
├── README.md
└── results/
    ├── influence_vitesse/
        ├── influence_masse_acceleration.png
        ├── influence_masse_compression.png
        ├── influence_masse_force.png
        ├── resultats_influence_masse.csv
    ├── influence_vitesse/
        ├── influence_vitesse_acceleration.png
        ├── influence_vitesse_compression.png
        ├── influence_vitesse_force.png
        ├── resultats_influence_vitesse.csv
    ├── influence_raideur/
        ├── influence_raideur_compression.png
        ├── influence_raideur_force.png
        ├── influence_raideur_acceleration.png
        ├── resultats_influence_raideur.csv
    ├── influence_amortissement/
        ├── influence_amortissement_compression.png
        ├── influence_amortissement_force.png
        ├── influence_amortissement_acceleration.png
        ├── resultats_influence_amortissement.csv
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

## 11. Étude de l'influence de la vitesse initiale

### 11.1 Objectif

Cette étude paramétrique vise à analyser l'influence de la vitesse verticale initiale (v_0) sur le comportement dynamique du système lors de l'impact à l'atterrissage.

L'objectif est d'observer l'évolution de la compression maximale, de la force de contact maximale, de l'accélération maximale en valeur absolue et du temps nécessaire pour atteindre la compression maximale.

### 11.2 Paramètres de l'étude

La vitesse initiale est le seul paramètre modifié. Les autres paramètres du modèle restent constants.

Les valeurs étudiées sont :

$$
v_0 \in \left\{2{,}0;\ 2{,}5;\ 3{,}05;\ 3{,}5;\ 4{,}0\right\} \mathrm{m/s}
$$

La valeur de référence est $v_0 = 3{,}05\ \mathrm{m/s}$.

### 11.3. Résultats numériques

| $v_0$ (m/s) | Compression maximale (mm) | Force maximale (kN) | Accélération maximale (m/s²) | Temps de compression maximale (s) |
|---:|---:|---:|---:|---:|
| 2,00 | 235,147 | 15,606 | 9,810 | 0,2695 |
| 2,50 | 261,251 | 18,726 | 13,125 | 0,2430 |
| 3,05 | 292,619 | 22,475 | 17,716 | 0,2245 |
| 3,50 | 319,513 | 25,690 | 21,653 | 0,2135 |
| 4,00 | 350,210 | 29,345 | 26,130 | 0,2050 |

Aucun événement de perte de contact n'a été détecté pendant la durée de simulation de 2 secondes pour les cinq vitesses étudiées.

### 11.4. Analyse des résultats

Les résultats montrent que l'augmentation de la vitesse verticale initiale entraîne une augmentation de la compression maximale, de la force de contact maximale et de l'accélération maximale en valeur absolue.

Entre 2,0 et 4,0 m/s :

- La compression maximale augmente d'environ 49 %.
- La force de contact maximale augmente d'environ 88 %.
- L'accélération maximale en valeur absolue est multipliée par environ 2,66.

Par ailleurs, le temps nécessaire pour atteindre la compression maximale diminue lorsque la vitesse initiale augmente.

Ces résultats montrent que la vitesse verticale initiale joue un rôle important dans la sévérité de l'impact.

### 11.5. Graphiques et données

Les graphiques et les résultats numériques de cette étude sont enregistrés dans le dossier `results/influence_vitesse/` :

- `influence_vitesse_compression.png` : influence de la vitesse initiale sur la compression maximale ;
- `influence_vitesse_force.png` : évolution de la force de contact ;
- `influence_vitesse_acceleration.png` : évolution de l'accélération ;
- `resultats_influence_vitesse.csv` : tableau des résultats numériques.

Le programme utilisé est `etude_influence_vitesse.py`.

### 11.6. Conclusion

L'étude paramétrique met en évidence une relation croissante entre la vitesse verticale initiale et la sévérité de l'impact dans le cadre du modèle simplifié.

Une vitesse initiale plus élevée conduit à une compression plus importante du système et à des efforts de contact plus élevés. Cette étude souligne donc l'importance de la vitesse verticale au moment du premier contact avec le sol.

## 12. Étude de l'influence de la raideur du système

### 12.1. Objectif

Cette étude vise à analyser l'influence de la raideur du ressort $k_c$ sur le comportement dynamique du train d'atterrissage pendant l'impact.

L'objectif est d'évaluer l'effet de la raideur sur :
- la compression maximale du système ;
- la force de contact maximale ;
- l'accélération maximale absolue ;
- le temps nécessaire pour atteindre la compression maximale.

### 12.2. Paramètres de simulation

Pour cette étude, la raideur du ressort est modifiée tandis que les autres paramètres sont maintenus constants.

| Paramètre | Valeur |
|---|---:|
| Masse équivalente $m$ | $816,5 kg$ |
| Coefficient d'amortissement $c_c$ | $7 337 N.s/m$ |
| Vitesse initiale $v_0$ | $3,05 m/s$ |
| Raideur $k_c$ | $30 000 ; 46 680 ; 60 000 N/m$ |
| Durée de simulation | $2 s$ |

### 12.3. Résultats

Les résultats obtenus sont présentés dans le tableau suivant.

| $k_c (N/m)$ | Compression maximale $(mm)$ | Force maximale $(kN)$ | Accélération maximale $(m/s²)$ | Temps de compression maximale $(s)$ |
|---:|---:|---:|---:|---:|
| 30 000 | 354,392 | 22,359 | 17,574 | 0,3115 |
| 46 680 | 292,619 | 22,475 | 17,716 | 0,2245 |
| 60 000 | 263,643 | 23,409 | 18,860 | 0,1915 |

Aucun événement de décollage n'a été détecté pendant les simulations.

### 12.4. Analyse des résultats

L'augmentation de la raideur entraîne une diminution de la compression maximale. Lorsque $k_c$ passe de $30 000$ à $60 000 N/m$, la compression maximale diminue d'environ $25,6 %$.

En revanche, la force de contact maximale augmente légèrement, passant de $22,359 kN$ à $23,409 kN$. L'accélération maximale absolue augmente également d'environ $7,3 %$.

Le temps nécessaire pour atteindre la compression maximale diminue de $0,3115 s$ à $0,1915 s$.

Ces résultats montrent qu'un ressort plus rigide limite la déformation du train d'atterrissage, mais entraîne une augmentation des efforts transmis et des accélérations.

Il existe donc un compromis entre la limitation de la compression et la réduction des charges dynamiques transmises à la structure.

### 12.5. Fichiers générés

Les résultats de cette étude sont enregistrés dans le dossier `results/influence_raideur/` :

- `resultats_influence_raideur.csv`
- `influence_raideur_compression.png`
- `influence_raideur_force.png`
- `influence_raideur_acceleration.png`



## 13. Étude de l'influence de l'amortissement du système

### 13.1. Objectif

Cette étude vise à analyser l'influence du coefficient d'amortissement $c_c$ sur le comportement dynamique du train d'atterrissage pendant l'impact.

L'amortisseur permet de dissiper une partie de l'énergie mécanique du système. Son coefficient influence donc la compression, les forces de contact et les accélérations pendant l'atterrissage.

### 13.2. Paramètres de simulation

Le coefficient d'amortissement est modifié tandis que les autres paramètres sont maintenus constants.

| Paramètre | Valeur |
|---|---:|
| Masse équivalente $m$ | $816,5 kg$ |
| Raideur $k_c$ | $46 680 N/m$ |
| Vitesse initiale $v_0$ | $3,05 m/s$ |
| Coefficient d'amortissement $c_c$ | $4 000 ; 7 337 ; 10 000 N.s/m$ |
| Durée de simulation | $2 s$ |

### 13.3. Résultats

Les résultats obtenus sont présentés dans le tableau suivant.

| $c_c (N·s/m)$ | Compression maximale $(mm)$ | Force maximale $(kN)$ | Accélération maximale $(m/s²)$ | Temps de compression maximale $(s)$ |
|---:|---:|---:|---:|---:|
| 4 000 | 387,683 | 20,654 | 15,486 | 0,2345 |
| 7 337 | 292,619 | 22,475 | 17,716 | 0,2245 |
| 10 000 | 243,650 | 30,434 | 27,463 | 0,2235 |

Aucun événement de décollage n'a été détecté pendant les simulations.

### 13.4. Analyse des résultats

L'augmentation du coefficient d'amortissement entraîne une diminution de la compression maximale. Lorsque $c_c$ passe de $4 000$ à $10 000 N.s/m$, la compression maximale diminue d'environ $37,2 %$.

Cependant, la force de contact maximale augmente de $20,654 kN$ à $30,434 kN$, soit une augmentation d'environ $47,4 %$.

L'accélération maximale absolue augmente également de $15,486 m/s²$ à $27,463 m/s²$, soit une augmentation d'environ $77,3 %$.

Le temps nécessaire pour atteindre la compression maximale varie relativement peu entre les trois simulations.

Ces résultats montrent qu'un amortissement plus important permet de limiter la compression du système grâce à une dissipation plus importante de l'énergie mécanique. Toutefois, un coefficient d'amortissement trop élevé peut entraîner une augmentation importante des forces transmises et des accélérations.

Le choix du coefficient d'amortissement doit donc prendre en compte à la fois la limitation de la compression et le confort dynamique de la structure.

### 13.5. Fichiers générés

Les résultats de cette étude sont enregistrés dans le dossier `results/influence_amortissement/` :

- `resultats_influence_amortissement.csv`
- `influence_amortissement_compression.png`
- `influence_amortissement_force.png`
- `influence_amortissement_acceleration.png`


## 14. Étude de l'influence de la masse équivalente

### 14.1. Objectif

Cette étude vise à analyser l'influence de la masse équivalente $m$ sur le comportement dynamique du train d'atterrissage pendant l'impact.

La masse représente l'inertie du système. Sa variation peut modifier la compression maximale, les forces de contact, les accélérations ainsi que les caractéristiques dynamiques du système.

L'objectif est donc d'évaluer l'influence de ce paramètre sur la réponse du modèle à un degré de liberté.

### 14.2. Paramètres de simulation

La masse équivalente est modifiée tandis que les autres paramètres du modèle sont maintenus constants.

La masse de référence est :

$$
m_{\mathrm{ref}}=\frac{1633}{2}=816,5\ \mathrm{kg}
$$

Les valeurs étudiées correspondent à $50 %$, $75 %$, $100 %$, $125 %$ et $150 %$ de cette masse de référence.

| Paramètre | Valeur |
| :--- | ---: |
| Masse équivalente $m$ | 408,25 ; 612,375 ; 816,5 ; 1 020,625 ; 1 224,75 kg |
| Raideur $k_c$ | 46 680 N/m |
| Coefficient d'amortissement $c_c$ | $7 337 N.s/m$ |
| Vitesse initiale $v_0$ | $3,05 m/s$ |
| Durée de simulation | $2 s$ |

La masse équivalente constitue le seul paramètre variable de cette étude.

### 14.3. Résultats numériques

Les résultats obtenus sont présentés dans le tableau suivant.

| Masse $m (kg)$ | Compression maximale $(mm)$ | Force maximale $(kN)$ | Accélération maximale $(m/s²)$ | Temps de compression maximale $(s)$ |
| ---: | ---: | ---: | ---: | ---: |
| 408,25 | 150,123 | 22,284 | 44,774 | 0,1360 |
| 612,375 | 221,638 | 22,351 | 26,689 | 0,1825 |
| 816,5 | 292,619 | 22,475 | 17,716 | 0,2245 |
| 1 020,625 | 363,408 | 24,056 | 13,759 | 0,2625 |
| 1 224,75 | 434,178 | 26,493 | 11,822 | 0,2985 |

Les paramètres dynamiques théoriques sont également calculés :

| Masse $m (kg)$ | Pulsation propre $\omega_n (rad/s)$ | Taux d'amortissement $\zeta$ |
| ---: | ---: | ---: |
| 408,25 | 10,6931 | 0,8403 |
| 612,375 | 8,7309 | 0,6861 |
| 816,5 | 7,5611 | 0,5942 |
| 1 020,625 | 6,7629 | 0,5315 |
| 1 224,75 | 6,1736 | 0,4852 |

Aucun événement de décollage n'a été détecté pendant les simulations pour les cinq masses étudiées.

### 14.4. Analyse des résultats

Les résultats montrent que l'augmentation de la masse équivalente entraîne une augmentation significative de la compression maximale du système.

Lorsque la masse passe de 408,25 kg à 1 224,75 kg, la compression maximale augmente de 150,123 mm à 434,178 mm, soit une augmentation d'environ 189,2 %.

La force de contact maximale augmente également, passant de 22,284 kN à 26,493 kN, soit une augmentation d'environ 18,9 %. Cette évolution est notamment liée à l'augmentation de la déformation du ressort, qui entraîne une augmentation de la composante élastique de la force de contact.

En revanche, l'accélération maximale absolue diminue lorsque la masse augmente. Elle passe de 44,774 m/s² à 11,822 m/s², soit une diminution d'environ 73,6 %.

Ce comportement est cohérent avec l'équation dynamique du système :

$$
\ddot z=g-\frac{F_c}{m}
$$

Pour une force de contact donnée, une masse plus importante entraîne une accélération plus faible.

Par ailleurs, la pulsation propre $\omega_n$ et le taux d'amortissement $\zeta$ diminuent avec l'augmentation de la masse. La pulsation propre passe de 10,6931 rad/s à 6,1736 rad/s, tandis que le taux d'amortissement diminue de 0,8403 à 0,4852.

Le temps nécessaire pour atteindre la compression maximale augmente également, passant de 0,1360 s à 0,2985 s.

Ces résultats montrent que l'augmentation de la masse équivalente entraîne une compression plus importante et une réponse dynamique plus lente, tout en réduisant l'accélération maximale absolue.

### 14.5. Graphiques et données

Les graphiques et les résultats numériques de cette étude sont enregistrés dans le dossier `results/influence_masse/` :

- `influence_masse_compression.png` : influence de la masse sur la compression maximale ;
- `influence_masse_force.png` : influence de la masse sur la force de contact maximale ;
- `influence_masse_acceleration.png` : influence de la masse sur l'accélération maximale ;
- `resultats_influence_masse.csv` : tableau des résultats numériques.

Le programme utilisé est `influence_masse.py`.

### 14.6. Conclusion

L'étude paramétrique met en évidence l'influence importante de la masse équivalente sur le comportement dynamique du train d'atterrissage.

Une augmentation de la masse entraîne une augmentation de la compression maximale et de la force de contact maximale, tandis que l'accélération maximale absolue diminue.

Cette étude montre donc que la masse équivalente constitue un paramètre essentiel dans l'analyse de l'impact à l'atterrissage.

Les résultats restent toutefois limités aux hypothèses du modèle simplifié et aux valeurs de masse étudiées.


## 15. Référence bibliographique

Kang, B.-H., Jo, B.-H., Kim, B.-G., Hwang, J.-H. et Choi, S.-B. (2023). Linear and Nonlinear Models for Drop Simulation of an Aircraft Landing Gear System with MR Dampers. *Actuators*, 12(7), 287.

[https://doi.org/10.3390/act12070287](https://doi.org/10.3390/act12070287)
