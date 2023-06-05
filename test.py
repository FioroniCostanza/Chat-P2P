import time
import os
import unittest
from peer import Peer
from random import randint
import pytest
import subprocess

class Test_Peer(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists("lista_peer.json"):
            subprocess.run(["rm", "lista_peer.json"])  # Rimuove il file lista_peer.json nel caso esistesse per non creare conflitti con i test
        if os.path.exists("backup_lista_peer.json"):
            subprocess.run(["rm", "backup_lista_peer.json"])  # Rimuove anche il file backup_lista_peer.json

    def test_init(self):
        peer = Peer("test_", "localhost", 2023)
        self.assertEqual(peer.username, "test_")
        self.assertEqual(peer.ip, "localhost")
        self.assertEqual(peer.port, 2023)
        self.assertEqual(peer.is_active, True)

    def test_encrypt(self):
        peer = Peer("encrypt_peer", "localhost", randint(1000, 9999))
        message = 'test'
        encrypted_message = peer.encrypt(message)
        self.assertNotEqual(message, encrypted_message)

    def test_decrypt(self):
        peer = Peer("decrypt_peer", "localhost", randint(1000, 9999))
        message = 'test'
        encrypted_message = peer.encrypt(message).encode('utf-8')
        decrypted_message = peer.decrypt(encrypted_message)
        self.assertEqual(message, decrypted_message)

    def test_leave_chat(self):
        peer = Peer("leave_chat_peer", "localhost", randint(1000, 9999))
        peer.leave_chat()
        self.assertEqual(peer.is_active, False)

    def test_stop(self):
        peer = Peer("stop_peer", "localhost", randint(1000, 9999))
        peer.stop()
        self.assertNotEqual(peer.is_active, True)

    def test_connection(self):
        peer2_in_peer = False
        peer_in_peer2 = False
        peer = Peer("connection_peer", "localhost", randint(1000, 9999))
        peer2 = Peer("connection_peer2", "localhost", randint(1000, 9999))
        time.sleep(0.02)
        if peer2.username in peer.lista_peer: peer2_in_peer = True
        if peer.username in peer2.lista_peer: peer_in_peer2 = True
        self.assertEqual(peer_in_peer2, True)
        self.assertEqual(peer2_in_peer, True)

    def test_send_message_broadcast(self):
        peer = Peer("send_message_broadcast_peer", "localhost", randint(1000, 9999))
        peer_ = Peer("send_message_broadcast_peer_", "localhost", randint(1000, 9999))
        time.sleep(0.02)
        message = 'test'
        msg = peer.split_message_into_blocks(message)
        message_sent = f'{peer.username}: {msg[0]}'
        peer.send_message_broadcast(message_sent)
        time.sleep(0.02)
        self.assertEqual(message, peer_.message_received)

    def test_send_message_unicast(self):
        peer = Peer("send_message_unicast_peer", "localhost", randint(1000, 9999))
        peer_ = Peer("send_message_unicast_peer_", "localhost", randint(1000, 9999))
        time.sleep(0.02)
        message = 'test'
        msg = peer.split_message_into_blocks(message)
        message_sent = f'{peer.username}: {msg[0]}'
        peer.send_message_unicast(peer_.username, message_sent)
        time.sleep(0.02)
        self.assertEqual(message, peer_.message_received)

    def test_send_message_multicast(self):
        peer = Peer("send_message_multicast_peer", "localhost", randint(1000, 9999))
        peer_ = Peer("send_message_multicast_peer_", "localhost", randint(1000, 9999))
        peer__ = Peer("send_message_multicast_peer__", "localhost", randint(1000, 9999))
        time.sleep(0.02)
        message = 'test'
        msg = peer.split_message_into_blocks(message)
        message_sent = f'{peer.username}: {msg[0]}'
        peer.send_message_multicast([peer_.username, peer__.username], message_sent)
        time.sleep(0.02)
        self.assertEqual(message, peer_.message_received)
        self.assertEqual(message, peer__.message_received)

    def test_update_user_status(self):
        peer = Peer("update_user_status_test", "localhost", randint(1000, 9999))
        peer.update_user_status("update_user_status_test", False)
        self.assertEqual(peer.lista_peer["update_user_status_test"]["is_active"], False)

args = ["-p", "no:trialtemp"]  # Lista degli argomenti da passare a pytest
pytest.main(args)  # Esegue pytest con gli argomenti specificati
