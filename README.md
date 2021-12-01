# Sub-Read-it

L'objectif de ce projet est de créer un programme capable de donner une indication de la fiabilité d'une subreddit donnée. Plus de précisions sont disponibles dans le fichier `Besoin_et_solution_envisagee` du dossier `WorkingDocs`.

## Contribution

Le projet est divisé en objectifs et en fonctionnalités disponibles dans le fichier `Fonctionnalites` du le dossier `WorkingDocs`. Le travail est réparti et attribué sur le board Trello disponible ici: https://trello.com/invite/b/2mE1Npif/ea59c0c548a226ca0fe09f58056a108f/t%C3%A2ches

Lorsque vous effectuez une modification, vérifiez après que les tests fonctionnent toujours avec la commande: `pytest tests`
On utilise le framework `pytest` pour effectuer les tests unitaires. Celui-ci n'est pas nécessaire pour exécuter le programme. Il s'installe avec `pip install -U pytest`

## Installation

Ce projet utilise `Python 3.8 64bits`, disponible ici: https://www.python.org/downloads/release/python-385/
De plus, les dépendances suivantes sont nécessaires:


- `numpy` installable avec `pip install numpy`
- `flask` installable avec `pip install flask`
- `sklearn` installable avec `pip install sklearn`
- `pandas` installable avec `pip install pandas`
- `lxml` installable avec `pip install lxml`
- `textblob` installable avec `pip install textblob`
- `wordcloud` installable avec `pip install wordcloud`
- `spacy` installable avec `pip install spacy` et `python -m spacy download en_core_web_sm` 

Vous pouvez installer toutes ces dépendences d'un coup avec la commande `pip install -r requirements.txt`.
N'oubliez pas de faire après la commande: `python -m spacy download en_core_web_sm` !

## Présentation

Elle est disponible ici: https://docs.google.com/presentation/d/1QPaKvQ8PYIeNzA-xKOXlo8AFXmhd95pPn6JzQoFMILA/

## Utilisation

Lancer le projet avec `start_flask.bat`
Aller avec son navigateur à l'adresse : `http://localhost` pour accéder à l'interface.
Si d'autres appareils sont connectés au même réseau (wifi) que vous, ceux-ci pourront accéder au site !
Il est donc possible d'utiliser le site sur votre mobile !

## Détails techniques

Ce projet utilise du machine learning avec sklearn pour fonctionner. Un fichier contenant un classificateur préentrainé est fourni.
Cependant, si vous rencontrez des erreurs, vous pouvez réentrainer le réseau en lançant: `python src\data_analysis\train_pac.py`

Attention, l'entrainement peut prendre jusqu'à 15 minutes, surtout si votre ordinateur est peu performant.

De plus, le système que l'on utilise crée un serveur web pour afficher la visualisation. Vous pouvez donc faire tourner ce projet sur
un serveur dédié de manière à rendre le site accessible à internet en ouvrant le port 80 du serveur.

## Membres 

- Membre 1 : Louis Fliche : louis.fliche@student-cs.fr
- Membre 2 : Antoine Delègue : antoine.delegue@student-cs.fr
- Membre 3 : Manh-Bao Nguyen : manh-bao.nguyen@student-cs.fr
- Membre 4 : Emmanuel Lembe Vardamides: lembe.vardamides@student-cs.fr
- Membre 5 : Tanguy Marsault : tanguy.marsault@student-cs.fr