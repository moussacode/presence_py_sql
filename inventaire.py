import mysql.connector

print("mysql-connector chargé avec succès ✅")
# Establish a connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="gestion_inventaire",
    charset="utf8mb4",
    use_unicode=True
)
# Check if the connection is successful
if connection.is_connected():
    print("Connected to MySQL database")

def create_table():
    cursor = connection.cursor()
    query_categories = """
CREATE TABLE IF NOT EXISTS categories (
    id_categorie INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(50) NOT NULL UNIQUE
);

    """
    query_produits = """
    CREATE TABLE IF NOT EXISTS produits (
        id_produit INT AUTO_INCREMENT PRIMARY KEY,
        designation VARCHAR(100) NOT NULL,
        prix DECIMAL(10,2) NOT NULL CHECK (prix >= 0),
        id_categorie INT NOT NULL,
        en_rupture BOOLEAN NOT NULL DEFAULT FALSE,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_produit_categorie
            FOREIGN KEY (id_categorie)
            REFERENCES categories(id_categorie)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
);
    """
    query_mouvements= """

    CREATE TABLE IF NOT EXISTS mouvements (
        id_mouvement INT AUTO_INCREMENT PRIMARY KEY,
        id_produit INT NOT NULL,
        type_mouvement ENUM('ENTREE', 'SORTIE') NOT NULL,
        quantite INT NOT NULL CHECK (quantite > 0),
        date_mouvement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_mouvement_produit
            FOREIGN KEY (id_produit)
            REFERENCES produits(id_produit)
            ON DELETE CASCADE
);
    
    """

    cursor.execute(query_categories)
    cursor.execute(query_produits)
    cursor.execute(query_mouvements)
    

    connection.commit()
    cursor.close()

    # print("Tables créées avec succès ")
create_table()

def categorie_existe(cursor, id_categorie):
    cursor.execute(
        "SELECT 1 FROM categories WHERE id_categorie = %s",
        (id_categorie,)
    )
    return cursor.fetchone() is not None


def produit_existe(cursor, id_produit):
    cursor.execute(
        "SELECT 1 FROM produits WHERE id_produit = %s",
        (id_produit,)
    )
    return cursor.fetchone() is not None

def ajout_categorie():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id_categorie, nom_categorie FROM categories order by id_categorie")
    print("\n Categories disponibles :")
    for c in cursor.fetchall():
        print(f"{c['id_categorie']} - {c['nom_categorie']}")
    while True:
            nom_categorie = input("Saisir le nom de la categorie :").strip()
            if nom_categorie.isalpha() :
                break
            else:
                print("categorie invalide. Veuillez réessayer.")

    ajout_categorie = """
    INSERT INTO categories (nom_categorie) VALUES
        (%s);
    """
    cursor.execute(ajout_categorie, (nom_categorie,))
    connection.commit()
def ajout_produit():
    cursor = connection.cursor(dictionary=True)
    afficher_produit()
    while True:
            designation = input("Saisir le nom du produit :").strip()
            if designation.isalpha() :
                break
            else:
                print("nom invalide. Veuillez réessayer.")
    while True:
            prix = int(input('Saisir le montant : '))
            if prix < 0 :
                print('Donner un montant superieur a 0')
            elif prix == 0:
                print("Vous avez decidez de quitter ")
                menu_produit()
            else :
                break
    cursor.execute("SELECT id_categorie, nom_categorie FROM categories order by id_categorie")
    print("\n Categories disponibles :")
    for c in cursor.fetchall():
        print(f"{c['id_categorie']} - {c['nom_categorie']}")

    while True:
        try:
            id_categorie = int(input("Saisir le numéro de la categorie : "))

            if categorie_existe(cursor, id_categorie):
                break
            else:
                print("Cette categorie n'existe pas. Réessaie.")

        except ValueError:
            print("Veuillez entrer un nombre valide.")
    
    print('Categorie trouver')  
    ajout_produit = """
    INSERT INTO produits (designation,prix,id_categorie) VALUES
        (%s,%s,%s);
    """
    cursor.execute(ajout_produit, (designation,prix,id_categorie))
    connection.commit()
