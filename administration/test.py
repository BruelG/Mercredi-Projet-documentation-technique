import datetime
import sqlite3
import json

from config import Myuser, myAccount, Mypassword,account_sid,auth_token,api_key_google

from twilio.rest import Client


def send_message(name,num) :
   
    client = Client(account_sid, auth_token)


    message = client.messages.create(
    from_='+12027309345',
    to=num,
    body=f"TECC INNOVATION: Admission :  {name} votre admission a ete acceptee , attendez 5 minutes puis dirigee vous vers le portail http://localhost:8000 le mdp ajoute tecc a la fin  .Merci"
    
    
  
)

    print(message.sid)



# Chemin d'accès à la base de données
DB_PATH1 = 'C:\\Users\\Admin\\source\\repos\\2023\\automne\\documentation\\Mercredi-Projet-documentation-technique\\Projet_admission\\db.sqlite3'
DB_PATH2 = 'C:\\Users\\Admin\\source\\repos\\2023\\automne\\documentation\\Mercredi-Projet-documentation-technique\\Lab_projet_ecole\\helsinki\\db.sqlite3'
JSON_FILE_PATH = 'C:\\Users\\Admin\\source\\repos\\2023\\automne\\documentation\\Mercredi-Projet-documentation-technique\\administration\\user_data.json' 
users_list = []  # Liste pour stocker les données des utilisateurs

try:
    # Connexion à la base de données
    conn = sqlite3.connect(DB_PATH1)
    print("Connecté avec succès à la base de données")
    cursor = conn.cursor()

    conn2 = sqlite3.connect(DB_PATH2)
    print("Connecté avec succès à la base de données numero 2")
    cursor2 =conn2.cursor()

    
                            #databases 1
    # Récupérer l'ID de la dernière personne ajoutée
    cursor.execute("SELECT id FROM Utilisateurs_utilisateurs ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        last_user_id = result[0]

        # Mettre à jour le statut dans demande_admission_demander_admission
        update_status_query = """
        UPDATE demande_admission_demander_admission
        SET statut_demande = 'accepte'
        WHERE demandeur_id = ?
        """
        cursor.execute(update_status_query, (last_user_id,))
        conn.commit()

        # Récupérer les informations de connexion de l'utilisateur
        select_user_query = """
        SELECT code_user, email, password FROM Utilisateurs_utilisateurs WHERE id = ?
        """
        cursor.execute(select_user_query, (last_user_id,))
        user_info = cursor.fetchone()

        if user_info:
            code_user, email, password = user_info
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Vérifier si le code utilisateur existe déjà dans candidants_comptes
            check_user_exists_query = """
            SELECT COUNT(*) FROM candidants_comptes WHERE code_Utilisateur = ?
            """
            cursor.execute(check_user_exists_query, (code_user,))
            user_exists = cursor.fetchone()[0] > 0

            if not user_exists:
                # Insérer dans candidants_comptes si l'utilisateur n'existe pas
                insert_candidant_query = """
                INSERT INTO candidants_comptes (code_Utilisateur, Password, Email, Actifs, DateCreation) 
                VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(insert_candidant_query, (code_user, password, email, 1, current_date))
                conn.commit()
                print("Nouvel utilisateur inséré dans candidants_comptes.")
            else:
                print("L'utilisateur avec ce code existe déjà dans candidants_comptes.")

            # Récupérer les informations personnelles de l'utilisateur
            info_query = """
            SELECT nom, prenom,adresse,telephone FROM demande_admission_information_personnelle  ORDER BY id DESC LIMIT 1
            """
            cursor.execute(info_query,)
            personal_info = cursor.fetchone()

            login_query = """
            SELECT code_user, password,email FROM Utilisateurs_utilisateurs WHERE id = ?
            """
            cursor.execute(login_query, (last_user_id,))
            login_info = cursor.fetchone()


            if personal_info and login_info:
                data_to_save = {
                    "id": last_user_id,
                    "nom": personal_info[0],
                    "prenom": personal_info[1],
                    "email": email,
                    "adresse": personal_info[2],
                    "telephone":personal_info[3],
                    "code_user": code_user,
                    "mdp": password
                }

                # Ajout des données à la liste des utilisateurs
                users_list.append(data_to_save)
                if users_list:
                    with open('user_data.json', 'w') as file:
                        json.dump(users_list, file)
                    print("Les données ont été enregistrées dans 'user_data.json'.")
                else:
                    print("Aucune donnée à enregistrer.")

    else:
        print("Aucun utilisateur récent trouvé.")

    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables dans la première base de données:")
    for table in cursor2.fetchall():
        print(table[0])


    with open(JSON_FILE_PATH, 'r') as file:
        users_data = json.load(file)

    # Utiliser le premier utilisateur pour la vérification et l'insertion
    user_data = users_data[0]

    # Vérifier si le pseudo existe déjà dans la deuxième base de données
    pseudo_check_query = "SELECT COUNT(*) FROM utilisateur_utilisateur WHERE pseudo = ?"
    cursor2.execute(pseudo_check_query, (user_data['code_user'],))
    exists = cursor2.fetchone()[0] > 0

    if not exists:
        # Insérer le nouvel utilisateur si le pseudo n'existe pas
        insert_user_query = """
        INSERT INTO utilisateur_utilisateur (nom, prenom, pseudo, adresse, email, mdp, last_login,cycle_id,programme_id,session_id)
        VALUES (?, ?, ?, ?, ?,?,?,?,?,?)
        """
        cursor2.execute(insert_user_query, (
            user_data['nom'],
            user_data['prenom'],
            user_data['code_user'],
            user_data['adresse'],
            user_data['email'],         
            user_data['mdp'],
            current_date,
            1,
            1,
            1
        ))
        conn2.commit()
        print("Nouvel utilisateur inséré dans la deuxième base de données.")
    else:
        print("L'utilisateur avec ce pseudo existe déjà dans la deuxième base de données.")
    

    #creation session
    id = 10
    pseudo = user_data['code_user']

    # Vérifier si l'ID existe déjà
    id_exists_query = "SELECT COUNT(*) FROM utilisateur_utilisateursession WHERE id_session = ?"
    while True:
        cursor2.execute(id_exists_query, (id,))
        if cursor2.fetchone()[0] > 0:
            id += 2  # Incrémenter l'ID de 2 si existant
        else:
            break

    # Vérifier si le pseudo existe déjà
    pseudo_exists_query = "SELECT COUNT(*) FROM utilisateur_utilisateursession WHERE user_id = ?"
    cursor2.execute(pseudo_exists_query, (pseudo,))
    if cursor2.fetchone()[0] > 0:
        print("Le pseudo existe déjà, l'utilisateur ne sera pas inséré.")
        send_message(user_data['nom'],user_data['telephone'])
    else:
        # Insérer les données dans la table
        insert_query = """
        INSERT INTO utilisateur_utilisateursession (id_session, last_login,user_id)
        VALUES (?, ?, ?)
        """
        # Ajouter d'autres valeurs requises dans la requête ci-dessus
        cursor2.execute(insert_query, (id, current_date, pseudo))  # Remplacer ... par d'autres valeurs
        conn2.commit()
        print("Nouvel utilisateur inséré avec user_ID:", pseudo)
        send_message(user_data['nom'],user_data['telephone'])

    

   

except Exception as e:
    print("Une erreur s'est produite:", e)
        

        
    

finally:
    # Fermer la connexion et le curseur
    if conn:
        conn.close()




