
#--------------------------------------------------
import socket
import time
from blockchain_voting import *

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

# Voting process
voter_id = input('Enter your voter ID: ')
constituency = voter_id[:1].upper()

if constituency not in ['A', 'B', 'C']: # Add more constituencies as needed
  print('Invalid constituency. Please try again.')
else:
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
  else: # Default to 'C' constituency
      candidates = {
          '1': 'Candidate D',
          '2': 'Candidate E',
          '3': 'Candidate F'
      }

  print(f'\nCandidates for constituency {constituency}:')
  for candidate_id, candidate_name in candidates.items():
      print(f'{candidate_id}: {candidate_name}')

  vote_casted = False
  while not vote_casted:
      candidate_id = input('Enter the candidate ID you want to vote for (or type "exit" to finish): ')
      if candidate_id.lower() == 'exit':
          break
      if candidate_id in candidates:
          vote = {'voter_id': voter_id, 'constituency': constituency, 'candidate_id': candidate_id}
          vote_json = json.dumps(vote)
          # Send vote to server
          client.send(vote_json.encode())
          print('Vote sent to server. Waiting for confirmation...')
          confirmation = ''        
          while not confirmation:
              chunk = client.recv(1024).decode()
              if chunk:
                  confirmation = chunk
              else:
                  break
          print(f'Confirmation received from server: {confirmation}')
          if confirmation == 'Vote confirmed.':
              print('Vote confirmed by server!')
              vote_casted = True
          else:
              print('Vote not confirmed by server. Please try again.')
      else:
          print('Invalid candidate ID. Please try again.')

# Receive updated blockchain
blockchain = client.recv(1024).decode()
print(f"Updated blockchain: {blockchain}")

client.close()

