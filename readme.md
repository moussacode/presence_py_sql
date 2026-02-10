# Gestion d’Inventaire – Python & MySQL

Projet de **gestion d’inventaire** développé en **Python** avec **MySQL (MariaDB)**.  
Il permet de gérer des **catégories**, des **produits**, le **stock** et les **mouvements d’entrée/sortie**, avec des règles d’intégrité bien définies.

---

## Fonctionnalités

### Gestion des catégories
- Ajouter une catégorie
- Modifier une catégorie
- Supprimer une catégorie  
   Impossible si elle est utilisée par des produits (`ON DELETE RESTRICT`)
- Afficher la liste des catégories

---

### Gestion des produits
- Ajouter un produit (désignation, prix, catégorie)
- Modifier :
  - la désignation
  - la catégorie
  - le prix
- Supprimer un produit  
  Impossible si des mouvements existent
- Afficher les produits avec leur **catégorie**
- Alerte : afficher les produits dont le **stock < 5**

---

### Gestion du stock
- Entrée de stock (`ENTREE`)
- Sortie de stock (`SORTIE`)
- Vérification automatique :
  - Stock jamais négatif
  - Sortie refusée si stock insuffisant
- Historique conservé dans la table `mouvements`

---

## Structure de la base de données

### Table `categories`
| Champ | Type |
|------|------|
| id_categorie | INT (PK) |
| nom_categorie | VARCHAR (UNIQUE) |

---

### Table `produits`
| Champ | Type |
|------|------|
| id_produit | INT (PK) |
| designation | VARCHAR |
| prix | DECIMAL |
| id_categorie | INT (FK) |
| stock | INT |
| en_rupture | BOOLEAN |
| date_creation | TIMESTAMP |

 Relation :

**FOREIGN KEY (id_categorie)
REFERENCES categories(id_categorie)
ON DELETE RESTRICT
ON UPDATE CASCADE**

---
###  Table `mouvements`

| Champ | Type |
|------|------|
| id_mouvement | INT (AUTO_INCREMENT, PK) |
| id_produit | INT (FK) |
| type_mouvement | ENUM('ENTREE','SORTIE') |
| quantite | INT |
| date_mouvement | TIMESTAMP |

---

 Relation :

**FOREIGN KEY (id_produit)
REFERENCES produits(id_produit)
ON DELETE CASCADE**

## Règles métier appliquées

- Une catégorie ne peut pas être supprimée si elle contient des produits
- Un produit ne peut pas être supprimé s’il possède des mouvements
- Le stock ne peut jamais être négatif
- Les produits dont le stock est inférieur à 5 unités sont signalés
- Les mouvements sont enregistrés avant la mise à jour du stock

---

## Installation et exécution

### Prérequis

- Python 3.x  
- MySQL ou MariaDB  
- Module Python requis : 

```bash
pip install mysql-connector-python
```
### Configuration de la base de données

Créer la base de données :
```bash
CREATE DATABASE gestion_inventaire;
```
Configurer la connexion dans le fichier Python :
```bash
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_inventaire",
    charset="utf8mb4",
    use_unicode=True
)
```
