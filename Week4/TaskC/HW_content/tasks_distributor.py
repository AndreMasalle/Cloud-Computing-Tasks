from data_worker import DataToWorker
import main_constants as mc
import zmq
import time
import random
import pickle

### Here's the step by step
### Create your context 
### Create 1 socket using the PUSH socket type
### Bind your PUSH socket to your desired endpoint.

###
####   YOUR CODE
###

print(f"Tasks distributor is running on {...}")
print("Sending tasks to workers")
print("There are 3 available tasks")
print("Sum; Multiply; Division")

while True:
    ### Generate 2 random numbers
    ### set the appropriate value for the given variables
    ## send the data
    time.sleep(5)
###
####   YOUR CODE
###
    task_code = random.choice([..., ..., ...])
    task_data = DataToWorker(..., ..., ...)
    sent_task = pickle.dumps(...)

    print(f"Sending task --- {...} ({...} & {...}) waiting for available worker to handle")
###
####   YOUR CODE
###
    print("--- Sent --- ")
