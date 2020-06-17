# NuSMV

## Description de la librairie:
NuSMV est une réimplémentation et une extension du vérificateur de modèle symbolique SMV, le premier outil de vérification de modèle basé sur des diagrammes de décision binaires. L'outil a été conçu comme une architecture ouverte pour la vérification des modèles.
La librairie est accessible [ici](http://nusmv.fbk.eu/).

## Contenu :
A partir du fichier *pyboolnetFileTest* les fichiers suivants ont pu être générés :
- booleanModel correspondant au modèle booléen du BDD calculé à partir du modèle entré
- flattenedModel correspond à la finite state machine (FSM) du modèle d'entrée
- traceVerbose4.txt contient la trace de NuSMV (i.e. les étapes de calcul et de model checking) de niveau 4 (niveau maximal)

Nous cherchions encore à ce stade à déterminer comment récupérer et calculer les primes implicants du BDD généré par NuSMV. 
