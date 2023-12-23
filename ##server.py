##server
import socket
import hashlib
import json

# List of valid candidates with their SHA-256 hashes
valid_candidates = {
    hashlib.sha256('Candidate 1'.encode()).hexdigest(): 'Candidate 1',
    hashlib.sha256('Candidate 2'.encode()).hexdigest(): 'Candidate 2',
    hashlib.sha256('Candidate 3'.encode()).hexdigest(): 'Candidate 3',
}

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []  # Initialize current_votes
        self.create_block(previous_hash='1')  # Genesis block

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'votes': self.current_votes,
            'previous_hash': previous_hash,
        }
        self.current_votes = []  # Reset current votes
        self.chain.append(block)

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

    def add_vote(self, encrypted_candidate):
        self.current_votes.append({'encrypted_candidate': encrypted_candidate})

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block['previous_hash'] != self.hash(previous_block):
                return False

        return True

def decrypt_candidate(encrypted_candidate):
    for candidate_id, candidate_name in valid_candidates.items():
        if candidate_id == encrypted_candidate:
            return candidate_name
    return "Invalid candidate"

def main():
    host = '127.0.0.1'  # Server's IP address or hostname
    port = 8088

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    blockchain = Blockchain()

    print("Server is listening...")
    conn, addr = server_socket.accept()
    print("Connection from: " + str(addr))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        encrypted_candidate = data
        blockchain.add_vote(encrypted_candidate)
        voter = conn.getpeername()
        decrypted_candidate = decrypt_candidate(encrypted_candidate)
        print(f"Received from {voter}: Encrypted Voter ID: {encrypted_candidate}, Decrypted Candidate: {decrypted_candidate}")
        
        # Create a new block for the votes
        blockchain.create_block(previous_hash=blockchain.hash(blockchain.get_last_block()))
        print("Blockchain is valid:", blockchain.validate_chain())

    conn.close()
    print("connection closed")

if __name__ == "__main__":
    main()
