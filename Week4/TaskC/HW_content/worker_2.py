import pickle
import main_constants as mc
from data_worker import DataToWorker
import zmq
import random

## Create context
## Create pull and push socket
## Bind the push socket
## Connect the pull socket


###
####   YOUR CODE
###

def task_1_sum(num1: float, num2: float) -> float:
    print(f"[x] {num1} + {num2} ")
    ### Your code

def task_2_multiply(num1: float, num2: float) -> float:
    print(f"[x] {num1} x {num2} ")
    ### Your code

def task_3_division(num1: float, num2: float) -> float:
    print(f"[x] {num1} / {num2} ")
    ### Your code

print("Successfully connected with the server ...")
print("Waiting for tasks ... ")

while True:
    ### receive the task using the pull socket
    ### load the task 
    ### Get the numbers
    ### do the operation based upon the operation of DataToWorker object
    ### set the result property of your DataToWorker object
    ### set the executor
    ### Push the updated object

    work_time = random.uniform(0.5, 1)
    ###
    #### Your code 
    ###
    task_data: DataToWorker = pickle.loads(...)
    print("WORKER-2: Handling the task")

    result: float = 0.0

    ###
    #### Your code 
    ###

    print("Data has been processed, sending them to the collector ...\n")
