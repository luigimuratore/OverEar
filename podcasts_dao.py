import sqlite3

def get_podcasts():
    conn = sqlite3.connect('database/podcasts.db') #apro la connessione
    conn.row_factory = sqlite3.Row  #ci restituisce la riga al posto della tupla -> stiamo 'dizionarizzando'
    cursor = conn.cursor() #definisco il cursore
    
    sql = 'SELECT * FROM podcast ORDER BY data DESC' #definisco la query e ordino i dati selezionati in ordine di data decrescente
    cursor.execute(sql) #eseguo la query

    podcasts = cursor.fetchall() #prendo tutti i dati

    cursor.close() #chiudo cursore e connessione
    conn.close()

    return podcasts

def get_series():
    conn = sqlite3.connect('database/podcasts.db') #apro la connessione
    conn.row_factory = sqlite3.Row  #ci restituisce la riga al posto della tupla -> stiamo 'dizionarizzando'
    cursor = conn.cursor() #definisco il cursore
    
    sql = 'SELECT * FROM serie ORDER BY titolo ASC' #definisco la query e ordino i dati selezionati in ordine di data decrescente
    cursor.execute(sql) #eseguo la query

    series = cursor.fetchall() #prendo tutti i dati

    cursor.close() #chiudo cursore e connessione
    conn.close()

    return series


