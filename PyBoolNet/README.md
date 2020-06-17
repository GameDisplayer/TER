# PyBoolNet

## Description de la librairie:
PyBoolNet est un package Python pour la génération, la modification et l'analyse de réseaux booléens. L'article de recherche associé est intitulé : [PyBoolNet: a python package for the generation, analysis and visualization of boolean networks](https://academic.oup.com/bioinformatics/article/33/5/770/2725550)
La librairie est accessible [ici](https://github.com/hklarner/PyBoolNet).

## Contenu des sous dossiers :
- Le dossier **commitment_sets** contient :
  1. un fichier ***commitment_sets*** qui a pour but de retracer les étapes de l'article en générant le state transition graph (STG) ainsi que les bassins d'attraction et les commitment sets à partir des attracteurs du fichier json d'un exemple simple (fichiers disponibles dans le dossier *visualisation*).
  2. un fichier ***understand*** qui a pour but de récupérer les logs de NuSMV lors de la création des commitment sets (sur le même exemple que ci-dessus) afin de comprendre l'évolution des CTL et plus généralement le model checking mis en place (disponibles dans le dossier *pyboolnet_accepting_files*).
- Le dossier **test_pyboolnet_semaphore** contient deux scripts python : 
  1. ***CTL_acc_states*** qui parse via les méthodes de PyBoolNet les réponses renvoyées par NuSMV-a sur les 2 CTL du fichier semaphore.smv (chaque CTL est comprise dans un fichier smv car NuSMV-a ne traite qu'une CTL à la fois)
  2. ***source_erreur*** qui permet de localiser l'erreur renvoyée par la méthode *output2counterexample* de PyBoolNet (sur la 2ème CTL fausse)
- Le dossier **version_pyboolnet_modifiee** contient un script python avec la méthode *check_primes_with_acceptingstates* modifiée afin de pouvoir récupérer le fichier généré (et enregistré dans /tmp) par la méthode *primes2smv*.
Un exemple d'utilisation tiré du tutoriel de PyBoolNet est aussi présent afin de pouvoir tester la méthode modifiée.

