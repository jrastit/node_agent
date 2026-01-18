# Tests API

Ce dossier contient les tests des endpoints d'API exposés par le projet.

- **test_api_test.py** : Vérifie le ping de l'API de test.
- **test_api.py** : Teste l'authentification et la protection des endpoints.
- **server/test_api_server.py** : Teste la création, la modification, la suppression et la récupération des serveurs via l'API.
- **oasis/test_api_oasis.py** : Teste la gestion des entités, réseaux, types de noeuds et noeuds Oasis via l'API.

Utilitaires :
- **utils/api_util.py** : Fonctions utilitaires pour les appels API dans les tests.
- **utils/test_node.py** : Chargement de noeuds de test pour les scénarios API.

Lancez les tests avec `pytest tests/api/`.
