import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []
        self.nodes = set()
        self.voter_ids = set()  # Set to keep track of used voter IDs
        self.candidates = {}  # {constituency: {candidate_id: {'name': candidate_name, 'votes': vote_count}}}

        # Genesis block
        self.new_block(proof=100, previous_hash='1')

    def new_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'votes': self.current_votes,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.current_votes = []
        self.chain.append(block)
        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def new_vote(self, person_id, vote):
        self.current_votes.append({
            'person_id': hashlib.sha256(str(person_id).encode()).hexdigest(),
            'vote': vote,
        })
        self.chain.append(self.current_votes)

    def confirm_vote(self):
        confirmation = input('Do you want to cast your vote? (yes/no): ').lower()
        return confirmation == 'yes'

    def increment_candidate_votes(self, constituency, candidate_id):
        if constituency not in self.candidates:
            self.candidates[constituency] = {}

        if constituency == 'A':
            candidate_names = ['Candidate A', 'Candidate B', 'Candidate C']
        elif constituency == 'B':
            candidate_names = ['Candidate X', 'Candidate Y', 'Candidate Z']
        else:  # Default to 'C' constituency
            candidate_names = ['Candidate D', 'Candidate E', 'Candidate F']

        if candidate_id not in self.candidates[constituency]:
            self.candidates[constituency][candidate_id] = {'name': candidate_names[int(candidate_id) - 1], 'votes': 1}
        else:
            self.candidates[constituency][candidate_id]['votes'] += 1

    def election_commission_view(self):
        login_id = input('Enter your login ID: ')
        if login_id != '55':
            return 'Access denied. Invalid login ID.'

        constituency = input('Enter the constituency to view results: ')
        if constituency not in self.candidates:
            return f'No votes recorded for constituency: {constituency}'

        votes = self.candidates[constituency]
        result = f'Total votes for constituency {constituency}:\n'
        for candidate_id, candidate_info in votes.items():
            result += f'Candidate {candidate_id}: {candidate_info["name"]} - Votes: {candidate_info["votes"]}\n'
        return result

    def view_blockchain(self):
        return self.chain

# Example usage:

# Initialize blockchain
blockchain = Blockchain()