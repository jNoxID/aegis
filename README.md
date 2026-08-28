# AEGIS

AEGIS est une plateforme destinée aux opérations de sécurité et aux tests autorisés, conçue autour d’un principe fondamental :

> **Aucune capacité active ne peut être exécutée sans une décision de politique vérifiable et auditable.**

Le projet se trouve actuellement en **Phase 0 / première étape des fondations**.

Il fournit un petit noyau exécutable de politique de périmètre (*scope policy kernel*) fonctionnant selon le principe **« refus par défaut » (deny-by-default)**.

À ce stade, AEGIS **ne fournit aucun scanner ni aucune capacité offensive**.

---

## Démarrage rapide

AEGIS nécessite **Python 3.13 ou une version plus récente**.

### 1. Cloner le dépôt

```bash
git clone https://github.com/jNoxID/aegis.git
cd aegis
```

### 2. Vérifier que l’on se trouve à la racine du dépôt

```bash
git rev-parse --show-toplevel
```

Tu dois être dans le répertoire contenant notamment :

```text
pyproject.toml
README.md
src/
tests/
```

### 3. Créer un environnement virtuel Python

```bash
python3 -m venv .venv
```

### 4. Activer l’environnement virtuel

Sous Linux/Bash :

```bash
source .venv/bin/activate
```

Après activation, ton terminal devrait généralement afficher quelque chose comme :

```text
(.venv) user@machine:~/aegis$
```

### 5. Installer AEGIS et ses dépendances de développement

```bash
python -m pip install -e '.[dev]'
```

L’option `-e` installe le projet en mode **editable**.

Cela signifie notamment que les modifications apportées au code source local d’AEGIS sont directement prises en compte sans devoir réinstaller le paquet après chaque modification.

### 6. Vérifier l’installation

```bash
aegis doctor
```

### 7. Démarrer le serveur AEGIS

```bash
aegis server
```

### 8. Exécuter les tests

Dans un autre terminal, après activation du même environnement virtuel :

```bash
cd aegis
source .venv/bin/activate
pytest
```

---

## Vérification du périmètre : `scope-check`

La commande :

```bash
aegis scope-check \
  --domain app.lab.example \
  --allow-domain app.lab.example
```

constitue une démonstration locale de l’évaluation du périmètre (*scope evaluation*).

Cette opération est conçue pour être **sans effet secondaire**.

Elle permet de voir comment AEGIS détermine si un domaine appartient au périmètre explicitement autorisé.

Dans cet exemple :

```text
Domaine demandé :
app.lab.example

Domaine autorisé :
app.lab.example
```

AEGIS peut donc évaluer la cible par rapport à la politique de périmètre fournie.

---

## Serveur AEGIS

La commande :

```bash
aegis server
```

démarre le premier environnement d’exécution persistant (*runtime*) d’AEGIS sur :

```text
http://127.0.0.1:8000
```

Plusieurs points d’accès HTTP deviennent alors disponibles.

### Racine

```text
/
```

### Vérification de l’état du serveur

```text
/health
```

### État de l’API versionnée

```text
/api/v1/status
```

### Documentation interactive de l’API

```text
/docs
```

Par exemple, depuis Linux :

```bash
curl http://127.0.0.1:8000/health
```

ou :

```bash
curl http://127.0.0.1:8000/api/v1/status
```

La documentation interactive peut être ouverte dans un navigateur à l’adresse :

```text
http://127.0.0.1:8000/docs
```

---

## Configuration du serveur

Pour afficher les options disponibles :

```bash
aegis server --help
```

Cela permet notamment de configurer l’adresse locale et le port utilisés par le serveur.

AEGIS peut également être lancé directement comme module Python.

La commande :

```bash
aegis server
```

possède donc l’équivalent :

```bash
python -m aegis server
```

---

## Si `pip` ne trouve pas `pyproject.toml`

L’installation doit être exécutée depuis la **racine du dépôt AEGIS**.

Vérifie d’abord ta position :

```bash
pwd
```

Puis :

```bash
git rev-parse --show-toplevel
```

Et vérifie la présence du fichier :

```bash
ls -l pyproject.toml
```

Tu peux également utiliser :

```bash
test -f pyproject.toml && echo "OK : pyproject.toml trouvé" || echo "ERREUR : pyproject.toml absent"
```

Si `pyproject.toml` n’est pas présent, tu te trouves probablement dans le mauvais répertoire ou ton clone du dépôt est incomplet.

**Ne crée pas un deuxième fichier de packaging.**

Ce dépôt constitue un projet Python unique utilisant notamment :

```text
src/aegis/
```

La configuration de packaging faisant autorité est :

```text
pyproject.toml
```

situé à la racine du dépôt.

---

## Documentation du projet

Pour comprendre davantage AEGIS, consulter :

```text
ARCHITECTURE.md
THREAT_MODEL.md
SECURITY.md
CONTRIBUTING.md
```

Ils décrivent respectivement :

* l’architecture d’AEGIS ;
* son modèle de menaces ;
* sa politique de sécurité ;
* les règles et recommandations pour contribuer au projet.

---

# Sécurité et état du projet

AEGIS doit uniquement être utilisé sur des systèmes :

* que tu possèdes ; ou
* pour lesquels tu disposes d’une **autorisation explicite de test**.

L’autorisation du périmètre (*scope authorization*) est **nécessaire mais ne sera pas suffisante** pour les futures opérations sensibles.

Celles-ci devront également passer par différents contrôles, notamment :

```text
Scope
  +
RBAC
  +
Approval
  +
Quota
  +
Environment checks
  +
Kill switch
```

Autrement dit, le fait qu’une cible appartienne au périmètre autorisé ne signifie pas automatiquement que n’importe quelle opération pourra être exécutée contre elle.

---

## État du projet

AEGIS est actuellement en :

**pré-alpha**

Les API et les formats de persistance ne sont donc **pas encore stables**.

Des changements incompatibles peuvent survenir pendant le développement.

---

# Licence

AEGIS est distribué sous :

**GNU General Public License v3.0 (GPLv3)**

Consulter le fichier :

```text
LICENSE
```

pour les conditions complètes de la licence.
