from peer_groups import Peer
from random import randint

if __name__ == "__main__":
    Peer(input("Username: "), "localhost", randint(1000,9999))