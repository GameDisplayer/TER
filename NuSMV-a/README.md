# NuSMV -a

## Description de la librairie:
NuSMV-a est une extension de NuSMV 2.6.0 qui ajoute l'option de ligne de commande -a pour afficher et enregistrer les états d'acceptation des requêtes. Il a été écrit par Frederike Heinitz et Sarah Nee dans le cadre d'un stage sous la direction de Hannes Klarner à la Freie Universität de Berlin.
La librairie est accessible [ici](https://github.com/hklarner/NuSMV-a).

## Contenu des sous dossiers :
- Le dossier **mucus_nusmv_a** a pour but d'analyser le fonctionnement de NuSMV-a sur le fichier d'étude mucusOperon.smv.
La ligne de commande pour obtenir le fichier de sortie mucus_accepting est la suivante : `NuSMV -a mucus_accepting mucusOperon.smv`
- Le dossier **parser_nusmv_a** contient les fichiers .c de la librairie NuSMV -a qui parsent les réponses de NuSMV et renvoient les accepting states.