def modifie_produit():
    cursor = connection.cursor(dictionary=True)
    afficher_produit()

    # Choix du produit
    while True:
        try:
            id_produit = int(input("Saisir le numéro du produit : "))
            if produit_existe(cursor, id_produit):
                break
            else:
                print("Ce produit n'existe pas.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    print("Produit trouvé ")

    while True:
        print("\n--- MODIFICATION PRODUIT ---")
        print("1. Modifier la désignation")
        print("2. Modifier la catégorie")
        print("3. Modifier le prix")
        print("0. Retour")

        choix = input("Choix : ").strip()

        # MODIFIER DESIGNATION
        if choix == "1":
            designation = input("Nouvelle désignation : ").strip()
            if not designation:
                print("Désignation invalide.")
                continue

            cursor.execute(
                "UPDATE produits SET designation = %s WHERE id_produit = %s",
                (designation, id_produit)
            )
            connection.commit()
            print("Désignation modifiée avec succès ")

        # MODIFIER CATEGORIE
        elif choix == "2":
            afficher_categorie()
            while True:
                try:
                    id_categorie = int(input("Nouvelle catégorie : "))
                    if categorie_existe(cursor, id_categorie):
                        break
                    else:
                        print("Catégorie inexistante.")
                except ValueError:
                    print("Nombre invalide.")

            cursor.execute(
                "UPDATE produits SET id_categorie = %s WHERE id_produit = %s",
                (id_categorie, id_produit)
            )
            connection.commit()
            print("Catégorie modifiée avec succès ")

        # MODIFIER PRIX
        elif choix == "3":
            while True:
                try:
                    prix = float(input("Nouveau prix : "))
                    if prix > 0:
                        break
                    else:
                        print("Prix invalide.")
                except ValueError:
                    print("Nombre invalide.")

            cursor.execute(
                "UPDATE produits SET prix = %s WHERE id_produit = %s",
                (prix, id_produit)
            )
            connection.commit()
            print("Prix modifié avec succès ")

        elif choix == "0":
            break

        else:
            print("Choix invalide.")
 

    


def modifie_categorie():
    cursor = connection.cursor(dictionary=True)
    afficher_produit()
    print('')
    while True:
        try:
            id_categorie = int(input("Saisir le numéro de la categorie : "))
            if id_categorie == 0:
                print("Redirection vers le menu ")
                menu_categorie()
            elif categorie_existe(cursor, id_categorie):
                break
            else:
                print("Cette categorie n'existe pas. Réessaie.")

        except ValueError:
            print("Veuillez entrer un nombre valide.")
    
    print('Categorie trouver')

    while True:
            nom_categorie = input("Modifier le nom de la categorie :").strip()
            if nom_categorie.isalpha() :
                break
            else:
                print("categorie invalide. Veuillez réessayer.")

    modifie_categorie = """
    UPDATE categories SET nom_categorie = %s WHERE id_categorie = %s
    """
    cursor.execute(modifie_categorie, (nom_categorie,id_categorie))
    connection.commit()
def supprimer_categorie():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id_categorie, nom_categorie FROM categories order by id_categorie")
    print("\n Categories disponibles :")
    for c in cursor.fetchall():
        print(f"{c['id_categorie']} - {c['nom_categorie']}")

    while True:
        try:
            id_categorie = int(input("Saisir le numéro de la categorie a supprimer : "))
            if id_categorie=='0':
                print("Redirection vers le menu ")
                menu_categorie()
            elif categorie_existe(cursor, id_categorie):
                break
            else:
                print("Cette categorie n'existe pas. Réessaie.")

        except ValueError:
            print("Veuillez entrer un nombre valide.")
    
    print('Categorie trouver')

    try :

        supprimer_categorie = """
            DELETE FROM categories WHERE id_categorie = %s
        """
        cursor.execute(supprimer_categorie , (id_categorie,))
        connection.commit()
        if cursor.rowcount:
            print(f"Catégorie '{id_categorie}' supprimée avec succès ")
        
    except  mysql.connector.IntegrityError as err:
        print(f"Erreur : Impossible de supprimer '{id_categorie}' car elle est utilisée par des produits.")
def afficher_categorie():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id_categorie, nom_categorie FROM categories order by id_categorie")
    print("\n Categories disponibles :")
    for c in cursor.fetchall():
        print(f"{c['id_categorie']} - {c['nom_categorie']}")
def afficher_produit():
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            p.id_produit,
            p.designation,
            c.nom_categorie
        FROM produits p
        JOIN categories c ON p.id_categorie = c.id_categorie
        ORDER BY p.id_produit
    """
    cursor.execute(query)

    print("\nLISTE DES PRODUITS")
    print("-" * 50)
    print(f"{'ID':<5} {'Produit':<20} {'Catégorie'}")
    print("-" * 50)

    for p in cursor.fetchall():
        print(f"{p['id_produit']:<5} {p['designation']:<20} {p['nom_categorie']}")


def entrer_mouvement():
    cursor = connection.cursor(dictionary=True)
    afficher_produit()  # affiche la liste des produits

    # Choix du produit
    while True:
        try:
            id_produit = int(input("Saisir le numéro du produit : "))
            if produit_existe(cursor, id_produit):
                break
            else:
                print("Ce produit n'existe pas. Réessaie.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Saisie de la quantité
    while True:
        try:
            quantite = int(input("Saisir la quantité à ajouter : "))
            if quantite < 0:
                print("Donner une quantité supérieure à 0")
            elif quantite == 0:
                print("Vous avez décidé de quitter.")
                return  # on sort de la fonction
            else:
                break
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    
    try:
        type_mouvement= 'ENTREE'
        cursor.execute(
            "INSERT INTO mouvements (id_produit, quantite,type_mouvement) VALUES (%s, %s,%s)",
            (id_produit, quantite,type_mouvement)
        )
        cursor.execute(
        "UPDATE produits SET stock = stock + %s WHERE id_produit = %s",
            (quantite, id_produit)
)
        connection.commit()
        
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout du mouvement : {err}")
        connection.rollback()
  

def sortir_mouvement():
    cursor = connection.cursor(dictionary=True)
    afficher_produit()  # affiche la liste des produits

    # Choix du produit
    while True:
        try:
            id_produit = int(input("Saisir le numéro du produit : "))
            if produit_existe(cursor, id_produit):
                break
            else:
                print("Ce produit n'existe pas. Réessaie.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Saisie de la quantité
    while True:
        try:
            quantite = int(input("Saisir la quantité à ajouter : "))
            if quantite < 0:
                print("Donner une quantité supérieure à 0")
            elif quantite == 0:
                print("Vous avez décidé de quitter.")
                return  # on sort de la fonction
            else:
                break
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    
    try:
        type_mouvement = 'SORTIE'

        cursor.execute(
            "SELECT stock FROM produits WHERE id_produit = %s",
            (id_produit,)
        )
        stock_actuel = cursor.fetchone()["stock"]

        if stock_actuel < quantite:
            print("Stock insuffisant ")
            return

        cursor.execute(
            "INSERT INTO mouvements (id_produit, quantite, type_mouvement) VALUES (%s, %s, %s)",
            (id_produit, quantite, type_mouvement)
        )

        cursor.execute(
            "UPDATE produits SET stock = stock - %s WHERE id_produit = %s",
            (quantite, id_produit)
        )

        connection.commit()

        
    except mysql.connector.Error as err:
        print(f"Erreur lors du retrait du mouvement : {err}")
        connection.rollback()
 
def menu_categorie():
    print('============= MENU CATEGORIE ===============')
    while True:
        print ('')
        print("1. Pour ajouter une categorie :")
        print("2. Pour modifier une categorie :")
        print("3. Pour suprimer une categorie :")
        print("4. Pour afficher une categorie :")

        print("0. Pour precedent :")
        print("9. Pour Quitter :")
        
        
        choix=input('Taper un choix : ').replace(" ", "")
        print('')
        if choix =='1' :
           ajout_categorie()
        elif choix =='2':
            modifie_categorie()
        elif choix =='3':
            supprimer_categorie()
        elif choix =='4':
            afficher_categorie()
        elif choix=="9":
            exit()
        elif choix =='0' :
            break
        else:
            print('Choix invalide')

def alerte_produit():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
SELECT designation, stock
FROM produits
WHERE stock < 5
""")

    for row in cursor.fetchall():
        print(f"{row['designation']} : stock = {row['stock']}")

