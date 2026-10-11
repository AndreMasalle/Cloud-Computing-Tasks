import main_constants as mc
from data_worker import DataToWorker
import pickle
import zmq

### Here's the step by step
### Create your context 
### Create a socket using the subscriber socket type
### Connect the socket to the publisher'socket 
### Set socket topic

index: int = 0
###
####   YOUR CODE
###

print("Waiting for a new message to arrive... ")

def show_content(result):
    result_obj: DataToWorker = pickle.loads(...)
    print(f"Input Numbers: {...} & {...}")
    print(f"Main Operation: {...}")
    print(f"Result: {...}")
    print(f"Message: {...}")
    print(f"EXECUTOR: {...}")

while True:
    ### Receive the data in multi part
    ### Call the show_content

    ###
    ####   YOUR CODE
    ###
    print("Received a new message: with topic's name", str(...))
    
    ###
    ####   YOUR CODE
    ###
    index += 1
    
    if index >= 5:
        print("\033c",end="")
        index = 0
    print("\nRepeating ...\n")
