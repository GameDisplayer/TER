# TER
Sujet : Analyse des phénotypes dans les réseaux de régulation génétiques: étude de cas du métabolisme énergétique dans le cancer du pancréas.

## Détails :
- Le dossier **Rapports** contient les différents rapports écrits au cours de nos recherches.

- Le dossier **test_pyboolnet_semaphore** contient deux scripts python : 
  1. ***CTL_acc_states*** qui parse via les méthodes de PyBoolNet les réponses renvoyées par NuSMV-a sur les 2 CTL du fichier semaphore.smv (chaque CTL est comprise dans un fichier smv car NuSMV-a ne traite qu'une CTL à la fois)
  2. ***source_erreur*** qui permet de localiser l'erreur renvoyée par la méthode *output2counterexample* de PyBoolNet (sur la 2ème CTL fausse)
  
- Le dossier **version_pyboolnet_modifiee** contient un script python avec la méthode *check_primes_with_acceptingstates* modifiée afin de pouvoir récupérer le fichier généré (et enregistré dans /tmp) par la méthode *primes2smv*.
Un exemple d'utilisation tiré du tutoriel de PyBoolNet est aussi présent afin de pouvoir tester la méthode modifiée.

- Le dossier **mucus_nusmv_a** a pour but d'analyser le fonctionnement de NuSMV-a sur le fichier d'étude mucusOperon.smv.
La ligne de commande pour obtenir le fichier de sortie mucus_accetping : `NuSMV -a mucus_accepting mucusOperon.smv`

- Le dossier **commitment_sets** contient :
  1. un fichier *commitment_sets* qui a pour but de retracer les étapes du paper https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8580379 en générant le state transition graph ainsi que les bassins d'attraction et les commitment sets (à partir des attracteurs du fichier json) sur un exemple simple.
  2. un fichier *understand* qui a pour but de récupérer les logs de NuSMV lors de la création des commitment sets (sur le même exemple que ci-dessus) afin de comprendre l'évolution des CTL (et plus généralement le model checking mis en place).

- Le dossier **parser_nusmv_a** contient les fichiers .c de la librairie NuSMV -a qui parsent les réponses de NuSMV et renvoient les accepting states.

## Objectifs pour le prochain rendez-vous:
- [x] Approfondir le fonctionnement de NuSMV-a en espérant récupérer des états acceptants sous une forme plus générale
- [x] Essayer de tracer complètement la démarche de l'article sur les commitment sets et comprendre comment sont obtenus les diagrammes de la figure 3 de l'article de départ. Essayer aussi de voir en détail les entrées/sorties vers NuSMV-a.
- [ ] Analyse du parser de NuSMV -a et compréhension de NuSMV
