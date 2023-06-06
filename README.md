# Peer-to-Peer Chat 

Questo è un programma di chat peer-to-peer scritto in Python. L'obiettivo principale del programma è consentire agli utenti di comunicare tra loro attraverso una rete locale utilizzando il protocollo UDP. Il programma offre una serie di funzionalità che permettono agli utenti di inviare e ricevere messaggi, creare gruppi di chat e gestire la connettività degli utenti.

## Requisiti

- Python 3.x
- Pycryptodome
- Pytest
- Per dettagli ulteriori: requirements.txt

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

Gli utenti possono inviare messaggi broadcast che vengono recapitati a tutti gli altri utenti connessi alla rete. Questo permette di comunicare con tutti gli utenti contemporaneamente senza dover inviare messaggi individuali.

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

Il programma gestisce la disconnessione degli utenti in modo robusto. Quando un utente si disconnette, gli altri utenti vengono notificati della sua disconnessione. Inoltre, ogni 10 peers i dati degli utenti vengono salvati in un file di backup JSON `backup_lista_peer.json` per poter essere ripristinati in caso di perdita del file principale.

### 9. Tolleranza ai guasti

Il programma è in grado di sopperire ad eventuali guasti del file JSON e dei peer, in quanto, in caso di guasto del file JSON è presente il file di backup. Nell'ipotesi in cui siano guasti entrambi i file JSON, nonostante non sia più gestibile la registrazione di nuovi peer e/o la creazione di nuovi gruppi, i peer già all'interno della rete possono continuare a comunicare tra di loro senza problemi. Questa continuità della comunicazione avverà anche in caso di guasto di un peer, poiché l'unica conseguenza di tale guasto sarebbe l'impossibilità di raggiungere o comunicare con il peer danneggiato.

## Utilizzo

Per avviare il programma, seguire i passaggi seguenti:

1. Aprire un terminale o una finestra della riga di comando.
2. Navigare nella directory in cui è presente il file "main.py".
3. Eseguire il seguente comando:
``` 
python3 main.py
```

Al primo avvio, il programma chiederà all'utente di inserire un username:
``` 
Username: Marco
```
Se l'username inserito è già presente nella lista dei peer, verrà richiesto all'utente di scegliere un nuovo username:
```
Username 'Marco' already exists and is active. Generating a new username...
Enter a new username: Giacomo
```
o riattivare l'username esistente:
```
Username 'Marco' already exists but is inactive.
Do you want to reactivate it? (yes/no):
yes
```
Se l'username è nuovo, verrà creato un nuovo peer con l'username, l'indirizzo IP e la porta specificati. Verranno anche generate una chiave RSA e una chiave pubblica per il peer.

Una volta avviato, il programma avvia due thread separati: uno per la ricezione dei messaggi e l'altro per l'invio dei messaggi.

Per inviare un messaggio, l'utente può semplicemente digitare il testo del messaggio e premere Invio. Il messaggio può essere un messaggio broadcast, un messaggio privato a un utente specifico o un messaggio di gruppo a un gruppo specifico. L'utente può selezionare un utente o un gruppo utilizzando i comandi `!SELECT` e `!GROUP`. Digitando il comando `!PEERS` è possibile visualizzare tutti i peer attivi in quel momento. È possibile inoltre rimuovere gruppi tramite il comando `!REMOVE`.

Per uscire dal programma, l'utente può digitare il comando `!EXIT`; nonostante l'utilizzo di questo comando sia preferibile, il programma gestisce anche l'uscita tramite `Ctrl+C` da terminale. Se l'utente è in una chat di gruppo, dovrà prima passare alla chat con tutti gli utenti utilizzando il comando `!GROUP ALL`, quindi utilizzare il comando `!EXIT` per uscire completamente.

In caso di necessità l'utente può visualizzare quando desidera l'elenco di questi comandi inserendo come messaggio il comando `!HELP`.
```
Commands:

!PEERS: show active peers
!SELECT <username>: select a user for private chat
!GROUP <group_name>: select (or create) a group for group chat
!GROUP ALL: switch to all users chat
!REMOVE <group_name>: delete a group
!EXIT: exit from the program
```

## Test

Per verificare il corretto funzionamento del programma, è possibile eseguire una suite di test (10 test che verificano le performance del programma) inclusa nel programma. Per avviare la suite di test, seguire i passaggi seguenti:

1. Aprire un terminale o una finestra della riga di comando.
2. Navigare nella directory in cui è presente il file `test.py`.
3. Eseguire il seguente comando:
``` 
pytest test.py
```

