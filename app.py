from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_bootstrap import Bootstrap5
from datetime import date
from flask_session import Session
import sqlite3
import podcasts_dao
from models import Utente
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) 
app.secret_key = 'IAW segreta'
app.config['SECRET_KEY'] = "IAW segreta"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Accedi per visualizzare questa pagina'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

@app.errorhandler(404) #controllo delle pagine non esistenti
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/') #home
def home():
    series = podcasts_dao.get_series()
    podcasts = podcasts_dao.get_podcasts()
    serie_trovate = podcasts_dao.get_series()
    podcast_trovati = podcasts_dao.trova_podcast()
    return render_template ("home.html", series=series, podcasts=podcasts,  serie_trovate = serie_trovate, podcast_trovati=podcast_trovati)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/where')
def where():
    return render_template("where.html")

@app.route('/story')
def story():
    return render_template("story.html")

@app.route('/singolo<int:id>', methods=['GET', 'POST']) #pagina dei podcast singoli dinamica con l'id
def singolo(id):
    utenti = podcasts_dao.trova_autori()  #mi trovo gli episodi e i titoli delle serie per stamparli alla pagina del singolo
    serie_trovate = podcasts_dao.get_series()
    podcast_trovati = podcasts_dao.trova_podcast()
    episodio= podcasts_dao.get_episodio(id)
    commenti = podcasts_dao.get_commenti()
    
    tit_id = episodio['serie_titolo'] #trovo l'id del podcast associato a quel commento
    serie = podcasts_dao.trova_serie(tit_id) 

    if request.method == 'POST':
        contenuto = request.form.get('commento') #richiedo un nuovo commento
        autore = current_user.nome
        podcast_id = episodio['id']

        nuovo_commento = {'contenuto':contenuto, 'autore':autore, 'podcast_id':podcast_id} #creo il nuovo commento

        if contenuto != ' ' and contenuto != '':
            success = podcasts_dao.aggiungi_commento(nuovo_commento) #lo passo al dao per aggiungerlo al db

            if success:
                flash('Commento pubblicato correttamente', 'success')
                return redirect(url_for('singolo', id = episodio['id']))
            else:
                flash('Errore nella pubblicazione del commento', 'danger')
                return redirect(url_for('singolo', id=episodio['id']))
    
    return render_template("singolo.html",  utenti=utenti, id=id, episodio=episodio, commenti=commenti, serie=serie, podcast_trovati=podcast_trovati, serie_trovate=serie_trovate)


@app.route('/generi')
def generi():
    return render_template("generi.html")

@app.route('/serie') #pagina delle serie (tutte)
def serie():
    serie_trovate = podcasts_dao.get_series()
    podcast_trovati = podcasts_dao.trova_podcast()
    return render_template("serie.html", podcast_trovati=podcast_trovati, serie_trovate=serie_trovate)

@app.route('/serie<int:id>') #pagina delle serie singole dinamica con id
def serie_singola(id):
    serie_trovate = podcasts_dao.get_series()
    podcast_trovati = podcasts_dao.trova_podcast()
    rif = podcasts_dao.trova_rif(id)

    return render_template("serie_singola.html", serie_trovate = serie_trovate, podcast_trovati=podcast_trovati, rif=rif)

@app.route('/categoria<k>') #pagina della categoria dinamica con k=categoria (es. k= storia -> categoriastoria)
def categoria(k):
    serie = podcasts_dao.trova_serie_categoria(k)
    podcast_trovati = podcasts_dao.trova_podcast()
    serie_trovate = podcasts_dao.get_series()

    return render_template('categoria.html', serie_trovate=serie_trovate, podcast_trovati=podcast_trovati, serie=serie)


@app.route('/autori')
def autori():
    autori = podcasts_dao.trova_autori()
    return render_template("autori.html", autori=autori)

    
