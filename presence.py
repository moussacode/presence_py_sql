import mysql.connector

print("mysql-connector chargé avec succès ✅")
# Establish a connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="gestion_presence"
)
# Check if the connection is successful
if connection.is_connected():
    print("Connected to MySQL database")

def create_table():
    cursor = connection.cursor()
    query_promos = """
   CREATE TABLE  IF NOT EXISTS Promos (
        id_promo INT NOT NULL AUTO_INCREMENT UNIQUE,
        labelle_promo VARCHAR(50) NOT NULL UNIQUE,
        description VARCHAR(50),
        PRIMARY KEY(id_promo)
);
    """
    query_etudiants = """
    CREATE TABLE  IF NOT EXISTS etudiants (
        id_etudiant INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        nom VARCHAR(50) NOT NULL,
        prenom VARCHAR(50) NOT NULL,
        id_promo INT NOT NULL,
        PRIMARY KEY(id_etudiant),
        FOREIGN KEY(id_promo) REFERENCES Promos(id_promo)
);
    """
    query_presences= """

    CREATE TABLE  IF NOT EXISTS presences(
        id_precence INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
        lable_presence VARCHAR(50) UNIQUE ,
        PRIMARY KEY(id_precence)
    );
    
    """
    query_pointages = """
    
    CREATE TABLE IF NOT EXISTS pointages (
    id_pointage INT AUTO_INCREMENT PRIMARY KEY,
    id_etudiant INT NOT NULL,
    id_precence INT NOT NULL,
    date_pointage DATE NOT NULL,
    heure_arrivee TIME NOT NULL,
    FOREIGN KEY (id_etudiant) REFERENCES etudiants(id_etudiant),
    FOREIGN KEY (id_precence) REFERENCES presences(id_precence),
    UNIQUE (id_etudiant, date_pointage)
);

    """

    cursor.execute(query_promos)
    cursor.execute(query_etudiants)
    cursor.execute(query_presences)
    cursor.execute(query_pointages)

    connection.commit()
    cursor.close()

    # print("Tables créées avec succès ")

create_table()
def list_etudiant():
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT E.nom, E.prenom, P.labelle_promo
        FROM etudiants E
        JOIN promos P ON E.id_promo = P.id_promo
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("Aucun étudiant trouvé.")
        return

    print("\nLISTE DES ÉTUDIANTS")
    print("-" * 50)
    print(f"{'Nom':<15} {'Prénom':<15} {'Promo':<15}")
    print("-" * 50)

    for row in rows:
        print(f"{row['nom']:<15} {row['prenom']:<15} {row['labelle_promo']:<15}")
    print("-" * 50)

def promo_existe(cursor, id_promo):
    cursor.execute(
        "SELECT 1 FROM promos WHERE id_promo = %s",
        (id_promo)
    )
    return cursor.fetchone() is not None

def etudiant_existe(cursor, id_etudiant):
    cursor.execute(
        "SELECT 1 FROM etudiants WHERE id_etudiant = %s",
        (id_etudiant,)
    )
    return cursor.fetchone() is not None
def presence_existe(cursor, id_precence):
    cursor.execute(
        "SELECT 1 FROM presences WHERE id_precence = %s",
        (id_precence,)
    )
    return cursor.fetchone() is not None

def ajout_etudiant():
    cursor = connection.cursor()
    
    while True:
            nom = input("Saisir votre nom ").strip()
            if nom.isalpha():
                break
            else:
                print("Nom invalide. Veuillez réessayer.")
    while True:
            prenom = input("Saisir votre prenom ").strip()
            if prenom.isalpha():
                break
            else:
                print("Prenom invalide. Veuillez réessayer.")

    while True:
        try:
            promo = int(input("Saisir le numéro de la promo : "))

            if promo_existe(cursor, promo):
                break
            else:
                print("Cette promo n'existe pas. Réessaie.")

        except ValueError:
            print("Veuillez entrer un nombre valide.")

    ajout_etudiant = """
    INSERT INTO etudiants (nom, prenom, id_promo) VALUES
        (%s,%s,%s);
    """
    cursor.execute(ajout_etudiant, (nom, prenom, promo))
    connection.commit()
def ajout_promo():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id_promo, labelle_promo FROM promos order by id_promo")
    print("\n Promos disponibles :")
    for p in cursor.fetchall():
        print(f"{p['id_promo']} - {p['labelle_promo']}")
    while True:
            promo = input("Saisir le numero de la promo P :").strip()
            if promo.isdigit():
                break
            else:
                print("Promo invalide. Veuillez réessayer.")

    promoP= 'P'+promo
    description = input ('Saisir une description : ')

    ajout_promo = """
    INSERT INTO promos (labelle_promo, description) VALUES
        (%s,%s);
    """
    cursor.execute(ajout_promo, (promoP,description))
    connection.commit()

