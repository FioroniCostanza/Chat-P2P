import json
import os
import sys
import socket
import threading
from random import randint
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import re


class Peer:
    def __init__(self, username, ip, port):
        self.lista_peer = {}
        self.file_path = self.verify_reachable_json()
        self.lock = threading.Lock()
        self.load_peers_from_json()
        self.username = self.verify_username(username)
        self.ip = ip
        self.port = self.verify_port_is_free(port)
        self.is_active = True
        self.public_key = self.import_key()
        self.cipher = PKCS1_OAEP.new(self.public_key)

        self.socket_peer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_peer.bind((self.ip, self.port))

        self.socket_message = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_message.bind((self.ip, 0))

        self.add_peer_to_json()
        self.notify_new_peers()

        self.connection_thread = threading.Thread(target=self.receive_message)
        self.communication_thread = threading.Thread(target=self.send_messages)

        self.start()

    def start(self):
        self.connection_thread.start()
        self.communication_thread.start()

    def verify_reachable_json(self):
        # Si verifica se il file JSON è raggiungibile
        if os.path.exists('lista_peer.json'):
            try:
                with open('lista_peer.json', 'r') as file:
                    file.close()
                return 'lista_peer.json'
            except FileNotFoundError:
                if os.path.exists('backup_lista_peer.json'):
                    try:
                        with open('backup_lista_peer.json', 'r') as file:
                            file.close()
                        return 'backup_lista_peer.json'
                    except FileNotFoundError:
                        print("Error: JSON file not found.")
                        sys.exit(1)
        return 'lista_peer.json'

    def verify_username(self, user):
        # Si verifica che l'username non sia già presente nella lista dei peer
        if user in self.lista_peer.keys():
            # Si verifica che l'username sia attivo
            if self.lista_peer[user]['is_active']:
                print(f"Username '{user}' already exists and is active. Generating a new username...")
                new_username = input("Enter a new username: ")
                return self.verify_username(new_username)
            else:
                # altrimenti si chiede se si vuole riattivare l'username o se si vuole cambiarlo
                print(f"Username '{user}' already exists but is inactive.")
                choice = input("Do you want to reactivate it? (yes/no): ")
                if choice.lower() == "yes":
                    self.update_user_status(user, True)  # Aggiorna lo stato dell'utente nel file JSON
                    return user
                else:
                    new_username = input("Enter a new username: ")
                    return self.verify_username(new_username)
        else:
            return user

    def verify_port_is_free(self, port):
        if os.path.exists(self.file_path):
            with self.lock:
                # Si verifica se esiste già una chiave associata all'username nel file JSON
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
                    file.close()
                if self.username in data:
                    return int(data[self.username]['port'])
                else:
                    # Altrimenti si verifica che la porta non sia già presente nella lista dei peer
                    for user, user_data in self.lista_peer.items():
                        if 'port' in user_data and user_data['port'] == port:
                            print(f"Port {user} busy. Generating new port...")
                            new_value = randint(1000, 9999)
                            return self.verify_port_is_free(new_value)
                    return port
        else:
            return port


    def import_key(self):
        # Si verifica se esiste già una chiave RSA
        with self.lock:
            if os.path.exists('key.pem'):
                with open('key.pem', 'rb') as f:
                    key_data = f.read()
                    f.close()
                return RSA.import_key(key_data)
            else:
                # altrimenti si crea una nuova chiave RSA e la si salva nel file key.pem
                key = RSA.generate(2048)
                with open("key.pem", "wb") as f:
                    f.write(key.exportKey('PEM'))
                    f.close()
                return key

    def load_peers_from_json(self):
        with self.lock:
            # Si verifica se esiste già un file JSON
            if os.path.exists(self.file_path):
                # Se esiste si carica il file JSON e si salvano i dati nella variabile lista_peer
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
                    for user, user_data in data.items():
                        if 'members' in user_data:
                            # Se l'utente è un gruppo si aggiunge il gruppo a lista_peer
                            self.lista_peer[user] = {'members': user_data['members']}
                        else:
                            # Se l'utente è un peer si aggiunge alla lista dei peer
                            self.lista_peer[user] = {
                                'ip': user_data['ip'],
                                'port': int(user_data['port']),
                                'is_active': user_data['is_active']
                            }
                    file.close()

    def add_peer_to_json(self):
        # Se l'utente ancora non è nella lista dei peer, lo si aggiunge
        if self.username not in self.lista_peer.keys():
            with self.lock:
                self.lista_peer[self.username] = {'ip': self.ip, 'port': self.port, 'is_active': self.is_active}
                with open(self.file_path, 'w') as file:
                    json.dump(self.lista_peer, file)
                    file.close()
                if len(self.lista_peer) % 10 == 0:
                    # Ogni 10 peer si aggiorna un file di backup (nel caso in cui non si stiano già recuperando i
                    # dati da tale backup)
                    path = 'backup_lista_peer.json'
                    if os.path.exists(path):
                        if path != self.file_path:
                            with open(path, 'w') as file:
                                json.dump(self.lista_peer, file)
                                file.close()
                    else:
                        with open(path, 'x') as file:
                            json.dump(self.lista_peer, file)
                            file.close()

    def update_user_status(self, username, is_active):
        with self.lock:
            # Aggiorna lo stato del peer nel programma e nel file JSON
            with open(self.file_path, "r") as file:
                data = json.load(file)
                data[username]["is_active"] = is_active
                file.close()
            with open(self.file_path, "w") as file:
                json.dump(data, file)
                file.close()
            if username in self.lista_peer:
                self.lista_peer[username]['is_active'] = is_active

    def create_group(self, group_name, group_members):
        # Si aggiunge il gruppo alla lista dei peer
        self.lista_peer[group_name] = {'members': group_members}
        with self.lock:
            with open(self.file_path, 'w') as file:
                json.dump(self.lista_peer, file)
                file.close()

    def remove_group(self, name):
        # Si rimuove un gruppo dalla lista dei peer
        if name in self.lista_peer:
            if 'members' in self.lista_peer[name]:
                del self.lista_peer[name]
            with self.lock:
                with open(self.file_path, 'w') as file:
                    json.dump(self.lista_peer, file)
                    file.close()

    def notify_new_peers(self):
        # Si invia un messaggio broadcast per notificare la presenza di un nuovo peer
        self.send_message_broadcast(f"NEW_PEER_TAG:{self.username}:{self.ip}:{self.port}:{self.is_active}")

    def split_message_into_blocks(self, message):
        message_blocks = []
        block_size = 150
        for i in range(0, len(message), block_size):
            if i + block_size > len(message):
                block_size = len(message) - i
            block = message[i:i + block_size]
            message_blocks.append(block)
        for i in range(len(message_blocks)):
            message_blocks[i] = f'{str(i + 1)}###{message_blocks[i]}'  # Aggiunge il numero del blocco al messaggio
        message_blocks[0] = f'{message_blocks[0]}###{str(len(message_blocks))}'  # Aggiunge il numero totale dei blocchi al primo blocco
        return message_blocks

    def handle_message_blocks(self, message_received):
        sender, message_received = message_received.split(": ")
        if len(message_received.split("###")) == 3:
            block_number = int(message_received.split("###")[0])
            self.total_blocks = int(message_received.split("###")[2])
        else:
            block_number = int(message_received.split("###")[0])
        if block_number == 1:
            self.message_received = ""
        self.message_received += message_received.split("###")[1]
        if block_number == self.total_blocks:
            message = f'{sender}: {self.message_received}'
            return message
        else:
            return None

    def receive_message(self):
        # Metodo di ricezione messaggi
        while self.is_active:
            try:
                # Si riceve il messaggio e lo si decripta
                message_received, address = self.socket_peer.recvfrom(1024)
                message_received = self.decrypt(message_received)
                # Si verifica se il messaggio ricevuto è un messaggio di presentazione di un nuovo peer
                if message_received.startswith("NEW_PEER_TAG"):
                    # In tal caso si aggiunge il nuovo peer alla lista dei peer
                    received_username = message_received.split(":")[1]
                    if received_username != self.username:
                        print(f'{received_username} has joined the chat')
                        self.lista_peer[received_username] = {'ip': message_received.split(":")[2],
                                                              'port': int(message_received.split(":")[3]),
                                                              'is_active': message_received.split(":")[4]}
                elif message_received.startswith("NEW_GROUP_TAG"):
                    received_group = message_received.split(":")[1]
                    # Isolo la lista dei membri dalle parentesi quadre e la divido in base alle virgole
                    received_members = message_received.split(":")[2].strip('[').strip(']').split(',')
                    for i in range(len(received_members)):
                        received_members[i] = received_members[i].strip(" '")
                    self.lista_peer[received_group] = {'members': received_members}
                    print(f"New group created: ''{received_group}'' with members: {received_members}")
                elif message_received.startswith("!EXIT"):
                    msg = message_received.split(": ")[1]
                    print(msg)
                else:
                    # Altrimenti si divide il messaggio in blocchi
                    msg = self.handle_message_blocks(message_received)
                    if msg is not None:
                        # Se il messaggio è completo si stampa a video
                        print(msg)
            except Exception as e:
                print("Connection lost")
                break

    def send_messages(self):
        selected_user = None  # Utente selezionato per la chat privata
        selected_group = None  # Gruppo selezionato per la chat di gruppo
        should_exit = False  # Variabile che indica se l'utente vuole uscire dal programma
        while self.is_active and not should_exit:
            try:
                message_sent = input("")  # Messaggio da inviare
                message_sent = self.split_message_into_blocks(message_sent)  # Si divide il messaggio in blocchi
                body_message = message_sent[0].split("###")[1]  # Si prende il messaggio del primo blocco da inviare
                if body_message.startswith("!EXIT"):
                    # Se il messaggio inizia con !EXIT si esce dal programma
                    if selected_group is None:
                        self.leave_chat()
                        self.stop()
                        should_exit = True
                    else:
                        print("You are currently in a group. Use !GROUP ALL to switch to all users. After that use !EXIT if you want.")
                elif body_message.startswith("!PEERS"):
                    # Se il messaggio inizia con !PEERS si stampa la lista dei peer attivi
                    active_peers = []
                    for user, user_data in self.lista_peer.items():
                        if user != self.username and 'is_active' in user_data:
                            if bool(self.lista_peer[user]['is_active']):
                                active_peers.append(user)
                    print(f'Active peers (excluding you): {active_peers}')
                elif body_message.startswith("!HELP"):
                    # Se il messaggio inizia con !HELP si stampa la lista dei comandi
                    print("\n")
                    print("Commands:\n")
                    print("!PEERS: show active peers")
                    print("!SELECT <username>: select a user for private chat")
                    print("!GROUP <group_name>: select (or create) a group for group chat")
                    print("!GROUP ALL: switch to all users chat")
                    print("!REMOVE <group_name>: delete a group")
                    print("!EXIT: exit from the program")
                elif body_message.startswith("!SELECT"):
                    # Se il messaggio inizia con !SELECT si seleziona un utente per la chat privata
                    selected_user = body_message.split(" ")[1]
                    if selected_user in self.lista_peer:
                        print(f"You have selected user: '{selected_user}'")
                    else:
                        print(f"User '{selected_user}' does not exist")
                        selected_user = None
                elif body_message.startswith("!GROUP"):
                    # Se il messaggio inizia con !GROUP si seleziona un gruppo per la chat di gruppo
                    group_name = body_message.split(" ")[1]
                    # Si potranno creare solo gruppi ridotti in seguito alla limitazione per singolo blocco di soli 150 caratteri
                    if group_name == "ALL":
                        # Se il gruppo selezionato è ALL si seleziona la chat con tutti gli utenti
                        selected_user = None
                        selected_group = None
                        print("You have selected to chat with all users")
                    elif group_name in self.lista_peer:
                        # Se il gruppo selezionato esiste si seleziona la chat di gruppo
                        selected_group = group_name
                        print(f"You have selected group: {selected_group}")
                    else:
                        # Altrimenti si chiede all'utente se vuole creare un nuovo gruppo
                        print(f"Group '{group_name}' does not exist. Create a new group? (yes/no)")
                        choice = input("")
                        if choice.lower() == "yes":
                            members = input("Enter group members (excluding you) separated by commas: ").split(",")
                            creation_failed = False
                            # Controllo che tutti gli utenti inseriti esistano
                            for member in members:
                                if member not in self.lista_peer:
                                    print(f"User '{member}' does not exist. Group not created.")
                                    creation_failed = True
                                    break
                            if creation_failed == False:
                                self.create_group(group_name, members)
                                selected_group = group_name
                                print(f"Group '{group_name}' created with members: {members}")
                                members.append(self.username)
                                self.send_message_multicast(members, f"NEW_GROUP_TAG:{group_name}:{members}")
                        else:
                            print("Group not created.")
                    selected_user = None
                elif body_message.startswith("!REMOVE"):
                    # Se il messaggio inizia con !REMOVE si rimuove un gruppo
                    name = body_message.split(" ")[1]
                    self.remove_group(name)
                    print(f"'{name}' has been removed.")
                    selected_group = None
                elif selected_user is not None:
                    # Se è stato selezionato un utente si invia un messaggio privato
                    intestazione = f'[Private message from {self.username}]'
                    for i in range(len(message_sent)):
                        self.send_message_unicast(selected_user, f'{intestazione}: {message_sent[i]}')
                elif selected_group is not None:
                    # Se è stato selezionato un gruppo si invia un messaggio di gruppo
                    group_members = self.lista_peer[selected_group]['members']
                    intestazione = f'[Group message from {self.username} to {selected_group}]'
                    for i in range(len(message_sent)):
                        self.send_message_multicast(group_members, f'{intestazione}: {message_sent[i]}')
                else:
                    # Altrimenti si invia un messaggio broadcast a tutti gli utenti
                    for i in range(len(message_sent)):
                        self.send_message_broadcast(f'{self.username}: {message_sent[i]}')
            except Exception as e:
                print("Connection lost")
                break

    def encrypt(self, msg):
        # Si aggiungono spazi per ogni carattere speciale per evitare problemi di lunghezza del messaggio cifrato
        special_chars = re.findall('([À-ÿ]+)', msg)
        if len(special_chars) > 0:
            for special_char in special_chars:
                for i in range(len(special_char)):
                    msg += " "
        ciphertext = self.cipher.encrypt(msg.encode('utf-8'))
        # Si invia la lunghezza del messaggio cifrato e il messaggio cifrato
        encrypted_msg = str(len(msg)) + "#" + ciphertext.hex()
        return encrypted_msg

    def decrypt(self, ctx):
        try:
            encrypted_msg = ctx.decode('utf-8')
            # Si riceve la lunghezza del messaggio cifrato e il messaggio cifrato
            length, ciphertext = encrypted_msg.split("#", 1)
            # Si decripta il messaggio
            msg = self.cipher.decrypt(bytes.fromhex(ciphertext))
            return msg[:int(length)].decode('utf-8')
        except Exception as e:
            print(e)

    def leave_chat(self):
        exit_message = f"!EXIT: {self.username} has left the chat"
        self.send_message_broadcast(exit_message)
        self.is_active = False
        self.update_user_status(self.username, False)

    def send_message_broadcast(self, message):
        message = self.encrypt(message)  # Si cifra il messaggio
        for user, user_data in self.lista_peer.items():
            # Si invia il messaggio a tutti gli utenti tranne a se stessi e ai gruppi
            if user != self.username and 'ip' in user_data and 'port' in user_data:
                if bool(self.lista_peer[user]['is_active']):
                    # Si invia il messaggio a tutti gli utenti tranne se stessi
                    self.socket_message.sendto(message.encode('utf-8'), (user_data['ip'], user_data['port']))

    def send_message_unicast(self, user, message):
        message = self.encrypt(message)
        # Si invia il messaggio all'utente selezionato
        if bool(self.lista_peer[user]['is_active']):
            self.socket_message.sendto(message.encode('utf-8'),(self.lista_peer[user]['ip'], self.lista_peer[user]['port']))

    def send_message_multicast(self, utenti, message):
        message = self.encrypt(message)
        group = []
        for user in utenti:
            if user != self.username:
                if bool(self.lista_peer[user]['is_active']):
                    # Si invia il messaggio a tutti gli utenti del gruppo
                    group.append(user)
                    self.socket_message.sendto(message.encode('utf-8'),(self.lista_peer[user]['ip'], self.lista_peer[user]['port']))

    def stop(self):
        # Si chiudono le connessioni e i socket
        if self.is_active is True:
            self.leave_chat()
        self.socket_peer.close()
        self.socket_message.close()
