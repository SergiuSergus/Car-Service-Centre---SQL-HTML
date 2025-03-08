from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
import random
 
app = Flask(__name__)
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Andrei1234!'
app.config['MYSQL_DB'] = 'proiect_service'

 
 
mysql = MySQL(app)

#if mysql.connection is None:
#    print("MySQL connection object is None")
#
#print(mysql)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Masini")
    masini_data = cur.fetchall()
    cur.execute("SELECT * FROM Clienti")
    clienti_data = cur.fetchall()
    cur.execute("SELECT * FROM Programari")
    programari_data = cur.fetchall()
    cur.execute("SELECT * FROM Piese")
    piese_data = cur.fetchall()
    cur.close()
    return render_template('index.html', masini=masini_data, clienti=clienti_data, programari=programari_data, piese=piese_data)



@app.route('/add_masina', methods=['POST'])
def add_masina():
    if request.method == 'POST':
        id = request.form['id']
        marca = request.form['marca']
        model = request.form['model']
        an_fabricatie = request.form['an_fabricatie']
        numar_inmatriculare = request.form['numar_inmatriculare']
        id_client = request.form['id_client']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Masini (ID_Masina, Marca, Model, An_de_fabricatie, Numar_de_inmatriculare, ID_Client) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, marca, model, an_fabricatie, numar_inmatriculare, id_client))
        
        
        data_programarii = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        v_descriere = ["schimb filtru ulei", "schimb piston Diesel","schimb piston benzina", "inlocuire bujii", "inlocuire stergatoare", "schimb bec far", "inlocuire frane"]
        
        descriere_serviciu = random.choice(v_descriere)
        cur.execute("INSERT INTO Programari (Data_programari, Descriere_serviciu, ID_Masina) VALUES (%s, %s, %s)",
                    (data_programarii, descriere_serviciu, id))
        
        id_programare = cur.lastrowid
        piesa_data = update_stoc(descriere_serviciu)
        add_factura(id_programare, piesa_data[0], piesa_data[1])
        mysql.connection.commit()
        cur.close()
        
        
        return redirect(url_for('index'))

@app.route('/delete_masina/<string:id>', methods=['POST'])
def delete_masina(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Masini WHERE ID_Masina = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))



@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        id = request.form['id']
        nume = request.form['nume']
        prenume = request.form['prenume']
        adresa = request.form['adresa']
        telefon = request.form['telefon']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Clienti (ID_Client, Nume, Prenume, Adresa, Numar_de_telefon, Email) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, nume, prenume, adresa, telefon, email))
        mysql.connection.commit()
        # id_programare = cur.lastrowid
        # piesa_data = update_stoc(descriere_serviciu)
        # add_factura(id_programare, piesa_data[0], piesa_data[1])
        cur.close()
        return redirect(url_for('index'))
    
def add_factura(id_programare, id_piesa, suma_totala):
    detalii_plata = random.choice(["cash", "card"])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Facturi (Suma_totala, Data_emiterii, Detalii_plata, ID_Programare, ID_Piesa) VALUES (%s, %s, %s, %s, %s)",
                (suma_totala, datetime.now(), detalii_plata, id_programare, id_piesa))
    mysql.connection.commit()
    cur.close()    