@app.route('/registrazione', methods=['POST', 'GET']) #form di registrazione
def registrazione():
    if request.method == 'POST':

        nome = request.form.get('nome') #richiedo tutti i campi
        cognome = request.form.get('cognome')
        email = request.form.get('email')
        password = request.form.get('password')
        foto = request.files['foto']
        codice = request.form.get('codice')

        data = date.today() #prendo la data attuale

        utente_in_db = podcasts_dao.get_utente_by_email(email) #controllo che la mail inserita non sia già presente nel db

        if utente_in_db:
            flash("Questa email è già stata utilizzata", 'danger')
            return redirect(url_for('registrazione'))
        else:
            if foto: #controllo che ci sia la foto altrimenti ne assegno una io
                foto.save('static/' + nome + cognome + '.jpeg')
                foto_nome = nome + cognome
            else:
                foto_nome = ' '

            #creo il nuovo utente
            nuovo_utente = {'nome': nome, 'cognome': cognome, 'email': email, 'password': generate_password_hash(password, method='sha256'), 'foto': foto_nome, 'data': data, 'codice': codice}
            
        #aggiungo il nuovo utente al db tramite il dao
        success = podcasts_dao.aggiungi_utente(nuovo_utente)
        if success:
            flash('Congratulazioni, adesso fai parte del nostro team!!', 'success')
            return redirect(url_for('home'))
        else:
            flash("OPS c'è stato un problema nella creazione dell'utente", 'danger')
            return redirect(url_for('home'))
    else:
        return render_template("registrazione.html")


@app.route('/login', methods=['POST', 'GET'] ) #form di login
def login():
    if request.method == 'POST':

        email = request.form.get('email')  #richiedo i campi
        password = request.form.get('password')

        utente_in_db = podcasts_dao.get_utente_by_email(email) #cerco nel db la mail inserita
 
        if not utente_in_db or not  check_password_hash(utente_in_db['password'], password): #controllo che la mail inserita esista nel db e che la password corrisponda a quel account
            flash('Credenziali non valide', 'danger')
            return redirect(url_for('login'))
        else:
            #creo il modello utente già impostato in models 
            utente = Utente(id=utente_in_db['id'], nome=utente_in_db['nome'], cognome=utente_in_db['cognome'], email=utente_in_db['email'], password=utente_in_db['password'], foto=utente_in_db['foto'], data=utente_in_db['data'], codice=utente_in_db['codice'])
            login_user(utente) #eseguo il login

            flash('Welcome', 'success')
            return redirect(url_for('home'))

    else:
        return render_template("login.html")
 
@login_manager.user_loader  #'carico l'utente in memoria' 
def load_user(utente_id):
    utente_in_db = podcasts_dao.get_utente_by_id(utente_id)

    utente = Utente(id=utente_in_db['id'], nome=utente_in_db['nome'], cognome=utente_in_db['cognome'], email=utente_in_db['email'], password=utente_in_db['password'], foto=utente_in_db['foto'], data=utente_in_db['data'], codice=utente_in_db['codice'])

    return utente

@app.route('/profilo', methods=['POST', 'GET'])
@login_required
def profilo():
    user = current_user.nome
    serie_seguite = podcasts_dao.trova_serie_seguite() #pagina di login dove stampo le informazioni e le serie seguite

    return render_template("profilo.html", user=user, serie_seguite=serie_seguite)

@app.route('/logout')  #funzione di logout dove 'elimino i dati nei coockie relativi all'utente connesso'
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/inserimento_podcast', methods=["POST", "GET"]) #form di inseriemnto podcast
@login_required
def inserimento_podcast():
    titoli_serie = podcasts_dao.trova_titoli_serie()

    if request.method == "POST":
        #app.logger.debug(request.form['Titolo'])
        
        titolo = request.form.get('titolo')   #richiedo tutti i campi
        descrizione =  request.form.get('descrizione')
        data =  request.form.get('data')
        audio_pod = request.files['audio']
        serie_titolo_nome_ç = request.form.get('serie_titolo')
        serie_titolo_nome = serie_titolo_nome_ç.replace("ç", " ")
        serie_titolo_completa = podcasts_dao.ser_in_db_completa(serie_titolo_nome)

        serie_titolo = serie_titolo_completa['id']

        autore =  current_user.nome

        
        pod_in_db = podcasts_dao.pod_in_db(titolo) #cerco nel db se il titolo è gia stato usato in un altro podcast
        ser_in_db = podcasts_dao.ser_in_db(titolo) #cerco nel db se il titolo è gia stato usato in una serie
        
        
        # sezione per validare i dati
        if pod_in_db or ser_in_db:
            flash('Titolo già usato!!', 'danger')
            return redirect(url_for('inserimento_podcast'))
        else:
            if data == '':
                data = date.today() #se non inserisce la data, metto io quella di oggi
            if titolo == '':
                titolo='Titolo non inserito'
            if serie_titolo=='':
                serie_titolo='INNOVAZIONI'
            if descrizione=='':
                descrizione = 'Nessuna descrizione inserita'

            #aggiungo audio
            if audio_pod:
                audio_pod.save('static/' + titolo.replace(" ", "") + '.mp3')
                audio = titolo.replace(" ", "") + '.mp3'
            else:
                audio = 'audio1.mp3'
            

            #creo nuovo podcast
            podcast = {'titolo': titolo, 'descrizione': descrizione, 'data': data, 'audio': audio, 'autore':autore, 'serie_titolo':serie_titolo}
            
            #aggiungo podcast a lista dei podcast
            success = podcasts_dao.add_podcast(podcast)

            if success:
                pod_trovato = podcasts_dao.trova_pod(titolo)
                flash('Podcast inserito correttamente!', 'success')
                return redirect(url_for('singolo', id=pod_trovato['id']))
            else:
                flash("Errore nell'inserimento del podcast", 'danger')
                return redirect(url_for('home'))
    else:
        return render_template("inserimento_podcast.html", titoli_serie=titoli_serie)

