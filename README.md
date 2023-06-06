# Peer-to-Peer Chat 

Questo è un programma di chat peer-to-peer scritto in Python. L'obiettivo principale del programma è consentire agli utenti di comunicare tra loro attraverso una rete locale utilizzando il protocollo UDP. Il programma offre una serie di funzionalità che permettono agli utenti di inviare e ricevere messaggi, creare gruppi di chat e gestire la connettività degli utenti.

## Funzionalità principali

Di seguito sono elencate le funzionalità principali del programma di chat peer-to-peer:

### 1. Creazione di un nuovo utente

Il programma consente agli utenti di creare un nuovo account specificando un username, un indirizzo IP e un numero di porta. Questi dettagli sono salvati in un file JSON per la gestione degli utenti.

### 2. Verifica dell'username e della porta

Prima di creare un nuovo utente, il programma verifica la disponibilità dell'username e della porta specificati. Se l'username o la porta sono già utilizzati da un altro utente, viene richiesto all'utente di scegliere un nuovo username o di riutilizzare l'username esistente se disconnesso.

### 3. Salvataggio dei dati degli utenti

I dati degli utenti, inclusi gli username, gli indirizzi IP, i numeri di porta e lo stato di attività di ogni utente, vengono salvati in un file JSON chiamato `lista_peer.json`. Questo file serve come database per mantenere i dettagli degli utenti e viene utilizzato per la gestione delle connessioni degli utenti.
```  
[
   {

      "Marco": 
      {
        "ip": "localhost", 
        "port": 6744, 
        "is_active": true
      }, 
     "Alessio": 
     {
        "ip": "localhost", 
        "port": 1855, 
        "is_active": true
      }
   }
]
```
### 4. Crittografia dei messaggi

Il programma utilizza la crittografia RSA per garantire la sicurezza dei messaggi scambiati tra gli utenti. Quando un utente invia un messaggio, viene utilizzata una chiave RSA per crittografare il contenuto del messaggio. Solo il destinatario designato può decriptare e leggere il messaggio utilizzando la chiave corrispondente.

### 5. Messaggi broadcast

Gli utenti possono inviare messaggi broadcast che vengono recapitati a tutti gli utenti connessi nella rete locale. Questo permette di comunicare con tutti gli utenti contemporaneamente senza dover inviare messaggi individuali.

### 6. Messaggi privati

Oltre ai messaggi broadcast, gli utenti possono inviare messaggi privati direttamente a un utente specifico. Questi messaggi sono visibili solo al destinatario e offrono un'opzione per le comunicazioni private tra due utenti.

### 7. Gruppi di chat

Il programma permette agli utenti di creare gruppi di chat, in cui più utenti possono partecipare e comunicare tra loro. Gli utenti possono inviare messaggi a tutti i membri del gruppo in modo da facilitare le discussioni di gruppo. I dati relativi ai gruppi e ai membri del gruppo vengono salvati sempre all'interno del file JSON chiamato `lista_peer.json`.
```  
[
   {
      "Calcetto":
      {
         "members": 
         [
           "Michele", 
           "Francesco", 
           "Giulio"
         ]
      },
      "Vacanze":
      {
         "members": 
         [
           "Federico", 
           "Emma", 
           "Lucia",
           "Riccardo"
         ]
      }
   }
]
```
### 8. Gestione della disconnessione

Il programma gestisce la disconnessione degli utenti in modo robusto. Quando un utente si disconnette, gli altri utenti vengono notificati della sua disconnessione. Inoltre, i dati degli utenti vengono salvati in un file di backup JSON `backup_lista_peer.json` per poter essere ripristinati in caso di perdita del file principale.

## Requisiti

- Per i dettagli: requirements.txt

## Utilizzo

Per avviare il programma, seguire i passaggi seguenti:

1. Aprire un terminale o una finestra della riga di comando.
2. Navigare nella directory in cui è presente il file "main.py".
3. Eseguire il seguente comando:
``` 
python3 main.py
```

Al primo avvio, il programma chiederà all'utente di inserire un username. Se l'username inserito è già presente nella lista dei peer, verrà richiesto all'utente di scegliere un nuovo username o riattivare l'username esistente. Se l'username è nuovo, verrà creato un nuovo peer con l'username, l'indirizzo IP e la porta specificati. Verranno anche generate una chiave RSA e una chiave pubblica per il peer.

Una volta avviato, il programma avvia due thread separati: uno per la ricezione dei messaggi e l'altro per l'invio dei messaggi.

Per inviare un messaggio, l'utente può semplicemente digitare il testo del messaggio e premere Invio. Il messaggio può essere un messaggio broadcast, un messaggio privato a un utente specifico o un messaggio di gruppo a un gruppo specifico. L'utente può selezionare un utente o un gruppo utilizzando i comandi `!SELECT` e `!GROUP`. Digitando il comando `!PEERS` è possibile visualizzare tutti i peers attivi in quel momento. È possibile inoltre rimuovere utenti o gruppi tramite il comando `!REMOVE`.

Per uscire dal programma, l'utente può digitare il comando `!EXIT`. Se l'utente è in una chat di gruppo, dovrà prima passare alla chat con tutti gli utenti utilizzando il comando `!GROUP ALL`, quindi utilizzare il comando `!EXIT` per uscire completamente.

In caso di necessità l'utente può visualizzare quando desidera l'elenco di questi comandi inserendo come messaggio il comando `!HELP`

## Test

Per verificare il corretto funzionamento del programma, è possibile eseguire una suite di test inclusa nel programma. Per avviare la suite di test, seguire i passaggi seguenti:

1. Aprire un terminale o una finestra della riga di comando.
2. Navigare nella directory in cui è presente il file `test.py`.
3. Eseguire il seguente comando:
``` 
pytest test.py
```

## Note

- Il programma utilizza un file JSON `lista_peer.json` per memorizzare i dettagli dei peer, inclusi gli username, gli indirizzi IP, le porte e lo stato di attività di ognuno e ogni 10 peer si aggiorna un file di backup `backup_lista_peer.json`. Il file permette anche di memorizzare i dettagli degli insiemi di utenti che appartengono ad una stessa chat di gruppo memorizzando il nome e i membri del gruppo stesso.
- I messaggi vengono crittografati utilizzando la crittografia RSA, in particolare il cifrario asimettrico PKCS1_OAEP. Il primo peer che crea la rete genera e salva una chiave RSA nel file `key.pem` che viene poi richiamato da tutti i membri della rete per criptare e decriptare i messaggi scambiati.
- I messaggi vengono divisi in blocchi di dimensioni massime di 150 caratteri in input (le intestazioni predefinite per le varie tipologie di messaggio non rientrano nel computo dei 150) per evitare problemi di lunghezza del messaggio cifrato.
- Il programma tiene traccia dei peer attivi e li notifica agli altri peer appena si collegano.
- È possibile creare gruppi di utenti per la chat di gruppo. I gruppi possono essere creati solo con un numero ridotto di membri a causa della limitazione di lunghezza dei blocchi di caratteri in quanto la stringa contenente i membri del gruppo è inviata a tutti i membri come un messaggio.


