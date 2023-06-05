# Peer-to-Peer Chat 

Questo è un programma di chat peer-to-peer scritto in Python. Consente agli utenti di comunicare tra loro attraverso una rete locale utilizzando il protocollo UDP.

## Funzionalità principali

- Creazione di un nuovo utente con username, indirizzo IP e numero di porta.
- Verifica della disponibilità dell'username e della porta.
- Salvataggio dei dati degli utenti in un file JSON.
- Crittografia dei messaggi utilizzando una chiave RSA.
- Invio di messaggi broadcast a tutti gli utenti connessi.
- Invio di messaggi privati a un utente specifico.
- Creazione di gruppi di chat e invio di messaggi a tutti i membri del gruppo.
- Gestione della disconnessione degli utenti.
- Ripristino dei dati utente da un file di backup JSON in caso di perdita del file principale.

## Requisiti

- Per i dettagli: requirements.txt

## Utilizzo

Per avviare il programma, eseguire:
``` 
python3 main.py
```

Al primo avvio, il programma chiederà all'utente di inserire un username. Se l'username inserito è già presente nella lista dei peer, verrà richiesto all'utente di scegliere un nuovo username o riattivare l'username esistente. Se l'username è nuovo, verrà creato un nuovo peer con l'username, l'indirizzo IP e la porta specificati. Verranno anche generate una chiave RSA e una chiave pubblica per il peer.

Una volta avviato, il programma avvia due thread separati: uno per la ricezione dei messaggi e l'altro per l'invio dei messaggi.

Per inviare un messaggio, l'utente può semplicemente digitare il testo del messaggio e premere Invio. Il messaggio può essere un messaggio broadcast, un messaggio privato a un utente specifico o un messaggio di gruppo a un gruppo specifico. L'utente può selezionare un utente o un gruppo utilizzando i comandi `!SELECT` e `!GROUP`. È possibile inoltre rimuovere utenti o gruppi tramite il comando `!REMOVE`.

Per uscire dal programma, l'utente può digitare il comando `!EXIT`. Se l'utente è in una chat di gruppo, dovrà prima passare alla chat con tutti gli utenti utilizzando il comando `!GROUP ALL`, quindi utilizzare il comando `!EXIT` per uscire completamente.

## Test

Per avviare la suite di test, eseguire da terminale il seguente comando: 
``` 
pytest test.py
```

## Note

- Il programma utilizza un file JSON `lista_peer.json` per memorizzare i dettagli dei peer, inclusi gli username, gli indirizzi IP, le porte e lo stato di attività di ognuno e ogni 10 peer si aggiorna un file di backup `backup_lista_peer.json`. Il file permette anche di memorizzare i dettagli degli insiemi di utenti che appartengono ad una stessa chat di gruppo memorizzando il nome e i membri del gruppo stesso.
- I messaggi vengono crittografati utilizzando la crittografia RSA, in particolare il cifrario asimettrico PKCS1_OAEP. Il primo peer che crea la rete genera e salva una chiave RSA nel file `key.pem` che viene poi richiamato da tutti i membri della rete per criptare e decriptare i messaggi scambiati.
- I messaggi vengono divisi in blocchi di dimensioni massime di 150 caratteri in input (le intestazioni predefinite per le varie tipologie di messaggio non rientrano nel computo dei 150) per evitare problemi di lunghezza del messaggio cifrato.
- Il programma tiene traccia dei peer attivi e li notifica agli altri peer appena si collegano.
- È possibile creare gruppi di utenti per la chat di gruppo. I gruppi possono essere creati solo con un numero ridotto di membri a causa della limitazione di lunghezza dei blocchi di caratteri in quanto la stringa contenente i membri del gruppo è inviata a tutti i membri come un messaggio.


