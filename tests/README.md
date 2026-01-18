# README des tests

Ce dossier contient l'ensemble des tests automatisés pour le projet node_agent.

## Structure des tests

- **api/** : Tests des endpoints d'API (authentification, serveur, oasis, etc.)
- **ansible/** : Tests liés à l'intégration Ansible.
- **data/** : Tests sur la gestion et la transformation des données de configuration.
- **model/** : Tests sur les modèles de base de données.
- **service/** : Tests des services métiers (Oasis, serveur, etc.).
- **shell/** : Tests des commandes shell et de leur intégration.
- **utils/** : Tests des utilitaires (threads, nodes, etc.).

## Lancer les tests

Utilisez la commande suivante à la racine du projet :

```bash
./test.sh
```

ou directement avec pytest :

```bash
pytest tests/
```

## Prérequis
- Base de données de test configurée
- Dépendances installées (`pip install -r requirements_test.txt`)

Chaque sous-dossier contient un README détaillant les tests spécifiques.
