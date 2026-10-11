import zmq
import pickle
from data_worker import DataToWorker
import main_constants as mc

### Here's the step by step
### Create your context 
### Create 2 sockets using the pull socket type
### Connect each pull socket variable to the worker's socket end point.

### Create a socket using the pub socket type to publish the message
### Bind your publisher socket to your desired endpoint.

###
####   YOUR CODE
###

def set_data_message(data: DataToWorker, message: str):
    data.set_message(message)
    return data

message_sum: str = "The summation process has been executed sucessfully"
message_multiply: str = "The multiplication process has been executed sucessfully"
message_div: str = "The div process has been executed sucessfully"

while True:

##  Receive tasks from the workers
### Loads the data 
### set the message property appropriately for the given operation 
### send the multipart data.

###
####   YOUR CODE
###

    print("Task is received")
    
    result: DataToWorker = pickle.loads(...)
    if mc.SUM == ...:
        ...
    elif mc.MUT == ...:
        ...
    elif mc.DIV == ...:
        ...
    print("Sending the results to subscribers...")

###
####   YOUR CODE
###
    print("--- Sent ---")
    
