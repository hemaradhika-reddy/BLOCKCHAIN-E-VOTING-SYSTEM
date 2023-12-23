import hashlib
import json
import time
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.font import Font
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

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
            'voter_id': hashlib.sha256(str(person_id).encode()).hexdigest(),
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

    def election_commission_view(self, login_id, constituency):
        if login_id != '55':
            return 'Access denied. Invalid login ID.'

        if constituency not in self.candidates:
            return f'No votes recorded for constituency: {constituency}'

        votes = self.candidates[constituency]
        result = f'Total votes for constituency {constituency}:\n'
        for candidate_id, candidate_info in votes.items():
            result += f'Candidate {candidate_id}: {candidate_info["name"]} - Votes: {candidate_info["votes"]}\n'
        return result

    def view_blockchain(self):
        return self.chain

class BlockchainGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Blockchain Voting System")
        self.blockchain = Blockchain()
        def_font = Font(weight='bold')
        def_font.config(size=18)

        def_font2 = Font(weight='bold')
        def_font2.config(size=24)
                                                                                           #, bg='maroon1'
        self.message_label = Label(root, text="Block Chain Voting System", font=def_font2, bg='orchid2')
        self.message_label.pack(pady = 10)

        # Create buttons                                         #
        self.cast_vote_button = Button(master, text="Cast Vote",font=def_font, command=self.cast_vote, bg='mediumpurple1')
        self.cast_vote_button.pack(pady = 10)

        self.ec_view_button = Button(master, text="Election Commission View",font=def_font, command=self.election_commission_view, bg='DarkOrchid1')
        self.ec_view_button.pack(pady = 10)

        self.view_blockchain_button = Button(master, text="View Blockchain",font=def_font, command=self.view_blockchain, bg='violetred')
        self.view_blockchain_button.pack(pady = 10)

        self.exit_button = Button(master, text="Exit",font=def_font, command=master.quit,bg='maroon1')
        self.exit_button.pack(pady = 10)

    def cast_vote(self):
        voter_id = simpledialog.askstring("Voter ID", "Enter your voter ID:")
        constituency = voter_id[:1].upper()

        if voter_id in self.blockchain.voter_ids:
            messagebox.showinfo("Error", "You have already casted a vote. Exiting...")
            return

        if constituency not in ['A', 'B', 'C']:  # Add more constituencies as needed
            messagebox.showinfo("Error", "Invalid constituency. Please try again.")
            return

        candidates = {}

        if constituency == 'A':
            candidates = {
                '1': 'Candidate A',
                '2': 'Candidate B',
                '3': 'Candidate C'
            }
        elif constituency == 'B':
            candidates = {
                '1': 'Candidate X',
                '2': 'Candidate Y',
                '3': 'Candidate Z'
            }
        else:  # Default to 'C' constituency
            candidates = {
                '1': 'Candidate D',
                '2': 'Candidate E',
                '3': 'Candidate F'
            }

        candidates_str = "\n".join([f'{candidate_id}: {candidate_name}' for candidate_id, candidate_name in candidates.items()])
        selected_candidate_id = simpledialog.askstring("Candidates", f'Candidates for constituency {constituency}:\n{candidates_str}\nEnter the candidate ID you want to vote for (or type "exit" to finish):')

        if selected_candidate_id.lower() == 'exit':
            return

        if selected_candidate_id in candidates:
            if messagebox.askyesno("Confirmation", "Do you want to cast your vote?"):
                self.blockchain.new_vote(voter_id, {'constituency': constituency, 'candidate_id': selected_candidate_id})
                self.blockchain.increment_candidate_votes(constituency, selected_candidate_id)
                self.blockchain.voter_ids.add(voter_id)  # Mark voter ID as used
                messagebox.showinfo("Success", "Vote casted successfully!")
            else:
                messagebox.showinfo("Info", "Vote cancelled.")
        else:
            messagebox.showinfo("Error", "Invalid candidate ID. Please try again.")

    def election_commission_view(self):
        login_id = simpledialog.askstring("Login ID", "Enter your login ID:")
        if login_id != '55':
            messagebox.showinfo("Access Denied", "Invalid login ID. Access denied.")
            return

        constituency = simpledialog.askstring("Constituency", "Enter the constituency to view results:")
        results = self.blockchain.election_commission_view(login_id, constituency)
        messagebox.showinfo("Election Commission View", results)

    def view_blockchain(self):
        blockchain_data = json.dumps(self.blockchain.view_blockchain(), indent=2)
        messagebox.showinfo("Blockchain", blockchain_data)

if __name__ == "__main__":
    root = Tk()
    root.title("Voting System")
    root.geometry('550x500')
    root.configure(bg='orchid2')
    
    app = BlockchainGUI(root)
    root.mainloop()