def get_episodio(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast WHERE id = ?'
    cursor.execute(sql, (id,)) #id, perchè è una tupla quindi è un singolo valore ma ha bisogna della virgola

    episodio = cursor.fetchone() #one perchè ci aspettiamo al massimo un valore
    
    cursor.close()
    conn.close()

    return episodio

def trova_rif(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE id = ?'
    cursor.execute(sql, (id,)) #id, perchè è una tupla quindi è un singolo valore ma ha bisogna della virgola

    rif = cursor.fetchone() #one perchè ci aspettiamo al massimo un valore
    
    cursor.close()
    conn.close()

    return rif

def trova_rif_pod(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast WHERE id = ?'
    cursor.execute(sql, (id,)) #id, perchè è una tupla quindi è un singolo valore ma ha bisogna della virgola

    rif_pod = cursor.fetchone() #one perchè ci aspettiamo al massimo un valore
    
    cursor.close()
    conn.close()

    return rif_pod

def trova_pod(id_podcast):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast WHERE id = ?'
    cursor.execute(sql, (id,)) #id, perchè è una tupla quindi è un singolo valore ma ha bisogna della virgola

    pod = cursor.fetchone() #one perchè ci aspettiamo al massimo un valore
    
    cursor.close()
    conn.close()

    return pod


def trova_autori():
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti ORDER BY nome ASC'
    cursor.execute(sql)

    autori = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return autori

def trova_podcast():
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast ORDER BY data DESC'
    cursor.execute(sql) 

    podcast_trovati = cursor.fetchall() 
    
    cursor.close()
    conn.close()

    return podcast_trovati


def pod_in_db(titolo):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast WHERE titolo = ?'
    cursor.execute(sql, (titolo,)) #id, perchè è una tupla quindi è un singolo valore ma ha bisogna della virgola

    pod_in_db = cursor.fetchone() #one perchè ci aspettiamo al massimo un valore
    
    cursor.close()
    conn.close()

    return pod_in_db

def ser_in_db(titolo):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE titolo = ?'
    cursor.execute(sql, (titolo,)) #id, perchè è una tupla quindi è un singolo valore ma ha bisogna della virgola

    ser_in_db = cursor.fetchone() #one perchè ci aspettiamo al massimo un valore
    
    cursor.close()
    conn.close()

    return ser_in_db

def ser_in_db_completa(serie_titolo_nome):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE titolo = ?'
    cursor.execute(sql, (serie_titolo_nome,))

    ser_in_db = cursor.fetchone() #one perchè ci aspettiamo al massimo un valore
    
    cursor.close()
    conn.close()

    return ser_in_db

def aggiungi_commento(nuovo_commento):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()   

    success = False

    sql = 'INSERT INTO commenti (contenuto, autore, podcast_id) VALUES (?,?,?)'
    
    try:
        cursor.execute(sql, (nuovo_commento['contenuto'], nuovo_commento['autore'], nuovo_commento['podcast_id']))
        conn.commit() #commit per completare e salvare l'inserimento
        success = True
    
    except Exception as e:
        print('ERROR', str(e)) #se qualcosa va storto durante la creazione
        conn.rollback()
    

    cursor.close()
    conn.close()

    return success


def add_podcast(podcast):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'INSERT INTO podcast (titolo, descrizione, data, audio, autore, serie_titolo ) VALUES (?,?,?,?,?,?)'
    
    try:
        cursor.execute(sql, (podcast['titolo'], podcast['descrizione'], podcast['data'], podcast['audio'], podcast['autore'],podcast['serie_titolo']))
        conn.commit() #commit per completare e salvare l'inserimento
        success = True
    
    except Exception as e:
        print('ERROR', str(e)) #se qualcosa va storto durante la creazione
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success

def add_serie(serie):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'INSERT INTO serie (titolo, descrizione, categoria, data, immagine, autore ) VALUES (?,?,?,?,?,?)'
    
    try:
        cursor.execute(sql, (serie['titolo'], serie['descrizione'], serie['categoria'], serie['data'], serie['immagine'], serie['autore']))
        conn.commit() #commit per completare e salvare l'inserimento
        success = True
    
    except Exception as e:
        print('ERROR', str(e)) #se qualcosa va storto durante la creazione
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success

def trova_titoli_serie():
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie ORDER BY titolo ASC'
    cursor.execute(sql)

    serie_trovate = cursor.fetchall()

    cursor.close()
    conn.close()

    return serie_trovate

def trova_serie(tit_id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE id = ?'
    cursor.execute(sql, (tit_id,))

    serie_cercata = cursor.fetchone()

    cursor.close()
    conn.close()

    return serie_cercata


def get_commenti():
    conn = sqlite3.connect('database/podcasts.db') 
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor() 
    
    sql = 'SELECT * FROM commenti ORDER BY id DESC' 
    cursor.execute(sql) 

    commenti = cursor.fetchall() 

    cursor.close()
    conn.close()

    return commenti

def get_commento(id):
    conn = sqlite3.connect('database/podcasts.db') 
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor() 
    
    sql = 'SELECT * FROM commenti WHERE id = ?' 
    cursor.execute(sql, (id, )) 

    commento = cursor.fetchone() 

    cursor.close()
    conn.close()

    return commento



def get_utente_by_email(email):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE email = ?'
    cursor.execute(sql, (email,))
    
    utente = cursor.fetchone()

    cursor.close()
    conn.close()

    return utente

def aggiungi_utente(nuovo_utente):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO utenti(nome, cognome, email, password, foto, data, codice) VALUES (?,?,?,?,?,?,?)'

    try:
        cursor.execute(sql, (nuovo_utente['nome'], nuovo_utente['cognome'], nuovo_utente['email'], nuovo_utente['password'], nuovo_utente['foto'], nuovo_utente['data'], nuovo_utente['codice']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE', str(e))
        conn.rollback()


    cursor.close()
    conn.close()

    return success

def get_utente_by_id(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE id = ?'
    cursor.execute(sql, (id, ))
    
    utente = cursor.fetchone()

    cursor.close()
    conn.close()

    return utente

def trova_pod(titolo):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast WHERE titolo = ?'
    cursor.execute(sql, (titolo, ))
    
    pod = cursor.fetchone()

    cursor.close()
    conn.close()

    return pod


def trova_ser(titolo):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE titolo = ?'
    cursor.execute(sql, (titolo, ))
    
    ser = cursor.fetchone()

    cursor.close()
    conn.close()

    return ser

def serie_seguite(user):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE autore = ?'
    cursor.execute(sql, (user, ))
    
    serie_seguite = cursor.fetchall()

    cursor.close()
    conn.close()

    return serie_seguite

def modifica_podcast(nuovo_id, podcast_mod):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'DELETE FROM podcast WHERE id = ?'
    
    try:
        cursor.execute(sql, (nuovo_id, ))
        conn.commit()
        success = True
    except Exception as e :
        print('ERRORE', str(e))
        conn.rollback()
    
    if success:
        success_mod=False

        sql = 'INSERT INTO podcast(id, titolo, descrizione, data, audio, autore, serie_titolo) VALUES (?,?,?,?,?,?,?)'

        try:
            cursor.execute(sql, (podcast_mod['id'], podcast_mod['titolo'], podcast_mod['descrizione'], podcast_mod['data'], podcast_mod['audio'], podcast_mod['autore'],podcast_mod['serie_titolo'],))
            conn.commit()
            success_mod=True
        except Exception as e:
            print('ERRORE', str(e))
            conn.rollback()

    cursor.close()
    conn.close()

    return success_mod

def modifica_serie(nuovo_id, serie_mod):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'DELETE FROM serie WHERE id = ?'
    
    try:
        cursor.execute(sql, (nuovo_id, ))
        conn.commit()
        success = True
    except Exception as e :
        print('ERRORE', str(e))
        conn.rollback()
    
    if success == True:
        success_mod=False

        sql = 'INSERT INTO serie(id, titolo, descrizione, categoria, data, immagine, autore) VALUES (?,?,?,?,?,?,?)'

        try:
            cursor.execute(sql, (serie_mod['id'], serie_mod['titolo'], serie_mod['descrizione'], serie_mod['categoria'], serie_mod['data'], serie_mod['immagine'], serie_mod['autore'],))
            conn.commit()
            success_mod=True
        except Exception as e:
            print('ERRORE', str(e))
            conn.rollback()

    cursor.close()
    conn.close()

    return success_mod

def get_commenti_by_id(id_pod):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM commenti WHERE podcast_id = ?'
    cursor.execute(sql, (id_pod, ))
    
    commento_trovato = cursor.fetchall()

    cursor.close()
    conn.close()

    return commento_trovato

def get_commenti_by_idd(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM commenti WHERE id = ?'
    cursor.execute(sql, (id, ))
    
    commento_trovato = cursor.fetchone()

    cursor.close()
    conn.close()

    return commento_trovato


def modifica_commento(nuovo_id, commento_mod):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    success_mod = False

    sql = 'DELETE FROM commenti WHERE id = ?'
    
    try:
        cursor.execute(sql, (nuovo_id, ))
        conn.commit()
        success = True
    except Exception as e :
        print('ERRORE', str(e))
        conn.rollback()
    
    if success:

        sql = 'INSERT INTO commenti(id, contenuto, autore, podcast_id) VALUES (?,?,?,?)'

        try:
            cursor.execute(sql, (commento_mod['id'], commento_mod['contenuto'], commento_mod['autore'], commento_mod['podcast_id'],))
            conn.commit()
            success_mod=True
        except Exception as e:
            print('ERRORE', str(e))
            conn.rollback()

    cursor.close()
    conn.close()

    return success_mod

def elimina_commento(id_comm):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'DELETE FROM commenti WHERE id = ?'
    
    try:
        cursor.execute(sql, (id_comm, ))
        conn.commit()
        success = True
    except Exception as e :
        print('ERRORE', str(e))

    cursor.close()
    conn.close()

    return success

def get_podcast_by_id(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast WHERE id = ?'
    cursor.execute(sql, (id, ))
    
    podcast = cursor.fetchone()

    cursor.close()
    conn.close()

    return podcast

def elimina_podcast_e_comm(id_pod, commenti_trovati):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    for comment in commenti_trovati:
        id_comm = comment['id']

        sql = 'DELETE FROM commenti WHERE id = ?'

        try:
            cursor.execute(sql, (id_comm, ))
            conn.commit()
        except Exception as e :
            print('ERRORE', str(e))


    sql = 'DELETE FROM podcast WHERE id = ?'
    
    try:
        cursor.execute(sql, (id_pod, ))
        conn.commit()
        success = True
    except Exception as e :
        print('ERRORE', str(e))

    cursor.close()
    conn.close()

    return success

def elimina_commento_by_idpod(id_commenti_trovati):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'DELETE FROM commenti WHERE id = ?'
    
    try:
        cursor.execute(sql, (id_commenti_trovati, ))
        conn.commit()
        success = True
    except Exception as e :
        print('ERRORE', str(e))

    cursor.close()
    conn.close()

    return success

def trova_serie_by_id(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE id = ?'
    cursor.execute(sql, (id,))

    serie_cercata = cursor.fetchone()

    cursor.close()
    conn.close()

    return serie_cercata

def trova_serie_gia_seguita(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM seguite WHERE id = ?'
    cursor.execute(sql, (id, ))
    
    serie_gia_seguita = cursor.fetchall()

    cursor.close()
    conn.close()

    return serie_gia_seguita


def aggiungi_serie_seguita(nuova_serie_seguita):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO seguite(id, titolo, utente) VALUES (?,?,?)'

    try:
        cursor.execute(sql, (nuova_serie_seguita['id'], nuova_serie_seguita['titolo'], nuova_serie_seguita['utente'],))
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE', str(e))
        conn.rollback()


    cursor.close()
    conn.close()

    return success

def trova_serie_seguite():
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM seguite'
    cursor.execute(sql,)
    
    serie_seguite = cursor.fetchall()

    cursor.close()
    conn.close()

    return serie_seguite

def trova_preferito_by_id(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM seguite WHERE id = ?'
    cursor.execute(sql, (id,))
    
    preferito = cursor.fetchall()

    cursor.close()
    conn.close()

    return preferito

def elimina_preferito(id, utente):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success_canc = False

    sql = 'SELECT * FROM seguite WHERE id = ?'
    
    try:
        cursor.execute(sql, (id, ))
        unfollow = cursor.fetchall()
        success_canc = True
    except Exception as e :
        print('ERRORE', str(e))

    if success_canc:
        success = False

        for u in unfollow:
            if u['utente'] == utente:
                
                sql = 'DELETE FROM seguite WHERE (utente, id) = (?,?)'
    
                try:
                    cursor.execute(sql, (utente, id,))
                    conn.commit()
                    success = True
                except Exception as e :
                    print('ERRORE', str(e))


    cursor.close()
    conn.close()

    return success

def trova_serie_categoria(k):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie WHERE categoria = ?'
    cursor.execute(sql, (k,))
    
    series = cursor.fetchall()

    cursor.close()
    conn.close()

    return series

def trova_id_podcast(id):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcast WHERE serie_titolo = ?'
    cursor.execute(sql, (id,))
    
    pod = cursor.fetchall()

    cursor.close()
    conn.close()

    return pod

def trova_commenti(i):
    conn = sqlite3.connect('database/podcasts.db') 
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor() 
    
    sql = 'SELECT * FROM commenti WHERE podcast_id = ?' 
    cursor.execute(sql, (i, )) 

    commento = cursor.fetchall() 

    cursor.close()
    conn.close()

    return commento

def elimina_serie(id_ser, indici_comm_da_canc, indici_pods_da_canc):
    conn = sqlite3.connect('database/podcasts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    for i in indici_comm_da_canc:
        sql = 'DELETE FROM commenti WHERE id = ?'

        try:
            cursor.execute(sql, (i ))
            conn.commit()
        except Exception as e :
            print('ERRORE', str(e))

    for j in indici_pods_da_canc:
        sql = 'DELETE FROM podcast WHERE id = ?'

        try:
            cursor.execute(sql, (j, ))
            conn.commit()
        except Exception as e :
            print('ERRORE', str(e))



    sql = 'DELETE FROM serie WHERE id = ?'

    try:
        cursor.execute(sql, (id_ser, ))
        conn.commit()
        success = True
    except Exception as e :
        print('ERRORE', str(e))


    cursor.close()
    conn.close()

    return success