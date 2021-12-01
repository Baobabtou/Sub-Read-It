# DECOUPAGE DU PROJET POUR REPARTIR LES TACHES : en objectifs et fonctionnalités numérotés

## Objectif 1: Récupérer des données

1. Prise en main de la collecte de posts reddits d'une subreddit donnée sur Reddit
2. Transformer les informations sur les posts collectées en dataframe en extrayant les informations pertinentes
3. Récupérer des méta-données : upvote, commentaires et réponses...

Bonus : Recycler le code pour récupérer les données de twitter et les convertir vers un format similaire à reddit (analyse comparative ultérieure possible)

## Objectif 2 : Premières analyses sur les données

1. Analyser le sujet d'un post (à partir de son texte), mots-clés ...
2. Analyser la structure de commentaires d'un post
3. Analyse de sentiments/polarité sur le contenu du post et de ses commentaires


## Objectif 3 : Vérifier la véracité d'une information

1. Faire un modèle naïf (non ML) pour avoir un score de fake (analyse à partir des commentaires, etc.)

2. Faire un modèle sophistiqué par Machine Learning : 
   - Récolter une base de donnée exploitable pour la supervision
   - Mettre en place l'algorithme à entraîner .
   - Le faire tourner avec les données et le tester.

## Objectif 4 : Synthèse des analyses du SubReddit

1. Passer de l'analyse de chacun des posts du Subreddit au SubReddit général en faisant des moyennes

## Objectif 5 : Interface utilisateur

1. Faire une interface simple matplotlib pour afficher les caractéristiques précédentes
2. Faire une interface web avec python flask avec bouton : "analyser la subreddit"
3. Raffiner l'interface

Bonus : Mettre dans l'interface web une input pour rentrer l'url directement : ainsi, l'utilisateur pourra analyser un post en particulier