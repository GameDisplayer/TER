# TRAVAIL D'ETUDE ET DE RECHERCHE - M1 Informatique Université Nice Côte d'Azur

## Auteurs

Nina SINGLAN et Romain MICHELUCCI sous la direction de Hélène COLLAVIZZA.

## Sujet:
Analyse des phénotypes dans les réseaux de régulation génétiques: étude de cas du métabolisme énergétique dans le cancer du pancréas.

## Objectifs:

Ce github a pour ambition de retracer les principales étapes d'analyse des librairies et des algorithmes étudiés tout au long de notre TER.
De manière non exhaustive vous trouverez les réponses à ces différents points :
- [x] Essayer de tracer complètement la démarche de l'article sur les commitment sets à l'aide de PyBoolNet et comprendre comment sont obtenus les diagrammes de la figure 3 de [l'article de départ](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8580379). 
- [x] Approfondir le fonctionnement de NuSMV-a en espérant récupérer des états acceptants sous une forme plus générale
- [x] Analyse du parser de NuSMV -a et compréhension de NuSMV
- [x] Etude de librairies annexes permettant la génération de primes implicants à partir d'un BDD

## Détails :
Une brève description des différents dossiers (un readme est présent dans chacun d'entre eux pour plus de précisions):
- **Rapports** contient les différents rapports écrits au cours du semestre sur nos recherches.
- **NuSMV** comprend une étude des options du vérificateur de modèle symbolique [NuSMV](http://nusmv.fbk.eu/).
- **PyBoolNet** contient de nombreux sous-dossiers liés à l'utilisation et l'étude complète de cette [librairie python](https://github.com/hklarner/PyBoolNet).
- **PyNuSMV** contient un fichier test permettant de mieux comprendre l'intérêt de la librairie du même nom accessible [ici](https://github.com/sbusard/pynusmv).
- **NuSMV-a** contient lui aussi plusieurs sous dossiers détaillés dans l'arborescence sur l'analyse de la librairie C.
- **Algorithmes** retrace l'étude approfondie d'algorithmes de graphe étudiés.