@app.route('/inserimento_serie', methods=["POST", "GET"]) #form di inserimento serie
@login_required
def inserimento_serie():
    if request.method == "POST":

        titolo = request.form.get('titolo')  #richiedo tutti i campi
        descrizione = request.form.get('descrizione')
        categoria = request.form.get('categoria')
        data = request.form.get('data')
        immagine = request.files['immagine']

        autore = current_user.nome
       
        #validare i dati
        if titolo == '':
            titolo = 'Titolo non inserito'
        if descrizione == '':
            descrizione = 'Nessuna descrizione inserita'
        if categoria == '':
           categoria = 'Nessuna categoria'
        if data == '':
            data = date.today()
        if immagine:
            immagine.save('static/' + titolo.replace(" ", "") + '.jpeg')
            immagine = titolo.replace(" ", "") + '.jpeg'
        else:
            immagine = 'nofoto.jpeg'
        
        #creo la sera
        serie = {'titolo': titolo, 'descrizione': descrizione, 'categoria':categoria, 'data':data, 'immagine':immagine, 'autore':autore}

        #aggiungo serie a lista delle serie
        success = podcasts_dao.add_serie(serie)
        
        tit = serie['titolo']
        if success:
            ser_trovata = podcasts_dao.trova_ser(tit)  #trovo la serie con quel titolo per passarla al redirect
            flash('Serie inserita correttamente!', 'success')
            return redirect(url_for('serie', id = ser_trovata['id']))
        else:
            flash("Errore nell'inserimento della serie", 'danger')
            return redirect(url_for('home'))
    else:
        return render_template("inserimento_serie.html")


@app.route('/cambiamentoserie<int:id>', methods=['POST', 'GET']) #form di cambiamento serie
def cambiamento_serie(id):
    serie_trovate = podcasts_dao.get_series()  #mi trovo tutte le serie e tutti i podcast per stamparli nella pagina di cambiamento
    podcast_trovati = podcasts_dao.trova_podcast()
    rif = podcasts_dao.trova_rif(id)

    if request.method == "POST":

        nuovo_titolo = request.form.get('nuovo_titolo') 
        nuova_descrizione = request.form.get('nuova_descrizione')
        nuova_data = request.form.get('nuova_data')
        nuova_immagine = request.files['nuova_immagine']
        nuova_categoria = rif['categoria']
        nuovo_id = rif['id']
        nuovo_autore =  rif['autore']
       
       #se non modifica gli altri campi, inserisco quelli precedenti
        if nuovo_titolo == '':
            nuovo_titolo = rif['titolo']
        if nuova_descrizione == '':
            nuova_descrizione = rif['descrizione']
        if nuova_data == '':
            nuova_data = date.today()
        if nuova_immagine:
            nuova_immagine.save('static/' + nuovo_titolo.replace(" ", "") + '.jpeg')
            nuova_immagine = nuovo_titolo.replace(" ", "") + '.jpeg'
        else:
            nuova_immagine = rif['immagine']

        #creo la nuova serie
        serie_mod = {'id': nuovo_id, 'titolo': nuovo_titolo, 'descrizione': nuova_descrizione, 'categoria': nuova_categoria, 'data':nuova_data, 'immagine':nuova_immagine, 'autore':nuovo_autore}

        success = podcasts_dao.modifica_serie(nuovo_id, serie_mod) #passo la nuova serie al dao
        
        if success:
            flash('Serie inserita correttamente!', 'success')
            return redirect(url_for('serie_singola', id = nuovo_id))
        else:
            flash("Errore nell'inserimento della serie", 'danger')
            return redirect(url_for('cambiamento_serie', id = nuovo_id))

    return render_template("cambiamento_serie.html", rif=rif, id=id, serie_trovate = serie_trovate, podcast_trovati=podcast_trovati)


