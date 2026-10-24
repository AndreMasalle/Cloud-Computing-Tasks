import os
import pickle
import random
import time

import zmq

import main_constants as mc
from data_worker import DataToWorker


def run_distributor():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind(f"tcp://*:{mc.DISTRIBUTOR_PORT}")

    total_tasks = int(os.getenv("DISTRIBUTOR_TOTAL_TASKS", "0"))
    startup_delay = float(os.getenv("DISTRIBUTOR_STARTUP_DELAY", "2"))
    task_interval = float(os.getenv("TASK_INTERVAL_SECONDS", "1"))
    print(f"Tasks distributor is running on port {mc.DISTRIBUTOR_PORT}", flush=True)
    print("Available tasks: SUM, MUT, DIV", flush=True)
    time.sleep(startup_delay)

    task_id = 0
    operations = (mc.SUM, mc.MUT, mc.DIV)
    try:
        while total_tasks == 0 or task_id < total_tasks:
            task_id += 1
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            operation = random.choice(operations)
            task_data = DataToWorker(num1, num2, operation)
            print(
                f"[Distributor -> PUSH] Task #{task_id}: {operation.upper()} "
                f"({num1}, {num2})",
                flush=True,
            )
            socket.send(pickle.dumps(task_data))
            print("--- Sent ---", flush=True)
            time.sleep(task_interval)
    except KeyboardInterrupt:
        print("[Distributor] Stopped", flush=True)
    finally:
        socket.close(linger=0)
        context.term()


if __name__ == "__main__":
    run_distributor()