def ajout_presence(): 
    cursor = connection.cursor(dictionary=True)
    while True:
        try:
            id_etudiant = int(input("Saisir le numéro de l'edtudiant : "))

            if etudiant_existe(cursor, id_etudiant):
                break
            else:
                print("Cette Etudiant n'existe pas. Réessaie.")

        except ValueError:
            print("Veuillez entrer un nombre valide.")
        
    while True:
        try:
                id_precence = int(input("Saisir 1 Abscent et 2 Present : "))

                if presence_existe(cursor, id_precence):
                    break
                else:
                    print("Veuillez choisir un choix valide")

        except ValueError:
                print("Veuillez entrer un nombre valide.")

    ajout_presence = """
    INSERT INTO pointages (id_etudiant, id_precence, date_pointage, heure_arrivee)
    VALUES (%s, %s, CURDATE(), CURTIME())
    """
    try:
        cursor.execute(ajout_presence, (id_etudiant, id_precence))
        connection.commit()
        print("Pointage enregistré")
    except mysql.connector.IntegrityError:
        print("Cet étudiant a déjà pointé aujourd’hui")

def etudiant_present():
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT
    E.id_etudiant 
    E.nom,
    E.prenom,
    P.date_pointage,
    P.heure_arrivee AS heure ,
    lable_presence
FROM pointages P
JOIN etudiants E ON P.id_etudiant = E.id_etudiant
JOIN presences PR ON p.id_precence =PR.id_precence
where PR.id_precence = 2
;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("Aucun étudiant present trouvé.")
        return

    print("\nLISTE DES ÉTUDIANTS PRESENT")
    print("-" * 60)
    print(f"{'Id Etudiant':<15} {'Nom':<15} {'Prénom':<15} {'Statut':<15} {'HEURE ARRIVER ':<15} ")
    print("-" * 60)

    for row in rows:
        heure = str(row['heure'])
        print(f"{row['id_etudiant']:<15} {row['nom']:<15} {row['prenom']:<15} {row['lable_presence']:<15} {heure:<15}")
    print("-" * 60)
    
def rechercher_apprenant():
    cursor = connection.cursor(dictionary=True)

    saisie = input("Entrez l'ID ou le nom/prénom de l'apprenant : ").strip()

    
    if saisie.isdigit():
        query = """
        SELECT 
            E.id_etudiant,
            E.nom,
            E.prenom,
            P.labelle_promo
        FROM etudiants E
        JOIN promos P ON E.id_promo = P.id_promo
        WHERE E.id_etudiant = %s
        """
        cursor.execute(query, (int(saisie),))

    
    else:
        query = """
        SELECT 
            E.id_etudiant,
            E.nom,
            E.prenom,
            P.labelle_promo
        FROM etudiants E
        JOIN promos P ON E.id_promo = P.id_promo
        WHERE E.nom LIKE %s OR E.prenom LIKE %s
        """
        valeur = f"%{saisie}%"
        cursor.execute(query, (valeur, valeur))

    resultats = cursor.fetchall()

    if not resultats:
        print("Aucun apprenant trouvé")
        return

    print("\nRESULTATS DE LA RECHERCHE")
    print("-" * 50)
    print(f"{'ID':<5} {'Nom':<15} {'Prénom':<15} {'Promo':<10}")
    print("-" * 50)

    for row in resultats:
        print(f"{row['id_etudiant']:<5} {row['nom']:<15} {row['prenom']:<15} {row['labelle_promo']:<10}")
    

def menu_etudiant():
    print ('============= MENU ETUDIANT ===============')
    while True :
        print ('')
        print("1. Pour voir la liste de tous les etudiants :")
        print("2. Pour voir la liste des etudiants present :")
        print("3. Pour ajouter des etudiants")
        print('')

        choix=input('Taper un choix : ').replace(" ", "")
        print('')
        if choix =='1' :
           list_etudiant()
        elif choix =='2':
            etudiant_present()
        elif choix =='3':
            ajout_etudiant()
        elif choix =='4':
            rechercher_apprenant()
        elif choix=="9":
            exit()
        elif choix =='0' :
            break
        else:
            print('Choix invalide')
    


def menu_precence():
    print('============= MENU PRESENCE ===============')
    while True:
        print ('')
        print("1. Pour Gerer les etudiants :")
        print("2. Pour voir la liste des presences :")
        print("3. Pour ajouter des etudiants")
        print("4. Pour ajouter des promos")
        print("5. Pour ajouter la precence")
        choix=input('Taper un choix : ').replace(" ", "")
        print(choix)
        if choix =='1' :
           menu_etudiant()
        elif choix =='2':
            print
        elif choix =='3':
            ajout_etudiant()
        elif choix =='4':
           ajout_promo()
        elif choix =='5':
           ajout_presence()
        
        elif choix=="9":
            exit()
        elif choix =='0' :
            break
        else:
            print('Choix invalide')
    

menu_precence()


connection.close()
if not connection.is_connected():
    print("MySQL connection closed.")