@app.route('/cambiamentopodcast<int:id>', methods=['POST', 'GET']) #form di cambiamento podcast
def cambiamento_podcast(id):
    serie_trovate = podcasts_dao.get_series() #mi trovo tutte le serie e tutti i podcast per stamparli nella pagina di cambiamento
    podcast_trovati = podcasts_dao.trova_podcast()
    rif_pod = podcasts_dao.trova_rif_pod(id)


    if request.method == 'POST':
        nuovo_titolo = request.form.get('nuovo_titolo')
        nuova_descrizione = request.form.get('nuova_descrizione')
        nuova_data = request.form.get('nuova_data')
        nuovo_audio = request.files['nuovo_audio']
        nuovo_id = rif_pod['id']
        nuovo_autore =  rif_pod['autore']
        nuova_serie_titolo = rif_pod['serie_titolo']
        pod_in_db = podcasts_dao.pod_in_db(nuovo_titolo)
        
        #verifico che il titolo non sia già stato usato da altri
        if pod_in_db:
            flash('Titolo già usato!!', 'danger')
            return redirect(url_for('cambiamento_podcast', id=nuovo_id))
        else:
            if nuova_data == '':
                nuova_data = date.today()     #se non modifica gli altri campi, inserisco quelli precedenti
            if nuovo_titolo == '':
                nuovo_titolo=rif_pod['titolo']
            if nuova_descrizione == '':
                nuova_descrizione=rif_pod['descrizione']
            if nuova_serie_titolo == '':
                nuova_serie_titolo=rif_pod['serie_titolo']
            if nuovo_audio:
                nuovo_audio.save('static/' + nuovo_titolo.replace(" ", "") + '.mp3')
                nuovo_audio =  nuovo_titolo.replace(" ", "") + '.mp3'
            else :
                nuovo_audio = rif_pod['audio']


            #creo il podcast modificato
            podcast_mod = {'id': nuovo_id, 'titolo': nuovo_titolo, 'descrizione': nuova_descrizione, 'data': nuova_data, 'audio': nuovo_audio, 'autore': nuovo_autore, 'serie_titolo':nuova_serie_titolo}
            print(podcast_mod)
            success = podcasts_dao.modifica_podcast(nuovo_id, podcast_mod)

            if success:
                flash('Podcast modificato correttamente!', 'success')
                return redirect(url_for('singolo', id=nuovo_id))
            else:
                flash("Errore nella modifica del podcast", 'danger')
                return redirect(url_for('singolo', id=nuovo_id))
    else:
        return render_template('cambiamento_podcast.html', id = id, serie_trovate = serie_trovate, podcast_trovati=podcast_trovati, rif=rif_pod)

@app.route('/cambiamentocommenti<int:id>', methods=['POST', 'GET']) #cambiamento commenti
def cambiamento_commenti(id):
    commento_trovato = podcasts_dao.get_commenti_by_idd(id)

    if request.method == 'POST':
        nuovo_contenuto = request.form.get('nuovo_commento') #richiedo i dati
        nuovo_autore = current_user.nome
        nuovo_id = commento_trovato['id']
        nuovo_podcast_id = commento_trovato['podcast_id']

        #creo il commento modificato
        commento_mod = {'id': nuovo_id, 'contenuto':nuovo_contenuto, 'autore':nuovo_autore, 'podcast_id':nuovo_podcast_id}
        print(commento_mod)

        #verifico che ci siano state modifiche
        if nuovo_contenuto != ' ' and nuovo_contenuto != '':
            success = podcasts_dao.modifica_commento(nuovo_id, commento_mod)
            if success:
                flash('Commento modificato correttamente', 'success')
                return redirect(url_for('singolo', id = commento_trovato['podcast_id']))
            else:
                flash('Errore nella modifica del commento', 'danger')
                return redirect(url_for('singolo', id = commento_trovato['podcast_id']))
        else:
            flash('Nessuna modifica effettuata!', 'info')
            return redirect(url_for('singolo', id = commento_trovato['podcast_id']))

    return render_template('cambiamento_commenti.html', commento_trovato=commento_trovato, id=id)



