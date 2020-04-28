Exemples biologiques
---------------------

Dossier fichiersTotem 
----------------------
- les fichiers .smb sont les descriptions sources
- fichier .out : donne tous les paramétrages et indique s'ils sont OK (formule CTL vérifiée) ou KO (formule CTL fausse)

Dossier fichiersNuSMV
----------------------
- contient les fichiers .smv générés par Totem pour des paramétrages OK
- la formule CTL est en principe formule donnant un attracteur
- il y a des exemples ou l'attracteur est 1 état qui fixe toutes les variables ( cf bacteriophageLambda2) mais dans la plupart, on sait seulement qu'une variable est attracteur. Donc par exemple, pour mucusOperon, operon=0 est attracteur, mais comme il y a aussi la variable mucuB, il devrait y avoir 2 attracteurs : (0,0) et (0,1) (pour mucuB=0 ou 1)
- il y a des exemples ou la formule du fichier .smb contient une implication (cf tadpole2 ((T3=3 & T4=1 & d2=1 & d3=0 & gi=1 & gp=1 & tr=1 & gt=0) -> AF(gt=1)))
Dans ce cas, j'ai remplacé la prémisse de l'implication par un bloc d'initialisation des variables.

Pour vos tests, commencez avec mucusOperon et pseudomonas qui sont petits.

Si vous réussissez à appliquer la séquence de l'article à des exemples avec des entiers, il pourra être intéressant de générer d'autres exemples de fichiers .smv, en particulier avec les paramétrages KO.
Pour cela, c'est simple, pour l'exemple toto.smb, vous regardez le fichier toto.out et vous modifiez le fichier toto.smv en mettant les valeurs des paramètres d'un modèle de votre choix en changeant les valeurs des K dans la partie "FROZENVAR".

On laisse tomber la traduction booléenne que j'ai générée pour l'instant. Si vous réussissez à traiter directement les .smv contenant des entiers, c'est encore bien mieux.
