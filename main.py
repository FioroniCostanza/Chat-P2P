from peer import Peer
from random import randint
import signal

def handler(signum, frame): # Ctrl-c handler
    peer.stop()
    print("Press enter to exit definitely...")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    peer = Peer(input("Username: "), "localhost", randint(1000, 9999))