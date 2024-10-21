"use strict";

let titoli = []
let titolis = document.getElementsByClassName('item_titoli');
for (let p of titolis){
    titoli.push(p.innerHTML);
}
console.log(titoli)

let descrizioni = []
let descrizionis = document.getElementsByClassName('item_descrizione');
for (let q of descrizionis ){
    descrizioni.push(q.innerHTML);
}
console.log(descrizioni)

let id =[]
let ids = document.getElementsByClassName('idpod');
for (let i of ids ){
    id.push(i.innerHTML);
}
console.log(id)

let podcast = []
for (let i=0; i < id.length; i++){
    podcast.push({'id':id[i], 'titolo':titoli[i], 'descrizione':descrizioni[i]});
}
console.log(podcast)

let bottone = document.getElementById('invia');

let input = document.getElementById('search_input');
input.addEventListener('input', (i => {
    let scritta = i.target.value
    console.log(scritta)
    bottone.addEventListener('click', (e => {
        e.preventDefault();
        for (let pod of podcast){
            if ( (pod['titolo'].toLowerCase()).includes(scritta.toLowerCase()) || (pod['descrizione']).includes(scritta.toLowerCase()) ){
                let episodio = document.getElementById('episodio' + pod['id']);
                console.log('trovato')
                episodio.classList.remove('nascosto');
            } else {
                let episodio = document.getElementById('episodio' + pod['id']);
                episodio.classList.add('nascosto');
            }
        }
    }))
}))