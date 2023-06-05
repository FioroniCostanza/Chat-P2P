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

- Python 3.x
- Libreria `pycryptodome` per la crittografia dei messaggi: `pip install pycryptodome`

## Utilizzo

Per avviare il programma, eseguire il file `peer.py` utilizzando Python 3.

Al primo avvio, il programma chiederà all'utente di inserire un username. Se l'username inserito è già presente nella lista dei peer, verrà richiesto all'utente di scegliere un nuovo username o riattivare l'username esistente. Se l'username è nuovo, verrà creato un nuovo peer con l'username, l'indirizzo IP e la porta specificati. Verranno anche generate una chiave RSA e una chiave pubblica per il peer.

Una volta avviato, il programma avvia due thread separati: uno per la ricezione dei messaggi e l'altro per l'invio dei messaggi.

Per inviare un messaggio, l'utente può semplicemente digitare il testo del messaggio e premere Invio. Il messaggio può essere un messaggio broadcast, un messaggio privato a un utente specifico o un messaggio di gruppo a un gruppo specifico. L'utente può selezionare un utente o un gruppo utilizzando i comandi `!SELECT` e `!GROUP`.

Per uscire dal programma, l'utente può digitare il comando `!EXIT`. Se l'utente è in una chat di gruppo, dovrà prima passare alla chat con tutti gli utenti utilizzando il comando `!GROUP ALL`, quindi utilizzare il comando `!EXIT` per uscire completamente.

## Note

- Il programma utilizza un file JSON `lista_peer.json` per memorizzare i dettagli dei peer, inclusi gli username, gli indirizzi IP, le porte e lo stato di attività e ogni 10 peer si aggiorna un file di backup `backup_lista_peer.json`.
- I messaggi vengono crittografati utilizzando la crittografia RSA. Viene generata una chiave RSA `key.pem` per ogni peer e viene utilizzata la crittografia PKCS1_OAEP.
- I messaggi vengono divisi in blocchi di dimensioni massime di 150 caratteri per evitare problemi di lunghezza del messaggio cifrato.
- Il programma tiene traccia dei peer attivi e li notifica agli altri peer appena si collegano.
- È possibile creare gruppi di utenti per la chat di gruppo. I gruppi possono essere creati solo con un numero ridotto di membri a causa della limitazione di lunghezza dei blocchi.


