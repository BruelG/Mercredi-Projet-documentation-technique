import sqlite3

# Chemins des fichiers de base de données SQLite
db_path2 = 'C:\\Users\\Admin\\source\\repos\\2023\\automne\\documentation\\Mercredi-Projet-documentation-technique\\Lab_projet_ecole\\helsinki\\db.sqlite3'
db_path1 = 'C:\\Users\\Admin\\source\\repos\\2023\\automne\python\\Projet_admission\\db.sqlite3'





try:
    # Connexion à la première base de données
    conn1 = sqlite3.connect(db_path1)
    print("Connecté avec succès à la première base de données")
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables dans la première base de données:")
    for table in cursor1.fetchall():
        print(table[0])

    # Connexion à la seconde base de données
    conn2 = sqlite3.connect(db_path2)
    print("Connecté avec succès à la seconde base de données")
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables dans la seconde base de données:")
    for table in cursor2.fetchall():
        print(table[0])

    # Vos opérations sur les bases de données ici
    # ...

except sqlite3.Error as e:
    print(f"Une erreur s'est produite lors de la connexion à la base de données: {e}")
finally:
    # Assurez-vous que les curseurs et les connexions sont fermés proprement
    if 'cursor1' in locals():
        cursor1.close()
    if 'conn1' in locals():
        conn1.close()
    if 'cursor2' in locals():
        cursor2.close()
    if 'conn2' in locals():
        conn2.close()
    print("Connexions fermées")