def supprimer_produit():
    cursor = connection.cursor(dictionary=True)

    afficher_produit()
    print("")

    # Choix du produit
    while True:
        try:
            id_produit = int(input("Saisir l'ID du produit à supprimer : "))
            if produit_existe(cursor, id_produit):
                break
            else:
                print("Ce produit n'existe pas.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Vérifier s'il y a des mouvements
    cursor.execute(
        "SELECT COUNT(*) AS total FROM mouvements WHERE id_produit = %s",
        (id_produit,)
    )
    nb_mouvements = cursor.fetchone()["total"]

    if nb_mouvements > 0:
        print(" Impossible de supprimer ce produit : des mouvements existent.")
        return

    # Confirmation
    confirm = input("Confirmer la suppression ? (o/n) : ").lower()
    if confirm != "o":
        print("Suppression annulée.")
        return

    # Suppression
    try:
        cursor.execute(
            "DELETE FROM produits WHERE id_produit = %s",
            (id_produit,)
        )
        connection.commit()
        print("Produit supprimé avec succès.")

    except mysql.connector.Error as err:
        print(f"Erreur lors de la suppression : {err}")

def menu_produit():
    print('============= MENU CATEGORIE ===============')
    while True:
        print ('')
        print("1. Pour ajouter un produit :")
        print("2. Pour modifier un produit :")
        print("3. Pour suprimer un produit :")
        print("4. Pour afficher les produit :")
        print("5. Afficher tous les produits dont stock < 5 unités :")

        print("0. Pour precedent :")
        print("9. Pour Quitter :")
        
        
        choix=input('Taper un choix : ').replace(" ", "")
        print('')
        if choix =='1' :
           ajout_produit()
        elif choix =='2':
            modifie_produit()
        elif choix =='3':
            supprimer_produit()
        elif choix =='4':
            afficher_produit()
        elif choix =='5':
            alerte_produit()
        elif choix=="9":
            exit()
        elif choix =='0' :
            break
        else:
            print('Choix invalide')

def menu_mouvement():
    print('============= MENU MOUVEMENT ===============')
    while True:
        print ('')
        print("1. Pour entrer un mouvement :")
        print("2. Pour sortir un mouvement :")
        print("3. Pour gerer les mouvements :")
        print("0. Pour precedent :")
        print("9. Pour Quitter :")
        
        
        choix=input('Taper un choix : ').replace(" ", "")
        print('')
        if choix =='1' :
           entrer_mouvement()
        elif choix =='2':
            sortir_mouvement()
        elif choix=="9":
            exit()
        elif choix =='0' :
            break
        else:
            print('Choix invalide')

def menu_inventaire():
    print('============= MENU INVENTAIRE ===============')
    while True:
        print ('')
        print("1. Pour gerer les categories :")
        print("2. Pour gerer les produits :")
        print("0. Pour precedent :")
        print("9. Pour Quitter :")
        
        
        choix=input('Taper un choix : ').replace(" ", "")
        print('')
        if choix =='1' :
           menu_categorie()
        elif choix =='2' :
           menu_produit()
        elif choix =='3' :
           menu_mouvement()
        
        elif choix=="9":
            exit()
        elif choix =='0' :
            break
        else:
            print('Choix invalide')
    
menu_inventaire()