@app.route('/delete_client/<string:id>', methods=['POST'])
def delete_client(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Clienti WHERE ID_Client = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/delete_programare/<string:id>', methods=['POST'])
def delete_programare(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Programari WHERE ID_Programare = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/delete_factura/<int:id>', methods=['POST'])
def delete_factura(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Facturi WHERE ID_Factura = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/update_masina', methods=['POST'])
def update_masina():
    if request.method == 'POST':
        id = request.form['id']
        column = request.form['column']
        value = request.form['value']
        cur = mysql.connection.cursor()
        query = f"UPDATE Masini SET {column} = %s WHERE ID_Masina = %s"
        cur.execute(query, (value, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    
@app.route('/update_client', methods=['POST'])
def update_client():
    if request.method == 'POST':
        id = request.form['id']
        column = request.form['column']
        value = request.form['value']
        cur = mysql.connection.cursor()
        query = f"UPDATE Clienti SET {column} = %s WHERE ID_Client = %s"
        cur.execute(query, (value, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))    


def update_stoc(descriere_serviciu):
    cur = mysql.connection.cursor()
    if descriere_serviciu == "schimb filtru ulei":
        cur.execute("UPDATE Piese SET Cantitate_stoc = Cantitate_stoc - 1 WHERE Nume = 'filtru ulei'")
        cur.execute("SELECT ID_Piesa, Pret FROM Piese WHERE Nume = 'filtru ulei'")
    elif descriere_serviciu == "inlocuire frane":
        cur.execute("UPDATE Piese SET Cantitate_stoc = Cantitate_stoc - 1 WHERE Nume = 'placute frana'")
        cur.execute("SELECT ID_Piesa, Pret FROM Piese WHERE Nume = 'placute frana'")
    elif descriere_serviciu == "schimb piston Diesel":
        cur.execute("UPDATE Piese SET Cantitate_stoc = Cantitate_stoc - 1 WHERE Nume = 'piston Diesel'")
        cur.execute("SELECT ID_Piesa, Pret FROM Piese WHERE Nume = 'piston Diesel'")
    elif descriere_serviciu == "schimb piston benzina":
        cur.execute("UPDATE Piese SET Cantitate_stoc = Cantitate_stoc - 1 WHERE Nume = 'piston benzina'")
        cur.execute("SELECT ID_Piesa, Pret FROM Piese WHERE Nume = 'piston benzina'")
    elif descriere_serviciu == "schimb bujie":
        cur.execute("UPDATE Piese SET Cantitate_stoc = Cantitate_stoc - 1 WHERE Nume = 'bujie'")
        cur.execute("SELECT ID_Piesa, Pret FROM Piese WHERE Nume = 'bujie'")
    elif descriere_serviciu == "schimb bec far halogen":
        cur.execute("UPDATE Piese SET Cantitate_stoc = Cantitate_stoc - 1 WHERE Nume = 'bec far halogen'")
        cur.execute("SELECT ID_Piesa, Pret FROM Piese WHERE Nume = 'bec far halogen'")
    
    piesa_data = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    
    
    return piesa_data  

@app.route('/reset_piese', methods=['POST'])
def reset_piese():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Piese SET Cantitate_stoc = 99")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/clienti_alfabetic')
def clienti_alfabetic():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clienti ORDER BY Nume ASC")
        clienti_data = cur.fetchall()
        cur.close()
        return render_template('clienti.html', clienti=clienti_data)

@app.route('/piese_ieftine')
def piese_ieftine():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Piese WHERE Pret < 500")
        piese_data = cur.fetchall()
        cur.close()
        return render_template('piese.html', piese=piese_data)

@app.route('/facturi_scumpe')
def facturi_scumpe():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Facturi ORDER BY Suma_totala DESC LIMIT 3")
        facturi_data = cur.fetchall()
        cur.close()
        return render_template('facturi.html', facturi=facturi_data)

@app.route('/programari_inlocuire_bujii')
def programari_inlocuire_bujii():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Programari WHERE Descriere_serviciu = 'inlocuire bujii'")
    programari_data = cur.fetchall()
    cur.close()
    return render_template('programari.html', programari=programari_data)

@app.route('/mecanici_platiti_bine')
def mecanici_platiti_bine():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Mecanici ORDER BY Salariu DESC LIMIT 2")
    mecanici_data = cur.fetchall()
    cur.close()
    return render_template('mecanici.html', mecanici=mecanici_data)

@app.route('/client_masini')
def client_masini():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT Masini.Marca, Masini.Model
        FROM Masini
        INNER JOIN Clienti ON Masini.ID_Client = Clienti.ID_Client
        WHERE Clienti.Nume = 'Condurache'
    """)
    masini_data = cur.fetchall()
    cur.close()
    return render_template('client_masini.html', masini=masini_data)

@app.route('/programari_masini_renault_opel')
def programari_masini_renault_opel():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT Masini.Marca, Masini.Model, Programari.Data_programari
        FROM Programari
        INNER JOIN Masini ON Programari.ID_Masina = Masini.ID_Masina
        WHERE Masini.Marca = 'Renault' OR Masini.Marca = 'Opel'
    """)
    programari_data = cur.fetchall()
    cur.close()
    return render_template('programari_masini_renault_opel.html', programari=programari_data)

    
if __name__ == '__main__':
    app.run(debug=True)