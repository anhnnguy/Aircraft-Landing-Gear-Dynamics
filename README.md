# Projet personnel : Aircraft Landing Gear Dynamics
Modélisation et simulation dynamique d’un amortisseur de train d’atterrissage d’avion

## 1. Contexte et mise en situation
Lors de l’atterrissage d’un avion, le contact entre les roues et la piste entraîne une variation rapide des efforts mécaniques transmis au train d’atterrissage. Le système d’amortissement doit absorber une partie de l’énergie de l’impact afin de limiter les oscillations et de réduire les efforts transmis à la structure de l’avion.

Les performances de ce système dépendent notamment de la masse supportée, de la raideur équivalente et du coefficient d’amortissement.

Dans ce projet, on souhaite étudier le comportement dynamique d’un modèle simplifié de train d’atterrissage à l’aide de Python. L’objectif est de comprendre l’influence des différents paramètres mécaniques sur la réponse du système et d’identifier les compromis entre la limitation du déplacement, de l’accélération et des efforts transmis.

## 2. Problématique
Lors de l’atterrissage d’un avion, le système d’amortissement du train d’atterrissage se comprime afin d’absorber l’énergie de l’impact. Comment la raideur équivalente et le coefficient d’amortissement influencent-ils le déplacement, l’accélération et les efforts transmis à la structure de l’avion ?

## 3. Hypothèses de modélisation
Pour simplifier l’étude, on adopte les hypothèses suivantes :
- Le système est représenté par un modèle mécanique à un degré de liberté.
- La masse supportée est assimilée à une masse ponctuelle.
- Le ressort est linéaire et caractérisé par une raideur constante.
- L’amortisseur est visqueux et caractérisé par un coefficient d’amortissement constant.
- Les déplacements sont étudiés autour de la position d’équilibre statique.
- Le mouvement est vertical ; les effets aérodynamiques, la rotation des roues et les non-linéarités du système réel sont négligés.
- L’étude initiale porte sur la réponse libre du système après une vitesse initiale représentative de l’impact.

*Ce modèle constitue une première approximation pédagogique. Il ne représente pas intégralement le comportement d’un train d’atterrissage réel, notamment son contact avec la piste et son amortissement oléopneumatique.*

## 4. Données numériques
On considère les valeurs illustratives suivantes :

| Paramètre | Symbole | Valeur |
| :--- | :---: | :---: |
| Masse équivalente | $m$ | 100 kg |
| Raideur du ressort | $k$ | 20 000 N/m |
| Coefficient d’amortissement de référence | $c$ | 1 500 N·s/m |
| Déplacement initial | $x(0)$ | 0 m |
| Vitesse initiale | $\dot{x}(0)$ | 1 m/s |
| Durée de simulation | $T$ | 2 s |