@app.route('/eliminacommento<int:id>',  methods=['GET', 'POST']) #eliminazione commento tramite id
def elimina_commento(id):
    commento_trovato = podcasts_dao.get_commenti_by_idd(id)
    id_comm = commento_trovato['id']

    id_podcast = commento_trovato['podcast_id']

    if request.method == 'POST':
        success = podcasts_dao.elimina_commento(id_comm)

        if success:
            flash('Commento eliminato correttamento', 'success')
            return redirect(url_for('singolo', id=id_podcast))
        else:
            flash("Errore durante l'eliminazione del commento", 'danger')
            return redirect(url_for('singolo', id=id_podcast))
    
@app.route('/eliminapodcast<int:id>',  methods=['GET', 'POST']) #eliminazione podcast tramite id
def elimina_podcast(id):
    podcast_trovato = podcasts_dao.get_podcast_by_id(id)
    id_pod = podcast_trovato['id']
    id_ser = podcast_trovato['serie_titolo']
    commenti_trovati = podcasts_dao.get_commenti_by_id(id_pod)

    if request.method == 'POST':
        success_elimina_podcast_comm = podcasts_dao.elimina_podcast_e_comm(id_pod, commenti_trovati) #elimino podcast e commenti associati a quel podcast
        if success_elimina_podcast_comm:
            flash('Podcast eliminato correttamento', 'success')
            return redirect(url_for('serie_singola', id = id_ser))
        else:
            flash("Errore durante l'eliminazione del podcast", 'danger')
            return redirect(url_for('singolo', id = id_pod))
        
@app.route('/eliminaserie<int:id>',  methods=['GET', 'POST']) #eliminazione serie tramite id
def elimina_serie(id):
    id_ser = id
    pods = podcasts_dao.trova_id_podcast(id)

    indici_pods_da_canc = []
    indici_comm_da_canc = []

    for p in pods:
        i_pod= p['id']
        indici_pods_da_canc.append(i_pod)

    for i in indici_pods_da_canc:
        commenti = podcasts_dao.trova_commenti(i)
        for c in commenti:
            i_c = c['id']
            indici_comm_da_canc.append(i_c)

    if request.method == 'POST':
        success = podcasts_dao.elimina_serie(id_ser, indici_comm_da_canc, indici_pods_da_canc)  #elimino serie, podcast e commenti associati a quel podcast
    
    if success:
        flash('Serie eliminata correttamente', 'success')
        return redirect(url_for('serie'))
    else:
        flash("Errore durante l'eliminazione della serie", 'danger')
        return redirect(url_for('serie'))


@app.route('/seguiserie<int:id>', methods=['GET', 'POST'] ) #funzione per seguire una serie
def segui_serie(id):
    serie = podcasts_dao.trova_serie_by_id(id)
    serie_gia_seguite = podcasts_dao.trova_serie_gia_seguita(id)
    utente = current_user.nome

    if serie_gia_seguite:
        for s in serie_gia_seguite:  
            if s['utente'] == utente:  #controllo e passo solo la serie che si riferisce al current user
                flash('Serie già seguita', 'danger')
                return redirect(url_for('serie_singola', id=serie['id']))
      
    nuova_serie_seguita = {'id': serie['id'], 'titolo': serie['titolo'], 'utente':utente} #aggiungo la serie al db 
    success = podcasts_dao.aggiungi_serie_seguita(nuova_serie_seguita)

    if success:
        flash('Serie inserita nei tuoi preferiti', 'success')
        return redirect(url_for('profilo'))
    else:
        flash("Errore durante l'inserimento della serie nei preferiti", 'danger')
        return redirect(url_for('profilo'))


@app.route('/eliminapreferito<int:id>', methods=["POST", "GET"]) #tolgo la serie seguita
def elimina_preferito(id):
    preferito = podcasts_dao.trova_preferito_by_id(id)
    utente = current_user.nome

    success = False
    
    success = podcasts_dao.elimina_preferito(id, utente) #elimino la serie dal db tramite id della serie e current user

    if success:
        flash('Serie eliminata dai tuoi preferiti!', 'success')
        return redirect(url_for('profilo'))
    else:
        flash("Errore durante l'eliminazione della serie dai tuoi preferiti", 'danger')
        return redirect(url_for('profilo'))


#if __name__ == "__main__":   #per sicurezza, perche se tutto venisse importato fuori le mie variabile rimarebbero associate alle mie funzioni e non sarebbero delle variabili globali
 #app.run(host='0.0.0.0', port=3000, debug=True)
