import mysql.connector

# Dati di connessione
conn = mysql.connector.connect(
    host='localhost',        # Il server del database
    user='root',             # Nome utente (usualmente 'root')
    password='',     # La tua password
    database='database_prenotazioni'  # Il nome del database
)
python db_connect.py

if conn.is_connected():
    print("Connesso al database!")
else:
    print("Errore nella connessione al database.")

# Esegui una query di test
cursor = conn.cursor()
cursor.execute("SELECT * FROM prenotazioni")  # Sostituisci con la tua tabella
results = cursor.fetchall()

for row in results:
    print(row)

# Chiudi la connessione
cursor.close()
conn.close()
