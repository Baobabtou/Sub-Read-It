# Projet Sub-Read-It

## Définition du besoin

Reddit est un réseau social encore peu utilisé en France. La diversité des sujets des communautés qui y sont présentes - les *subreddits* - fait que leur contenu est plus ou moins fiable ...

**Quoi ?** Un programme qui à une subreddit donnée renvoie un *indicateur clair* de sa *fiabilité* (i.e. de la véracité globale de son contenu).

**Pourquoi ?** Certaines subreddits, portant sur des sujets très précis, ou étant moins actives, voient parfois le partage d'informations qui sont des *Fake News* : il faut en être conscient avant de s'y inscrire !

**Pour qui.** Pour le néophyte sur Reddit qui veut s'assurer de la qualité d'information globale d'une subreddit avant d'intégrer cette communauté.

**User Story :** En tant que néophyte hésitant à intégrer une subreddit douteuse, je voudrais avoir un indicateur clair de la fiabilité globale des informations partagées dans cette subreddit -- au-delà du MVP : et si possible avoir un aperçu global du contenu de cette subreddit (mots-clés et analyses statistiques).

*Note* : Le MVP répond à un besoin assez simple avec une réponse aussi simple. On pourra ensuite ajouter d'autres analyses plus précises sur la subreddit , qui permettront à l'utilisateur d'affiner son choix de suivre, ou non, la subreddit.

## Expérience utilisateur recherchée

L'utilisateur se rend sur une **interface HTML** et peut :

- Saisir le nom exact de la subreddit qu'il veut examiner
- On lui renvoie alors un indicateur clair de la fiabilité de cette subreddit (une valeur numérique claire).
- On peut aussi lui renvoyer (au-delà du MVP) d'autres données caractérisant le type de posts sur ce subreddit (mots-clés, ...).


## Solution envisagée
**Collecte de données**
Nous récupèrerons des données sur le site https://reddit.com, que nous analyserons. Il s'agit d'un site web communautaire américain d’actualités sociales fonctionnant via le partage de signets. L'intérêt de ce site par rapport à Twitter ou Facebook par exemple est qu'il donne accès une récupération d'informations simplifiée et **sans limite**, permettant des analyses de plus grande ampleur (éventuellement en direct), tout en étant un site extrêmement fréquenté dans le monde anglophobe, et de plus en plus en France.

**Analyse des données**
Une fois ces données collectées, nous chercherons à les analyser, afin de pouvoir classifier les messages en tant que fake news ou non (indicateur entre 0 et 1 de véracité).
Nous essaierons plusieurs méthodes pour ce faire, dont une utilisant du machine learning, pour apprendre à notre modèle à analyser la véracité d'un texte.
En faisant la synthèse de l'analyse de véracité de chaque post de la subreddit en question, on en déduira un indicateur moyen de fiabilité de la subreddit.
(On pourra inclure d'autres paramètres statistiques d'analyse de la subreddit : sur les commentaires, le vocabulaire, etc.)

**Visualisation des résultats**
Enfin, nous créerons un outil de visualisation permettant de : 

- Afficher les résultats de nos analyses statistiques : indicateur de fiabilité
- Afficher d'autres paramètres pouvant éclairer l'utilisateur sur le contenu de la subreddit qu'il souhaite évaluer.