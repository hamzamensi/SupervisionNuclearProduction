# SupervisionNuclearProduction

Pré-requis:
- Il faut avoir une version python 3.9.
- Il faut avoir un compte RTE, et Mettre le clientId, SecretId dans des variables d'environnements.

Installation:
- cloner le projet en local.
- python -m venv [nom de virtual env]
- pip install -r requiremnts.txt
- python app.py

Informations utiles: 
- http://localhost:5000/ : une route pour accéder à une page qui affiche un barplot de la somme de la production infrajournalière par heure
du jour sur la période 01/12/2022 à 10/12/2022.
- http://localhost:5000/realtime: une route pour accéder à ue page qui affiche en temps réel sur une période hebdomadaire
glissante.