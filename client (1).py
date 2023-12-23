##client
import socket
import hashlib

# Dictionary to store voters and the candidates they have voted for
voters_choices = {}

# Dictionary to store candidates, their SHA-256 hashes, and their political parties
candidates_info = {
    'Candidate 1': {'hash': hashlib.sha256('Candidate 1'.encode()).hexdigest(), 'party': 'Party A'},
    'Candidate 2': {'hash': hashlib.sha256('Candidate 2'.encode()).hexdigest(), 'party': 'Party B'},
    'Candidate 3': {'hash': hashlib.sha256('Candidate 3'.encode()).hexdigest(), 'party': 'Party A'},
}

def encrypt_candidate(candidate_name):
    return hashlib.sha256(candidate_name.encode()).hexdigest()

def display_candidate_list():
    print("List of Candidates and their Political Parties:")
    for candidate, info in candidates_info.items():
        print(f"{candidate} ({info['party']})")

def main():
    host = '127.0.0.1'  # Server's IP address or hostname
    port = 8088   

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Display the list of candidates and their parties
    display_candidate_list()

    while True:
        candidate_name = input("Enter the candidate's name: ")

        if candidate_name.lower() == 'exit':
            break

        if candidate_name in candidates_info:
            if client_socket.getpeername() in voters_choices:
                print("You have already voted for a candidate. Please choose another candidate.")
            else:
                encrypted_candidate = encrypt_candidate(candidate_name)
                client_socket.send(encrypted_candidate.encode())
                # Add the voter's choice to the dictionary
                voters_choices[client_socket.getpeername()] = candidate_name
                print("Your vote for", candidate_name, "has been cast.")
        else:
            print("Invalid candidate. Please choose a candidate from the list.")

    client_socket.close()

if __name__ == "__main__":
    main()

