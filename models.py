from flask_login import UserMixin

# andiamo a definire la nostra classe 'utente' modificando la definizione di default 'usermixin'

class Utente(UserMixin):
    def __init__ (self, id, nome, cognome, email, password, foto, data, codice):
        self.id = id 
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
        self.foto = foto
        self.data = data
        self.codice = codice