N.B. Si consiglia di eseguire la suite di test prima di effettuare un qualunque utilizzo del sistema di chat poiché, per esigenze di progettazione (in particolar modo la rigenerazione di un nuovo username nel caso in cui fosse già presente), prima di eseguire i test, la suite elimina sia il file `lista_peer.json` che il file di backup `backup_lista_peer.json`.

## Note

- I messaggi vengono crittografati utilizzando la crittografia RSA, in particolare il cifrario asimettrico PKCS1_OAEP. Il primo peer che crea la rete genera e salva una chiave RSA nel file `key.pem` che viene poi richiamato da tutti i membri della rete per criptare e decriptare i messaggi scambiati.
- I messaggi vengono divisi in blocchi di dimensioni massime di 150 caratteri in input (le intestazioni predefinite per le varie tipologie di messaggio non rientrano nel computo dei 150) per evitare problemi di lunghezza del messaggio cifrato.
- Il programma tiene traccia dei peer attivi e li notifica agli altri peer appena si collegano.
- È possibile creare gruppi di utenti per la chat di gruppo. I gruppi possono essere creati solo con un numero ridotto di membri a causa della limitazione di lunghezza dei blocchi di caratteri in quanto la stringa contenente i membri del gruppo è inviata a tutti i membri come un messaggio.

## Miglioramenti futuri

### Sicurezza avanzata

- Utilizzo di una chiave simmetrica per la crittografia dei messaggi: invece di utilizzare una chiave RSA unica per crittografare i messaggi, si può generare una chiave simmetrica casuale per ciascuna comunicazione tra due peer, in modo da realizzare una crittografia di tipo end-to-end. Questa chiave simmetrica può essere utilizzata per crittografare e decriptare i messaggi scambiati tra i due peer. In questo modo, ogni comunicazione avrà una chiave di crittografia diversa, migliorando la sicurezza complessiva del sistema.
- Scambio sicuro delle chiavi simmetriche: per consentire ai peer di scambiarsi le chiavi simmetriche in modo sicuro, si può utilizzare un protocollo di scambio delle chiavi sicuro, come il protocollo Diffie-Hellman o il protocollo di scambio delle chiavi Elliptic Curve Diffie-Hellman (ECDH). Questi protocolli consentono ai peer di stabilire una chiave segreta condivisa senza dover trasmettere direttamente la chiave tramite la rete.
- Rotazione periodica delle chiavi simmetriche: per aumentare la sicurezza delle comunicazioni nel tempo, si può implementare una rotazione periodica delle chiavi simmetriche. Ad esempio, si definisce una durata di validità per ogni chiave simmetrica e, dopo un determinato periodo, generare una nuova chiave e utilizzarla per le comunicazioni successive. In questo modo, anche se una chiave viene compromessa, l'impatto sarà limitato al periodo di validità di quella chiave.
- Implementazione di meccanismi di autenticazione: oltre alla crittografia dei messaggi, si può considerare l'implementazione di meccanismi di autenticazione per garantire che i messaggi siano inviati e ricevuti solo da peer legittimi. Si possono utilizzare firme digitali basate su algoritmi di crittografia asimmetrica per garantire l'integrità e l'autenticità dei messaggi.

### Gestione della scalabilità

Gli alberi AVL (Adelson-Velsky e Landis) potrebbero essere una strategia efficace per migliorare la gestione della scalabilità in questo programma:
- Struttura dati per i peer: ogni peer può essere rappresentato come un nodo nell'albero, con le informazioni pertinenti come l'indirizzo IP, la porta e lo stato di attività associate al nodo. L'uso di un albero AVL garantisce che l'albero sia bilanciato, il che porta a tempi di ricerca efficienti e riduce la possibilità di congestionamento.
- Inserimento e rimozione dei peer: quando un nuovo peer si connette o un peer esistente viene disconnesso, vengono eseguite le operazioni di inserimento o rimozione direttamente nell'albero AVL. L'albero si adatterà automaticamente per mantenere il bilanciamento, garantendo prestazioni ottimali anche con un grande numero di peer.
- Ricerca e gestione dei peer: si possono utilizzare le operazioni di ricerca dell'albero AVL per trovare rapidamente le informazioni di un peer specifico. Ad esempio, se si ha bisogno di recuperare le informazioni di un peer dato il suo indirizzo IP, è possibile eseguire una ricerca nell'albero AVL in tempo logaritmico, ottenendo così un accesso rapido alle informazioni desiderate.
- Bilanciamento automatico: gli alberi AVL si auto-bilanciano automaticamente dopo ogni operazione di inserimento o rimozione. Ciò garantisce che l'albero mantenga un'altezza bilanciata e che le operazioni di ricerca e aggiornamento siano efficienti, indipendentemente dal numero di peer connessi.
